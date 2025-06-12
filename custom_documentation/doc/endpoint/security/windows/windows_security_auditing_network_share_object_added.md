# A network share object was added.

- OS: Windows
- Data Stream: `logs-endpoint.events.security-*`
- KQL: `event.action : "network-share-object-added" and event.dataset : "endpoint.events.security" and event.module : "endpoint" and event.provider : "Microsoft-Windows-Security-Auditing" and host.os.type : "windows"`

This event is generated when a network share object was added

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
| user.domain |
| user.id |
| user.name |
| winlog.event_data.ShareLocalPath |
| winlog.event_data.ShareName |

