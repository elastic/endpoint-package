# Endpoint Metadata

- OS: Linux, Windows, macOS
- Data Stream: `metrics-endpoint.metadata-*`
- KQL: `event.action : "endpoint_metadata" and event.dataset : "endpoint.metadata" and event.module : "endpoint"`

This is a relatively small state management document that includes details about an installed Endpoint.


| Field |
|---|
| @timestamp |
| Endpoint.capabilities |
| Endpoint.configuration.isolation |
| Endpoint.policy.applied.endpoint_policy_version |
| Endpoint.policy.applied.id |
| Endpoint.policy.applied.name |
| Endpoint.policy.applied.status |
| Endpoint.policy.applied.version |
| Endpoint.state.isolation |
| Endpoint.status |
| agent.build.original |
| agent.id |
| agent.type |
| agent.version |
| data_stream.dataset |
| data_stream.namespace |
| data_stream.type |
| ecs.version |
| elastic.agent.id |
| event.action |
| event.category |
| event.created |
| event.dataset |
| event.id |
| event.kind |
| event.module |
| event.sequence |
| event.type |
| host.architecture |
| host.hostname |
| host.id |
| host.ip |
| host.mac |
| host.name |
| host.os.Ext.variant |
| host.os.family |
| host.os.full |
| host.os.kernel |
| host.os.name |
| host.os.platform |
| host.os.type |
| host.os.version |
| message |

