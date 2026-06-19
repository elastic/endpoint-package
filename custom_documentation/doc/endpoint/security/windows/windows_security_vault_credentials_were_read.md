# Vault credentials were read.

- OS: Windows
- Data Stream: `logs-endpoint.events.security-*`
- KQL: `event.action : "vault_credentials_read" and event.dataset : "endpoint.events.security" and event.module : "endpoint" and event.provider : "Microsoft-Windows-Security-Auditing" and host.os.type : "windows"`

This event is generated when vault credentials were read.

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
| process.Ext.api.metadata.return_value |
| process.Ext.authentication_id |
| process.Ext.code_signature.exists |
| process.Ext.code_signature.status |
| process.Ext.code_signature.subject_name |
| process.Ext.code_signature.thumbprint_sha256 |
| process.Ext.code_signature.trusted |
| process.Ext.token.integrity_level_name |
| process.code_signature.exists |
| process.code_signature.status |
| process.code_signature.subject_name |
| process.code_signature.thumbprint_sha256 |
| process.code_signature.trusted |
| process.entity_id |
| process.executable |
| process.name |
| process.parent.executable |
| process.pid |
| user.domain |
| user.id |
| user.name |
| winlog.event_data.Flags |
| winlog.event_data.Identity |
| winlog.event_data.PackageSid |
| winlog.event_data.Resource |
| winlog.event_data.Schema |
| winlog.event_data.SchemaFriendlyName |

