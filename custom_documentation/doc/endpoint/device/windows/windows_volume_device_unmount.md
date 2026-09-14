# Windows Device Unmount

- OS: Windows
- Data Stream: `logs-endpoint.events.device-*`
- KQL: `event.action : "unmount" and event.dataset : "endpoint.events.device" and event.module : "endpoint" and host.os.type : "windows"`

This event is generated when a device is unmounted.

| Field |
|---|
| @timestamp |
| agent.id |
| agent.type |
| agent.version |
| data_stream.dataset |
| data_stream.namespace |
| data_stream.type |
| device.product.name |
| device.serial_number |
| device.type |
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
| process.entity_id |
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

