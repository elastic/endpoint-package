---
type: automatic_troubleshooting
sub_type: incompatible_software
date: '2026-03-11'
---

## Symptom

A third-party application malfunctions, crashes, or causes system instability when Elastic Defend (or the Endgame Sensor) is installed. Common manifestations include: application crashes (e.g. browsers closing unexpectedly), network policies or VPN functionality breaking, CPU spikes rendering the system unresponsive, or virtual machines hanging during policy changes. The issue resolves when the endpoint security product is uninstalled or specific protection features are disabled.


## Summary

Elastic Defend operates at multiple system levels — kernel-mode drivers for file system and network filtering, user-mode DLL injection for exploit protection (Endgame Sensor), and eBPF probes on Linux for host isolation and event collection. These deep integrations can conflict with other software that operates at similarly privileged levels: other security products with kernel drivers, eBPF-based networking tools, VPN clients that intercept DNS or network traffic, and applications that generate extreme volumes of system activity.

The resolution depends on which Elastic Defend subsystem is conflicting. In many cases, targeted policy changes (disabling a specific event type or protection feature) can restore compatibility without removing protection entirely. In other cases, a Trusted Application entry or an agent upgrade resolves the conflict.


## Common issues

### AWS VPC CNI plugin eBPF conflict on Linux (Kubernetes)

On Linux nodes running both Elastic Defend and the AWS VPC CNI plugin (which uses eBPF for Kubernetes network policies), the CNI plugin's network policies stop enforcing correctly after a variable period — typically around 18 hours. Traffic that should be denied by a `NetworkPolicy` is unexpectedly allowed.

The root cause is that Elastic Defend installs TC (Traffic Control) eBPF probes to implement host isolation. The endpoint installs its TC probes forcefully to ensure priority, which can disable or override other TC eBPF probes on the system, including those used by the AWS VPC CNI `aws-network-policy-agent`. Disabling network event collection in the Elastic Defend policy alone does not resolve this because the TC probes are installed for host isolation, not event collection.

When Elastic Defend is deployed as a Kubernetes DaemonSet, host isolation is automatically disabled and the TC probes are not installed. However, DaemonSet deployment is not officially supported. For process-based installations on Kubernetes nodes, set `linux.advanced.host_isolation.allowed` to `false` in the Elastic Defend advanced policy settings. This completely disables the host isolation plugin and prevents Elastic Defend from installing any TC eBPF probes, eliminating the conflict with other eBPF-based networking tools.

This conflict is not limited to AWS VPC CNI — any eBPF-based networking tool using TC probes (e.g. Cilium, Calico eBPF mode) may be affected.

### Browser crashes from exploit protection DLL after Windows updates (Endgame Sensor)

On systems running the Endgame Sensor, Chrome, Edge, and potentially other Chromium-based browsers crash within seconds of opening. The crash dump shows a heap corruption or access violation in `esensordbi.dll` (the Endgame exploit protection injection DLL), specifically in `HookManager_InstallExternalHook`. This issue is triggered by specific Windows security updates (e.g. KB5074109 on Windows 11 25H2) that change the set of DLLs loaded into browser processes.

The root cause is a bug in the Endgame Sensor's hook manager linked list. When the maximum number of hooks (4) for a particular function in a module is reached, the error handling path frees a `HOOK_ENTRY` that is still part of the global hook list. The next traversal of the list encounters corrupted `flink`/`blink` pointers and crashes. Windows updates that add new DLLs to browser processes increase the number of hooks installed, making it more likely to hit the limit and trigger the bug.

**Fixed in**: Endgame Sensor 3.65.3.

**Workaround** (for older sensor versions): In the Endgame policy under Threats > Exploit, uncheck Chrome and Edge to disable exploit protection injection into those browsers. Additionally, under Settings > Event Collection > Windows Event Collection, disable beta event sources. This prevents `esensordbi.dll` from being injected into the affected processes.

Disabling exploit protection for browsers reduces defense against browser exploitation. Keep browsers and the OS fully patched to minimize the window of exposure.

### Security products causing CPU spikes via high-volume network activity (Silverfort, CrowdStrike)

Other security products running alongside Elastic Defend can generate extreme volumes of network connections, overwhelming Endpoint's network event processing pipeline. The system becomes unresponsive or experiences sustained 100% CPU usage.

Silverfort AD Adapter on Windows domain controllers is a well-documented example. Silverfort duplicates DC network packets using WinDivert to send them to the Silverfort server for identity threat analysis, generating over 10,000 TCP connect/disconnect events within seconds. Each event triggers Elastic Defend's network event processing pipeline, including enrichment and behavioral rule evaluation. Even with Silverfort executables added as Trusted Applications, the kernel driver still captures the network activity — the Trusted Application evaluation happens in user mode after significant processing has already occurred.

For these cases, disabling either behavioral protections or network event collection alone may not resolve the issue — both feed from the same kernel-level network data. The most effective mitigations are:

1. Set `windows.advanced.kernel.network: false` to disable the kernel network driver entirely. This eliminates all network event processing overhead. Host isolation remains functional because issuing an isolation task temporarily re-enables the network filter.
2. Upgrade to Elastic Defend 8.16+ where the kernel driver drops network activity from Trusted Applications much earlier in the pipeline, significantly reducing CPU overhead from high-volume trusted processes.
3. Set `windows.advanced.network_events_exclude_local: true` to drop RFC 1918 private IP traffic in user mode, which can help if the conflicting software generates primarily internal traffic.

CrowdStrike and other kernel-mode security products can cause similar contention through file system, registry, and network filter driver callbacks competing with Elastic Defend's driver.

### VPN clients causing DNS resolution failures on macOS

VPN clients such as Twingate and Palo Alto GlobalProtect can conflict with Elastic Defend's network event collection on macOS. The conflict typically manifests as DNS resolution failures — internal domains fail to resolve while the VPN is connected and Elastic Defend is running, but resolve correctly when either product is disabled.

Elastic Defend's network monitoring on macOS intercepts DNS traffic to generate DNS events. VPN clients that implement split-tunnel DNS or custom DNS routing may conflict with this interception, causing DNS queries to be dropped or routed incorrectly.

To diagnose: compare DNS resolution behavior with Elastic Defend enabled vs disabled while the VPN is connected. Use `nslookup` or `dig` to test resolution of both internal (VPN-routed) and external domains.

To resolve: if DNS events are not essential, disable DNS event collection in the Elastic Defend policy. If DNS events are needed, add the VPN client process as a Trusted Application to stop Endpoint from monitoring its network activity. If the conflict persists, set `mac.advanced.capture.env.dns: false` in advanced policy settings to disable DNS event capture at a lower level.

### Microsoft DFSR replication issues with file monitoring

On Windows Server systems running Distributed File System Replication (DFSR), Elastic Defend's file system filter driver can interfere with replication operations. Symptoms include replication backlogs, unexpected staging folder growth, or DFSR service errors in the event log. The issue is exacerbated when rollback self-healing (`windows.advanced.artifacts.global.rollback.self_healing.enabled`) is active, as Elastic Defend may detect and attempt to roll back legitimate DFSR staging operations that involve suspicious file patterns.

To mitigate: add the DFSR process (`C:\Windows\System32\DFSRs.exe`) as a Trusted Application. If rollback self-healing is causing excessive I/O on DFSR servers, consider disabling it via advanced policy settings on the affected endpoints. Monitor the DFSR staging folder size and replication backlog after changes to confirm the conflict is resolved.

### Network event collection causing VM hangs in Citrix/VDI environments

In virtual desktop infrastructure (VDI) environments — particularly Citrix — enabling network event collection in the Elastic Defend policy can cause virtual machines to hang during policy changes or system shutdown. The VM becomes unresponsive, the RDP session terminates, and the endpoint shows as inactive in Fleet. A hard reboot of the VM is required.

The issue occurs because the kernel network driver's initialization or reconfiguration during a policy change blocks other system operations in the VM's constrained environment. Disabling network event collection in the policy prevents the hang.

If network visibility is required in VDI environments, test policy changes during maintenance windows and consider using `windows.advanced.kernel.network: false` as an alternative to full network event disablement — this disables the kernel driver while allowing behavioral protections that do not depend on kernel-level network capture to remain active.


## Investigation priorities

1) Identify the conflicting third-party software by correlating the onset of symptoms with software installation, updates, or configuration changes. Query `logs-endpoint.events.process-*` for recently started processes that match known conflicting software.
2) Determine which Elastic Defend subsystem is involved — kernel network driver (`windows.advanced.kernel.network`), eBPF probes (`linux.advanced.host_isolation.allowed`), exploit protection DLL injection (Endgame policy), or file system filter driver. Each has different mitigation controls.
3) Check `metrics-endpoint.metrics-*` for CPU usage patterns and correlate with `logs-endpoint.events.process-*` for processes generating high event volumes. Use `elastic-endpoint top` on the affected host to identify which processes and event types drive resource consumption.
4) For browser crashes on Windows, collect crash dumps from `%HOMEPATH%\AppData\Local\Google\Chrome\User Data\Crashpad\reports` or `%LOCALAPPDATA%\CrashDumps` and check for `esensordbi.dll` in the faulting module. Verify the Endgame Sensor version and check if a fix is available.
5) For eBPF conflicts on Linux Kubernetes nodes, verify whether host isolation is needed. If not, set `linux.advanced.host_isolation.allowed` to `false` and confirm network policies resume correct enforcement.
6) For CPU spikes caused by security products, use ProcMon or `elastic-endpoint top` to identify the process generating the most network events. Set `windows.advanced.kernel.network: false` as immediate mitigation, then plan an upgrade to 8.16+ where Trusted Application network event filtering is more efficient.
7) Check `logs-elastic_agent.endpoint_security-*` for error patterns that correlate with the onset of the incompatibility, including driver initialization failures, output errors, or crash recovery messages.
