---
type: automatic_troubleshooting
sub_type: missed_checkins
os: [Windows]
date: '2026-03-07'
---

## Symptom

An Elastic Defend endpoint on Windows appears as "Offline", "Inactive", or "Unhealthy" in the endpoint list. The agent has stopped checking in to Fleet, and no new metadata or policy response documents are being indexed for the host.


## Summary

Elastic Defend runs as a Windows service (`ElasticEndpoint`) that communicates with the Elastic Agent over local named pipes and with Fleet Server over HTTPS. A missed check-in means the endpoint process has either crashed, failed to start, lost its communication channel to the agent, or been killed by the OS. The `.fleet-agents` index tracks the agent's last check-in time, and `metrics-endpoint.metadata_current_*` tracks the endpoint's last metadata document. A gap between "last seen" and now indicates the endpoint stopped reporting.


## Common issues

### Endpoint process crash

When `elastic-endpoint.exe` crashes, it generates a dump file (`elasticendpoint.dmp`) in `C:\Program Files\Elastic\Endpoint\`. The service may or may not automatically restart depending on the Windows service recovery settings. A crash often leaves error entries in the Windows Application event log and in `logs-elastic_agent.endpoint_security-*`.

Check for `.dmp` files in the Endpoint installation directory. If a dump file exists, the endpoint crashed and needs to be restarted or reinstalled. Collect the dump file and endpoint logs for Elastic support if the crash recurs after restart.

### "No valid comms client available"

This message in the endpoint state log means the endpoint process is running but cannot communicate with the Elastic Agent. This typically occurs when the agent was reinstalled or re-enrolled without properly stopping the existing endpoint, leaving the endpoint bound to a stale communication channel.

Check `logs-elastic_agent.endpoint_security-*` for the exact error message. Restarting both the Elastic Agent service and the ElasticEndpoint service usually resolves the issue. If the problem persists, a full uninstall and reinstall of the agent may be required.

### Port conflicts on 6788/6789

The endpoint and agent communicate over local TCP ports 6788 and 6789. If another process has bound to these ports, the endpoint cannot establish its communication channel and will fail to start or lose connectivity.

Run `netstat -ano | findstr "6788 6789"` on the affected host to identify port conflicts. If another process is using these ports, either reconfigure the conflicting application or stop it. After resolving the conflict, restart the Elastic Agent service.

### Failed upgrade leaving endpoint in a broken state

An interrupted or failed agent upgrade can leave the endpoint in a partially updated state where binaries are mismatched or configuration files are corrupted. The endpoint may fail to start after the upgrade, or start but immediately crash.

Check the agent upgrade logs and the endpoint service status. If the service is in a failed state after an upgrade, attempt a manual restart. If the restart fails, a clean reinstall of the Elastic Agent (uninstall, then re-enroll) is the most reliable remediation.

### Endpoint service killed by resource limits

Windows may terminate the endpoint process if it exceeds memory limits enforced by a Group Policy Job Object, or if the system is critically low on resources. This is more common in resource-constrained environments such as VDI instances or servers with aggressive memory policies.

Check the Windows System event log for termination events referencing the `ElasticEndpoint` service. Review the host's available memory and any GPO-enforced resource limits. If the endpoint is consistently being killed, consider increasing the host's available resources or adjusting the endpoint's policy to reduce memory footprint (disable unnecessary event types under `windows.advanced.events`).

### Antivirus or EDR quarantining endpoint binaries

In rare cases, another security product may quarantine or block Elastic Defend binaries, preventing the service from starting. This is especially common on initial deployment before exclusions are configured.

Check the other security product's quarantine log or event history. Add exclusions for the Elastic Defend installation directory (`C:\Program Files\Elastic\`) in the other product's configuration.


## Investigation priorities

1) Query `.fleet-agents` for the agent's `last_checkin` timestamp and current `status` to confirm the agent is offline
2) Query `metrics-endpoint.metadata_current_*` for the host's last metadata document timestamp to determine when the endpoint last reported
3) Query `logs-elastic_agent.endpoint_security-*` for crash, abort, or communication error messages around the time the endpoint went offline
4) Query `metrics-endpoint.policy-*` for FAILED policy responses that may indicate a configuration or startup issue
5) Check for `.dmp` files on the host at `C:\Program Files\Elastic\Endpoint\` to confirm a crash occurred
6) Run `netstat -ano | findstr "6788 6789"` on the host to check for port conflicts
