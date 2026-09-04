---
type: policy_management
sub_type: os_tuning
os: [MacOS]
date: '2026-08-22'
link: https://www.elastic.co/docs/solutions/security/configure-elastic-defend/configure-an-integration-policy-for-elastic-defend
---

# Tuning an Elastic Defend policy on macOS

This article helps you choose Elastic Defend policy configuration for macOS event collection and DNS event collection next to VPN clients. It is not a guide for a failed policy response or incident diagnosis, and it is not a host-permissions guide.

## When to use this article

Use this article when you are configuring a healthy macOS Elastic Defend policy: which process, file, and network events the policy collects, and how DNS event collection interacts with VPN clients. Do not use it as a Full Disk Access, system-extension, or network-filter failure checklist, and do not use it to diagnose a policy response failure.

## Event collection on macOS

Event Collection in the policy chooses which process, file, and network events the policy forwards. Narrowing collection is a visibility-versus-volume choice: it reduces what is indexed for visibility. A complete macOS event-collection inventory is unavailable in this package; use the policy UI or the maintained field reference for the current event controls.

Host isolation on macOS is a response action. It depends on the host approvals below and on working macOS network filtering; it is not enabled by an Event Collection choice.

## Host permissions are prerequisites, not policy settings

The macOS policy choices in this article only take effect after the host grants the approvals Elastic Endpoint requires: Full Disk Access, system extension approval, and network content filtering approval. Those approvals are host prerequisites, not policy settings, and granting them does not choose which events the policy forwards. This article does not teach how to grant them. When they are missing or failing, see the `macos_full_disk_access`, `macos_connect_kernel`, and `macos_detect_network_events` knowledge base docs.

## VPN clients versus DNS event collection

VPN clients can conflict with Elastic Defend DNS event collection on macOS. Turning DNS event collection off in the policy is the policy-side lever. The incompatible_software_third_party knowledge base doc covers that conflict; confirm the current event-collection controls in the policy UI.

Which ransomware controls exist on which macOS releases is unavailable in this package; use the policy UI or the maintained field reference.

## Exact settings

Do not invent policy paths, defaults, licenses, or agent versions. Use the Elastic Defend policy UI or the maintained field reference for exact setting names and values.

## Related troubleshooting

When Full Disk Access is not granted, see the macos_full_disk_access knowledge base doc. When the system extension is not approved, see the macos_connect_kernel knowledge base doc. When network content filtering is not allowed, see the macos_detect_network_events knowledge base doc. When a VPN client conflicts with DNS event collection, see the incompatible_software_third_party knowledge base doc.
