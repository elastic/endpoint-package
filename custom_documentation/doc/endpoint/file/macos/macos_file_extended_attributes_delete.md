# macOS File Extended Attributes Delete

- OS: macOS
- Data Stream: `logs-endpoint.events.file-*`
- KQL: `event.action : "extended_attributes_delete" and event.dataset : "endpoint.events.file" and event.module : "endpoint" and host.os.type : "macos"`

This event is generated when extended file attributes are deleted.


| Field |
|---|
| @timestamp |
| Effective_process.entity_id |
| Effective_process.executable |
| Effective_process.name |
| Effective_process.pid |
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
| file.attributes |
| file.hash.sha256 |
| file.inode |
| file.name |
| file.path |
| file.size |
| group.Ext.real.id |
| group.Ext.real.name |
| group.id |
| group.name |
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
| process.code_signature.exists |
| process.code_signature.signing_id |
| process.code_signature.status |
| process.code_signature.subject_name |
| process.code_signature.team_id |
| process.code_signature.trusted |
| process.entity_id |
| process.executable |
| process.name |
| process.parent.pid |
| process.pid |
| user.Ext.real.id |
| user.Ext.real.name |
| user.id |
| user.name |

