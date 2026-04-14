---
type: automatic_troubleshooting
sub_type: endpoint_exceptions
date: '2026-03-11'
---

## Symptom

Elastic Defend is expected to be generating alerts (e.g. malware detections, behavioral alerts), but no alert documents appear in `logs-endpoint.alerts-*`. The endpoint may appear healthy in Fleet, protections are enabled in the policy, and events may still be flowing to other indices — but alerts specifically are absent.


## Summary

When alerts are missing from `logs-endpoint.alerts-*`, the cause falls into one of three categories: the endpoint is generating alerts but they are not reaching Elasticsearch (a shipping/output problem), the endpoint is not generating alerts at all because protections are disabled or misconfigured, or the endpoint is not actually blocking activity — the perceived problem is caused by an interaction with another application on the host rather than by Elastic Defend.

This is distinct from the "exceptions not working" scenario where alerts *are* being generated but an exception fails to suppress them. Here, the issue is that expected alerts are completely absent from the data.


## Common issues

### Output shipping failure (Kafka or Logstash misconfiguration)

If the endpoint's configured output (Kafka, Logstash, or Elasticsearch) is misconfigured, unreachable, or rejecting messages, alert documents may never reach Elasticsearch even though the endpoint is generating them locally.

Common indicators:
- The endpoint shows `DEGRADED` status in Fleet with output-related error messages.
- `logs-elastic_agent.endpoint_security-*` contains errors such as:
  - `Endpoint is setting status to DEGRADED, reason: Unable to connect to output server`
  - `SSL handshake with Logstash server at [host]:[port] encountered an error`
  - `Logstash connection is down`
  - `KafkaClient failed to deliver record with unrecoverable error: Broker: Message size too large`
- Other endpoint event indices (`logs-endpoint.events.process-*`, `logs-endpoint.events.file-*`) are also empty or stale for the same endpoint, confirming a general shipping problem rather than an alert-specific issue.

For Kafka deployments, verify that the broker and topic `max.message.bytes` settings are compatible with the endpoint's client-side default (1,000,000 bytes). A topic-level override lower than the broker default is a common cause of silent message rejection.

For Logstash deployments, verify that the Logstash pipeline is running, accepting connections, and correctly forwarding to Elasticsearch. Check the Logstash pipeline logs for parsing errors or output failures.

For more details on output-related issues, see the `output_kafka_message_size` knowledge base doc.

### Protections not enabled or in wrong mode

If no protections are enabled in the Elastic Defend integration policy, the endpoint will not generate alerts. Verify the policy configuration:

- **Malware protection**: Must be set to "detect" or "prevent" to generate alerts with `event.code: malicious_file`.
- **Behavioral protection (Malicious Behavior)**: Must be enabled to generate alerts with `event.code: behavior`.
- **Memory threat protection**: Must be enabled to generate alerts with `event.code: memory_signature`.
- **Ransomware protection**: Must be enabled to generate alerts with `event.code: ransomware`.

Check the policy configuration via `get_package_configurations` or in the Kibana Security UI under Manage > Policies. If all protections show as disabled, alerts will not be generated regardless of activity on the host.

Also verify the policy has been successfully applied to the endpoint. Check `metrics-endpoint.policy-*` for the most recent policy response — a `FAILED` status indicates the policy did not apply and the endpoint may be running with an older or default configuration.

### Inter-application incompatibility masquerading as a detection gap

Sometimes it appears that Elastic Defend should be generating alerts for suspicious activity on a host, but the activity is actually caused by an incompatibility between Elastic Defend and another application — not by genuinely malicious behavior. In this case, alerts are absent because Elastic Defend is not detecting anything malicious; the problem is the application interaction itself.

Indicators that this is the cause:
- Alerts are being ingested into Elasticsearch from other hosts running the same policy, confirming protections are working in general.
- The affected host has another security product, AV, or system management tool installed that may be interfering with Elastic Defend.
- The problematic behavior only occurs when both Elastic Defend and the other application are running simultaneously.

A targeted **Trusted Application** entry for the conflicting application's process is the most common solution. This stops Elastic Defend from monitoring that process, which can resolve the interaction without disabling protections for the rest of the system.

To test whether alerts are being generated at all, use the EICAR test file if Malware protection is enabled:
```
curl https://secure.eicar.org/eicar.com.txt --output eicar.com.txt
```
If an alert appears in `logs-endpoint.alerts-*` for the EICAR file, the endpoint's alert generation and shipping pipeline is working correctly, and the missing alerts for the original activity point to an application interaction or a legitimate non-detection.

### Endpoint not running or in a failed state

If the Endpoint process is not running (crashed, failed to start, or stuck in a broken install state), no alerts will be generated. The agent may report the endpoint as `FAILED` with "endpoint service missed 3 check-ins."

Check `metrics-endpoint.metadata_current_*` for the endpoint's last known status and timestamp. A stale timestamp indicates the endpoint has been offline. See the `missed_checkins` knowledge base docs for detailed troubleshooting.


## Investigation priorities

1) Check whether *any* endpoint data is flowing from the affected host — query `logs-endpoint.events.process-*` and `logs-endpoint.events.file-*` for recent documents. If all endpoint indices are empty, the issue is a shipping/output problem, not alert-specific.
2) Check `logs-elastic_agent.endpoint_security-*` for output errors (DEGRADED status, SSL errors, Kafka delivery failures, Logstash connection errors).
3) Verify protection features are enabled in the integration policy via `get_package_configurations` or the Kibana UI. Confirm the policy was successfully applied by checking `metrics-endpoint.policy-*` for the most recent policy response.
4) Check `metrics-endpoint.metadata_current_*` for the endpoint's health status and last seen timestamp to confirm the endpoint is running.
5) If other hosts on the same policy are generating alerts normally, investigate whether the affected host has a conflicting application. Use the EICAR test file to verify the alert pipeline is functional.
6) Check whether the affected host has another security product installed that may be interfering with Elastic Defend. If so, try adding it as a Trusted Application.
