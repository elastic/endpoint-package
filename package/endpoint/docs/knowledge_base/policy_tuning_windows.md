---
type: policy_management
sub_type: os_tuning
os: [Windows]
date: '2026-08-22'
link: https://www.elastic.co/docs/solutions/security/configure-elastic-defend/configure-an-integration-policy-for-elastic-defend
---

# Tuning an Elastic Defend policy on Windows

This article helps you choose Elastic Defend policy configuration for Windows event collection, Malicious Behavior Protection, file scanning and hashing cost, and network collection. It is not a guide for a failed policy response or incident diagnosis.

## When to use this article

Use this article when you are configuring a healthy Windows Elastic Defend policy: which events to collect, how those choices interact with protection engines, and qualitative file and network cost. Do not use it to diagnose a policy response failure, a blue screen, or a high-CPU incident.

## Kernel-mode file-system and network filtering

Windows kernel-mode file-system and network filtering use the Endpoint kernel driver. Disabling or disconnecting that driver can break many Elastic Endpoint features; do not infer an exemption for Malicious Behavior Protection or Security event processing. See the windows_connect_kernel knowledge base doc when the driver fails to connect. This article is not an installation-failure playbook.

## Event collection versus Malicious Behavior Protection

Event Collection and protection engines are not the same control. Event Collection chooses which event types the policy forwards to Elasticsearch; protection engines can still consume selected host activity when equivalent telemetry is not indexed. On Windows, Malicious Behavior Protection can process Security events required by behavioral rules even when Security is removed from Event Collection. Disabling an Event Collection category therefore does not prove that the related protection work has stopped. The `policy_tradeoffs_events` knowledge base doc explains why indexed volume and protection monitoring are separate choices. Confirm exact event and protection controls in the policy UI. The high_cpu knowledge base doc already names an advanced Security-event control used on some agent versions; do not copy that key as a catalogue or assume it exists on every version.

## File scanning and hashing cost

Windows file cost comes from separate controls. Malware protection can scan files when they are modified; when that option is disabled, malware scanning occurs when files are executed. Advanced event settings can emit hashes for process, library, and file events, and file-event hashing can add CPU and I/O cost. Do not assume that every executable or DLL is always hashed and signature-verified when it loads.

When file scanning or hashing cost becomes an incident on specific hosts, see the `windows_high_cpu` knowledge base doc. Do not treat CPU percentages or login-time figures from incident write-ups as a general policy threshold.

## Network collection and host isolation

Kernel-level network capture feeds Windows network events and can add cost on hosts with high connection volume. Third-party network or security software can create compatibility or cost incidents; use the `incompatible_software_third_party` knowledge base doc for those incidents instead of treating them as a healthy-policy baseline.

Current official documentation does not specify how disabling the Windows kernel network setting affects host isolation. Do not infer from this article that isolation remains available or becomes unavailable. When host isolation is required, do not change that advanced setting unless the current supported product behavior has been verified. The high_cpu knowledge base doc already names the kernel network advanced setting.

## Exact settings

Do not invent policy paths, defaults, licenses, or agent versions. Use the Elastic Defend policy UI or the maintained field reference for exact setting names and values.

## Related troubleshooting

When a Windows kernel-connect choice fails to apply, see the windows_connect_kernel knowledge base doc. When file, Security-event, or network cost appears as a high-CPU incident, see the high_cpu knowledge base doc. When third-party security products conflict, see the incompatible_software_third_party knowledge base doc. Indexed volume versus protection monitoring is described in the `policy_tradeoffs_events` knowledge base doc and, for output incidents, in the output_kafka_message_size knowledge base doc.
