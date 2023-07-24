# Endpoint Heartbeat

- OS: Linux, Windows, macOS
- Data Stream: `logs-endpoint.heartbeat-*`
- KQL: `data_stream.dataset : "endpoint.heartbeat"`

This is a small state management document generated periodically to validate that Endpoint is running and can write to Elasticsearch.


| Field |
|---|
| @timestamp |
| agent.id |
| data_stream.dataset |
| data_stream.namespace |
| data_stream.type |
| message |

