---
type: automatic_troubleshooting
sub_type: missed_checkins
os: [Linux]
date: '2026-03-09'
---

## Symptom

Elastic Agent reports the Endpoint component as `FAILED` or `DEGRADED` with the message "Failed: endpoint service missed 3 check-ins". The Endpoint may appear unhealthy in Fleet, and endpoint events, alerts, and metadata stop being ingested.


## Summary

The "missed 3 check-ins" message means Elastic Agent is running but the Endpoint process is not communicating with it. Elastic Agent expects Endpoint to check in over a local connection on ports 6788/6789 at regular intervals. When three consecutive check-ins are missed, Agent marks the Endpoint component as FAILED. On Linux, the most common causes are SELinux denying execution, systemd failing to start the service, the endpoint process crashing or being killed by the OOM killer, and port conflicts.


## Common issues

### SELinux blocking Endpoint execution (exit status 203/EXEC)

On RHEL, CentOS, and other SELinux-enforcing distributions, SELinux may prevent systemd from executing the Endpoint binary if the files under `/opt/Elastic/Endpoint/` have the wrong security context (e.g. `unlabeled_t` instead of `bin_t`). The systemd journal shows `code=exited, status=203/EXEC` and the Endpoint service restarts in a loop every 15 seconds.

The SELinux audit log confirms the denial. Check with: `ausearch -m avc -c '(endpoint)'` or search `/var/log/audit/audit.log` for `denied { execute }` referencing `elastic-endpoint`.

To fix:

```
sudo semanage fcontext -a -t bin_t '/opt/Elastic/Endpoint(/.*)?'
sudo restorecon -Rv /opt/Elastic/Endpoint
sudo systemctl restart ElasticEndpoint.service
```

This sets the correct SELinux file context so systemd is permitted to execute the Endpoint binary. The fix persists across Endpoint upgrades as long as the `semanage` rule remains.

### "No valid comms client available" in Endpoint logs

This message in the Endpoint state logs (`endpoint-*.log`) indicates that the Endpoint process started but cannot establish a communication channel with Elastic Agent. Common causes:

- The Agent process restarted or is not yet ready to accept connections when Endpoint initializes.
- A firewall rule or security policy is blocking localhost connections on ports 6788/6789.
- The Endpoint process is aborting shortly after startup due to another issue (look for `Aborting due to signal` immediately after the comms error).

If the comms error is followed by `Aborting due to signal`, focus on the root cause of the abort (often SELinux, a crash, or a permission issue) rather than the comms message itself.

### Wrong cgroup configuration (exit status 231)

On Linux systems using cgroup v2 exclusively or with non-standard cgroup configurations, the Endpoint service may fail to start with `exit status 231`. This typically occurs when systemd cannot place the Endpoint process into the expected cgroup hierarchy.

Check `journalctl -u ElasticEndpoint.service` for cgroup-related errors. Verify the system's cgroup version with `stat -fc %T /sys/fs/cgroup/` (returns `cgroup2fs` for v2). If the system uses a mixed cgroup setup or a container runtime that manages cgroups differently, the Endpoint service unit file may need adjustment.

### Endpoint process crash or core dump

The Endpoint process can crash due to bugs, memory corruption, or incompatible kernel modules. On Linux, a core dump may be generated depending on the system's `ulimit -c` setting and core dump handler configuration (e.g. `systemd-coredump`, `abrt`).

Check for:
- Core dumps via `coredumpctl list elastic-endpoint` (on systemd systems)
- Crash messages in `journalctl -u ElasticEndpoint.service`
- `Aborting due to signal` messages in Endpoint logs at `logs-elastic_agent.endpoint_security-*`

If the crash is reproducible, collect the core dump and Endpoint diagnostic output (`/opt/Elastic/Endpoint/elastic-endpoint diagnostics`) and report to Elastic support.

### Port conflict on 6788/6789

Elastic Agent and Endpoint communicate over TCP ports 6788 and 6789 on localhost. If another process is already bound to one of these ports, Endpoint cannot establish its communication channel with Agent and will miss check-ins.

To check: run `ss -tlnp | grep -E '6788|6789'` on the affected host. If a non-Elastic process is listening on either port, it must be reconfigured to use a different port, or the Endpoint communication port can be changed via advanced policy settings.

### Endpoint service killed by OOM killer or resource limits

If the Linux OOM killer terminates the Endpoint process due to memory pressure, or if systemd resource limits (e.g. `MemoryMax`, `TasksMax` in the service unit) are too restrictive, the Endpoint stops running and Agent reports missed check-ins.

Check for OOM kills with: `dmesg | grep -i "oom.*elastic-endpoint"` or `journalctl -k | grep -i oom`. Also check systemd's resource accounting: `systemctl status ElasticEndpoint.service` will show if the process was killed due to resource limits.

If the Endpoint is consistently using too much memory, investigate high-volume event sources using `elastic-endpoint top` and consider adding Event Filters to reduce processing load.

### Failed upgrade leaving Endpoint in broken state

An interrupted Endpoint upgrade (due to system shutdown, process kill, or disk space exhaustion during the upgrade) can leave the Endpoint in a partially installed state where it cannot start. The Agent log may show repeated install/upgrade attempts that fail.

To fix:
1. Run `elastic-endpoint diagnostics --log stdout --log-level trace` to capture the current state.
2. If the diagnostic shows a partial install, try restarting Elastic Agent: `sudo systemctl restart elastic-agent`.
3. If the restart does not resolve it, manually remove the Endpoint installation (`sudo /opt/Elastic/Endpoint/elastic-endpoint uninstall --log stdout`) and restart Elastic Agent to trigger a clean reinstall.

### Endpoint diagnostics returning "Denied" status

When the Endpoint is in a failed state, running `elastic-endpoint diagnostics` may return `Send status: Denied` because the Endpoint process is not running or not responding. This is a symptom, not a cause. The diagnostic tool requires a running Endpoint process to communicate with.

If diagnostics are denied, collect the Elastic Agent diagnostic bundle instead (`elastic-agent diagnostics`) which includes Endpoint logs even when the Endpoint process is not running.


## Investigation priorities

1) Check `journalctl -u ElasticEndpoint.service` for startup failures, exit codes (203, 231), and crash messages
2) Check `logs-elastic_agent.endpoint_security-*` for error messages: look for `No valid comms client available`, `Aborting due to signal`, `exit status 203`, or `exit status 231`
3) Check SELinux audit logs with `ausearch -m avc -c '(endpoint)'` for execution denials
4) Check `.fleet-agents*` for the agent's `last_checkin` timestamp and current status to confirm the endpoint is actually missing check-ins vs. the entire agent being offline
5) Run `ss -tlnp | grep -E '6788|6789'` on the host to check for port conflicts
6) Check `dmesg` and `journalctl -k` for OOM killer events targeting the Endpoint process
7) Check `metrics-endpoint.policy-*` for FAILED policy responses indicating the endpoint tried to start but could not apply its policy
8) Verify the Endpoint binary exists and has correct permissions: `ls -la /opt/Elastic/Endpoint/elastic-endpoint` and `file /opt/Elastic/Endpoint/elastic-endpoint` (confirm it is the correct architecture — x86-64 vs ARM)
