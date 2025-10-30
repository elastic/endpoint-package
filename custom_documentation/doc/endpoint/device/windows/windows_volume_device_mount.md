# Windows Device Mount

- OS: Windows
- Data Stream: `logs-endpoint.events.device-*`
- KQL: `event.action : "mount" and event.dataset : "endpoint.events.device" and event.module : "endpoint" and host.os.type : "windows"`

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
| process.Ext.code_signature.thumbprint_sha256 |
| process.Ext.code_signature.exists |
| process.Ext.code_signature.status |
| process.code_signature.trusted |
| process.code_signature.subject_name |
| process.code_signature.thumbprint_sha256 |
| process.code_signature.exists |
| process.code_signature.status |
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
| message |
| device.product.name |
| device.product.id |
| device.vendor.name |
| device.vendor.id |
| device.serial_number |
| device.type |
| user.domain |
| user.name |
| user.id |

