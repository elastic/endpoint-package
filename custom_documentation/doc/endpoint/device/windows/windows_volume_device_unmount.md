# Windows Device Unmount

- OS: Windows
- Data Stream: `logs-endpoint.events.device-*`
- KQL: `event.action : "unmount" and event.dataset : "endpoint.events.device" and event.module : "endpoint" and host.os.type : "windows"`

This event is generated when a device is unmounted.

| Field |
|---|
| volume.device_name |
| volume.bus_type |
| volume.removable |
| volume.mount_name |
| volume.file_system_type |
| volume.writable |
| agent.id |
| agent.type |
| agent.version |
| process.name |
| process.pid |
| process.entity_id |
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
| device.vendor.name |
| device.serial_number |
| device.type |
| user.domain |
| user.name |
| user.id |

