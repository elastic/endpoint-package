# Schedule Task Updated

- OS: Windows
- Data Stream: `logs-endpoint.events.security-*`
- KQL: `event.action : "scheduled-task-updated" and event.dataset : "endpoint.events.security" and event.module : "endpoint" and event.provider : "Microsoft-Windows-Security-Auditing" and host.os.type : "windows"`

This event is generated when a schedule task was updated.

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
| process.parent.pid |
| process.pid |
| user.domain |
| user.id |
| user.name |
| winlog.event_data.TaskContentNew |
| winlog.event_data.TaskName |

