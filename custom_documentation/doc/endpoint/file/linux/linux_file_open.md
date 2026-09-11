# Linux File Open

- OS: Linux
- Data Stream: `logs-endpoint.events.file-*`
- KQL: `event.action : "open" and event.dataset : "endpoint.events.file" and event.module : "endpoint" and host.os.type : "linux"`

This event is generated when a file whose path matches a configured sensitive path pattern is opened, or when such an open fails with EACCES, EPERM or ENOENT. Each combination of file and access class is reported once per process life. A successful open reports the path the kernel resolved; a failed open has no resolved path and reports the path the caller requested, so a denied open through a symlink or a relative spelling that matches no pattern is not reported.


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
| error.code |
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
| file.Ext.access.flags |
| file.Ext.access.matched_path |
| file.Ext.access.mode |
| file.Ext.procfs.interface |
| file.Ext.procfs.target.entity_id |
| file.Ext.procfs.target.pid |
| file.Ext.procfs.target.thread.id |
| file.extension |
| file.gid |
| file.group |
| file.inode |
| file.mode |
| file.name |
| file.owner |
| file.path |
| file.size |
| file.target_path |
| file.uid |
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
| process.command_line |
| process.entity_id |
| process.entry_leader.entity_id |
| process.entry_leader.parent.entity_id |
| process.executable |
| process.group_leader.entity_id |
| process.name |
| process.parent.entity_id |
| process.pid |
| process.session_leader.entity_id |
| process.thread.id |
| user.Ext.real.id |
| user.Ext.real.name |
| user.id |
| user.name |

