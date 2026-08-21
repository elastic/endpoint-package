---
type: policy_management
sub_type: events
date: '2026-08-22'
link: https://www.elastic.co/docs/solutions/security/manage-elastic-defend/event-capture-elastic-defend
---

# Event collection tradeoffs in an Elastic Defend policy

This article helps you choose Elastic Defend policy configuration for event collection and indexed volume: which event types the policy forwards, and how protection monitoring relates to what is indexed. It is not a guide for a failed policy response or incident diagnosis.

## When to use this article

Use this article when you are deciding Elastic Defend policy configuration for:

- Which event types to collect for visibility in Elasticsearch
- How far event collection should go relative to protection, given the workload of the host
- How high-churn process or file activity on a host changes the visibility versus operational-cost tradeoff

Do not use this article to diagnose Kafka or Logstash delivery failures, or to inventory every event-collection control in the policy UI. Artifact-based volume reduction, such as Event Filters and Trusted Applications, is not covered in this article.

## Event types at product grain

Elastic Defend collects selective host activity so it can detect and prevent threats while balancing storage and performance overhead. At product grain, that includes process execution events, file creation and modification, network connections, security alerts and detections, and host metadata. Data lands in indices such as `logs-endpoint.events.*` and `logs-endpoint.alerts.*`.

For additional product documentation of captured events, see [Event capture and Elastic Defend](https://www.elastic.co/docs/solutions/security/manage-elastic-defend/event-capture-elastic-defend). Which event cards exist on which operating system, and the exact policy paths that enable them, are not listed here.

## Protection monitoring versus indexed volume

Turning an event type off in Event Collection reduces what is indexed. It does not always stop protection engines from consuming the same activity.

On Windows, when Malicious Behavior Protection is enabled, Elastic Defend still collects and processes Security events for behavioral rules even if Security is removed from Event Collection. Disabling Malicious Behavior Protection stops that Security-event processing, and also removes behavioral detection capability. Indexed volume and protection monitoring are therefore separate choices: Event Collection controls what you store; protection engines can still require events that never appear as collected telemetry.

## Volume versus visibility

Event collection is a visibility choice with operational cost. High-churn workloads increase both indexed volume and the work protection engines do on each event.

On Linux, process collection is especially costly when a parent script or automation runtime spawns many short-lived children. Each process-start event is enriched and evaluated against behavioral rules, so a monitoring or CI parent can dominate volume even when no single child looks interesting.

On Windows, file-intensive operations such as Office updates, backup software, and database maintenance can generate large bursts of file events. Those bursts increase indexed volume and output throughput.

There is no package-supported numeric “safe” event rate. Choose collection from the visibility you need and the workload texture of the host, then use the policy UI for the concrete controls. When event volume already appears as an incident, the `output_kafka_message_size` and `high_cpu` knowledge base docs cover the failure side, including artifact-based volume reduction.

## Exact settings

Do not invent event-collection paths, defaults, licenses, or versions from this article. Use the Elastic Defend policy UI or the maintained field reference for exact setting names and values.

## Related troubleshooting

When event volume appears as an incident rather than a configuration choice, see the `output_kafka_message_size` knowledge base doc for output failures and the `high_cpu` knowledge base docs for Windows Security-event processing and Linux short-lived process churn. Those articles are diagnostic; they are not a field catalogue for event collection.
