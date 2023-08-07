# Windows Shellcode Thread Alert

- OS: Windows
- Data Stream: `logs-endpoint.alerts-*`
- KQL: `event.code : "shellcode_thread" and event.dataset : "endpoint.alerts" and event.module : "endpoint" and host.os.type : "windows"`

This alert is generated when a Shellcode Threat alert occurs.


| Field |
|---|
| @timestamp |
| Endpoint.policy.applied.artifacts.global.identifiers.name |
| Endpoint.policy.applied.artifacts.global.identifiers.sha256 |
| Endpoint.policy.applied.artifacts.global.version |
| Endpoint.policy.applied.artifacts.user.identifiers.name |
| Endpoint.policy.applied.artifacts.user.identifiers.sha256 |
| Endpoint.policy.applied.artifacts.user.version |
| Memory_protection.cross_session |
| Memory_protection.feature |
| Memory_protection.parent_to_child |
| Memory_protection.self_injection |
| Memory_protection.unique_key_v1 |
| Responses.@timestamp |
| Responses.action.action |
| Responses.action.file.attributes |
| Responses.action.file.path |
| Responses.action.file.reason |
| Responses.action.key.actions |
| Responses.action.key.path |
| Responses.action.key.values.actions |
| Responses.action.key.values.name |
| Responses.action.source.attributes |
| Responses.action.source.path |
| Responses.message |
| Responses.result |
| Target.process.Ext.architecture |
| Target.process.Ext.code_signature.exists |
| Target.process.Ext.dll.Ext.code_signature.exists |
| Target.process.Ext.dll.Ext.code_signature.status |
| Target.process.Ext.dll.Ext.code_signature.subject_name |
| Target.process.Ext.dll.Ext.code_signature.trusted |
| Target.process.Ext.dll.Ext.mapped_address |
| Target.process.Ext.dll.Ext.mapped_size |
| Target.process.Ext.dll.code_signature.exists |
| Target.process.Ext.dll.code_signature.status |
| Target.process.Ext.dll.code_signature.subject_name |
| Target.process.Ext.dll.code_signature.trusted |
| Target.process.Ext.dll.hash.md5 |
| Target.process.Ext.dll.hash.sha1 |
| Target.process.Ext.dll.hash.sha256 |
| Target.process.Ext.dll.name |
| Target.process.Ext.dll.path |
| Target.process.Ext.memory_region.allocation_base |
| Target.process.Ext.memory_region.allocation_protection |
| Target.process.Ext.memory_region.allocation_size |
| Target.process.Ext.memory_region.allocation_type |
| Target.process.Ext.memory_region.bytes_address |
| Target.process.Ext.memory_region.bytes_allocation_offset |
| Target.process.Ext.memory_region.mapped_path |
| Target.process.Ext.memory_region.memory_pe_detected |
| Target.process.Ext.memory_region.region_base |
| Target.process.Ext.memory_region.region_protection |
| Target.process.Ext.memory_region.region_size |
| Target.process.Ext.memory_region.region_state |
| Target.process.Ext.memory_region.strings |
| Target.process.Ext.protection |
| Target.process.Ext.token.domain |
| Target.process.Ext.token.elevation |
| Target.process.Ext.token.elevation_type |
| Target.process.Ext.token.integrity_level_name |
| Target.process.Ext.token.sid |
| Target.process.Ext.token.user |
| Target.process.Ext.user |
| Target.process.args |
| Target.process.args_count |
| Target.process.code_signature.exists |
| Target.process.command_line |
| Target.process.entity_id |
| Target.process.executable |
| Target.process.hash.md5 |
| Target.process.hash.sha1 |
| Target.process.hash.sha256 |
| Target.process.name |
| Target.process.parent.Ext.architecture |
| Target.process.parent.Ext.code_signature.exists |
| Target.process.parent.Ext.code_signature.status |
| Target.process.parent.Ext.code_signature.subject_name |
| Target.process.parent.Ext.code_signature.trusted |
| Target.process.parent.Ext.protection |
| Target.process.parent.Ext.user |
| Target.process.parent.args |
| Target.process.parent.args_count |
| Target.process.parent.code_signature.exists |
| Target.process.parent.code_signature.status |
| Target.process.parent.code_signature.subject_name |
| Target.process.parent.code_signature.trusted |
| Target.process.parent.command_line |
| Target.process.parent.entity_id |
| Target.process.parent.executable |
| Target.process.parent.hash.md5 |
| Target.process.parent.hash.sha1 |
| Target.process.parent.hash.sha256 |
| Target.process.parent.name |
| Target.process.parent.pid |
| Target.process.parent.ppid |
| Target.process.parent.start |
| Target.process.parent.uptime |
| Target.process.pid |
| Target.process.ppid |
| Target.process.start |
| Target.process.thread.Ext.call_stack.instruction_pointer |
| Target.process.thread.Ext.call_stack.memory_section.memory_address |
| Target.process.thread.Ext.call_stack.memory_section.memory_size |
| Target.process.thread.Ext.call_stack.memory_section.protection |
| Target.process.thread.Ext.call_stack.module_name |
| Target.process.thread.Ext.call_stack.module_path |
| Target.process.thread.Ext.call_stack.symbol_info |
| Target.process.thread.Ext.call_stack_summary |
| Target.process.thread.Ext.original_start_address |
| Target.process.thread.Ext.original_start_address_allocation_offset |
| Target.process.thread.Ext.original_start_address_bytes |
| Target.process.thread.Ext.original_start_address_bytes_disasm |
| Target.process.thread.Ext.original_start_address_bytes_disasm_hash |
| Target.process.thread.Ext.original_start_address_module |
| Target.process.thread.Ext.start_address |
| Target.process.thread.Ext.start_address_allocation_offset |
| Target.process.thread.Ext.start_address_bytes |
| Target.process.thread.Ext.start_address_bytes_disasm |
| Target.process.thread.Ext.start_address_bytes_disasm_hash |
| Target.process.thread.Ext.start_address_module |
| Target.process.thread.id |
| Target.process.uptime |
| agent.build.original |
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
| event.risk_score |
| event.sequence |
| event.severity |
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
| process.Ext.architecture |
| process.Ext.code_signature.exists |
| process.Ext.dll.Ext.code_signature.exists |
| process.Ext.dll.Ext.code_signature.status |
| process.Ext.dll.Ext.code_signature.subject_name |
| process.Ext.dll.Ext.code_signature.trusted |
| process.Ext.dll.Ext.mapped_address |
| process.Ext.dll.Ext.mapped_size |
| process.Ext.dll.code_signature.exists |
| process.Ext.dll.code_signature.status |
| process.Ext.dll.code_signature.subject_name |
| process.Ext.dll.code_signature.trusted |
| process.Ext.dll.hash.md5 |
| process.Ext.dll.hash.sha1 |
| process.Ext.dll.hash.sha256 |
| process.Ext.dll.name |
| process.Ext.dll.path |
| process.Ext.protection |
| process.Ext.token.domain |
| process.Ext.token.elevation |
| process.Ext.token.elevation_type |
| process.Ext.token.integrity_level_name |
| process.Ext.token.sid |
| process.Ext.token.user |
| process.Ext.user |
| process.args |
| process.args_count |
| process.code_signature.exists |
| process.command_line |
| process.entity_id |
| process.executable |
| process.hash.md5 |
| process.hash.sha1 |
| process.hash.sha256 |
| process.name |
| process.parent.Ext.architecture |
| process.parent.Ext.code_signature.exists |
| process.parent.Ext.code_signature.status |
| process.parent.Ext.code_signature.subject_name |
| process.parent.Ext.code_signature.trusted |
| process.parent.Ext.protection |
| process.parent.Ext.user |
| process.parent.args |
| process.parent.args_count |
| process.parent.code_signature.exists |
| process.parent.code_signature.status |
| process.parent.code_signature.subject_name |
| process.parent.code_signature.trusted |
| process.parent.command_line |
| process.parent.entity_id |
| process.parent.executable |
| process.parent.hash.md5 |
| process.parent.hash.sha1 |
| process.parent.hash.sha256 |
| process.parent.name |
| process.parent.pid |
| process.parent.ppid |
| process.parent.start |
| process.parent.uptime |
| process.pid |
| process.ppid |
| process.start |
| process.thread.Ext.call_stack.instruction_pointer |
| process.thread.Ext.call_stack.memory_section.memory_address |
| process.thread.Ext.call_stack.memory_section.memory_size |
| process.thread.Ext.call_stack.memory_section.protection |
| process.thread.Ext.call_stack.module_name |
| process.thread.Ext.call_stack.module_path |
| process.thread.Ext.call_stack.symbol_info |
| process.thread.Ext.call_stack_final_user_module.name |
| process.thread.Ext.call_stack_summary |
| process.thread.Ext.start_address |
| process.thread.Ext.start_address_module |
| process.thread.id |
| process.uptime |
| rule.ruleset |
| user.domain |
| user.name |
