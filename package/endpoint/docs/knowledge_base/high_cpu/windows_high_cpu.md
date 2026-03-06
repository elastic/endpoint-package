---
type: automatic_troubleshooting
sub_type: high_cpu
os: [Windows]
date: '2026-03-07'
---

## Symptom

Elastic Defend (elastic-endpoint.exe) is consuming an abnormally high percentage of CPU on a Windows host, causing system slowdowns or user complaints.


## Summary

Elastic Defend monitors process, file, network, registry, library, and other system activity in real time. CPU usage scales with the volume and complexity of monitored events. When a workload generates a burst of activity — many short-lived processes, heavy file I/O, or rapid network connections — the endpoint sensor must inspect each event, which can temporarily or persistently spike CPU. Misconfigured outputs (Logstash/Kafka disconnections) can also cause internal retry loops that consume CPU independently of event volume.


## Common issues

### File-intensive operations

Office updates, Windows Update, backup agents, database engines (SQL Server), and antivirus full-disk scans can generate thousands of file events per second. The endpoint sensor inspects each file operation, driving CPU proportionally. These workloads are often periodic (nightly backups, monthly patch cycles) and correlate with scheduled tasks.

To confirm, run `elastic-endpoint top` during the spike and look for the responsible process. If the process is a known legitimate application (e.g. `MsMpEng.exe`, `sqlservr.exe`, backup agent), consider adding an Event Filter for the specific event category (e.g. `file` events from that process path) to reduce storage cost without creating a monitoring blind spot. Only add a Trusted Application if full monitoring bypass is acceptable for that process.

### Third-party security product conflicts

Other security products that hook into the same kernel-level instrumentation — Silverfort, iBoss, CrowdStrike Falcon, other AV engines — can cause contention with Elastic Defend's minifilter driver or ETW consumers. The conflict manifests as sustained high CPU on `elastic-endpoint.exe` or the conflicting product's process, sometimes both.

To confirm, check whether CPU returns to normal when the conflicting product is temporarily disabled. If so, add the conflicting product as a Trusted Application so Elastic Defend stops monitoring its process tree. Alternatively, add Elastic Defend's binary paths to the other product's exclusion list.

### Short-lived child process churn

Monitoring frameworks, RMM tools, or deployment scripts that rapidly spawn and tear down child processes (e.g. PowerShell one-liners, WMI queries on timers) generate a high rate of process-start events. Each process creation requires hash computation, signature verification, and rule evaluation.

Use `elastic-endpoint top` to identify the parent process. If the spawning pattern is legitimate, add an Event Filter on `process` events matching the parent executable. Alternatively, review `windows.advanced.events` policy settings to disable event types that are not needed (e.g. `api`, `library` events) to reduce overall event throughput.

### Logstash or Kafka output disconnection

When the configured output (Logstash or Kafka) becomes unreachable, the endpoint buffers events and retries delivery. Sustained retry loops consume CPU independently of host workload. CPU usage often spikes simultaneously across many endpoints, correlating with an output infrastructure outage.

Check `logs-elastic_agent.endpoint_security-*` for output error messages such as `KafkaClient failed to deliver record` or Logstash connection timeouts. Resolve the output connectivity issue. If using Kafka, verify that `max.message.bytes` on the broker aligns with the Elastic Endpoint message size configuration.

### Trusted Applications configured but not reducing CPU

A Trusted Application entry may fail to take effect if the condition uses the wrong field (e.g. `file.path` instead of `process.executable`), has incorrect wildcard syntax, or is assigned to the wrong integration policy.

Verify the Trusted Application entry's field matches the actual process executable path as reported in `logs-endpoint.events.process-*`. Also confirm the entry is assigned to the correct integration policy covering the affected endpoint.


## Investigation priorities

1) Run `elastic-endpoint top` on the affected host to identify which processes are driving event volume and CPU
2) Query `metrics-endpoint.metrics-*` for the host to review CPU usage trends and event throughput rates
3) Query `logs-elastic_agent.endpoint_security-*` for output errors or retry messages
4) Query `logs-endpoint.events.process-*` for high-frequency short-lived processes
5) Review policy configuration for unnecessary event types enabled under `windows.advanced.events`
6) Check whether any Trusted Application or Event Filter entries are misconfigured
