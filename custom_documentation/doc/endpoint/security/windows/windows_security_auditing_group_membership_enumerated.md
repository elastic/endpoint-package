# A security-enabled local group membership was enumerated.

- OS: Windows
- Data Stream: `logs-endpoint.events.security-*`
- KQL: `event.action : "group-membership-enumerated" and event.dataset : "endpoint.events.security" and event.module : "endpoint" and event.provider : "Microsoft-Windows-Security-Auditing" and host.os.type : "windows"`

This event is generated when a security-enabled local group membership was enumerated.

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
| event.code |
| event.created |
| event.dataset |
| event.id |
| event.kind |
| event.module |
| event.outcome |
| event.provider |
| event.sequence |
| event.type |
| host.id |
| host.name |
| host.os.type |
| message |
| process.Ext.authentication_id |
| process.Ext.code_signature.exists |
| process.Ext.code_signature.status |
| process.code_signature.exists |
| process.code_signature.status |
| process.executable |
| process.pid |
| user.domain |
| user.effective.domain |
| user.effective.id |
| user.effective.name |
| user.id |
| user.name |

