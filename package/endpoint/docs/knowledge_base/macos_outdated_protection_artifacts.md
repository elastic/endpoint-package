---
type: automatic_troubleshooting
sub_type: policy_response_failure
action.name: download_global_artifacts
action.message: 'Global artifacts snapshot {version} does not match target snapshot: {date}'
os: [MacOS]
date: '2025-08-15'
---

## Summary

Elastic Defend is trying to apply a pinned global protection artifact snapshot, but the endpoint cannot download or apply the requested snapshot. This causes the `download_global_artifacts` policy action to report a warning and can make the endpoint unhealthy or degraded.

## Diagnostic match

Use this context when Elastic Defend on macOS reports a policy response failure or degraded policy application involving `download_global_artifacts`, including log messages such as:

- `Failed to download new global artifacts manifest`
- `Failure HTTP code: 404`
- `Global configuration artifact is not available`
- `download_global_artifacts: warning`
- `Global artifacts snapshot {version} does not match target snapshot: {date}`
- `Endpoint is setting status to DEGRADED, reason: Policy Application Status`

This issue is about global protection artifact snapshots. Do not treat it as a `download_user_artifacts` failure for user artifacts such as Trusted Apps, Event Filters, or Endpoint Exceptions.

When the policy response says `Global artifacts snapshot latest does not match target snapshot: YYYY-MM-DD`, `latest` is the snapshot currently applied on the endpoint and `YYYY-MM-DD` is the requested pinned target snapshot. Do not describe the policy as using `latest`; the policy is requesting the target date.

## Evidence to extract

Before explaining the root cause, identify these values from endpoint data:

1. The target pinned snapshot date from the `download_global_artifacts` message or policy configuration.
2. The endpoint or agent build date from `agent.build.original` in the `logs-endpoint.policy-*` or `metrics-endpoint.policy-*` document. Prefer `agent.build.original` for this comparison; do not substitute the applied artifact version date unless `agent.build.original` is unavailable.
3. Whether the target pinned snapshot date is inside the 18-month artifact retention window.

## Root cause decision

Apply these checks in order and keep them distinct:

1. Artifact retention window: old artifacts are only available for the last 18 months. If the pinned date is older than 18 months, retention can explain the failure. If the pinned date is within the last 18 months, explicitly state that retention is not the root cause.

2. Endpoint build-date compatibility: the pinned snapshot date must be later than the Elastic Agent and Elastic Endpoint build date from `agent.build.original`. If the endpoint or agent build date is later than the pinned snapshot date, the pinned snapshot predates the binary and is incompatible for that endpoint build. This can happen even when the pinned date is inside the 18-month retention window.

Example: if the pinned snapshot is `2025-08-15` and `agent.build.original` shows the endpoint was built on `2026-05-31`, then the pinned snapshot is too old for that endpoint build. The correct conclusion is build-date incompatibility, not artifact retention and not CDN propagation.

Only consider CDN propagation or transient availability after both checks pass: the pinned date is within the retention window and the pinned date is later than the endpoint build date.

## Remediation

Check the Elastic Defend policy's Protection Updates setting. If the pinned snapshot is invalid for retention or build-date compatibility, switch Protection Updates to automatic updates (`latest`) or choose a pinned date that is both inside the retention window and later than the endpoint build date.

For troubleshooting, run:

- `sudo /Library/Elastic/Endpoint/elastic-endpoint test output`

When explaining this issue, include the target pinned date, the endpoint build date, the retention-window result, the build-date compatibility result, and the recommended policy change.
