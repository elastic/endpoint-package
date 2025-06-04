# Windows Already Running Process

- OS: Windows
- Data Stream: `logs-endpoint.events.process-*`
- KQL: `event.action : "already_running" and event.dataset : "endpoint.events.process" and event.module : "endpoint" and host.os.type : "windows"`

This event is generated for a process that was already running before Endpoint's process collection was enabled.


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
| process.Ext.authentication_id |
| process.Ext.code_signature.exists |
| process.Ext.code_signature.status |
| process.Ext.code_signature.subject_name |
| process.Ext.code_signature.trusted |
| process.Ext.command_line_truncated |
| process.Ext.desktop_name |
| process.Ext.mitigation_policies |
| process.Ext.protection |
| process.Ext.relative_file_creation_time |
| process.Ext.session_info.authentication_package |
| process.Ext.session_info.client_address |
| process.Ext.session_info.id |
| process.Ext.session_info.logon_type |
| process.Ext.session_info.relative_logon_time |
| process.Ext.session_info.relative_password_age |
| process.Ext.session_info.user_flags |
| process.Ext.token.elevation_level |
| process.Ext.token.integrity_level_name |
| process.Ext.token.security_attributes |
| process.Ext.windows.zone_identifier |
| process.args |
| process.args_count |
| process.code_signature.exists |
| process.code_signature.status |
| process.code_signature.subject_name |
| process.code_signature.trusted |
| process.command_line |
| process.entity_id |
| process.executable |
| process.hash.md5 |
| process.hash.sha1 |
| process.hash.sha256 |
| process.name |
| process.origin_referrer_url |
| process.origin_url |
| process.parent.Ext.code_signature.exists |
| process.parent.Ext.code_signature.status |
| process.parent.Ext.code_signature.subject_name |
| process.parent.Ext.code_signature.trusted |
| process.parent.Ext.command_line_truncated |
| process.parent.args |
| process.parent.args_count |
| process.parent.code_signature.exists |
| process.parent.code_signature.status |
| process.parent.code_signature.subject_name |
| process.parent.code_signature.trusted |
| process.parent.command_line |
| process.parent.entity_id |
| process.parent.executable |
| process.parent.name |
| process.parent.pid |
| process.pe.imphash |
| process.pe.original_file_name |
| process.pid |
| process.working_directory |
| user.domain |
| user.id |
| user.name |

