---
type: automatic_troubleshooting
sub_type: high_cpu
os: [Linux]
date: '2026-03-07'
---

## Symptom

Elastic Defend (elastic-endpoint) is consuming an abnormally high percentage of CPU on a Linux host, causing system slowdowns, OOM kills, or user complaints.


## Summary

Elastic Defend monitors process, file, network, and other system activity via kernel-level instrumentation (eBPF or kprobes). CPU usage scales with the volume of monitored events. Linux workloads that generate high rates of process creation (monitoring scripts, cron jobs, orchestration tools) or file I/O (backup systems, CI/CD pipelines, database engines) cause proportional CPU consumption by the endpoint sensor. Misconfigured outputs can also cause internal retry loops that spike CPU independently of host activity.


## Common issues

### Monitoring scripts and scheduled tasks spawning short-lived processes

This is the most common cause of high CPU on Linux. Monitoring frameworks (Nagios, Zabbix, Prometheus node_exporter scripts, custom cron jobs) and orchestration tools (Ansible, Puppet, Chef) frequently spawn hundreds of short-lived shell processes per minute. Each process creation triggers hash computation, rule evaluation, and event generation by the endpoint sensor.

To confirm, run `elastic-endpoint top` during the spike to identify the parent process driving child process churn. Common culprits include `/usr/bin/bash` or `/usr/bin/sh` invoked by a monitoring daemon. Add an Event Filter on `process` events matching the parent executable to reduce event volume without creating a monitoring blind spot. Only add a Trusted Application if full monitoring bypass is acceptable for that process tree.

### File-intensive operations

Backup systems (Veeam, rsync-based backups), CI/CD build agents, package managers (`yum`, `apt`), and database engines (PostgreSQL, MySQL) performing heavy file I/O generate thousands of file events per second. The endpoint inspects each file operation.

Use `elastic-endpoint top` to identify the responsible process. If the process is a known legitimate high-I/O application, add an Event Filter for `file` events from that process path. For databases, consider filtering the specific data directory paths. Review `linux.advanced.events` policy settings to disable event types that are not required for your detection use case.

### Third-party security product conflicts

Other security products running on the same host — CrowdStrike Falcon Sensor, Qualys agent, Rapid7 agent — can conflict with Elastic Defend's kernel-level instrumentation. Both products may be monitoring the same syscalls, causing amplified overhead.

To confirm, check whether CPU normalizes when the conflicting product is temporarily disabled. If so, add the conflicting product's binaries as a Trusted Application so Elastic Defend stops monitoring its process tree. Coordinate with the other product's team to add reciprocal exclusions.

### Logstash or Kafka output disconnection

When the configured output becomes unreachable, the endpoint buffers events and retries delivery. Sustained retry loops consume CPU independently of host workload. This often manifests as simultaneous CPU spikes across many Linux endpoints, correlating with an output infrastructure outage.

Check `logs-elastic_agent.endpoint_security-*` for output error messages such as `KafkaClient failed to deliver record` or Logstash connection timeouts. Resolve the output connectivity issue. If using Kafka, verify that `max.message.bytes` on the broker aligns with the Elastic Endpoint message size configuration. On agent versions 8.18.3+, oversized messages are dropped gracefully rather than retried.

### Trusted Applications configured but not reducing CPU

A Trusted Application entry may fail to take effect if the condition uses the wrong field (e.g. `file.path` instead of `process.executable`), has incorrect wildcard syntax, or is assigned to the wrong integration policy. On Linux, path case sensitivity matters — ensure the trusted app path exactly matches the binary path (Linux paths are case-sensitive unlike Windows).

Verify the Trusted Application entry's field matches the actual process executable path as reported in `logs-endpoint.events.process-*`. Also confirm the entry is assigned to the correct integration policy covering the affected endpoint.

### Container and orchestration overhead

On containerized hosts (Docker, Kubernetes nodes), the endpoint monitors activity across all containers. High pod churn (frequent container creation and destruction) generates a burst of process and file events. Combined with host-level monitoring scripts, this can saturate CPU.

Review whether the endpoint needs to monitor all containers or if specific namespaces can be excluded. Consider tuning `linux.advanced.events` to disable event types not required for your detection rules.


## Investigation priorities

1) Run `elastic-endpoint top` on the affected host to identify which processes are driving event volume and CPU
2) Query `metrics-endpoint.metrics-*` for the host to review CPU usage trends and event throughput rates
3) Query `logs-elastic_agent.endpoint_security-*` for output errors or retry messages
4) Query `logs-endpoint.events.process-*` for high-frequency short-lived processes (look for parent processes spawning many children)
5) Review policy configuration for unnecessary event types enabled under `linux.advanced.events`
6) Check whether any Trusted Application or Event Filter entries are misconfigured
