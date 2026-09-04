---
type: policy_management
sub_type: detect_to_prevent
date: '2026-08-23'
---

# Moving an Elastic Defend policy from detect to prevent

This article helps you choose Elastic Defend policy configuration for a detect-to-prevent transition: the order and evidence of a mode change on a policy that is already healthy. It is not a guide for a failed policy response or incident diagnosis, and it is not a deployment-baseline article.

Prevention and detection are separate Elastic Defend capabilities. Detection uses endpoint telemetry—process, file, and network activity—together with behavior-based detections to raise alerts. Prevention applies layered enforcement such as malware and ransomware protection, behavior-based threat prevention, and memory threat protection, and can block or quarantine the same activity. A protection in detect mode alerts without blocking; in prevent mode it enforces.

## When to use this article

Use this article when a healthy Elastic Defend policy already exists and you want a detect-then-prevent sequence:

- Start the relevant protection capabilities in detect, watch what those protections alert on, then move to prevent
- Vocabulary for that sequence as a mode change on the policy, not a named Fleet preset

Do not use this article to assign the change to a subset of hosts first; that assignment sequence lives in the `policy_staged_rollout` knowledge base doc. Do not use it to diagnose missing alerts, false positives, or a failed policy response. Device Control block versus detect is out of scope; if that is an incident, see the `device_control_notification` knowledge base doc.

## Transition sequence

A detect-then-prevent transition is a sequence, not a named Fleet preset and not a factory default. The sequence is detect mode then prevent mode: start in detect on the relevant protection capabilities, observe the alerts those protections raise and the operational cost of running them, resolve false positives, then move to prevent.

Do not treat this article as Kibana steps, setting names, or a recipe that flips every protection at once.

## Detect evidence is qualitative, not a guarantee

Before you flip to prevent, treat what you observed in detect as qualitative progression evidence, not a numeric target and not a forecast of prevent behavior:

- Alerts that appeared in detect show which kinds of activity and software the protections react to, so they indicate what Prevent mode might affect. Detect mode does not enforce, so detect alerts do not guarantee what Prevent mode will block once enforcement is active.
- False positives are handled. When detect alerts or prevent blocks land on legitimate software, see the `false_positive_malware_detection` knowledge base doc.
- Operational cost is acceptable for the hosts the policy serves.

This package does not publish a safe alert count or CPU threshold as a policy target. If expected alerts are missing, see the `endpoint_alerts_not_appearing` knowledge base doc.

## Independent protection modes

Malware, malicious behavior, memory threat protection, and ransomware are separate enable and mode choices. A detect to prevent transition can move one protection to prevent without moving the others.

Which detect or prevent mode to pick for memory threat protection is not catalogued here. Use the `policy_tradeoffs_memory_protection` knowledge base doc for that coverage-versus-cost choice, and the policy UI for the mode control.

## How assignment relates

If the mode change should reach a subset of hosts first, that assignment is staged rollout. Use the `policy_staged_rollout` knowledge base doc.

## Exact settings

Do not invent policy paths, defaults, licenses, or versions from this article. Use the Elastic Defend policy UI or the maintained field reference for exact setting names and legal values.

## Related troubleshooting

When expected detect or prevent alerts are missing after a mode choice, see the `endpoint_alerts_not_appearing` knowledge base doc. When detect alerts or prevent blocks land on legitimate software during the transition, see the `false_positive_malware_detection` knowledge base doc. When cost appears after the policy is assigned, see the `windows_high_cpu` knowledge base doc and the `linux_high_cpu` knowledge base doc. When a third-party security product interacts with the change, see the `incompatible_software_third_party` knowledge base doc. Those remain incident playbooks; they are not an alternative transition sequence.
