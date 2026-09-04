---
type: policy_management
sub_type: staged_rollout
date: '2026-08-23'
---

# Staging an Elastic Defend policy rollout across host cohorts

This article helps you choose Elastic Defend policy configuration for policy assignment over time: how a policy or policy change reaches hosts in a staged rollout. It is not a guide for a failed policy response, and it is not a Protection Updates or artifact-pinning article.

## When to use this article

Use this article when you are deciding Elastic Defend policy configuration for:

- A policy, or a policy change, that should reach some hosts before others
- Vocabulary for a pilot policy, canary, or phased assignment that uses separate agent policies and a host cohort
- A gradual rollout of a configuration change, including—but not only—a detect-to-prevent change

Do not use this article to choose pin versus `latest` or global versus user artifacts; see the `policy_tradeoffs_artifacts` knowledge base doc. Do not use it to choose the detect-to-prevent mode sequence; see the `policy_detect_to_prevent` knowledge base doc. Do not use it to diagnose Fleet 429s, missed check-ins, failed artifact downloads, or BSODs. Do not treat README field text about global artifact channels as this topic.

## Policy assignment versus protection artifacts

A staged policy rollout is about which hosts receive which agent policy. Pin versus `latest` is a snapshot-freshness choice for protection artifacts, not a host-cohort rollout. Use the `policy_tradeoffs_artifacts` knowledge base doc for that choice; this article does not restate pinning or artifact-channel mechanics.

## What a cohort is

A host cohort is a set of hosts that share an agent policy assignment. Separate agent policies are the package-visible way to stage a change: a pilot policy or canary assignment is a smaller cohort; later expansion is a larger one. This is not a named Fleet preset and not an operating-system role. This article does not document Fleet UI click-paths or assignment screens.

## Staged assignment sequence

A staged assignment sequence is vocabulary, not a playbook: start with a small pilot, observe that the policy applies and hosts remain healthy, then branch on what the pilot evidence shows.

- **Expand on success.** When the pilot policy applies and the pilot hosts remain healthy, expand the change to larger cohorts.
- **Hold, adjust, or revert on adverse evidence.** When the pilot evidence is adverse—the policy fails to apply, hosts become unhealthy, or protections act on activity they should not—do not expand. Hold the rollout, adjust the change or revert the pilot cohort to its prior policy, then re-observe the pilot before expanding.

In this article, phased assignment and gradual rollout of a policy change mean policy assignment over time across cohorts. This is not a percentage schedule for policy content or a wait interval. Fleet also uses gradual rollout for percentage-based Elastic Agent version upgrades; that separate mechanism is outside this article. Apply-state counts and assignment APIs are not documented here.

## What staged rollout is not

Keep this model distinct from nearby topics:

- Changing protection mode on a policy is a detect-to-prevent transition. Use the `policy_detect_to_prevent` knowledge base doc for the mode sequence; this article owns only how that change is assigned to cohorts.
- Pinning a protection snapshot is not a host-cohort rollout. Use the `policy_tradeoffs_artifacts` knowledge base doc.
- Relieving Fleet Server 429s by staggering policy updates is an incident mitigation in the `windows_missed_checkins` knowledge base doc, not this rollout model.
- Using separate agent policies for older OS versions after a BSOD is an incident prevention note in the `windows_bsod_endpoint_driver` knowledge base doc, not this article's cohort model.

## Exact settings

Do not invent assignment APIs, agent-policy field paths, cohort controls, defaults, licenses, or versions from this article. Use the Elastic Defend policy UI or the maintained field reference for exact setting names and legal values.

## Related troubleshooting

When a policy does not apply or an agent misses check-ins, see the `windows_missed_checkins` and `linux_missed_checkins` knowledge base docs. When a pinned global snapshot fails to apply, see the `windows_outdated_protection_artifacts`, `macos_outdated_protection_artifacts`, and `linux_outdated_protection_artifacts` knowledge base docs. When Trusted Applications, Event Filters, or other user artifacts fail to download, see the matching `download_user_artifacts` knowledge base docs. After a driver-related BSOD, see the `windows_bsod_endpoint_driver` knowledge base doc. Those articles are diagnostic; they are not a staged-rollout assignment model.
