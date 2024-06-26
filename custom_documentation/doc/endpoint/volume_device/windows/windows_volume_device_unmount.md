# Windows Device Unmount

- OS: Windows
- Data Stream: `logs-endpoint.events.volume_device-*`
- KQL: `event.action : "unmount" and event.dataset : "endpoint.events.volume_device" and event.module : "endpoint" and host.os.type : "windows"`

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
| process.Ext.ancestry |
| process.entity_id |
| process.name |
| process.pid |
| user.domain |
| user.id |
| user.name |
| volume.bus_type |
| volume.device_type |
| volume.dos_name |
| volume.file_system_type |
| volume.nt_name |
| volume.product_name |
| volume.serial_number |
| volume.vendor_name |

