# macOS Device Mount

- OS: macOS
- Data Stream: `logs-endpoint.events.device-*`
- KQL: `event.action : "mount" and event.dataset : "endpoint.events.device" and event.module : "endpoint" and host.os.type : "macos"`

This event is generated when a device is mounted.

| Field |
|---|
| @timestamp |
| agent.id |
| agent.type |
| agent.version |
| data_stream.dataset |
| data_stream.namespace |
| data_stream.type |
| device.image_path |
| device.product.id |
| device.product.name |
| device.serial_number |
| device.type |
| device.vendor.id |
| device.vendor.name |
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
| group.id |
| group.name |
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
| process.Ext.code_signature.exists |
| process.Ext.code_signature.status |
| process.Ext.code_signature.subject_name |
| process.Ext.code_signature.trusted |
| process.code_signature.exists |
| process.code_signature.signing_id |
| process.code_signature.status |
| process.code_signature.subject_name |
| process.code_signature.team_id |
| process.code_signature.trusted |
| process.entity_id |
| process.executable |
| process.name |
| process.pid |
| user.Ext.real.id |
| user.domain |
| user.id |
| user.name |
| volume.bus_type |
| volume.device_name |
| volume.file_system_type |
| volume.mount_name |
| volume.removable |
| volume.size |
| volume.writable |

