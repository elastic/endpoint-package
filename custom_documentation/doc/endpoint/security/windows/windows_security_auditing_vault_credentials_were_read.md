# Vault credentials were read or enumerated.

- OS: Windows
- Data Stream: `logs-endpoint.events.security-*`
- KQL: `event.action : "vault-credentials-were-read" and event.dataset : "endpoint.events.security" and event.module : "endpoint" and event.provider : "Microsoft-Windows-Security-Auditing" and host.os.type : "windows"`

This event is generated when vault credentials were read or enumerated.

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
| process.pid |
| user.domain |
| user.id |
| user.name |
| winlog.event_data.CountOfCredentialsReturned |
| winlog.event_data.Flags |
| winlog.event_data.Identity |
| winlog.event_data.PackageSid |
| winlog.event_data.Resource |
| winlog.event_data.Schema |
| winlog.event_data.SchemaFriendlyName |

