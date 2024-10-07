# Windows API

- OS: Windows
- Data Stream: `logs-endpoint.events.api-*`
- KQL: `event.dataset : "endpoint.events.api" and event.module : "endpoint" and event.provider : "Microsoft-Windows-TCPIP" and host.os.type : "windows"`

This event is generated when ETW Microsoft-Windows-TCPIP events are generated.

| Field |
|---|
| @timestamp |
| agent.id |
| agent.type |
| agent.version |
| data_stream.dataset |
| data_stream.namespace |
| data_stream.type |
| destination.ip |
| destination.port |
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
| network.transport |
| network.type |
| process.Ext.api.behaviors |
| process.Ext.api.name |
| process.Ext.api.summary |
| process.Ext.code_signature.exists |
| process.Ext.code_signature.status |
| process.Ext.code_signature.subject_name |
| process.Ext.code_signature.trusted |
| process.Ext.token.integrity_level_name |
| process.code_signature.exists |
| process.code_signature.status |
| process.code_signature.subject_name |
| process.code_signature.trusted |
| process.command_line |
| process.entity_id |
| process.executable |
| process.name |
| process.parent.executable |
| process.pid |
| process.thread.id |
| user.domain |
| user.id |
| user.name |

