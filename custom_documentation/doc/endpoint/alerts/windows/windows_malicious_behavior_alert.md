# Windows Malicious Behavior Alert

- OS: Windows
- Data Stream: `logs-endpoint.alerts-*`
- KQL: `event.code : "behavior" and event.dataset : "endpoint.alerts" and event.module : "endpoint" and host.os.type : "windows"`

This alert occurs when a Malicious Behavior alert occurs.


| Field |
|---|
| @timestamp |
| Endpoint.policy.applied.artifacts.global.channel |
| Endpoint.policy.applied.artifacts.global.identifiers.name |
| Endpoint.policy.applied.artifacts.global.identifiers.sha256 |
| Endpoint.policy.applied.artifacts.global.manifest_type |
| Endpoint.policy.applied.artifacts.global.snapshot |
| Endpoint.policy.applied.artifacts.global.update_age |
| Endpoint.policy.applied.artifacts.global.version |
| Endpoint.policy.applied.artifacts.user.identifiers.name |
| Endpoint.policy.applied.artifacts.user.identifiers.sha256 |
| Endpoint.policy.applied.artifacts.user.version |
| Endpoint.policy.applied.endpoint_policy_version |
| Endpoint.policy.applied.id |
| Endpoint.policy.applied.name |
| Endpoint.policy.applied.version |
| Events.*<br /><br />Events is a list containing embedded copies of all events that triggered the Malicious Behavior alert. All fields that can exist in any event document can appear in this list. |
| Events._label |
| Events._state |
| Responses.@timestamp |
| Responses.action.action |
| Responses.action.field |
| Responses.action.file.attributes |
| Responses.action.file.path |
| Responses.action.file.reason |
| Responses.action.key.actions |
| Responses.action.key.path |
| Responses.action.key.values.actions |
| Responses.action.key.values.name |
| Responses.action.source.attributes |
| Responses.action.source.path |
| Responses.action.state |
| Responses.action.tree |
| Responses.message |
| Responses.process.entity_id |
| Responses.process.name |
| Responses.process.pid |
| Responses.result |
| Target.*<br /><br />Target contains target process data from the primary event in Events. It can contain any fields that any other events includes within the Target fieldset. |
| agent.build.original |
| agent.id |
| agent.type |
| agent.version |
| data_stream.dataset |
| data_stream.namespace |
| data_stream.type |
| destination.ip |
| destination.port |
| dll.*<br /><br />dll contains dll data from the primary event in Events. It can contain any fields that any other events includes within the dll fieldset. |
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
| event.risk_score |
| event.sequence |
| event.severity |
| event.type |
| file.*<br /><br />file contains the file data from the primary event in Events. It can contain any fields that any other events includes within the file fieldset. |
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
| network.transport |
| network.type |
| process.*<br /><br />process contains the process data from the primary event in Events. It can contain any fields that any other events includes within the process fieldset. |
| registry.*<br /><br />registry contains the registry data from the primary event in Events. It can contain any fields that any other events includes within the registry fieldset. |
| rule.description |
| rule.id |
| rule.name |
| rule.reference |
| rule.ruleset |
| rule.version |
| source.ip |
| source.port |
| threat.framework |
| threat.tactic.id |
| threat.tactic.name |
| threat.tactic.reference |
| threat.technique.id |
| threat.technique.name |
| threat.technique.reference |
| threat.technique.subtechnique |
| threat.technique.subtechnique.id |
| threat.technique.subtechnique.name |
| threat.technique.subtechnique.reference |
| user.domain |
| user.effective.domain |
| user.effective.id |
| user.effective.name |
| user.id |
| user.name |
| user.target.domain |
| user.target.name |
| winlog.*<br /><br />winlog contains information about the Windows Event Log. |

