---
type: policy_management
sub_type: memory_protection
date: '2026-08-22'
---

# Memory threat protection tradeoffs in an Elastic Defend policy

This article helps you choose Elastic Defend policy configuration for memory threat protection: coverage versus scan cost. It is not a guide for a failed policy response or a scan-cost investigation checklist.

## When to use this article

Use this article when you are deciding Elastic Defend policy configuration for:

- Whether to enable memory threat protection on a policy, given scan cost on large processes
- Whether memory-signature coverage is in scope for this policy
- Which protection mode the capability should run in

Do not use this article to enumerate advanced memory-protection keys or popup copy, or as a high-CPU investigation checklist. Process-specific carve-outs that stop memory scanning are artifact decisions outside this article.

## Coverage

Memory threat protection is a licensed Elastic Defend capability. Which licenses and serverless product tiers include it is documented in the package README licensing tables. This article does not copy those tables or setting-level license predicates; confirm availability in the policy UI.

When memory threat protection is enabled, Elastic Defend scans process memory for malicious activity and can generate alerts identified by `event.code: memory_signature`. The capability supports Detect and Prevent modes. Detect generates an alert without blocking the activity. Prevent is the default: it generates an alert and forces the offending process or thread to stop. Enabling the capability therefore adds both memory-threat coverage and, in Prevent mode, an enforcement consequence. Leaving the capability off means that coverage is out of scope for the policy.

Choose the mode in the policy UI. This article does not catalogue advanced controls. For the mode-transition sequence, see the `policy_detect_to_prevent` knowledge base doc.

## Scan cost versus coverage

Memory scanning is not free. When a process with a large memory footprint starts — large-footprint processes named in the high_cpu knowledge base docs — the scan can dominate CPU and memory on the host for as long as it runs. That cost is why some deployments disable the capability on specific policies.

The configuration tradeoff is coverage versus that scan cost:

- Keep memory threat protection enabled when you need memory-signature coverage on the policy.
- Expect large processes to be the expensive cases, not a reason to treat every host as if it had a published numeric CPU budget. This package does not define a safe scan-time or memory ceiling.

If scan cost is unacceptable for a specific process, the process-specific carve-out is decided outside this article; the `high_cpu` knowledge base docs cover memory-scan cost incidents. Do not turn the capability off for a whole policy as the first response, unless you have decided that memory-signature coverage is not required on those hosts.

## Exact settings

Do not invent memory-protection paths, defaults, licenses, or versions from this article. Use the Elastic Defend policy UI or the maintained field reference for the capability toggle and any advanced controls. This article does not list those keys.

## Related troubleshooting

When memory-signature alerts are absent, see the `endpoint_alerts_not_appearing` knowledge base doc (the capability must be enabled). When scan cost shows up as high CPU on a large process, see the `high_cpu` knowledge base docs. Those articles are diagnostic; they are not a catalogue of memory-protection settings.
