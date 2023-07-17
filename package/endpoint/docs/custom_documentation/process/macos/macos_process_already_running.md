# macOS Already Running Process

- OS: macOS
- Data Stream: `logs-endpoint.events.process-*`
- KQL: `event.action : "already_running" and event.dataset : "endpoint.events.process" and event.module : "endpoint" and host.os.type : "macos"`

This event is generated for a process that was already running before Endpoint's process event collection was enabled.


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
| process.args |
| process.args_count |
| process.code_signature.exists |
| process.code_signature.signing_id |
| process.code_signature.status |
| process.code_signature.subject_name |
| process.code_signature.team_id |
| process.code_signature.trusted |
| process.command_line |
| process.entity_id |
| process.executable |
| process.hash.md5 |
| process.hash.sha1 |
| process.hash.sha256 |
| process.name |
| process.parent.args_count |
| process.parent.entity_id |
| process.parent.pid |
| process.pid |
| user.Ext.real.id |
| user.Ext.real.name |
| user.id |
| user.name |

