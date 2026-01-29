# macOS Device Mount

- OS: macOS
- Data Stream: `logs-endpoint.events.device-*`
- KQL: `event.action : "mount" and event.dataset : "endpoint.events.device" and event.module : "endpoint" and host.os.type : "macos"`

This event is generated when a device is mounted.

| Field |
|---|
| volume.device_name |
| volume.bus_type |
| volume.size |
| volume.removable |
| volume.mount_name |
| volume.file_system_type |
| volume.writable |
| agent.id |
| agent.type |
| agent.version |
| process.Ext.code_signature.trusted |
| process.Ext.code_signature.subject_name |
| process.Ext.code_signature.exists |
| process.Ext.code_signature.status |
| process.code_signature.trusted |
| process.code_signature.subject_name |
| process.code_signature.exists |
| process.code_signature.status |
| process.code_signature.signing_id |
| process.code_signature.team_id |
| process.name |
| process.pid |
| process.entity_id |
| process.executable |
| @timestamp |
| ecs.version |
| data_stream.namespace |
| data_stream.type |
| data_stream.dataset |
| elastic.agent.id |
| host.os.type |
| host.name |
| host.id |
| event.sequence |
| event.created |
| event.kind |
| event.module |
| event.action |
| event.id |
| event.category |
| event.type |
| event.dataset |
| event.outcome |
| group.Ext.real.id |
| group.id |
| group.name |
| message |
| device.product.name |
| device.product.id |
| device.vendor.name |
| device.vendor.id |
| device.serial_number |
| device.type |
| user.domain |
| user.Ext.real.id |
| user.name |
| user.id |

