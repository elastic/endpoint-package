# Windows User Log On

- OS: Windows
- Data Stream: `logs-endpoint.events.security-*`
- KQL: `event.action : "log_on" and event.dataset : "endpoint.events.security" and event.module : "endpoint" and host.os.type : "windows"`

This event is generated when a user logs on to the computer.


| Field |
|---|
| @timestamp |
| Target.process.Ext.authentication_id |
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
| event.code |
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
| process.Ext.ancestry |
| process.Ext.authentication_id |
| process.Ext.code_signature.exists |
| process.Ext.code_signature.status |
| process.Ext.code_signature.subject_name |
| process.Ext.code_signature.trusted |
| process.Ext.session_info.logon_type |
| process.code_signature.exists |
| process.code_signature.status |
| process.code_signature.subject_name |
| process.code_signature.trusted |
| process.entity_id |
| process.executable |
| process.name |
| user.domain |
| user.effective.domain |
| user.effective.email |
| user.effective.full_name |
| user.effective.hash |
| user.effective.id |
| user.effective.name |
| user.id |
| user.name |

