---
type: automatic_troubleshooting
sub_type: policy_response_failure
action.name: download_global_artifacts
action.message: 'Global artifacts snapshot {version} does not match target snapshot: {date}'
os: [Windows]
date: '2025-08-15'
---

## Remediation

Protection artifacts version is out of date. Check if automatic updates are enabled for the policy under the protection updates tab.

## Diagnostic match

Use this context when Elastic Defend on Windows reports a policy response failure or degraded policy application involving `download_global_artifacts`, including log messages such as:

- `Failed to download new global artifacts manifest`
- `Failure HTTP code: 404`
- `Global configuration artifact is not available`
- `download_global_artifacts: warning`
- `Global artifacts snapshot {version} does not match target snapshot: {date}`
- `Endpoint is setting status to DEGRADED, reason: Policy Application Status`

This issue is about global protection artifact snapshots. Do not treat it as a `download_user_artifacts` failure for user artifacts such as Trusted Apps, Event Filters, or Endpoint Exceptions.

Artifact snapshots are enabled (requested), but the artifacts currently in use don't yet match the expected snapshot. This is typically due to propagation delays on the Global Artifacts CDN. The Endpoint should fetch the requested artifacts once they're available. For troubleshooting, run:

- `C:\Program Files\Elastic\Endpoint\elastic-endpoint.exe test output`

Note: `latest` is a special label that means "no snapshot—use the most recent artifacts." This status can appear whenever a new snapshot is set in policy—for example, during a transition from `latest` to `YYYY-MM-DD`, or from one `YYYY-MM-DD` date to another.

When explaining this issue, include these validation checks and keep them distinct:

1. Artifact retention window: old artifacts are only available for the last 18 months. If the pinned date is older than 18 months, retention can explain the failure. If the pinned date is within the last 18 months, do not describe retention as the root cause; continue to the endpoint build-date check.

2. Endpoint build-date compatibility: the pinned date must be more recent than the release date of the Elastic Agent and Elastic Endpoint version. This can be checked by looking at compile date in agent.build.original in the Endpoint's logs-endpoint.policy-* document. A pinned date can be within the 18-month retention window and still be invalid for an Endpoint build that is newer than the pinned artifact date.
