# Windows DNS Lookup Result

- OS: Windows
- Data Stream: `logs-endpoint.events.network-*`
- KQL: `event.action : "lookup_result" and event.dataset : "endpoint.events.network" and event.module : "endpoint" and host.os.type : "windows"`

This event is generated when results are returned for a DNS lookup request.


| Field |
|---|
| @timestamp |
| agent.id |
| agent.type |
| agent.version |
| data_stream.dataset |
| data_stream.namespace |
| data_stream.type |
| destination.port |
| dns.Ext.options |
| dns.Ext.status |
| dns.question.name |
| dns.resolved_ip |
| ecs.version |
| elastic.agent.id |
| event.action |
| event.category |
| event.created |
| event.dataset |
| event.id |
| event.kind |
| event.module |
| event.outcome |
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
| network.destination.port |
| network.protocol |
| process.Ext.ancestry |
| process.Ext.code_signature.exists |
| process.Ext.code_signature.status |
| process.Ext.code_signature.subject_name |
| process.Ext.code_signature.trusted |
| process.code_signature.exists |
| process.code_signature.status |
| process.code_signature.subject_name |
| process.code_signature.trusted |
| process.entity_id |
| process.executable |
| process.name |
| process.pid |
| user.domain |
| user.id |
| user.name |

