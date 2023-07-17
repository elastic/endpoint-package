# Windows Malware Unquarantine

- OS: Windows
- Data Stream: `logs-endpoint.events.file-*`
- KQL: `event.action : "endpoint_unquarantine" and event.dataset : "endpoint.events.file" and event.module : "endpoint" and host.os.type : "windows"`

This event is generated when Endpoint restores a file from the malware quarantine.


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
| event.Ext.correlation.id |
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
| file.Ext.original.path |
| file.hash.md5 |
| file.hash.sha1 |
| file.hash.sha256 |
| file.name |
| file.path |
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

