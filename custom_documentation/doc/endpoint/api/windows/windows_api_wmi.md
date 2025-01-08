# Windows API

- OS: Windows
- Data Stream: `logs-endpoint.events.api-*`
- KQL: `event.dataset : "endpoint.events.api" and event.module : "endpoint" and event.provider : "Microsoft-Windows-WMI-Activity" and host.os.type : "windows"`

This event is generated when WMI Activity-related APIs are called.

| Field |
|---|
| @timestamp |
| Target.process.Ext.protection |
| Target.process.name |
| Target.process.pid |
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
| process.Ext.api.behaviors |
| process.Ext.api.metadata.client_is_local |
| process.Ext.api.metadata.client_machine |
| process.Ext.api.metadata.client_machine_fqdn |
| process.Ext.api.metadata.client_process_id |
| process.Ext.api.name |
| process.Ext.api.parameters.consumer_details |
| process.Ext.api.parameters.consumer_name |
| process.Ext.api.parameters.consumer_type |
| process.Ext.api.parameters.event_filter_details |
| process.Ext.api.parameters.event_filter_name |
| process.Ext.api.parameters.namespace |
| process.Ext.api.parameters.operation |
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

