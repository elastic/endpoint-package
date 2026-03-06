---
type: automatic_troubleshooting
sub_type: bsod
os: [Windows]
date: '2026-03-07'
---

## Symptom

A Windows host experiences a Blue Screen of Death (BSOD) or kernel crash (bugcheck), and the memory dump analysis points to `elastic_endpoint_driver.sys` or a related Elastic Defend kernel-mode driver on the call stack.


## Summary

Elastic Defend uses a kernel-mode minifilter driver (`elastic_endpoint_driver.sys`) on Windows to intercept file, process, registry, and network activity in real time. Because kernel-mode code runs at the highest privilege level, a bug or incompatibility in the driver — or a conflict with another kernel-mode component — can trigger a bugcheck (BSOD). These crashes most commonly surface immediately after an Elastic agent upgrade that ships a new driver version, after a Windows cumulative update (KB) that changes kernel interfaces, or when another security product's kernel driver conflicts with the Elastic minifilter.


## Common issues

### BSOD after agent upgrade

The most frequent pattern is a BSOD that begins occurring on one or more hosts shortly after upgrading the Elastic agent to a new version. The new agent version may bundle an updated `elastic_endpoint_driver.sys` that has a defect on specific hardware or OS configurations. This is especially common on Windows Server 2016, Windows Server 2022, and Hyper-V cluster nodes where kernel behavior can differ from desktop editions.

To confirm, correlate the BSOD onset timestamp with the agent upgrade time in `.fleet-agents-*` (check `upgrade_started_at` and `upgraded_at` fields). If the BSOD started within hours of the upgrade, the new driver version is the likely cause. As immediate mitigation, roll back the agent to the previously stable version using Fleet. Collect the full memory dump (`C:\Windows\MEMORY.DMP` or minidumps from `C:\Windows\Minidump\`) and report them to Elastic support.

### IRQL_NOT_LESS_OR_EQUAL bugcheck

This specific bugcheck (stop code 0x0000000A) with `elastic_endpoint_driver!unknown_function` on the stack indicates the driver accessed paged memory at an elevated IRQL, or accessed an invalid address. This is a driver-level defect that requires a fix from Elastic.

Run `!analyze -v` in WinDbg on the memory dump to confirm the faulting module. If the stack trace shows `elastic_endpoint_driver.sys`, escalate to Elastic support with the dump file and the WinDbg output. Roll back to the previous agent version as immediate mitigation.

### Incompatibility with other kernel-mode drivers

Other security products — CrowdStrike Falcon, Carbon Black, Symantec Endpoint Protection — also install kernel-mode minifilter drivers. Two minifilters operating on the same file system stack can deadlock or corrupt shared state, resulting in a BSOD. The bugcheck may or may not name `elastic_endpoint_driver.sys` directly; sometimes the other product's driver appears on the stack but the interaction with Elastic's driver was the trigger.

To investigate, check the list of loaded minifilters using `fltmc filters` on the affected host. If another security product's minifilter is loaded at a similar altitude, there may be a conflict. Try temporarily uninstalling or disabling the other product's kernel component to confirm. If the BSOD stops, the two products are conflicting. Report the conflict to both vendors with the loaded filter list and memory dump.

### Windows update (KB) causing driver incompatibility

A Windows cumulative update can change kernel APIs or data structures that the Elastic driver depends on. If BSODs begin appearing across multiple hosts shortly after a specific KB is installed — but no agent upgrade occurred — the Windows update is likely the trigger.

Check `metrics-endpoint.metadata_current_*` for the OS build number. Cross-reference with the Windows Update history on the affected hosts to identify the specific KB. Report the KB number and memory dumps to Elastic support. As a workaround, uninstalling the specific KB may stop the BSODs, but coordinate with your Windows team on security implications.

### Hyper-V and virtualization-specific crashes

Hyper-V cluster nodes and hosts running Virtualization-Based Security (VBS) or Credential Guard have additional kernel-mode components that can interact with the Elastic driver. BSODs on these hosts may only reproduce under specific conditions such as live migration, VM checkpoint creation, or heavy VM density.

Collect the memory dump and note the specific Hyper-V operation that was in progress when the BSOD occurred. Check if the crash reproduces only on Hyper-V hosts or also on bare-metal servers with the same agent version. If isolated to Hyper-V, report the environment details to Elastic support.


## Investigation priorities

1) Collect the memory dump file (`C:\Windows\MEMORY.DMP` or minidumps from `C:\Windows\Minidump\`) and run `!analyze -v` in WinDbg to identify the faulting module and bugcheck code
2) Query `.fleet-agents-*` for the affected host to check the agent version and whether a recent upgrade occurred
3) Query `metrics-endpoint.metadata_current_*` for the host's OS version and build number to identify any recent Windows updates
4) Query `metrics-endpoint.policy-*` for `connect_kernel` failures which indicate the driver failed to load after a crash
5) Look for gaps in `metrics-endpoint.metadata_current_*` timestamps for the host — a gap indicates the endpoint was offline, likely due to repeated BSODs
6) Check whether the BSOD affects a single host or multiple hosts (if multiple, suspect a common agent upgrade or Windows KB)
7) If the driver is confirmed as the faulting module, roll back the agent version via Fleet and escalate the dump files to Elastic support
