# Windows API

- OS: Windows
- Data Stream: `logs-endpoint.events.api-*`
- KQL: `event.dataset : "endpoint.events.api" and event.module : "endpoint" and event.type : "access" and host.os.type : "windows"`

This event is generated when a process attempts to access priviledged credentials. 

| Field |
|---|
| @timestamp |
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
| process.Ext.api.name |
| process.Ext.api.parameters.desired_access |
| process.Ext.api.parameters.desired_access_numeric |
| process.Ext.api.parameters.handle_type |
| process.Ext.code_signature.exists |
| process.Ext.code_signature.status |
| process.Ext.code_signature.subject_name |
| process.Ext.code_signature.trusted |
| process.code_signature.exists |
| process.code_signature.status |
| process.code_signature.subject_name |
| process.code_signature.trusted |
| process.entity_id |
| process.executable |
| process.name |
| process.pid |
| process.thread.Ext.call_stack.instruction_pointer |
| process.thread.Ext.call_stack.module_path |
| process.thread.Ext.call_stack_contains_unbacked |
| process.thread.Ext.call_stack_final_user_module.path |
| process.thread.id |
| user.domain |
| user.id |
| user.name |

