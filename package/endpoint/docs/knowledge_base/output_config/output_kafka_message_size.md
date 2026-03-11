---
type: automatic_troubleshooting
sub_type: output_config
date: '2026-03-11'
---

## Symptom

Elastic Defend logs show Kafka delivery failures (`KafkaClient failed to deliver record with unrecoverable error: Broker: Message size too large`), events are silently lost or repeatedly retried, or the endpoint's CPU spikes to 100% when a Logstash or Kafka output becomes unreachable. In the Logstash case, the endpoint reports DEGRADED status with `Unable to connect to output server` and CPU remains elevated until connectivity is restored.


## Summary

Elastic Defend's output layer is implemented in C++ using librdkafka (for Kafka) and a custom Logstash client, separate from the Go-based output used by Beats and Elastic Agent. This means Elastic Defend does not share the same resiliency, configuration options, or retry behavior as other integrations on the same agent. Two distinct failure modes are common: Kafka message size rejections (where individual events or batches exceed the broker's size limit) and Logstash connectivity loss (where the endpoint enters a retry or backoff loop that can consume significant CPU).

For Kafka, the endpoint uses librdkafka's default `message.max.bytes` of 1,000,000 bytes. Messages exceeding the broker's or topic's `max.message.bytes` are rejected. Prior to 8.18.3, rejected messages were retried indefinitely, causing a tight error loop. On 8.18.3+, oversized messages are dropped after the first delivery failure instead of being retried.

For Logstash, when the output becomes unreachable the endpoint enters a backoff-based reconnection loop. On versions 8.8.0 through 8.13.3, a bug in the retry logic caused a tight CPU spin that consumed 100% of one core. This was fixed in 8.13.4. Even on fixed versions, after a prolonged disconnection, the endpoint may accumulate a backlog of events and take time to catch up after reconnection — the data is not lost, but delivery is delayed proportionally to the outage duration.


## Common issues

### Kafka `Message size too large` broker rejection

The Kafka broker rejects messages that exceed its configured `max.message.bytes` limit. The endpoint logs the error:

```
KafkaClient.cpp:561 KafkaClient failed to deliver record with unrecoverable error: Broker: Message size too large [10] | non-retriable
```

The error originates from the broker itself, meaning the message passed the client-side size check (librdkafka default: 1,000,000 bytes) but was rejected at the broker or topic level. This typically occurs during high-volume event bursts — for example, a Microsoft Office automatic update generating over 11,000 file events in a short window, which get batched into a single oversized Kafka message.

The size limits are enforced at three levels:

| Level | Setting | Default |
|-------|---------|---------|
| Endpoint (librdkafka client) | `message.max.bytes` | 1,000,000 |
| Kafka broker | `max.message.bytes` | 1,048,588 |
| Kafka topic | `max.message.bytes` | Inherits from broker unless overridden |

A topic-level override lower than the broker default is the most common cause of unexpected rejections when the client and broker defaults appear compatible. Use the Kafka AdminClient API or `kafka-configs.sh --describe` to inspect per-topic configuration and check for `max.message.bytes` overrides with source `DYNAMIC_TOPIC_CONFIG`.

On versions prior to 8.18.3, oversized messages were retried indefinitely, generating repeated error log entries and consuming CPU in a delivery retry loop. On 8.18.3+, the endpoint treats the `Message size too large` error as non-retriable and drops the message after logging the failure. The error is still logged on the first attempt, but no retry loop occurs.

To confirm whether messages are being dropped (rather than the error no longer occurring): if the `Message size too large` error no longer appears in `logs-elastic_agent.endpoint_security-*`, it means the condition is not being triggered — not that messages are being silently dropped. Dropped messages still produce the error log entry on the first attempt.

### Logstash output disconnection causing CPU spike

When the Logstash output becomes unreachable, the endpoint enters a reconnection loop. On versions 8.8.0 through 8.13.3, a bug in the retry logic caused the `elastic-endpoint` process to consume 100% of one CPU core within minutes of losing connectivity. The CPU returns to normal within approximately 40 seconds of connectivity being restored.

Characteristic log pattern during the outage:

```
AgentContext.cpp:565 Endpoint is setting status to DEGRADED, reason: Unable to connect to output server
LogstashClient.cpp:662 SSL handshake with Logstash server at [host]:[port] encountered an error
BulkQueueConsumer.cpp:192 Logstash connection is down
```

These messages repeat every 20 seconds while the output is unreachable. The CPU spike is caused by the endpoint's C++ Logstash client, not by the Beats/Agent Go-based outputs — removing the Endpoint Security integration from the policy immediately drops CPU back to normal even while Logstash remains down, confirming the issue is specific to Elastic Defend's output implementation.

**Fixed in 8.13.4** (endpoint-dev PR #13065). On fixed versions, the endpoint still logs connection errors but uses a proper exponential backoff that does not spin CPU.

### Logstash output event backlog after reconnection

After a prolonged Logstash disconnection, the endpoint accumulates unsent events in its internal queue. When connectivity is restored, the endpoint resumes sending but starts with the oldest queued events. The delivery delay equals the duration of the outage — if the output was down for one hour, events will be approximately one hour behind real time until the backlog is drained.

The backlog does not self-resolve faster than real-time ingestion because the endpoint sends queued events at the same rate as live events. On deployments with high event volume (e.g. 45,000+ agents behind a Logstash cluster), this delay can persist for the same duration as the outage.

The endpoint implements a backoff algorithm for reconnection attempts. If the backoff interval has grown large due to repeated failures, the connection may not be reattempted immediately even after connectivity is restored. Running `elastic-endpoint test output` on the affected host manually cancels the backoff and triggers an immediate reconnection attempt. The corresponding log entry is:

```
ServiceCommsFunctions.cpp:234 Canceling output backoff due to 'test output' command
```

Unlike Beats-based integrations that automatically reconnect and drain backlogs efficiently, Elastic Defend's C++ Logstash client does not have the same resiliency or configuration options. There is no user-configurable backoff or batch size setting for Elastic Defend's Logstash output.

### Large event bursts from file-intensive operations

Certain operations generate massive volumes of file events in a short period — Microsoft Office automatic updates, Windows Update, backup software (Veeam, Commvault), and database maintenance. When these events are batched for output delivery, individual batches can exceed Kafka message size limits or overwhelm Logstash throughput capacity.

In one observed case, a Microsoft Office update at 4–5 AM generated 11,000 file events alongside a CPU spike on the host. The events were batched into Kafka messages that exceeded the broker's size limit, triggering repeated `Message size too large` rejections.

To mitigate: add **Event Filters** for known high-volume, low-security-value event sources (e.g. Office update temp directories, backup staging paths). Event Filters prevent the event documents from being written to Elasticsearch while still allowing Elastic Defend to monitor the activity for threats. This reduces both message sizes and output throughput requirements without creating a monitoring blind spot.

For Kafka specifically, if the high-volume events are from processes that do not need monitoring at all, a **Trusted Application** entry stops event generation entirely, preventing oversized messages at the source.


## Investigation priorities

1) Check `logs-elastic_agent.endpoint_security-*` for `Message size too large`, `KafkaClient failed to deliver`, `Unable to connect to output server`, `Logstash connection is down`, or `SSL handshake` error messages to identify which output failure mode is occurring
2) For Kafka size errors, inspect the broker and topic-level `max.message.bytes` configuration using `kafka-configs.sh --describe --topic <topic>` or the AdminClient API. Compare against the endpoint's client-side default of 1,000,000 bytes
3) Check `metrics-endpoint.metadata_current-*` for the endpoint's agent version — Kafka oversized message handling improved in 8.18.3+, and the Logstash CPU spin bug was fixed in 8.13.4
4) For Logstash CPU spikes, correlate the onset of high CPU in `metrics-endpoint.metrics-*` with output connectivity errors in `logs-elastic_agent.endpoint_security-*`. If removing the Endpoint Security integration from the policy drops CPU immediately, the Logstash retry loop is confirmed
5) For Logstash event backlogs after reconnection, check `logs-elastic_agent.endpoint_security-*` for `Sent N documents to Logstash` messages and compare the document timestamps with the current time to measure the delivery delay
6) Identify the source of large event bursts by querying `logs-endpoint.events.file-*` for time windows that correlate with Kafka size errors, and check whether Event Filters or Trusted Applications can reduce the volume
