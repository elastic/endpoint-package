# Windows Device Mount

- OS: Windows
- Data Stream: `logs-endpoint.events.device-*`
- KQL: `event.action : "mount" and event.dataset : "endpoint.events.device" and event.module : "endpoint" and host.os.type : "windows"`

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
| host.id |
| host.name |
| host.os.type |
| message |
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

