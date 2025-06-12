# A service was installed in the system.

- OS: Windows
- Data Stream: `logs-endpoint.events.security-*`
- KQL: `event.action : "service-installed" and event.dataset : "endpoint.events.security" and event.module : "endpoint" and event.provider : "Microsoft-Windows-Security-Auditing" and host.os.type : "windows"`

This event is generated when a service was installed in the system.

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
| process.pid |
| user.domain |
| user.id |
| user.name |
| winlog.event_data.ServiceAccount |
| winlog.event_data.ServiceFileName |
| winlog.event_data.ServiceName |
| winlog.event_data.ServiceStartType |
| winlog.event_data.ServiceType |

