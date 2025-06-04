# Endpoint Policy Response

- OS: Linux, Windows, macOS
- Data Stream: `metrics-endpoint.policy-*`
- KQL: `event.action : "endpoint_policy_response" and event.dataset : "endpoint.policy" and event.module : "endpoint"`

This is a state management document that is generated every time Endpoint refreshes it's policy. It contains details of what Endpoint features are and are not in a healthy state.


| Field |
|---|
| @timestamp |
| Endpoint.configuration.isolation |
| Endpoint.policy.applied.actions.message |
| Endpoint.policy.applied.actions.name |
| Endpoint.policy.applied.actions.status |
| Endpoint.policy.applied.actions.status |
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
| Endpoint.policy.applied.response.configurations.antivirus_registration.concerned_actions |
| Endpoint.policy.applied.response.configurations.antivirus_registration.status |
| Endpoint.policy.applied.response.configurations.attack_surface_reduction.concerned_actions |
| Endpoint.policy.applied.response.configurations.attack_surface_reduction.status |
| Endpoint.policy.applied.response.configurations.behavior_protection.concerned_actions |
| Endpoint.policy.applied.response.configurations.behavior_protection.status |
| Endpoint.policy.applied.response.configurations.events.concerned_actions |
| Endpoint.policy.applied.response.configurations.events.status |
| Endpoint.policy.applied.response.configurations.host_isolation.concerned_actions |
| Endpoint.policy.applied.response.configurations.host_isolation.status |
| Endpoint.policy.applied.response.configurations.logging.concerned_actions |
| Endpoint.policy.applied.response.configurations.logging.status |
| Endpoint.policy.applied.response.configurations.malware.concerned_actions |
| Endpoint.policy.applied.response.configurations.malware.status |
| Endpoint.policy.applied.response.configurations.memory_protection.concerned_actions |
| Endpoint.policy.applied.response.configurations.memory_protection.status |
| Endpoint.policy.applied.response.configurations.ransomware.concerned_actions |
| Endpoint.policy.applied.response.configurations.ransomware.status |
| Endpoint.policy.applied.response.configurations.response_actions.concerned_actions |
| Endpoint.policy.applied.response.configurations.response_actions.status |
| Endpoint.policy.applied.response.configurations.streaming.concerned_actions |
| Endpoint.policy.applied.response.configurations.streaming.status |
| Endpoint.policy.applied.response.diagnostic.behavior_protection.concerned_actions |
| Endpoint.policy.applied.response.diagnostic.behavior_protection.status |
| Endpoint.policy.applied.response.diagnostic.malware.concerned_actions |
| Endpoint.policy.applied.response.diagnostic.malware.status |
| Endpoint.policy.applied.response.diagnostic.memory_protection.concerned_actions |
| Endpoint.policy.applied.response.diagnostic.memory_protection.status |
| Endpoint.policy.applied.response.diagnostic.ransomware.concerned_actions |
| Endpoint.policy.applied.response.diagnostic.ransomware.status |
| Endpoint.policy.applied.status |
| Endpoint.policy.applied.version |
| Endpoint.state.isolation |
| Endpoint.state.tamper_protection |
| agent.build.original |
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

