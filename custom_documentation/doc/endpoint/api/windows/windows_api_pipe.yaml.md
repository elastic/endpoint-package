# Windows Pipe API

- OS: Windows
- Data Stream: `logs-endpoint.events.api-*`
- KQL: `event.dataset : "endpoint.events.api" and event.module : "endpoint" and event.provider : "MinifilterCallback" and host.os.type : "windows"`

This event is generated when a pipe (Named Pipe/Mailslot) creation API is called

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
| event.category |
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
| process.Ext.api.name |
| process.Ext.api.parameters.desired_access_numeric |
| process.Ext.api.parameters.desired_access |
| process.Ext.api.parameters.is_remote |
| process.Ext.api.parameters.operation |
| process.Ext.api.parameters.pipe_mode |
| process.Ext.api.parameters.pipe_path |
| process.Ext.api.parameters.pipe_type |
| process.Ext.api.parameters.read_mode |
| process.Ext.token.integrity_level_name |
| process.entity_id |
| process.executable |
| process.name |
| process.pid |
| process.thread.id |
| user.domain |
| user.id |
| user.name |

