# A user account was created.

- OS: Windows
- Data Stream: `logs-endpoint.events.security-*`
- KQL: `event.action : "added-user-account" and event.dataset : "endpoint.events.security" and event.module : "endpoint" and event.provider : "Microsoft-Windows-Security-Auditing" and host.os.type : "windows"`

This event is generated when a user account was created.

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
| process.Ext.authentication_id |
| user.domain |
| user.effective.domain |
| user.effective.id |
| user.effective.name |
| user.id |
| user.name |
| winlog.event_data.AccountExpires |
| winlog.event_data.AllowedToDelegateTo |
| winlog.event_data.DisplayName |
| winlog.event_data.HomeDirectory |
| winlog.event_data.HomePath |
| winlog.event_data.LogonHours |
| winlog.event_data.NewUacValue |
| winlog.event_data.OldUacValue |
| winlog.event_data.PasswordLastSet |
| winlog.event_data.PrimaryGroupId |
| winlog.event_data.PrivilegeList |
| winlog.event_data.ProfilePath |
| winlog.event_data.SamAccountName |
| winlog.event_data.ScriptPath |
| winlog.event_data.SidHistory |
| winlog.event_data.UserAccountControl |
| winlog.event_data.UserParameters |
| winlog.event_data.UserPrincipalName |
| winlog.event_data.UserWorkstations |

