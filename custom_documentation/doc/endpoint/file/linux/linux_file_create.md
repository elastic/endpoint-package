# Linux File Create

- OS: Linux
- Data Stream: `logs-endpoint.events.file-*`
- KQL: `event.action : "creation" and event.dataset : "endpoint.events.file" and event.module : "endpoint" and host.os.type : "linux"`

This event is generated when a file is created.


| Field |
|---|
| @timestamp |
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
| event.outcome |
| event.sequence |
| event.type |
| file.extension |
| file.hash.sha256 |
| file.name |
| file.path |
| file.hash.sha256 |
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
| user.Ext.real.id |
| user.Ext.real.name |
| user.id |
| user.name |

