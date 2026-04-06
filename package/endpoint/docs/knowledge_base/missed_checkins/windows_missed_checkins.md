---
type: automatic_troubleshooting
sub_type: missed_checkins
os: [Windows]
date: '2026-03-09'
---

## Symptom

The Agent appears `ORPHANED` in Fleet, and Endpoint policy changes do not apply nor response actions can execute. In some cases thousands of endpoints go unhealthy simultaneously.

## Summary

Elastic Endpoint has lost communication with Elastic Agent, but is still protecting the system according to last known policy and sends all events and alerts to the stack.

## Common issues

### Elastic Agent not running

Elastic Agent crashed, has been explicitly disabled or removed.

### Communication between Agent and Endpoint services not working

Elastic Agent reports the Endpoint component as `FAILED` or `DEGRADED` with the message "Failed: endpoint service missed 3 check-ins". For troubleshooting see next symptom below.

## Symptom

Elastic Agent appears `UNHEALTHY` in fleet and Elastic Defend integration indicates errors. Elastic Agent reports the Endpoint component as `FAILED` or `DEGRADED` with the message "Failed: endpoint service missed 3 check-ins". Endpoint events, alerts, and metadata stop being ingested. In some cases thousands of endpoints go unhealthy simultaneously.

## Summary

The "missed 3 check-ins" message means Elastic Agent is running but the Endpoint process is not communicating with it. Elastic Agent expects Endpoint to check in over a local connection on ports 6788/6789 at regular intervals. When three consecutive check-ins are missed, Agent marks the Endpoint component as FAILED. The underlying cause is almost always that the Endpoint process has crashed, failed to start, or is stuck in a broken install/upgrade state.


## Common issues

### Endpoint process crash (dump file generated)

The Endpoint process can crash due to memory corruption, driver conflicts, or product bugs. When this happens, a crash dump file (`elasticendpoint.dmp`) is written to `C:\Program Files\Elastic\Endpoint\` or `C:\Program Files\Elastic\Endpoint\cache\CrashDumps\`. After a crash, the Endpoint service attempts to restart automatically, but if the crash is persistent (e.g. corrupted binary in memory), it can crash repeatedly — up to 15-16 times in quick succession — before Agent marks it as FAILED.

To investigate: check for `.dmp` files at the paths above. If a dump exists, run WinDbg with `!analyze -v` against it to identify the crash location. Check `logs-elastic_agent.endpoint_security-*` for patterns like `Aborting due to signal` or unhandled exception stack traces.

If the crash is caused by memory corruption (corrupted `.text` section of the Endpoint binary, random bit flips), it may be a transient hardware issue. Run Windows Memory Diagnostic or memtest86 to check for bad DIMMs. If the crash recurs at the same code location, collect the dump and report to Elastic support.

Restarting the Endpoint service or rebooting the host typically resolves transient crashes.

### Failed upgrade leaving Endpoint in broken state (exit status 231)

During a Windows shutdown or reboot, a race condition can cause Agent to be restarted by the Windows Service Control Manager (SCM) while the system is shutting down. Agent then triggers an Endpoint health check, determines Endpoint is unhealthy (because shutdown APIs are returning errors), and begins an uninstall/reinstall cycle. When the shutdown force-terminates this process mid-way, Endpoint is left in a partially uninstalled state.

On the next boot, the ELAM driver service may still be registered but its backing files are gone. Endpoint's install attempt fails with `exit status 231` and logs `ELAM driver service was unable to be deleted or scheduled for deletion` and `System reboot required to finish uninstall`.

To fix:
1. Reboot the host. In many cases a second reboot clears the stale ELAM service registration and allows Endpoint to self-repair.
2. If a reboot does not resolve it, manually clean up using the registry merge described in the Elastic support guidance, then run: `sc.exe failure "Elastic Agent" reset= 10 actions= restart/60000` to prevent the SCM from restarting Agent during future shutdowns.
3. If the Endpoint remains broken, take the matching-version `elastic-endpoint.exe` binary to the host and run `elastic-endpoint.exe uninstall --log stdout`, then restart Elastic Agent to trigger a clean install.

The root cause race condition was fixed in Agent 8.8.1. Upgrading to 8.8.1+ prevents recurrence.

### Windows image integrity verification failure after reboot

On some Windows versions (particularly Server 2012 R2 and Windows 8.1), the Endpoint binary may fail to start after a reboot with the Windows event log error: "Windows is unable to verify the image integrity of the file ... elastic-endpoint.exe because file hash could not be found on the system."

This is a symptom of the same shutdown race condition described above. The partial uninstall corrupts the Endpoint's code signing state. The self-healing logic introduced in 8.4.3 attempts to repair on reboot, but the repair can itself fail on certain OS versions if the rollback zip file was created but the reinstall was interrupted.

To fix: follow the same remediation as for exit status 231 above. Upgrade to Agent 8.8.1+ to prevent the triggering race condition.

### Unicode conversion crash on non-English Windows (pre-8.13.3)

On Windows systems using non-English locales (confirmed on Chinese GB2312 and Korean editions), a unicode conversion bug causes the Endpoint process to crash in a loop immediately after startup. The crash occurs during kernel communication initialization and produces hundreds of restarts per log file. Agent reports the Endpoint as FAILED because it never completes startup.

This was fixed in Endpoint 8.13.3.

To fix: upgrade to 8.13.3 or later. If the system is an English-locale Windows installation, this is not the cause.

### Port conflict on 6788/6789

Elastic Agent and Endpoint communicate over TCP ports 6788 and 6789 on localhost. If another process is already bound to one of these ports, Endpoint cannot establish its communication channel with Agent and will miss check-ins.

To check: run `netstat -ano | findstr "6788 6789"` on the affected host. If a non-Elastic process is listening on either port, it must be reconfigured to use a different port.

### Artifact download or verification failure causing mass unhealthiness

When Endpoint receives a new policy, it must download and verify user artifact manifests (trusted apps, exception lists, blocklists) from Fleet Server. If the artifact manifest is corrupted — for example, `compression_algorithm` is set to `none` instead of `zlib` due to a known stack bug fixed in 8.7.1 — Endpoint rejects all artifacts and the policy fails to apply. Logs show `All artifacts are being rejected because endpoint-trustlist-windows-v1 is invalid` and `Failed to process artifact manifest`.

At scale, simultaneous policy pushes can also overwhelm Fleet Server, producing HTTP 429 responses and causing a cascading failure where all endpoints go unhealthy at once.

To fix the artifact corruption bug: add or remove an entry in the affected artifact list (e.g. add a dummy Trusted Application for Windows, then delete it) to force a manifest rebuild. Then upgrade the stack to 8.7.1+ to prevent recurrence. For scale-related 429 failures, ensure Fleet Server has adequate resources and consider staggering policy updates.

### Endpoint service killed by OOM or resource limits

If Windows terminates the Endpoint process due to excessive memory usage or if a system-level resource limit is hit, the Endpoint stops running and Agent reports missed check-ins. This is more common on hosts with constrained memory or where Endpoint is processing very high event volumes.

Check Windows Event Viewer (System log) for process termination events referencing `elastic-endpoint.exe`. Review `metrics-endpoint.metrics-*` for memory usage trends leading up to the failure.


## Investigation priorities

1) Check `.fleet-agents*` for the agent's `last_checkin` timestamp and current status to confirm the endpoint is actually missing check-ins vs. the entire agent being offline
2) Check `logs-elastic_agent.endpoint_security-*` for error messages: look for `exit status 231`, `ELAM driver`, `Aborting due to signal`, `No valid comms client available`, `CompletionPort.cpp`, or `Failed to process artifact manifest`
3) Check `metrics-endpoint.policy-*` for FAILED policy responses indicating the endpoint tried to start but could not apply its policy
4) Look for `.dmp` files on the host at `C:\Program Files\Elastic\Endpoint\` and `C:\Program Files\Elastic\Endpoint\cache\CrashDumps\`
5) Run `netstat -ano | findstr "6788 6789"` on the host to check for port conflicts
6) Check `metrics-endpoint.metadata_current_*` for the last known endpoint version and health status — if the metadata timestamp has a gap, the endpoint was offline during that period
7) Check the agent version — if pre-8.8.1, the shutdown race condition is a likely cause; if pre-8.13.3 on non-English Windows, the unicode bug is a likely cause
