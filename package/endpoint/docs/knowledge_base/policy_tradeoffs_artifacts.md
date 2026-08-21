---
type: policy_management
sub_type: artifacts
date: '2026-08-22'
---

# Protection artifacts and pinning in an Elastic Defend policy

This article helps you choose Elastic Defend policy configuration for Protection Updates, global artifacts versus user artifacts, pinning versus `latest`, and retention. It is not a guide for a failed policy response or artifact download failure.

## When to use this article

Use this article when you are deciding Elastic Defend policy configuration for:

- Whether endpoints should follow automatic Protection Updates (`latest`) or a pinned global protection snapshot
- How global protection artifacts differ from user artifacts such as Trusted Applications, Event Filters, Endpoint Exceptions, and blocklists
- Which retention and endpoint build-date constraints a pin must satisfy

Do not use this article to diagnose a degraded `download_global_artifacts` or `download_user_artifacts` policy response.

## Global artifacts versus user artifacts

Elastic Defend applies two artifact channels that are easy to conflate in the policy UI.

**Global protection artifacts** are protection snapshots the endpoint downloads and applies as a dated bundle (or as `latest`). Protection Updates in the Elastic Defend policy selects that channel. A mismatch or download problem on this channel is about the global snapshot, not about operator-authored lists.

**User artifacts** are the lists you author and assign: Trusted Applications, Event Filters, Endpoint Exceptions, and blocklists. Endpoints download those lists separately from the global protection snapshot. A user-artifact download problem does not mean the global snapshot is wrong, and an outdated global snapshot does not mean Trusted Applications or Event Filters failed to apply.

Keep the two channels distinct when you change policy: pinning Protection Updates does not freeze user artifacts, and editing a Trusted Application does not move the global snapshot.

## Pinning versus latest

Protection Updates is a choice between automatic updates and a pinned snapshot.

- **`latest`** (automatic updates) asks endpoints to apply the current global protection snapshot as Elastic publishes it.
- **A pin** asks endpoints to apply a specific snapshot date and to stay on that snapshot until you change the policy.

If you pin, the policy is requesting the target date, not automatic updates.

Pinning is a stability choice: the protection bundle stops moving until you pick a new date or switch back to automatic updates. `latest` is a freshness choice: endpoints track published snapshots without a policy edit for each update.

Elastic strongly advises keeping automatic updates enabled to ensure the highest level of security. Proceed with caution if you disable automatic updates and pin a snapshot.

Confirm availability in the policy UI for the current deployment. This article does not infer a setting-level license requirement from the package README tables or turn the capability into a setting list.

## Retention and build date as pinning constraints

A pin must satisfy the retention window and endpoint build-date constraints named in the `windows_outdated_protection_artifacts`, `macos_outdated_protection_artifacts`, and `linux_outdated_protection_artifacts` knowledge base docs. Use those articles for the checks; this article does not restate those decision rules.

Choose a pin that meets both constraints for every endpoint that should apply it, or use `latest`. Exact snapshot identifiers and writable policy paths for the pin are not documented here.

## User artifacts and download path

User artifacts reach endpoints over a separate download path from the global protection snapshot. When those lists fail to download, see the matching `download_user_artifacts` knowledge base docs; this article does not restate download-path failure mechanics.

When a pin or user-artifact download fails to apply, treat that as an incident and use the troubleshooting articles below. Do not use those failure playbooks as the configuration model for pinning or retention.

## Exact settings

Do not invent artifact paths, defaults, licenses, or versions from this article. Use the Elastic Defend policy UI or the maintained field reference for Protection Updates, pinning, and any advanced user-artifact download controls.

## Related troubleshooting

When a global snapshot cannot be downloaded or applied, see the `windows_outdated_protection_artifacts`, `macos_outdated_protection_artifacts`, and `linux_outdated_protection_artifacts` knowledge base docs. When Trusted Applications, Event Filters, or other user artifacts fail to download, see the matching `download_user_artifacts` knowledge base docs. Those articles are diagnostic; they are not a catalogue of artifact identifiers.
