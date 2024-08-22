# Windows Library Load

- OS: Windows
- Data Stream: `logs-endpoint.events.library-*`
- KQL: `event.action : "load" and event.dataset : "endpoint.events.library" and event.module : "endpoint" and host.os.type : "windows"`

This event is generated when a DLL or driver is loaded.


| Field |
|---|
| @timestamp |
| agent.id |
| agent.type |
| agent.version |
| data_stream.dataset |
| data_stream.namespace |
| data_stream.type |
| dll.Ext.code_signature.exists |
| dll.Ext.code_signature.status |
| dll.Ext.code_signature.subject_name |
| dll.Ext.code_signature.trusted |
| dll.Ext.defense_evasions |
| dll.Ext.load_index |
| dll.Ext.relative_file_creation_time |
| dll.Ext.relative_file_name_modify_time |
| dll.Ext.size |
| dll.code_signature.exists |
| dll.code_signature.status |
| dll.code_signature.subject_name |
| dll.code_signature.trusted |
| dll.hash.md5 |
| dll.hash.sha1 |
| dll.hash.sha256 |
| dll.name |
| dll.path |
| dll.pe.file_version |
| dll.pe.imphash |
| dll.pe.original_file_name |
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
| process.Ext.code_signature.exists |
| process.Ext.code_signature.status |
| process.Ext.code_signature.subject_name |
| process.Ext.code_signature.trusted |
| process.Ext.protection |
| process.code_signature.exists |
| process.code_signature.status |
| process.code_signature.subject_name |
| process.code_signature.trusted |
| process.entity_id |
| process.executable |
| process.name |
| process.pid |
| process.uptime |
| user.domain |
| user.id |
| user.name |

