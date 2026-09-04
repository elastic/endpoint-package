---
type: policy_management
sub_type: os_tuning
os: [Linux]
date: '2026-08-26'
link: https://www.elastic.co/docs/solutions/security/configure-elastic-defend/configure-an-integration-policy-for-elastic-defend
---

# Tuning an Elastic Defend policy on Linux

This article helps you choose Elastic Defend policy configuration for Linux fanotify filesystem coverage, event-pipeline cost, session lineage and terminal I/O on the process datastream, and eBPF coexistence with host isolation. It is not a guide for a failed policy response or incident diagnosis.

## When to use this article

Use this article when you are configuring a healthy Linux Elastic Defend policy: which filesystems malware protection can watch, how event collection feeds protection engines, and when host isolation shares the host with other eBPF tools. Do not use it to diagnose a configure-malware deadlock, a cron-driven high-CPU incident, or missed check-ins.

Healthy-policy Linux tuning also covers session lineage and terminal I/O on the process datastream.

## Fanotify and filesystem-type compatibility

Linux malware protection uses fanotify. Fanotify coverage is filesystem-type dependent; untested filesystems get less malware fanotify coverage than the policy's malware toggle implies. Do not treat that gap as skipped Event Collection file events; file-event collection uses a different pipeline, below.

Advanced policy settings related to fanotify exist for compatibility; this article does not list them. If malware protection is disabled because of a potential deadlock, see the linux_configure_malware knowledge base doc. Do not copy that remediation into a healthy-policy baseline.

## Event-pipeline cost

Elastic Defend on Linux can use kprobes, eBPF, or Quark to gather system activity. The policy's automatic capture mode uses Quark when possible on Elastic Defend 9.3 and later. Process, file, network, and DNS events then pass through the applicable enrichment, protection, and forwarding pipeline. Short-lived child processes from monitoring scripts, cron or systemd timers, CI runners, and similar high-churn parents generate bursts of process events that the pipeline still has to handle.

Reducing pipeline cost by trusting or filtering specific processes is an artifact decision outside this article; when that cost becomes an incident, the high_cpu knowledge base docs cover it.

DNS events are a Linux Event Collection toggle. Do not treat the toggle as universally on or off by default; use the policy UI or the maintained field reference for the applicable configuration. Enabling the toggle increases DNS visibility and telemetry volume. The high_cpu knowledge base doc already names an advanced DNS event control used on some agent versions; do not copy that key as a catalogue or assume that it exists on every version.

Do not treat CPU percentages, cron-window durations, or hashing times from incident write-ups as general policy thresholds.

## Session and terminal visibility

Linux process telemetry can include session lineage: the entry and session leaders that show how a process reached the host, and whether a controlling TTY marks an interactive session. Capture on the process datastream can also include terminal I/O in chunks, subject to capture limits. Terminal control codes in that output can keep string queries from matching a word. Use the Elastic Defend policy UI or the maintained field reference for exact setting names and values.

## Host isolation versus other eBPF

Host isolation on Linux can share the host with other eBPF networking tools. If host isolation is not required on a Linux host, confirm the current isolation control in the policy UI. When other eBPF networking tools conflict with isolation, see the incompatible_software_third_party knowledge base doc.

## Working-agent prerequisite

A Linux policy assumes a running Endpoint. On SELinux-enforcing distributions, an incorrect security context under the Endpoint install path can prevent the binary from starting. See the linux_missed_checkins knowledge base doc; this article does not diagnose missed check-ins.

## Exact settings

Do not invent policy paths, defaults, licenses, or agent versions. Use the Elastic Defend policy UI or the maintained field reference for exact setting names and values.

## Related troubleshooting

When fanotify compatibility disables malware protection, see the linux_configure_malware knowledge base doc. When short-lived processes or DNS events appear as a high-CPU incident, see the high_cpu knowledge base doc. When other eBPF networking tools conflict with host isolation, see the incompatible_software_third_party knowledge base doc. When the agent cannot start the Endpoint, see the linux_missed_checkins knowledge base doc. When session or terminal capture volume appears as a high-CPU incident, see the high_cpu knowledge base doc.
