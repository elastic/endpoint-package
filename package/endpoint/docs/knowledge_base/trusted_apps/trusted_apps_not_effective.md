---
type: automatic_troubleshooting
sub_type: trusted_apps
link: https://www.elastic.co/docs/solutions/security/manage-elastic-defend/optimize-elastic-defend
date: '2026-03-09'
---

## Symptom

A Trusted Application has been configured in Elastic Defend, but the endpoint still appears to monitor the trusted process, consume high CPU for it, or generate alerts related to it. The process may still appear in `elastic-endpoint top` output, or malware/behavioral alerts continue to fire.


## Summary

A Trusted Application tells Elastic Defend to stop monitoring a process entirely — it creates an intentional blind spot. This is fundamentally different from an Endpoint Alert Exception, which only suppresses alerts while continuing to monitor. Many "trusted app not working" issues stem from using the wrong artifact type, misconfiguring the entry's condition fields, or running a version affected by known event-processing bugs.

Key distinction:
- **Trusted Application**: Stops Endpoint from *monitoring* the process. Use only for software conflicts or performance issues where full bypass is acceptable.
- **Endpoint Alert Exception**: Stops Endpoint from *generating alerts or blocking processes*. Use for false positives where you still want monitoring.

Even when working correctly, Trusted Applications still generate process events for visualizations and internal Elastic Stack use. Some CPU usage from a trusted process is expected.


## Common issues

### Wrong condition field or value

The most common misconfiguration is a Trusted Application entry whose condition field does not match the actual process data. For example, using `file.path` (which refers to a file being acted upon) instead of `process.executable` (the running process binary), or specifying a directory path like `C:\Program Files\Software\` instead of the full executable path like `C:\Program Files\Software\app.exe`.

Verify the entry's field and value by querying `logs-endpoint.events.process-*` for the actual `process.executable` value of the target process. Ensure the Trusted Application entry uses `process.executable` with the exact path as reported in event data. If the path contains a directory, append a wildcard (e.g. `C:\Program Files\Software\*`) and use the `matches` operator rather than `is`.

### Incorrect wildcard syntax

Wildcard entries require the `matches` operator in the Trusted Application condition. Using the `is` operator with a wildcard pattern (e.g. `C:\Temp\*\bin\app.exe` with operator `is`) will attempt a literal string match and fail silently. Always select `matches` when using `*` or `?` wildcards in path values.

### Behavioral detections still firing (pre-9.2)

On Elastic Defend versions prior to 9.2, behavioral detection alerts still fire for processes marked as Trusted Applications. The Trusted Application entry stops direct file-level threat analysis but the behavioral protection engine continues monitoring system-wide activity patterns including actions by trusted processes.

On 9.2+, behavioral detections are turned off for Trusted Applications to improve performance. If the endpoint is running a version before 9.2, either upgrade or create an Endpoint Alert Exception to suppress the specific behavioral alerts.

### DNS, Security, and API events not dropped early enough (pre-8.19.9 / pre-9.2.3)

On versions prior to 8.19.9, 9.2.3, or 9.3.0, Elastic Defend did not determine that DNS, Security, and API events originated from Trusted Applications until after most event-related processing had already been performed. This meant the endpoint still used CPU, I/O, and memory to create and enrich these events even though they were ultimately discarded.

To test if this affects you: disable all protections and all event sources except DNS, Security, and API, then check if CPU remains high. If so, also disable DNS, Security, and API events — if CPU drops, this bug is the cause. Upgrade to 8.19.9+, 9.2.3+, or 9.3.0+ where the fix drops these events much earlier in the pipeline. As a workaround on older versions, set `windows.advanced.events.api` to `false` in the Advanced Policy settings.

### Confusing Trusted Applications with Endpoint Alert Exceptions

Users often create a Trusted Application when they actually need an Endpoint Alert Exception. If the goal is to stop alerts from firing for a legitimate process (a false positive), an Endpoint Alert Exception is the correct artifact — it suppresses alerts while keeping monitoring active. A Trusted Application is overkill for this use case and creates an unnecessary blind spot.

Common scenarios where an Endpoint Alert Exception should be used instead:
- Malware engine false positive on a known-good binary: add an exception on the file hash.
- Malware On Write blocking a legitimate file: Trusted Applications operate at the process level and do not prevent Malware On Write from scanning files as they are written to disk by another process (e.g. `explorer.exe` extracting an archive). Use an Endpoint Alert Exception for the specific file.
- Process injection alerts for legitimate software: use an Endpoint Alert Exception targeting the specific alert fields.

### Trusted Application assigned to wrong policy or OS

A Trusted Application entry is scoped to specific integration policies. If the entry is not assigned to the policy covering the affected endpoint, it has no effect. Similarly, a Trusted Application configured for the wrong OS will not apply.

In the Kibana Trusted Applications UI, verify the "Assignment" column shows the correct integration policy. If using "Global" assignment, confirm the affected endpoint's policy is not explicitly excluded.

### Network drive or VHD path mapping mismatch

On Windows, processes running from mounted VHD drives or mapped network shares may report their executable path using NT/kernel path format (e.g. `\\?\Volume{guid}\path\app.exe`) instead of the expected Win32 path (e.g. `V:\path\app.exe`). If the Trusted Application entry uses the drive letter path but the endpoint resolves the kernel path, the entry will not match.

Query `logs-endpoint.events.process-*` for the affected process to check the actual `process.executable` value. If it uses a volume GUID path, add an additional Trusted Application entry using a wildcard pattern like `\\?\Volume{*}\path\app.exe` with the `matches` operator.


## Investigation priorities

1) Confirm the Trusted Application entry's condition field (`process.executable`), operator (`is` vs `matches`), and value match the actual process path by querying `logs-endpoint.events.process-*`
2) Query `logs-endpoint.alerts-*` for alerts still triggering on the process to determine the alert type (malware, behavioral, process injection) and whether an Endpoint Alert Exception is the correct fix
3) Check the endpoint's agent version — if pre-9.2, behavioral alerts are expected for trusted apps; if pre-8.19.9/9.2.3, DNS/Security/API event processing overhead is expected
4) Verify the Trusted Application is assigned to the correct integration policy covering the affected endpoint
5) If CPU is the concern, run `elastic-endpoint top` to confirm whether the trusted process still appears and which processing stage (BHVR, RULES, etc.) is consuming CPU
6) Check the `process.executable` value for non-standard path formats (volume GUIDs, UNC paths) that may not match the Trusted Application entry
