# Linux Malicious Behavior Alert

- OS: Linux
- Data Stream: `logs-endpoint.alerts-*`
- KQL: `event.code : "behavior" and event.dataset : "endpoint.alerts" and event.module : "endpoint" and host.os.type : "linux"`

This alert is generated when a Malicious Behavior alert occurs.


| Field |
|---|
| @timestamp |
| Endpoint.policy.applied.artifacts.global.identifiers.name |
| Endpoint.policy.applied.artifacts.global.identifiers.sha256 |
| Endpoint.policy.applied.artifacts.global.snapshot |
| Endpoint.policy.applied.artifacts.global.update_age |
| Endpoint.policy.applied.artifacts.global.version |
| Endpoint.policy.applied.artifacts.user.identifiers.name |
| Endpoint.policy.applied.artifacts.user.identifiers.sha256 |
| Endpoint.policy.applied.artifacts.user.version |
| Events.*<br /><br />Events is a list containing embedded copies of all events that triggered the Malicious Behavior alert. All fields that can exist in any event document can appear in this list. |
| Events._label |
| Events._state |
| Responses.@timestamp |
| Responses.action.action |
| Responses.action.field |
| Responses.action.state |
| Responses.action.tree |
| Responses.message |
| Responses.process.entity_id |
| Responses.process.name |
| Responses.process.pid |
| Responses.result |
| agent.build.original |
| agent.id |
| agent.type |
| agent.version |
| cloud.account.id |
| cloud.instance.name |
| cloud.project.id |
| cloud.provider |
| cloud.region |
| container.id |
| container.image.hash.all |
| container.image.name |
| container.image.tag |
| container.name |
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
| event.risk_score |
| event.sequence |
| event.severity |
| event.type |
| file.*<br /><br />file contains the file data from the primary event in Events. It can contain any fields that any other events includes within the file fieldset. |
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
| orchestrator.cluster.id |
| orchestrator.cluster.name |
| orchestrator.namespace |
| orchestrator.resource.ip |
| orchestrator.resource.name |
| orchestrator.resource.parent.type |
| orchestrator.resource.type |
| process.*<br /><br />process contains the process data from the primary event in Events. It can contain any fields that any other events includes within the process fieldset. |
| rule.description |
| rule.id |
| rule.name |
| rule.reference |
| rule.ruleset |
| rule.version |
| threat.framework |
| threat.tactic.id |
| threat.tactic.name |
| threat.tactic.reference |
| threat.technique.id |
| threat.technique.name |
| threat.technique.reference |
| threat.technique.subtechnique |
| user.Ext.real.id |
| user.Ext.real.name |
| user.id |
| user.name |

