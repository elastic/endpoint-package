---
type: automatic_troubleshooting
sub_type: high_cpu
os: [Linux]
date: '2026-03-09'
---

## Symptom

Elastic Defend's `elastic-endpoint` process consumes sustained high CPU on Linux hosts, causing system slowdown, degraded application performance, or resource exhaustion. CPU may spike during specific intervals (cron jobs, monitoring scripts), during policy application, or continuously due to output connectivity failures.


## Summary

Elastic Defend on Linux uses eBPF and fanotify to monitor process, file, network, and DNS activity in real time. Each event is enriched, hashed, evaluated against behavioral rules, and forwarded to the configured output. The most common drivers of high CPU on Linux are monitoring scripts that spawn many short-lived child processes (each generating process events that trigger behavioral rules), output server disconnections causing retry storms, the Events plugin hashing large binaries during policy application with an empty cache, and memory scanning of large processes.

Use `sudo elastic-endpoint top` on the affected host to identify which processes and internal processing stages consume the most CPU. Query `metrics-endpoint.metrics-*` for `Endpoint.metrics.system_impact` to identify the top processes remotely.


## Common issues

### Monitoring scripts spawning many short-lived child processes

Monitoring and automation scripts that run on a schedule (cron, systemd timers) and spawn many child processes are the most common cause of high CPU on Linux. A single monitoring script invoking `curl`, `mysql`, `ssh`, `grep`, `sed`, `awk`, and `bash` in rapid succession generates a burst of process creation events, each of which Elastic Defend must enrich and evaluate against behavioral rules.

A typical pattern is hourly CPU spikes lasting 5–10 minutes, aligning with cron schedules (e.g. xx:31–xx:41 every hour). In one case, a script at `/var/cache/system-monitoring/helper/compare-inventory.sh` that used `curl` to collect data triggered the behavioral rule "Suspicious Download and Redirect by Web Server" 86,340 times in a single diagnostics window, driving endpoint service CPU above 200% (out of 800% on 8 cores).

Adding the parent script as a Trusted Application stops monitoring of its process tree but does not prevent behavioral rules from firing if the rule matches on child process characteristics. On versions prior to 9.2, behavioral detections still fire for trusted processes. On 9.2+, behavioral detections are disabled for Trusted Applications.

Remediations:
- Create an **Endpoint Alert Exception** targeting the specific rule ID and parent process:
  - `rule.id IS <rule-id>` AND `process.parent.executable IS /path/to/script`
- Upgrade to 8.19.11+ or 9.2+ for improved handling of trusted process behavioral rules.
- Review `linux.advanced.events` settings to disable unnecessary event types (e.g. `linux.advanced.events.dns` if DNS monitoring is not needed).
- Use **Event Filters** to reduce event volume from known-noisy directories without creating a monitoring blind spot.

To verify an exception is applied, check Fleet agent logs (dataset `elastic_agent.endpoint_security`) for `"Set user exception list"` messages.

### Output server disconnection causing retry storms

When the configured Logstash output server becomes unreachable (network route removed, server down, firewall change), `elastic-endpoint` enters a tight retry loop attempting to reconnect, consuming 100% CPU on one core. This was a bug in versions prior to 8.13.4.

Log messages indicating this issue:
- `Endpoint is setting status to DEGRADED, reason: Unable to connect to output server`
- `SSL handshake with Logstash server at [host]:[port] encountered an error: (null)`
- `Logstash connection is down`

CPU returns to normal within approximately 40 seconds after connectivity is restored. The command `sudo /opt/Elastic/Endpoint/elastic-endpoint test output` can be used to verify output connectivity — on affected versions this command itself will spike CPU when the output is unreachable.

Upgrade to 8.13.4+ where the retry loop includes proper backoff. Check `logs-elastic_agent.endpoint_security-*` for the error patterns above.

For Kafka outputs, `Message size too large` errors cause repeated delivery failures. On 8.18.3+, oversized messages are dropped gracefully instead of retried indefinitely.

### Events plugin hung hashing large binaries during policy application

During policy application, Elastic Defend hashes all running processes and their executables. When the file cache (`/opt/Elastic/Endpoint/state/cache.db`) is empty — first install, cache deleted, or after upgrade — the endpoint must hash every binary from scratch. Large binaries (e.g. Oracle at `/data/app/oracle/product/*/bin/oracle`) can cause the Events plugin to hang in `ConfigurationCallback` while performing SHA1 hashing, driving CPU to 100% for extended periods.

The endpoint will report status as CONFIGURING during this time:
- `Endpoint is setting status to CONFIGURING, reason: Policy Application Status`

On first run with an empty cache, the CONFIGURING phase can take 5–30 minutes depending on the number and size of running processes. This is expected behavior. Subsequent restarts are fast because the cache persists.

This behavior was improved in 8.14+ where the hashing is less likely to hang the Events plugin. On older versions, restarting the service (`sudo systemctl restart elastic-endpoint`) may temporarily resolve the hang.

Do not delete `/opt/Elastic/Endpoint/state/cache.db` unless necessary, as this forces a full re-hash of all binaries on the next start.

### Memory Threat Protection scanning large processes

Memory Threat Protection scans process memory for known malicious signatures. When a process with a large memory footprint launches (Firefox, Chrome, Java applications), the scan can consume 100% of one CPU core for several minutes and use significant memory (30%+ of 16 GB in one case).

To confirm, disable Memory Threat Protection in the policy and check if CPU drops. If it does, the options are:
- Add the specific process as a **Trusted Application** (e.g. `process.executable IS /usr/lib/firefox/firefox`) to bypass all monitoring including memory scanning.
- Add an **Endpoint Alert Exception** with `event.code IS memory_signature` AND `process.executable IS /path/to/process` to suppress only memory scanning alerts while keeping other monitoring active. This is the recommended approach as it reduces CPU from minutes to 1–2 seconds for that process while maintaining visibility.

### Third-party security product or kernel module conflicts

Other security products, eBPF-based tools, or kernel modules that hook into the same system call paths as Elastic Defend can cause elevated CPU from processing conflicts. AWS VPC CNI plugin's eBPF programs are a known conflict that can cause network policy failures after approximately 18 hours of coexistence.

Check for other security products in the process list and whether they appear in `elastic-endpoint top` output. If a conflict is identified, add the third-party product's processes as Trusted Applications and add Elastic Defend's paths to the third-party product's exclusion list.

For eBPF conflicts specifically, check if disabling network event collection (`linux.advanced.events.network` set to `false`) resolves the issue.

### Trusted Applications configured but not reducing CPU

If a Trusted Application entry has been added but CPU remains high for the trusted process, the entry may be misconfigured. Common mistakes:
- Using `file.path` (refers to files being acted upon) instead of `process.executable` (the running process binary).
- Using operator `is` with a wildcard pattern instead of `matches`.
- On versions prior to 9.2, behavioral detections still fire for trusted processes.
- On versions prior to 8.19.9 and 9.2.3, DNS, Security, and API events from trusted processes are not dropped early enough in the pipeline, so CPU overhead persists for those event types.

Verify the entry's field, operator, and value by querying `logs-endpoint.events.process-*` for the actual `process.executable` value. Refer to the trusted_apps knowledge base doc for detailed troubleshooting.


## Investigation priorities

1) Run `sudo elastic-endpoint top` on the affected host to identify which processes and processing stages consume the most CPU
2) Query `metrics-endpoint.metrics-*` for `Endpoint.metrics.system_impact` to identify the top processes by `overall.week_ms` and the dominant event category
3) Check if CPU spikes correlate with cron schedules or monitoring script execution intervals
4) Check `logs-elastic_agent.endpoint_security-*` for output connectivity errors (DEGRADED status, SSL handshake failures, Logstash connection down messages)
5) Check `metrics-endpoint.metadata_current-*` for the endpoint's agent version — many CPU issues have version-specific fixes (8.13.4 for retry storms, 8.14 for hashing hangs, 9.2 for behavioral rule bypass of trusted apps)
6) Review `linux.advanced.events` settings in the policy to determine which event types are enabled and whether unnecessary types can be disabled
7) If the endpoint status shows CONFIGURING for an extended period, check whether the file cache exists at `/opt/Elastic/Endpoint/state/cache.db` and how long ago the endpoint was installed or upgraded
