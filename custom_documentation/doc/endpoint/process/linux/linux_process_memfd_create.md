# Linux memfd Creation Events

- OS: Linux
- Data Stream: `logs-endpoint.events.process-*`
- KQL: `event.action : "memfd_create" and event.dataset : "endpoint.events.process" and event.module : "endpoint" and host.os.type : "linux"`

This event is generated when when a memfd anonymous file is created.

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
| group.Ext.real.id |
| group.Ext.real.name |
| group.id |
| group.name |
| host.id |
| host.name |
| host.os.type |
| message |
| process.args |
| process.args_count |
| process.command_line |
| process.entity_id |
| process.entry_leader.parent.entity_id |
| process.entry_leader.parent.pid |
| process.entry_leader.parent.start |
| process.executable |
| process.Ext.memfd.flag_hugetlb |
| process.Ext.memfd.flag_allow_seal |
| process.Ext.memfd.flags |
| process.Ext.memfd.name |
| process.Ext.memfd.flag_exec |
| process.Ext.memfd.flag_cloexec |
| process.Ext.memfd.flag_noexec_seal |
| process.group.id |
| process.group.name |
| process.group_leader.args |
| process.group_leader.args_count |
| process.group_leader.entity_id |
| process.group_leader.executable |
| process.group_leader.group.id |
| process.group_leader.group.name |
| process.group_leader.interactive |
| process.group_leader.name |
| process.group_leader.pid |
| process.group_leader.real_group.id |
| process.group_leader.real_group.name |
| process.group_leader.real_user.id |
| process.group_leader.real_user.name |
| process.group_leader.same_as_process |
| process.group_leader.start |
| process.group_leader.user.id |
| process.group_leader.user.name |
| process.group_leader.working_directory |
| process.hash.sha256 |
| process.interactive |
| process.name |
| process.parent.args_count |
| process.parent.pid |
| process.pid |
| process.real_group.id |
| process.real_group.name |
| process.real_user.id |
| process.real_user.name |
| process.session_leader.args |
| process.session_leader.args_count |
| process.session_leader.entity_id |
| process.session_leader.executable |
| process.session_leader.group.id |
| process.session_leader.group.name |
| process.session_leader.interactive |
| process.session_leader.name |
| process.session_leader.pid |
| process.session_leader.real_group.id |
| process.session_leader.real_group.name |
| process.session_leader.real_user.id |
| process.session_leader.real_user.name |
| process.session_leader.same_as_process |
| process.session_leader.start |
| process.session_leader.user.id |
| process.session_leader.user.name |
| process.session_leader.working_directory |
| process.start |
| process.user.id |
| process.user.name |
| process.working_directory |
| user.Ext.real.id |
| user.Ext.real.name |
| user.id |
| user.name |
