---
type: automatic_troubleshooting
sub_type: high_cpu
os: [Windows]
date: '2026-03-09'
---

## Symptom

Elastic Defend's `elastic-endpoint.exe` process consumes sustained high CPU on Windows hosts, causing system slowdown, application unresponsiveness, or login delays. CPU may spike during specific activities (application launches, user logons, Office updates) or build gradually over hours until the system becomes unusable.


## Summary

Elastic Defend performs real-time file hashing, digital signature verification, memory scanning, behavioral rule evaluation, and event enrichment. Each protection layer adds processing overhead, and the cumulative effect depends on the workload profile of the host. The most common drivers of high CPU on Windows are third-party security product conflicts creating mutual scanning loops, high-volume security events (logon/logoff) overwhelming the Malicious Behavior engine, file-intensive operations triggering repeated hashing of large binaries, and VDI/Citrix environments where the file metadata cache is empty on every session.

Use `elastic-endpoint top` on the affected host to identify which processes and internal processing stages (MLWR, BHVR, RULES, etc.) consume the most CPU. Query `metrics-endpoint.metrics-*` for `Endpoint.metrics.system_impact` to identify the top processes by `overall.week_ms` remotely.


## Common issues

### Third-party security product conflicts

When another security product (Silverfort, Symantec/Broadcom, N-Able AV Defender, CrowdStrike) runs alongside Elastic Defend, each product intercepts the other's file and process activity, creating a scanning feedback loop. This commonly manifests as sustained 100% CPU with both products' processes at the top of task manager.

Silverfort is a particularly acute case on Domain Controllers because its `SilverfortServer.exe` generates over 10,000 TCP connections per minute via WinDivert, each producing a network event that Elastic Defend must process. Combined with Malicious Behavior Protection requiring network event enrichment, this can saturate CPU and eventually cause blue screens.

Add all 3rd party security applications as **Trusted Applications** in Elastic Defend to break feedback loops. Also add Elastic Defend's paths to the third-party product's exclusion list.
To confirm the problem on Endpoint side check `elastic-endpoint top` for the third-party product's processes. If they dominate `overall.week_ms` in the metrics.

For Silverfort specifically, if Trusted Applications are not sufficient due to sheer network event volume, set `windows.advanced.kernel.network` to `false` in the policy's advanced settings to stop network event generation at the kernel level. This disables host isolation capability.

### High security event volume (logon/logoff events)

On hosts with heavy authentication activity (print servers, file servers, Domain Controllers), Windows Security event log entries 4624 (Logon) and 4634 (Logoff) can generate tens of events per second. When Malicious Behavior Protection is enabled, Elastic Defend collects and processes Security events regardless of whether Security event collection is enabled in the policy, because the malicious behavior rules need this data.

A host generating 60+ logon/logoff events per second will see sustained high CPU from the event or Malicious Behavior processing pipelines. Query `metrics-endpoint.metrics-*` and check `Endpoint.metrics.system_impact` — if `authentication_events` dominates, this is the cause.

Remediations:
- On 9.2.0+, use the advanced policy setting `windows.advanced.events.security.event_disabled` to exclude event IDs 4624 and 4634 specifically.
- On older versions, add `C:\Windows\System32\lsass.exe` as a Trusted Application to drop logoff events (attributed to lsass). This reduces visibility into lsass file and registry activity.
- Disabling Malicious Behavior Protection stops Security event collection entirely but removes behavioral detection capability.
- Removing "Security" from the Event Collection settings in the policy does not help while Malicious Behavior Protection is enabled, since behavioral rules require these events.

### File-intensive operations and large binary hashing

Elastic Defend hashes and verifies digital signatures of executables and DLLs when they are loaded. Large binaries like `msedge.dll` (195 MB) can take 10–15 seconds per hash operation. On hosts running browsers, Office applications, or developer tools that load many large DLLs, this creates sustained CPU spikes.

The endpoint maintains a file metadata cache to avoid re-hashing known files.

Office update processes, backup software (Veeam, Commvault), and database servers (SQL Server) that perform continuous file I/O also trigger high hashing overhead. Add these as Trusted Applications if full monitoring bypass is acceptable, or use **Event Filters** to reduce event volume without creating a blind spot.

### VDI, Citrix, and RDS environments with empty cache

On non-persistent VDI, Citrix, or RDS environments, every new user session starts with an empty file metadata cache. This forces Elastic Defend to hash and verify every executable and DLL from scratch, causing CPU spikes of 30%+ during login that can last several minutes.

On a 3,000-endpoint VDI deployment running 8.13.4, login times reached 6 minutes with Elastic Defend. Adding `C:\Program Files\*` and `C:\Program Files (x86)\*` as Trusted Applications reduced login time to under 3 minutes and CPU from 30% to 5%. This is acceptable when users cannot write to Program Files (requires admin privileges).

For a more targeted approach, use **Endpoint Alert Exceptions** to disable specific protections rather than bypassing all monitoring:
- `event.code IS malicious_file` with `file.path MATCHES C:\Program Files\*` for malware scanning
- `event.code IS memory_signature` with `process.executable MATCHES C:\Program Files\*` for memory scanning

To pre-populate the cache in VDI template images: install Elastic Defend on the base image, log in once so the cache at `C:\Program Files\Elastic\Endpoint\state\cache.db` is populated, then snapshot. The cache persists across sessions and eliminates first-login hashing overhead.

Upgrade to 8.18.0+ for significant performance improvements in CPU, memory, application responsiveness, and Windows startup time on VDI.

### Output connectivity issues causing retry storms

When the configured output (Logstash, Kafka, or Elasticsearch) becomes unreachable, Elastic Defend may enter a tight retry loop that consumes 100% CPU on one core. This is most common with Logstash outputs and was fixed for the worst case in 8.13.4.

Symptoms include `elastic-endpoint` CPU spiking shortly after the output becomes unreachable, with log messages like:
- `Endpoint is setting status to DEGRADED, reason: Unable to connect to output server`
- `SSL handshake with Logstash server at [host]:[port] encountered an error`
- `Logstash connection is down`

Check `logs-elastic_agent.endpoint_security-*` for these error patterns. CPU returns to normal within approximately 40 seconds after connectivity is restored. Upgrade to 8.13.4+ to fix the retry loop behavior.

For Kafka outputs, `Message size too large` errors cause repeated delivery failures. On 8.18.3+, oversized messages are dropped gracefully instead of retried.

### DNS, Security, and API events not dropped early enough for Trusted Applications (pre-8.19.9 / pre-9.2.3)

On versions prior to 8.19.9 and 9.2.3, Elastic Defend did not determine that DNS, Security, and API events originated from Trusted Applications until after most event processing had already completed. The endpoint still used CPU, I/O, and memory to create and enrich these events even though they were ultimately discarded.

To test: disable all protections and event sources except DNS, Security, and API, then check CPU. If CPU remains high, also disable those three — if CPU drops, this bug is the cause. Upgrade to 8.19.9+ or 9.2.3+ for the fix. As a workaround on older versions, set `windows.advanced.events.api` to `false`.


## Investigation priorities

1) Run `elastic-endpoint top` on the affected host to identify which processes and processing stages consume the most CPU
2) Query `metrics-endpoint.metrics-*` for `Endpoint.metrics.system_impact` to identify the top processes by `overall.week_ms` and the dominant event category (authentication_events, file_events, network_events, etc.)
3) Check for third-party security products in the process list and whether they appear in `elastic-endpoint top` output
4) Check `logs-elastic_agent.endpoint_security-*` for output connectivity errors (DEGRADED status, SSL handshake failures, Logstash/Kafka errors)
5) Check `metrics-endpoint.metadata_current-*` for the endpoint's agent version — many CPU issues have version-specific fixes
6) Review `windows.advanced.events` settings in the policy to determine which event types are enabled and whether unnecessary types can be disabled
7) For VDI/Citrix environments, check whether the file cache (`cache.db`) persists across sessions
