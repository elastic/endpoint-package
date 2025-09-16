# Windows User Log On

- OS: Windows
- Data Stream: `logs-endpoint.events.security-*`
- KQL: `event.action : "log_on" and event.dataset : "endpoint.events.security" and event.module : "endpoint" and event.provider : "Microsoft-Windows-Security-Auditing" and host.os.type : "windows"`

This event is generated when a user logs on to the computer.

| Field |
|---|
| @timestamp |
| Target.process.Ext.authentication_id |
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
| process.Ext.code_signature.exists |
| process.Ext.code_signature.status |
| process.Ext.code_signature.subject_name |
| process.Ext.code_signature.trusted |
| process.Ext.protection |
| process.Ext.session_info.authentication_package |
| process.Ext.session_info.failure_reason |
| process.Ext.session_info.logon_process_name |
| process.Ext.session_info.logon_type |
| process.Ext.token.elevation |
| process.Ext.token.impersonation_level |
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
| source.ip |
| user.domain |
| user.effective.domain |
| user.effective.id |
| user.effective.name |
| user.id |
| user.name |
| user.target.domain |
| user.target.name |
| winlog.event_data.KeyLength |
| winlog.event_data.LmPackageName |
| winlog.event_data.LoginGuid |
| winlog.event_data.PrivilegeList |
| winlog.event_data.RemoteCredentialGuard |
| winlog.event_data.RestrictedAdminMode |
| winlog.event_data.Status |
| winlog.event_data.SubStatus |
| winlog.event_data.TargetInfo |
| winlog.event_data.TargetLinkedLogonId |
| winlog.event_data.TargetLogonGuid |
| winlog.event_data.TargetServerName |
| winlog.event_data.TransmittedServices |
| winlog.event_data.VirtualAccount |
| winlog.event_data.WorkstationName |

