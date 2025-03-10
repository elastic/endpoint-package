# macOS DNS Lookup Result

- OS: macOS
- Data Stream: `logs-endpoint.events.network-*`
- KQL: `event.action : "lookup_result" and event.dataset : "endpoint.events.network" and event.module : "endpoint" and host.os.type : "macos"`

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
| destination.address |
| destination.ip |
| destination.port |
| dns.Ext.options |
| dns.Ext.status |
| dns.question.name |
| dns.question.type |
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
| group.Ext.real.id |
| group.Ext.real.name |
| group.id |
| group.name |
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
| network.protocol |
| network.transport |
| network.type |
| process.Ext.ancestry |
| process.code_signature.exists |
| process.code_signature.signing_id |
| process.code_signature.status |
| process.code_signature.subject_name |
| process.code_signature.team_id |
| process.code_signature.trusted |
| process.command_line |
| process.entity_id |
| process.executable |
| process.name |
| process.parent.entity_id |
| process.pid |
| source.address |
| source.ip |
| source.port |
| user.Ext.real.id |
| user.Ext.real.name |
| user.id |
| user.name |

