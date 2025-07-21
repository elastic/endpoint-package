# Linux DNS Lookup Result

- OS: Linux
- Data Stream: `logs-endpoint.events.network-*`
- KQL: `event.action : ("lookup_result" or "lookup_requested") and event.dataset : "endpoint.events.network" and event.module : "endpoint" and host.os.type : "linux"`

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
| host.id |
| host.name |
| host.os.type |
| message |
| network.protocol |
| network.transport |
| process.Ext.ancestry |
| process.command_line |
| process.entity_id |
| process.executable |
| process.name |
| process.parent.entity_id |
| process.pid |
| process.thread.capabilities.effective |
| process.thread.capabilities.permitted |
| source.address |
| source.ip |
| source.port |
| user.Ext.real.id |
| user.Ext.real.name |
| user.id |
| user.name |

