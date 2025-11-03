# Windows Win32k API

- OS: Windows
- Data Stream: `logs-endpoint.events.api-*`
- KQL: `event.dataset : "endpoint.events.api" and event.module : "endpoint" and event.provider : "Microsoft-Windows-Win32k" and host.os.type : "windows"`

This event is generated when keylogging-related Win32k APIs are called.

| Field |
|---|
| @timestamp |
| Target.process.Ext.desktop_name |
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
| process.Ext.api.metadata.background_callcount |
| process.Ext.api.metadata.ms_since_last_keyevent |
| process.Ext.api.metadata.procedure_symbol |
| process.Ext.api.metadata.return_value |
| process.Ext.api.metadata.start_address_allocation_protection |
| process.Ext.api.metadata.start_address_module |
| process.Ext.api.metadata.target_address_name |
| process.Ext.api.metadata.target_address_path |
| process.Ext.api.metadata.thread_info_flags |
| process.Ext.api.metadata.visible_windows_count |
| process.Ext.api.metadata.windows_count |
| process.Ext.api.name |
| process.Ext.api.parameters.address |
| process.Ext.api.parameters.allocation_type |
| process.Ext.api.parameters.flags |
| process.Ext.api.parameters.hook_module |
| process.Ext.api.parameters.hook_type |
| process.Ext.api.parameters.procedure |
| process.Ext.api.parameters.protection |
| process.Ext.api.parameters.protection_old |
| process.Ext.api.parameters.size |
| process.Ext.api.parameters.usage |
| process.Ext.api.parameters.usage_page |
| process.Ext.api.summary |
| process.Ext.code_signature.exists |
| process.Ext.code_signature.status |
| process.Ext.code_signature.subject_name |
| process.Ext.code_signature.thumbprint_sha256 |
| process.Ext.code_signature.trusted |
| process.Ext.protection |
| process.Ext.token.integrity_level_name |
| process.code_signature.exists |
| process.code_signature.status |
| process.code_signature.subject_name |
| process.code_signature.thumbprint_sha256 |
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

