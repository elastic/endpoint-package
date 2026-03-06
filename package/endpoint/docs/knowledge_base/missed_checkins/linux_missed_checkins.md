---
type: automatic_troubleshooting
sub_type: missed_checkins
os: [Linux]
date: '2026-03-07'
---

## Symptom

An Elastic Defend endpoint on Linux appears as "Offline", "Inactive", or "Unhealthy" in the endpoint list. The agent has stopped checking in to Fleet, and no new metadata or policy response documents are being indexed for the host.


## Summary

Elastic Defend runs as a systemd service (`elastic-endpoint`) that communicates with the Elastic Agent over a local Unix domain socket and with Fleet Server over HTTPS. A missed check-in means the endpoint process has crashed, failed to start due to permission or environment issues, been killed by the OOM killer, or lost its communication channel. The `.fleet-agents` index tracks the agent's last check-in time, and `metrics-endpoint.metadata_current_*` tracks the endpoint's last metadata document. A gap between "last seen" and now indicates the endpoint stopped reporting.


## Common issues

### Endpoint process crash

When `elastic-endpoint` crashes on Linux, a core dump may be generated depending on the system's core dump configuration (`ulimit -c`, `kernel.core_pattern`). The crash may leave error entries in the system journal and in `logs-elastic_agent.endpoint_security-*`.

Check `journalctl -u elastic-endpoint` for segfault or abort messages. Check the configured core dump directory for dump files. If a crash occurred, restart the service with `systemctl restart elastic-endpoint`. Collect the core dump and endpoint logs for Elastic support if the crash recurs.

### Startup failure — exit status 203/EXEC (SELinux or permission issues)

Exit status 203 from systemd means the service binary could not be executed. On SELinux-enforcing systems, this is typically caused by the SELinux policy denying execution of the endpoint binary. On non-SELinux systems, it may indicate incorrect file permissions or a missing binary.

Run `ausearch -m avc -ts recent` to check for SELinux denials targeting the elastic-endpoint binary. If SELinux is the cause, create a custom policy module to allow execution, or set the correct SELinux context on the binary with `restorecon`. Verify the binary exists at the expected path and has execute permission (`chmod +x`).

### Startup failure — exit status 231 (wrong cgroup version)

Exit status 231 from systemd indicates the service cannot be started due to a cgroup configuration mismatch. This occurs on systems using cgroup v2 exclusively when the endpoint or agent expects cgroup v1, or when systemd resource control settings are incompatible.

Check `systemctl status elastic-endpoint` for the exact error. Verify whether the host uses cgroup v1, v2, or hybrid mode with `stat -fc %T /sys/fs/cgroup/`. If cgroup v2 is in use and the endpoint version does not support it, upgrade to a version with cgroup v2 support. As a workaround, some systems can enable hybrid cgroup mode via kernel boot parameters.

### "No valid comms client available"

This message in the endpoint state log means the endpoint process is running but cannot communicate with the Elastic Agent. This typically occurs when the agent was reinstalled or re-enrolled without properly stopping the existing endpoint, leaving the endpoint bound to a stale communication socket.

Check `logs-elastic_agent.endpoint_security-*` for the exact error message. Restarting both the Elastic Agent and elastic-endpoint services usually resolves the issue. If the problem persists, a full uninstall and reinstall of the agent may be required.

### Port conflicts on 6788/6789

The endpoint and agent communicate over local TCP ports 6788 and 6789. If another process has bound to these ports, the endpoint cannot establish its communication channel and will fail to start or lose connectivity.

Run `ss -tlnp | grep -E '6788|6789'` on the affected host to identify port conflicts. If another process is using these ports, either reconfigure the conflicting application or stop it. After resolving the conflict, restart the Elastic Agent service.

### Endpoint killed by OOM killer

The Linux OOM killer may terminate `elastic-endpoint` if the system is critically low on memory. This is common on hosts with limited RAM running multiple agents or services. The OOM kill event is logged in the kernel ring buffer.

Check `dmesg | grep -i "oom.*elastic"` or `journalctl -k | grep -i "oom"` for OOM kill events targeting the endpoint process. If the endpoint is consistently being OOM-killed, increase the host's available memory, reduce the endpoint's memory footprint by disabling unnecessary event types under `linux.advanced.events`, or adjust the system's `vm.overcommit_memory` and OOM score settings.

### Failed upgrade leaving endpoint in a broken state

An interrupted or failed agent upgrade can leave the endpoint in a partially updated state where binaries are mismatched or configuration files are corrupted. The endpoint may fail to start after the upgrade, or start but immediately crash.

Check the agent upgrade logs and `systemctl status elastic-endpoint` for failure details. If the service is in a failed state after an upgrade, attempt `systemctl restart elastic-endpoint`. If the restart fails, a clean reinstall of the Elastic Agent (uninstall, then re-enroll) is the most reliable remediation.


## Investigation priorities

1) Query `.fleet-agents` for the agent's `last_checkin` timestamp and current `status` to confirm the agent is offline
2) Query `metrics-endpoint.metadata_current_*` for the host's last metadata document timestamp to determine when the endpoint last reported
3) Query `logs-elastic_agent.endpoint_security-*` for crash, abort, or communication error messages around the time the endpoint went offline
4) Query `metrics-endpoint.policy-*` for FAILED policy responses that may indicate a configuration or startup issue
5) Check `journalctl -u elastic-endpoint` on the host for startup failures, SELinux denials, or crash messages
6) Run `ss -tlnp | grep -E '6788|6789'` on the host to check for port conflicts
7) Check `dmesg` or `journalctl -k` for OOM kill events targeting the endpoint process
