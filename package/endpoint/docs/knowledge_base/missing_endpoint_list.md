---
type: automatic_troubleshooting
sub_type: missing_endpoint_list
date: '2026-01-16'
---

## Symptom

Missing or no (empty) Elastic Defend endpoints are shown on the Elastic Defend endpoint list page even though there are Elastic Defend endpoints connected.


## Summary

The Elastic Defend endpoint list page pulls data from the `.metrics-endpoint.metadata_united_*` index. Only documents containing both `united.endpoint` and `united.agent` values as well as `united.agent.active: true` are displayed.


## Common issues

### Missing `united.endpoint` or `united.agent` values

If either of these fields are missing, the document will not be returned in the Elastic Defend endpoint list page's query. This is typically an issue with the underlying transforms. Refer to below sections for more details.

### Transforms

If the Elastic Defend transforms are not healthy, the `.metrics-endpoint.metadata_united_*` documents will not be properly populated. There should be exactly two healthy transforms running: `endpoint.metadata_united-*` and `endpoint.metadata_current-*`.

Even if the Elastic Defend transforms are healthy, there can be configuration overrides (details below) that cause the documents to not be merged correctly. All differences between the default settings and current settings should be reviewed in depth.

#### Transforms not healthy or not running

If the Elastic Defend transforms are not healthy, restarting both transforms may help. If they are not running, they should be started.

#### Old versioned transforms still running

If old Elastic Defend transforms were not properly deleted during the upgrade process, they can interfer with each other. Old transforms should be deleted. If deleting these from the Kibana UI, it is important to not delete the destination index as all versions of the transforms point to the same destination index. After deleting the old transforms, restart the current version transforms.

### Configuration overrides

Transform and ingest pipeline setting alterations can cause issues. Review the current Elastic Defend transform and ingest pipeline settings and compare it to the default endpoint-package (Elastic Defend) defined settings. In particular, modifications to the following can be problematic:
* changes to the `endpoint.metadata_united-*` transform's `group_by` and `sync.time.field` values
* changes to the `endpoint.metadata_current-*` transform's `group_by` and `sync.time.field` values
* changes to `metrics-endpoint.metadata-*` ingest pipelines
  * expected values:
    * `default_pipeline` is typically `metrics-endpoint.metadata-*`
    * `final_pipeline` is typically `.fleet_final_pipeline-*`

### Cluster resourcing

If the transform stats show high `operations_behind` or failures, this can be indicative of a resourcing issue. The `endpoint.metadata_united-*` transform runs an aggregation so in setups with a large endpoint count, can sometimes be one of the first symtoms of resource bottlenecking. Review the node stats to see if resourcing is a concern.

## Investigation priorities

1) Confirm if `.metrics-endpoint.metadata_united_*` documents have `united.endpoint` and `united.agent` values
2) Confirm the transform state
3) Confirm if there are differences between the default and current transform settings
4) Confirm if there are differences between the default and current ingest pipeline settings
5) Confirm if cluster resourcing is sufficient