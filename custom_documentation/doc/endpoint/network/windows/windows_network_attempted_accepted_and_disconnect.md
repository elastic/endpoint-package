# Windows TCP Connection and UDP Flow Events

- OS: Windows
- Data Stream: `logs-endpoint.events.network-*`
- KQL: `event.action : ("connection_attempted" or "connection_accepted" or "disconnect_received" or "udp_flow_outbound" or "udp_flow_inbound" or "udp_flow_ended") and event.dataset : "endpoint.events.network" and event.module : "endpoint" and host.os.type : "windows" and network.transport : ("tcp" or "udp")`

This event is generated when a TCP connection is attempted, accepted, or
terminated, or when a tracked UDP flow starts or ends. The UDP start actions
`udp_flow_outbound` and `udp_flow_inbound` report the start of a tracked flow,
not each datagram. TCP disconnects use `disconnect_received`.

`udp_flow_ended` carries the final `source.bytes` and `destination.bytes` of
the tracked UDP flow. It means tracking ended, not that a disconnect packet
was received or the remote socket closed.

UDP collection and forwarding are disabled by default. Collection can be
enabled by either production policy or diagnostic configuration. Forwarding
UDP events to Elasticsearch requires both Windows policy switches
`events.network` and `events.udp_send_to_es` to remain enabled. When UDP
collection is turned off, existing tracked flows are ended and their final
events can still be forwarded if both output switches remain enabled.
Turning off production UDP collection does not stop collection while it
remains enabled by diagnostic configuration.

| Field |
|---|
| @timestamp |
| agent.id |
| agent.type |
| agent.version |
| data_stream.dataset |
| data_stream.namespace |
| data_stream.type |
| destination.address |
| destination.bytes |
| destination.ip |
| destination.port |
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
| host.domain |
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
| network.direction |
| network.transport |
| network.type |
| process.Ext.ancestry |
| process.Ext.code_signature.exists |
| process.Ext.code_signature.status |
| process.Ext.code_signature.subject_name |
| process.Ext.code_signature.thumbprint_sha256 |
| process.Ext.code_signature.trusted |
| process.code_signature.exists |
| process.code_signature.status |
| process.code_signature.subject_name |
| process.code_signature.thumbprint_sha256 |
| process.code_signature.trusted |
| process.entity_id |
| process.executable |
| process.name |
| process.pid |
| process.uptime |
| source.address |
| source.bytes |
| source.ip |
| source.port |
| user.domain |
| user.id |
| user.name |

