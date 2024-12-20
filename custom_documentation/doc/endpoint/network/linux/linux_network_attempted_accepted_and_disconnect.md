# Linux Network Connection Attempted, Connection Accepted, and Disconnect

- OS: Linux
- Data Stream: `logs-endpoint.events.network-*`
- KQL: `event.action : ("connection_attempted" or "connection_accepted" or "disconnect_received") and event.dataset : "endpoint.events.network" and event.module : "endpoint" and host.os.type : "linux"`

This event is generated when a network session is accepted, attempted or terminated.


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
| destination.bytes |
| destination.ip |
| destination.port |
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
| network.direction |
| network.transport |
| network.type |
| process.Ext.ancestry |
| process.command_line |
| process.entity_id |
| process.entry_leader.entity_id |
| process.entry_leader.parent.entity_id |
| process.executable |
| process.group_leader.entity_id |
| process.name |
| process.parent.entity_id |
| process.pid |
| process.session_leader.entity_id |
| process.thread.capabilities.effective |
| process.thread.capabilities.permitted |
| process.uptime |
| source.address |
| source.bytes |
| source.ip |
| source.port |
| user.Ext.real.id |
| user.Ext.real.name |
| user.domain |
| user.id |
| user.name |

