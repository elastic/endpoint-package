# Elastic Defend Integration

This integration sets up templates and index patterns required for Elastic Defend.

## Compatibility

For compatibility information view our [documentation](https://www.elastic.co/guide/en/security/current/index.html).

## Logs

The log type of documents are stored in the `logs-endpoint.*` indices. The following sections define the mapped fields
sent by the endpoint.

### alerts

{{fields "alerts"}}

### file

{{fields "file"}}

### library

{{fields "library"}}

### network

{{fields "network"}}

### process

{{fields "process"}}

### registry

{{fields "registry"}}

### security

{{fields "security"}}

## Metrics

The metrics type of documents are stored in `metrics-endpoint.*` indices. The following sections define the mapped fields
sent by the endpoint.

### metadata

{{fields "metadata"}}

### metrics

Metrics documents contain performance information about the endpoint executable and the host it is running on.

{{fields "metrics"}}

### policy response

{{fields "policy"}}
