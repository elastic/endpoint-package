---
type: automatic_troubleshooting
sub_type: endpoint_exceptions
link: https://www.elastic.co/docs/solutions/security/manage-elastic-defend/optimize-elastic-defend
date: '2026-03-11'
---

## Symptom

An Endpoint Alert Exception has been created in Elastic Defend, but the endpoint continues to generate alerts or block processes that should be excluded. Alert documents matching the exception criteria still appear in `logs-endpoint.alerts-*`.


## Summary

Endpoint Alert Exceptions tell Elastic Defend to stop generating alerts or blocking processes when specific conditions are met. Elastic Endpoint evaluates exceptions before most other processing — if a match is found, the endpoint stops monitoring the process for that detection type, which can also improve performance. Unlike Trusted Applications (which stop all monitoring and create a blind spot), Endpoint Alert Exceptions only suppress the alert while keeping full visibility.

For exceptions to reach endpoints, Kibana's manifest manager must successfully package exception entries into artifacts and commit them via the Fleet Actions pipeline. If any part of this pipeline is broken — artifact packaging failures, policy scoping errors, or field mismatches — the exception silently has no effect on the endpoint.


## Common issues

### Exception field or value does not match alert data

The most common misconfiguration is an exception entry whose field name or value does not exactly match the corresponding field in the alert document. Endpoint Alert Exceptions perform literal matching (or wildcard matching with the `matches` operator), so even small differences cause the exception to miss.

Common mismatches include:
- **Case sensitivity**: An exception value of `C:\Program Files\App\app.exe` will not match an alert where the field contains `c:\program files\app\APP.EXE`. Use the `matches` operator with a case-insensitive wildcard pattern if the file system is case-insensitive.
- **Trailing whitespace or invisible characters**: Values copied from spreadsheets or ticketing systems sometimes include trailing spaces or non-breaking space characters that are invisible in the UI but cause a literal mismatch.
- **Wrong field name**: Using `file.path` (the file being acted upon) when the alert populates `process.executable` (the running binary), or vice versa. Check the actual alert document in `logs-endpoint.alerts-*` to confirm which fields are populated and what values they contain.
- **Keyword vs text field type**: If the exception references a field mapped as `text` (analyzed, tokenized) rather than `keyword` (exact value), the match behavior may differ. Exception entries work against the raw field values stored by the endpoint, so verify the field mapping in the alert index.

To diagnose: query `logs-endpoint.alerts-*` for a recent alert that should have been suppressed. Compare each field and value in the exception entry against the actual alert document fields character-by-character.

### Exception scoped to wrong integration policy

Endpoint Alert Exceptions are currently applied globally across all integration policies. Per-policy scoping for exceptions is planned for 9.4 and will be opt-in. If an exception appears to not take effect on a specific endpoint, the issue is not policy scoping — look for field mismatches, artifact distribution failures, or other causes listed in this document.

### Artifact distribution failure due to nested object limit

When a deployment has a large number of Endpoint Alert Exceptions, Trusted Applications, Event Filters, Blocklist entries, and Host Isolation Exceptions across many integration policies, the total artifact payload stored in the `.kibana_security_solution` index can exceed the Elasticsearch `index.mapping.nested_objects.limit` (default: 10000). When this limit is exceeded, Kibana's manifest manager task fails with an error like:

```
The number of nested documents has exceeded the allowed limit of [10000].
This limit can be set by changing the [index.mapping.nested_objects.limit] index level setting.
```

When the manifest task cannot commit, **no artifact updates are distributed to any endpoint**. This means newly created exceptions, trusted apps, blocklist entries, and other changes silently stop reaching endpoints. Existing artifacts on endpoints continue to work, but any additions or modifications have no effect until the pipeline is restored.

To diagnose: check Kibana logs for the error above. If present, increase the limit:

1. Create a role with `all` privileges on `.kibana_security_solution*` with `allow_restricted_indices: true`.
2. As a user with that role, run: `PUT /.kibana_security_solution/_settings { "index": { "mapping": { "nested_objects": { "limit": 20000 } } } }`.
3. Monitor Kibana logs for "Committed manifest" messages, which indicate the manifest task is recovering and distributing artifacts again.

If the limit is still exceeded after raising it to 20000, increase further in increments of 10000. Deployments with hundreds of policies and thousands of artifact entries may need 30000 or higher.

### Exception on wrong cluster in cross-cluster search (CCS) setups

In some architectures Fleet-managed agents are managed via an "analyst cluster" but write bulk data to a "data cluster". In these architectures, analysts query data via CCS from the data cluster, Endpoint Alert Exceptions must be created on the analyst cluster (the one running Fleet Server). Exceptions created on the data cluster are not distributed to endpoints because CCS does not support Fleet Actions.

If exceptions exist only on the data cluster, alert documents will continue to be generated by endpoints and indexed on the data cluster. The analyst cluster will then alert on those documents via CCS.

To fix: create the Endpoint Alert Exceptions on the analyst cluster where Fleet Server is running and where Elastic Agents are enrolled. After the manifest task commits and endpoints pull the updated artifacts, the alerts should stop being generated at the source.

### Alerts created by SIEM rules require SIEM exceptions, not Endpoint exceptions

Endpoint Alert Exceptions suppress alerts generated by the endpoint itself — they prevent the endpoint from creating alert documents in `logs-endpoint.alerts-*`. Alerts created by most SIEM detection rules (e.g. Custom Query Rules, Threshold Rules) are separate from endpoint-generated alerts and require **Detection Rule Exceptions** on the Kibana rule itself, not Endpoint Alert Exceptions.

To distinguish: check the `kibana.alert.rule.rule_type_id` field. Endpoint-generated alerts have `event.module: endpoint` and `event.dataset: endpoint.alerts`. Kibana detection rule alerts have fields like `kibana.alert.rule.category: "Custom Query Rule"` and `kibana.alert.rule.producer: "siem"`.

### Inter-application incompatibility

Sometimes it seems like Endpoint is blocking system activity because of a false positive but actually it's caused by an incompatibility between Endpoint and another application on the host. If alerts are being ingested into Elasticsearch in other scenarios from the same host this points to an incompatibility as the underlying cause. A targeted Trusted App entry is a common solution. If Malware protection is enabled, use `curl https://secure.eicar.org/eicar.com.txt --output eicar.com.txt` to test if alerts are being ingested into Elasticsearch.


## Investigation priorities

1) Query `logs-endpoint.alerts-*` for a recent alert that should have been suppressed. Compare every field and value in the exception entry against the actual alert document to identify mismatches.
2) Check Kibana logs for "nested documents has exceeded the allowed limit" errors, which indicate the artifact distribution pipeline is broken and no exceptions are reaching endpoints.
3) In CCS setups, confirm that exceptions are created on the analyst cluster (the one running Fleet Server), not the data cluster.
4) Distinguish between endpoint-generated alerts (`event.module: endpoint`) and Kibana detection rule alerts (`kibana.alert.rule.rule_type_id`) to determine whether the exception needs to be on the endpoint or on a Kibana detection rule.
5) Review the full policy configuration for non-obvious protection features like `attack_surface_reduction.credential_hardening` that may be blocking processes independently of the malware protection mode setting.
