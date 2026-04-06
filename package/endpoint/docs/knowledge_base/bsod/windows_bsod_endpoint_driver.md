---
type: automatic_troubleshooting
sub_type: bsod
os: [Windows]
date: '2026-03-09'
---

## Symptom

A Windows system running Elastic Defend experiences a Blue Screen of Death (BSOD) or kernel crash. The memory dump analysis references `elastic_endpoint_driver.sys` or `elastic-endpoint-driver.sys`. The crash may occur shortly after an agent upgrade, 3rd party security product installation or its configuration change, during heavy I/O workloads, or after the system has been running for some time with many network connections. In severe cases the system enters a boot loop.


## Summary

Elastic Defend uses a kernel-mode driver (`elastic_endpoint_driver.sys`) for file system filtering, network monitoring, and process/object callbacks. Most BSOD issues traced to the endpoint driver fall into a few categories: regressions introduced in specific driver versions, conflicts with other kernel-mode drivers (third-party security products), or running on unsupported OS versions.

Collecting a full kernel memory dump and sharing it with Elastic Support is essential for root-cause determination. The bugcheck code alone is not sufficient — the faulting call stack identifies which code path triggered the crash.


## Common issues

### Network driver pool corruption (8.17.8, 8.18.3, 9.0.3)

A regression in the network driver introduced in Elastic Defend versions 8.17.8, 8.18.3, and 9.0.3 can cause kernel pool corruption on systems with a large number of long-lived network connections that remain inactive for 30+ minutes. The corruption manifests as BSODs with various bugcheck codes including `IRQL_NOT_LESS_OR_EQUAL`, `SYSTEM_SERVICE_EXCEPTION`, `KERNEL_MODE_HEAP_CORRUPTION`, or `PAGE_FAULT_IN_NONPAGED_AREA`.

This is the most frequently reported BSOD pattern and affects Windows Server environments with persistent connections (e.g. database servers, backup servers running Veeam with PostgreSQL).

**Affected versions**: 8.17.8, 8.18.3, 9.0.3 only.

**Fixed versions**: 8.17.9, 8.18.4, 9.0.4. Hotfix builds are also available: 8.18.3+build202507101319 and 9.0.3+build202507110136.

**Mitigation**: Upgrade to a fixed version. If immediate upgrade is not possible, set `advanced.kernel.network: false` in the Elastic Defend advanced policy settings to disable the kernel network driver.

### ODX-enabled volume crash (8.19.8, 9.1.8, 9.2.2)

A regression introduced in versions 8.19.8, 9.1.8, and 9.2.2 causes BSODs on systems with ODX (Offloaded Data Transfer) enabled volumes, particularly affecting Hyper-V clusters and Windows Server 2016 Datacenter. The crash can appear 2-3 hours after an agent upgrade, often triggered when the storage subsystem processes asynchronous offload write operations.

**Affected versions**: 8.19.8, 9.1.8, 9.2.2 only.

**Fixed version**: 9.2.4.

**Mitigation**: Upgrade to 9.2.4+ which contains the fix.

### Third-party kernel driver conflicts

Other security products running kernel-mode drivers can interfere with Elastic Defend's driver initialization or runtime operation. The most commonly reported conflicts include:

- **Trellix Access Control**: Trellix's kernel driver can intercept the Windows Base Filtering Engine (BFE) service, causing Defend's WFP (Windows Filtering Platform) driver initialization to hang or take an extremely long time. This interaction was introduced by an Elastic Defend refactor in 8.16.0. Fixed in 8.17.6, 8.18.1, and 9.0.1. Upgrade to a fixed version to resolve.

- **CrowdStrike, Kaspersky, Windows Defender coexistence**: Running multiple endpoint security products increases the probability of kernel-level interactions. Each additional kernel-mode filter driver introduces another point of contention for file system, registry, and network callbacks. When BSODs occur on systems with multiple security products, simplify by removing redundant products.

### Unsupported OS version

Upgrading Elastic Defend to a version that does not support the host's Windows version causes immediate BSODs or boot loops. Support for Windows Server 2012 R2 was dropped in 8.13.0 and re-added in 8.16.0. The system crashes during driver load because the driver uses kernel APIs unavailable on the older OS.

**Recovery**: Boot into Safe Mode or the Windows Recovery Console and delete `C:\Windows\System32\drivers\elastic-endpoint-driver.sys`. This prevents the driver from loading on the next boot. Then move the agent to a policy without the Elastic Defend integration, or upgrade to a version that re-added support (8.16.0+ for Windows Server 2012 R2).

**Prevention**: Check the [Elastic Defend support matrix](https://www.elastic.co/support/matrix) before upgrading agents across a fleet. Use separate agent policies for older OS versions that require pinned agent versions.

## Investigation priorities

1) Collect the full kernel memory dump (`C:\Windows\MEMORY.DMP` or minidumps from `C:\Windows\Minidump\`). Share the dump with Elastic.
2) Check the Elastic Defend version at the time of crash. Query `.fleet-agents*` for the agent version and `metrics-endpoint.metadata_current_*` for the endpoint version and OS details. Cross-reference against the known affected versions listed above (8.17.8, 8.18.3, 9.0.3 for network driver; 8.19.8, 9.1.8, 9.2.2 for ODX).
3) Determine whether the BSOD started after a specific agent or OS upgrade. Check `.fleet-agents*` for recent version changes and correlate with the crash timeline.
4) Identify other kernel-mode security products installed on the system. Look for drivers like `klflt.sys` (Kaspersky), `mfehidk.sys` (Trellix/McAfee), `csagent.sys` (CrowdStrike), or other filter drivers in the WinDbg module list.
5) Check the Windows version against the Elastic Defend support matrix. Query `metrics-endpoint.metadata_current_*` for `host.os.version` and `host.os.name`.
6) Look for gaps in endpoint metadata timestamps in `metrics-endpoint.metadata_current_*` — an offline gap followed by a version change often indicates a crash-recovery-rollback sequence.
7) Check `metrics-endpoint.policy-*` for `connect_kernel` failures, which indicate the driver failed to load or initialize properly after a crash.
8) If the system is in a boot loop, guide the user to boot into Safe Mode, delete the driver file at `C:\Windows\System32\drivers\elastic-endpoint-driver.sys`, then boot normally and downgrade or uninstall the agent.
