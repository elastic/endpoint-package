# alerts
### Sample Event
<details>
<summary>
Click to expand
</summary>

```json
{
    "agent": {
        "build": {
            "original": "version: 8.3.0-SNAPSHOT, compiled: Fri Apr 1 06:00:00 2022, branch: main, commit: f8b0ed879ad40ee1ae561ced31ec8a4027a2bf53"
        },
        "id": "2b1eb7f7-bd61-436a-98af-c2b182043476",
        "type": "endpoint",
        "version": "8.3.0-SNAPSHOT"
    },
    "container": {
        "id": "4c9c9cb3-f80f-44d8-9c89-6168243b7f21",
        "image": {
            "name": "docker.io/library/nginx",
            "tag": "latest"
        },
        "name": "nginx"
    },
    "cloud": {
        "account": {
            "id": "1234"
        },
        "instance": {
            "name": "webserver-12"
        },
        "project": {
            "id": "1234"
        },
        "provider": "aws",
        "region": "us-east-1"
    },
    "orchestrator": {
        "cluster": {
            "name": "webservers"
        },
        "namespace": "webapp",
        "resource": {
            "name": "webservers",
            "type": "kubernetes"
        }
    },
    "process": {
        "Ext": {
            "ancestry": [
                "MmIxZWI3ZjctYmQ2MS00MzZhLTk4YWYtYzJiMTgyMDQzNDc2LTAtMTMyOTM1NDczMTkuOTk5Mjc0NjAw"
            ],
            "protection": "PsProtectedSignerWinSystem",
            "user": "SYSTEM",
            "architecture": "x86_64",
            "token": {
                "elevation": true,
                "integrity_level_name": "system",
                "domain": "NT AUTHORITY",
                "user": "SYSTEM",
                "elevation_type": "default",
                "sid": "S-1-5-18"
            },
            "memory_region": {
                "region_size": 4096,
                "region_protection": "RWX",
                "allocation_base": 2401471234048,
                "allocation_type": "PRIVATE",
                "bytes_allocation_offset": 0,
                "region_state": "COMMIT",
                "bytes_compressed_present": false,
                "region_start_bytes": "58354f2150254041505b345c505a58353428505e2937434329377d2445494341522d5354414e444152442d414e544956495255532d544553542d46494c452124",
                "allocation_protection": "RW-",
                "region_base": 2401471238144,
                "allocation_size": 8192,
                "bytes_address": 2401471234048
            }
        },
        "parent": {
            "Ext": {
                "protection": "",
                "user": "",
                "architecture": "unknown"
            },
            "name": "System Idle Process",
            "start": "2022-04-04T12:15:41.4606245Z",
            "pid": 0,
            "entity_id": "MmIxZWI3ZjctYmQ2MS00MzZhLTk4YWYtYzJiMTgyMDQzNDc2LTAtMTMyOTM1NDczMTkuOTk5Mjc0NjAw",
            "command_line": "",
            "executable": "",
            "ppid": 0,
            "uptime": 822
        },
        "pe": {},
        "name": "System",
        "start": "2022-04-04T12:15:41.4606245Z",
        "pid": 4,
        "entity_id": "MmIxZWI3ZjctYmQ2MS00MzZhLTk4YWYtYzJiMTgyMDQzNDc2LTQtMTMyOTM1NDczMTkuOTk5Mjc0NjAw",
        "command_line": "",
        "executable": "",
        "thread": {
            "Ext": {
                "call_stack": [
                    {
                        "instruction_pointer": 140705188471348,
                        "memory_section": {
                            "memory_address": 140705187827712,
                            "memory_size": 1163264,
                            "protection": "R-X"
                        },
                        "module_name": "ntdll.dll",
                        "module_path": "c:\\windows\\system32\\ntdll.dll",
                        "symbol_info": "c:\\windows\\system32\\ntdll.dll!NtAlpcSendWaitReceivePort+0x14"
                    },
                    {
                        "instruction_pointer": 140705158956066,
                        "memory_section": {
                            "memory_address": 140705158664192,
                            "memory_size": 921600,
                            "protection": "R-X"
                        },
                        "module_name": "rpcrt4.dll",
                        "module_path": "c:\\windows\\system32\\rpcrt4.dll",
                        "symbol_info": "c:\\windows\\system32\\rpcrt4.dll!0x7FF879048422"
                    },
                    {
                        "instruction_pointer": 140705158944113,
                        "memory_section": {
                            "memory_address": 140705158664192,
                            "memory_size": 921600,
                            "protection": "R-X"
                        },
                        "module_name": "rpcrt4.dll",
                        "module_path": "c:\\windows\\system32\\rpcrt4.dll",
                        "symbol_info": "c:\\windows\\system32\\rpcrt4.dll!0x7FF879045571"
                    },
                    {
                        "instruction_pointer": 140705158854463,
                        "memory_section": {
                            "memory_address": 140705158664192,
                            "memory_size": 921600,
                            "protection": "R-X"
                        },
                        "module_name": "rpcrt4.dll",
                        "module_path": "c:\\windows\\system32\\rpcrt4.dll",
                        "symbol_info": "c:\\windows\\system32\\rpcrt4.dll!0x7FF87902F73F"
                    },
                    {
                        "instruction_pointer": 140705155101013,
                        "memory_section": {
                            "memory_address": 140705154535424,
                            "memory_size": 2334720,
                            "protection": "R-X"
                        },
                        "module_name": "combase.dll",
                        "module_path": "c:\\windows\\system32\\combase.dll",
                        "symbol_info": "c:\\windows\\system32\\combase.dll!0x7FF878C9B155"
                    },
                    {
                        "instruction_pointer": 140705155097096,
                        "memory_section": {
                            "memory_address": 140705154535424,
                            "memory_size": 2334720,
                            "protection": "R-X"
                        },
                        "module_name": "combase.dll",
                        "module_path": "c:\\windows\\system32\\combase.dll",
                        "symbol_info": "c:\\windows\\system32\\combase.dll!0x7FF878C9A208"
                    },
                    {
                        "instruction_pointer": 140705155090820,
                        "memory_section": {
                            "memory_address": 140705154535424,
                            "memory_size": 2334720,
                            "protection": "R-X"
                        },
                        "module_name": "combase.dll",
                        "module_path": "c:\\windows\\system32\\combase.dll",
                        "symbol_info": "c:\\windows\\system32\\combase.dll!0x7FF878C98984"
                    },
                    {
                        "instruction_pointer": 140705155093243,
                        "memory_section": {
                            "memory_address": 140705154535424,
                            "memory_size": 2334720,
                            "protection": "R-X"
                        },
                        "module_name": "combase.dll",
                        "module_path": "c:\\windows\\system32\\combase.dll",
                        "symbol_info": "c:\\windows\\system32\\combase.dll!0x7FF878C992FB"
                    },
                    {
                        "instruction_pointer": 140705155073556,
                        "memory_section": {
                            "memory_address": 140705154535424,
                            "memory_size": 2334720,
                            "protection": "R-X"
                        },
                        "module_name": "combase.dll",
                        "module_path": "c:\\windows\\system32\\combase.dll",
                        "symbol_info": "c:\\windows\\system32\\combase.dll!0x7FF878C94614"
                    },
                    {
                        "instruction_pointer": 140705155277630,
                        "memory_section": {
                            "memory_address": 140705154535424,
                            "memory_size": 2334720,
                            "protection": "R-X"
                        },
                        "module_name": "combase.dll",
                        "module_path": "c:\\windows\\system32\\combase.dll",
                        "symbol_info": "c:\\windows\\system32\\combase.dll!0x7FF878CC633E"
                    },
                    {
                        "instruction_pointer": 140705158666224,
                        "memory_section": {
                            "memory_address": 140705158664192,
                            "memory_size": 921600,
                            "protection": "R-X"
                        },
                        "module_name": "rpcrt4.dll",
                        "module_path": "c:\\windows\\system32\\rpcrt4.dll",
                        "symbol_info": "c:\\windows\\system32\\rpcrt4.dll!0x7FF8790017F0"
                    },
                    {
                        "instruction_pointer": 140705155255496,
                        "memory_section": {
                            "memory_address": 140705154535424,
                            "memory_size": 2334720,
                            "protection": "R-X"
                        },
                        "module_name": "combase.dll",
                        "module_path": "c:\\windows\\system32\\combase.dll",
                        "symbol_info": "c:\\windows\\system32\\combase.dll!0x7FF878CC0CC8"
                    },
                    {
                        "instruction_pointer": 140705155775858,
                        "memory_section": {
                            "memory_address": 140705154535424,
                            "memory_size": 2334720,
                            "protection": "R-X"
                        },
                        "module_name": "combase.dll",
                        "module_path": "c:\\windows\\system32\\combase.dll",
                        "symbol_info": "c:\\windows\\system32\\combase.dll!0x7FF878D3FD72"
                    },
                    {
                        "instruction_pointer": 140704876148243,
                        "memory_section": {
                            "memory_address": 140704875483136,
                            "memory_size": 708608,
                            "protection": "R-X"
                        },
                        "module_name": "fastprox.dll",
                        "module_path": "c:\\windows\\system32\\wbem\\fastprox.dll",
                        "symbol_info": "c:\\windows\\system32\\wbem\\fastprox.dll!0x7FF868293613"
                    },
                    {
                        "instruction_pointer": 140699640718787,
                        "memory_section": {
                            "memory_address": 140699634241536,
                            "memory_size": 9220096,
                            "protection": "R-X"
                        },
                        "module_name": "alertstests.exe",
                        "module_path": "c:\\users\\vagrant\\endpoint-dev\\build\\_ws-vs2019-x64-dbg\\alertstests\\debug\\alertstests.exe",
                        "symbol_info": "c:\\users\\vagrant\\endpoint-dev\\build\\_ws-vs2019-x64-dbg\\alertstests\\debug\\alertstests.exe!0x7FF7301AE5C3"
                    },
                    {
                        "instruction_pointer": 140699640807495,
                        "memory_section": {
                            "memory_address": 140699634241536,
                            "memory_size": 9220096,
                            "protection": "R-X"
                        },
                        "module_name": "alertstests.exe",
                        "module_path": "c:\\users\\vagrant\\endpoint-dev\\build\\_ws-vs2019-x64-dbg\\alertstests\\debug\\alertstests.exe",
                        "symbol_info": "c:\\users\\vagrant\\endpoint-dev\\build\\_ws-vs2019-x64-dbg\\alertstests\\debug\\alertstests.exe!0x7FF7301C4047"
                    },
                    {
                        "instruction_pointer": 140705160001044,
                        "memory_section": {
                            "memory_address": 140705159909376,
                            "memory_size": 520192,
                            "protection": "R-X"
                        },
                        "module_name": "kernel32.dll",
                        "module_path": "c:\\windows\\system32\\kernel32.dll",
                        "symbol_info": "c:\\windows\\system32\\kernel32.dll!BaseThreadInitThunk+0x14"
                    },
                    {
                        "instruction_pointer": 140705188161185,
                        "memory_section": {
                            "memory_address": 140705187827712,
                            "memory_size": 1163264,
                            "protection": "R-X"
                        },
                        "module_name": "ntdll.dll",
                        "module_path": "c:\\windows\\system32\\ntdll.dll",
                        "symbol_info": "c:\\windows\\system32\\ntdll.dll!RtlUserThreadStart+0x21"
                    }
                ],
                "call_stack_final_hook_module": {
                    "code_signature": [
                        {
                            "exists": true,
                            "status": "trusted",
                            "subject_name": "Microsoft Corporation",
                            "trusted": true
                        }
                    ],
                    "hash": {
                        "sha256": "e5bfc1a2967fa513177a0327770927d9a2efa5a4f33ac18f716bae7c3f857994"
                    },
                    "path": "c:\\program files (x86)\\microsoft\\edgewebview\\application\\131.0.2903.112\\msedge_elf.dll"
                },
                "call_stack_final_user_module": {
                    "code_signature": [
                        {
                            "exists": true,
                            "status": "trusted",
                            "subject_name": "Microsoft Windows",
                            "trusted": true
                        }
                    ],
                    "hash": {
                        "sha256": "8c9740e7fe9c97d5782b8d3db102c7880c40f0b27f20d3ec9f334fe0161b7e55"
                    },
                    "name": "rpcrt4.dll",
                    "path": "c:\\windows\\system32\\rpcrt4.dll"
                },
                "call_stack_summary": "ntdll.dll, rpcrt4.dll, combase.dll, rpcrt4.dll, combase.dll, fastprox.dll, alertstests.exe, kernel32.dll, ntdll.dll",
                "hardware_breakpoint_set": true,
                "start_address": 140699640807104,
                "start_address_module": "C:\\Users\\vagrant\\endpoint-dev\\Build\\_WS-vs2019-x64-dbg\\AlertsTests\\Debug\\AlertsTests.exe"
            },
            "id": 5752
        },
        "uptime": 822
    },
    "rule": {
        "ruleset": "production"
    },
    "message": "Malware Prevention Alert",
    "@timestamp": "2022-04-04T12:15:41.5944062Z",
    "file": {
        "Ext": {
            "temp_file_path": "C:\\Windows\\TEMP\\90edbe42-fe6c-4965-8a6b-222aa2b15cf2",
            "code_signature": [
                {
                    "exists": false
                }
            ],
            "quarantine_path": "C:\\.equarantine\\20a65f043449c96f10e538a860a415b55ff46c93",
            "quarantine_message": "Success",
            "quarantine_result": true,
            "malware_classification": {
                "identifier": "endpointpe-v4-model",
                "score": 0.692318737506866,
                "threshold": 0.58,
                "version": "4.0.19000"
            }
        },
        "owner": "Administrators",
        "extension": "dll",
        "drive_letter": "C",
        "created": "2022-04-04T12:15:41.4606245Z",
        "accessed": "2022-04-04T12:15:41.4606245Z",
        "mtime": "2022-04-04T12:15:41.4606245Z",
        "directory": "C:\\sysmon",
        "path": "C:\\sysmon\\9C0E42A47D34240A9A4101CC5D3BC5787DC5AD73DEBF08C09D49337FBE7ACDE4D374924290143DFB2E3210F18E1BCC50EB6C3961D11071E3EC024215B8835E468FA63E53DAE02F32A21E03CE65412F6E56942DAA.dll",
        "code_signature": {
            "exists": false
        },
        "size": 4608,
        "pe": {
            "file_version": "0.0.0.0",
            "description": " ",
            "original_file_name": "5t5mpwxc.dll",
            "Ext": {
                "dotnet": true,
                "streams": [
                    {
                        "name": "#~",
                        "hash": {
                            "md5": "debf08c09d49337fbe7acde4d3749242",
                            "sha256": "90143dfb2e3210f18e1bcc50eb6c3961d11071e3ec024215b8835e468fa63e53"
                        }
                    },
                    {
                        "name": "#Blob",
                        "hash": {
                            "md5": "debf08c09d49337fbe7acde4d3749242",
                            "sha256": "90143dfb2e3210f18e1bcc50eb6c3961d11071e3ec024215b8835e468fa63e53"
                        }
                    }
                ],
                "sections": [
                    {
                        "name": ".reloc",
                        "hash": {
                            "md5": "debf08c09d49337fbe7acde4d3749242",
                            "sha256": "90143dfb2e3210f18e1bcc50eb6c3961d11071e3ec024215b8835e468fa63e53"
                        }
                    }
                ]
            }
        },
        "name": "9C0E42A47D34240A9A4101CC5D3BC5787DC5AD73DEBF08C09D49337FBE7ACDE4D374924290143DFB2E3210F18E1BCC50EB6C3961D11071E3EC024215B8835E468FA63E53DAE02F32A21E03CE65412F6E56942DAA.dll",
        "hash": {
            "sha1": "9c0e42a47d34240a9a4101cc5d3bc5787dc5ad73",
            "sha256": "90143dfb2e3210f18e1bcc50eb6c3961d11071e3ec024215b8835e468fa63e53",
            "md5": "debf08c09d49337fbe7acde4d3749242"
        }
    },
    "Endpoint": {
        "policy": {
            "applied": {
                "artifacts": {
                    "global": {
                        "identifiers": [
                            {
                                "sha256": "e57a7d5638060e9655c64ac1d02f7949b87e5f5f27f2074329608db1e06d645b",
                                "name": "diagnostic-configuration-v1"
                            },
                            {
                                "sha256": "c33693fcadb720d4d37706cd2ca77b28a8c59a424ab3f251b2b07ac7975eb2f4",
                                "name": "diagnostic-endpointpe-v4-blocklist"
                            },
                            {
                                "sha256": "d47bfd600e3a8f79e290dfb0306e8abe7be11b75b36ba98132f46b8971f7f071",
                                "name": "diagnostic-endpointpe-v4-exceptionlist"
                            },
                            {
                                "sha256": "8609faa372f8761bf199a03325f56577d2fd47630d6dba386b6eb33562aef6e3",
                                "name": "diagnostic-endpointpe-v4-model"
                            },
                            {
                                "sha256": "52bc8b59292b5017bb091f97fa395881b127b07dec6182f91c4b84074ae6e7bc",
                                "name": "diagnostic-malware-signature-v1-windows"
                            },
                            {
                                "sha256": "dcbaa744fc672d8db32010a1422aafa6e0cf86816d34b1d4df9f273f106be425",
                                "name": "diagnostic-ransomware-v1-windows"
                            },
                            {
                                "sha256": "b680beed0f3ca83ae78802e972bf4bb12ecea2b1649a7aafd16e6fec8c9a0ede",
                                "name": "diagnostic-rules-windows-v1"
                            },
                            {
                                "sha256": "1d591a12ce8ae215ebdcdabc81fc912cd51162e7a8e35bcdc1676bc3125cebbf",
                                "name": "endpointpe-v4-blocklist"
                            },
                            {
                                "sha256": "d784c2aa70a2216dd5bfeecfdd67a83ff5b656e9321bd70cf345a8667a63fb2e",
                                "name": "endpointpe-v4-exceptionlist"
                            },
                            {
                                "sha256": "c05c025cce1c2b5808c180dc4986eb519c0affd30d7c27f67fdd14bde3224638",
                                "name": "endpointpe-v4-model"
                            },
                            {
                                "sha256": "b98dc812e3cd9c9aa21462bb8b2bac86158d6d2d97ea4aac6731c069f6babb4d",
                                "name": "global-configuration-v1"
                            },
                            {
                                "sha256": "7acbe147698a40c817775d471ea30c2fe4dfa7a9f54271e6dbc073131c5a3bcb",
                                "name": "global-exceptionlist-windows"
                            },
                            {
                                "sha256": "dfb2b428357b756d9f5b593c02dce99b026c9e2afeb76cdb8e8c76c6db78290a",
                                "name": "global-trustlist-windows-v1"
                            },
                            {
                                "sha256": "611a02c398c58ebe2f6d9d63621778de96263ef7fa885098ce62a22c411d67bc",
                                "name": "production-malware-signature-v1-windows"
                            },
                            {
                                "sha256": "363cb9d7bbc013d9bc171a6a29fdfe486f1c987ef2c0cdfa3c283fc4c5a4a595",
                                "name": "production-ransomware-v1-windows"
                            },
                            {
                                "sha256": "b07cf3beacd69e6922d344448a8c6d03e96ae6d5ec1e540415fe2f4804bcb631",
                                "name": "production-rules-windows-v1"
                            }
                        ],
                        "update_age": 0,
                        "snapshot": "2023-09-26",
                        "version": "1.0.260"
                    },
                    "user": {
                        "identifiers": [
                            {
                                "sha256": "d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                                "name": "endpoint-blocklist-windows-v1"
                            },
                            {
                                "sha256": "d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                                "name": "endpoint-eventfilterlist-windows-v1"
                            },
                            {
                                "sha256": "d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                                "name": "endpoint-exceptionlist-windows-v1"
                            },
                            {
                                "sha256": "d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                                "name": "endpoint-hostisolationexceptionlist-windows-v1"
                            },
                            {
                                "sha256": "d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                                "name": "endpoint-trustlist-windows-v1"
                            }
                        ],
                        "version": "1.0.0"
                    }
                }
            }
        }
    },
    "ecs": {
        "version": "1.11.0"
    },
    "data_stream": {
        "namespace": "default",
        "type": "logs",
        "dataset": "endpoint.alerts"
    },
    "elastic": {
        "agent": {
            "id": "2b1eb7f7-bd61-436a-98af-c2b182043476"
        }
    },
    "host": {
        "hostname": "security-win-1",
        "os": {
            "Ext": {
                "variant": "Windows Server 2019 Datacenter"
            },
            "kernel": "1809 (10.0.17763.2686)",
            "name": "Windows",
            "family": "windows",
            "type": "windows",
            "version": "1809 (10.0.17763.2686)",
            "platform": "windows",
            "full": "Windows Server 2019 Datacenter 1809 (10.0.17763.2686)"
        },
        "ip": [
            "10.201.0.34",
            "fe80::4850:4f4f:4b53:8103",
            "127.0.0.1",
            "::1"
        ],
        "name": "security-win-1",
        "id": "bbea673e-eae6-4b03-8724-2183f79da331",
        "mac": [
            "00-00-5E-00-53-23"
        ],
        "architecture": "x86_64"
    },
    "event": {
        "severity": 73,
        "code": "malicious_file",
        "risk_score": 73,
        "created": "2022-04-04T12:15:41.5944062Z",
        "kind": "alert",
        "module": "endpoint",
        "type": [
            "info",
            "change",
            "denied"
        ],
        "agent_id_status": "verified",
        "sequence": 29414,
        "ingested": "2022-04-04T12:19:33Z",
        "action": "rename",
        "id": "MYfSjQEEEFe1o09b+++++D5Q",
        "category": [
            "malware",
            "intrusion_detection",
            "file"
        ],
        "dataset": "endpoint.alerts",
        "outcome": "success"
    },
    "user": {
        "domain": "NT AUTHORITY",
        "name": "SYSTEM"
    },
    "Memory_protection": {
        "cross_session": false,
        "feature": "shellcode_thread",
        "parent_to_child": false,
        "self_injection": false,
        "unique_key_v2": "00633d00b651c48e61a94589db67e00fd454a5a905409e38de4e48c183105f67"
    },
    "Responses": [
        {
            "@timestamp": "2023-04-13T16:15:16.0Z",
            "action": {
                "action": "file_rollback",
                "file": {
                    "attributes": [
                        "invalid"
                    ],
                    "path": "",
                    "reason": 2147484160
                },
                "source": {
                    "attributes": [
                        "archive"
                    ],
                    "path": "\\\\?\\GLOBALROOT\\Device\\HarddiskVolumeShadowCopy55\\git\\endpoint-dev\\Python\\runtime\\failed_test_logs\\20230413_181248\\EndpointRollbackTestCase\\test_rollback_trigger_malware_1_prevent\\tmp\\TRA14KA5Z2\\ExceptionlistTester-Windows.1d1phoq97d"
                }
            },
            "message": "Successful production rollback",
            "result": 0
        },
        {
            "@timestamp": "2023-04-13T16:15:16.0Z",
            "action": {
                "action": "registry_rollback",
                "key": {
                    "actions": [
                        "Deleted"
                    ],
                    "path": "\\REGISTRY\\MACHINE\\SOFTWARE\\WOW6432Node\\TestRollback\\1"
                }
            },
            "message": "Successful production registry rollback",
            "result": 0
        },
        {
            "@timestamp": "2023-04-13T16:15:16.0Z",
            "action": {
                "action": "registry_rollback",
                "key": {
                    "actions": [
                        "Modified"
                    ],
                    "path": "\\REGISTRY\\MACHINE\\SOFTWARE\\WOW6432Node\\TestRollback.valuetest",
                    "values": [
                        {
                            "actions": [
                                "Deleted"
                            ],
                            "name": "SomeValue"
                        }
                    ]
                }
            }
        },
        {
            "@timestamp": "2023-07-19T14:21:05.0Z",
            "action": {
                "action": "process_rollback",
                "process": {
                    "path": "C:\\Users\\Pawel Mirski\\AppData\\Local\\Programs\\Python\\Python38-32\\python.exe"
                }
            },
            "message": "Successful production process rollback",
            "result": 0
        }
    ]
}
```
</details>

### [Fields](alerts.md)
- [@timestamp](alerts.md#@timestamp)
- [Events](alerts.md#Events)
- [message](alerts.md#message)
- [Endpoint](alerts.md#Endpoint)
- [Memory_protection](alerts.md#Memory_protection)
- [Ransomware](alerts.md#Ransomware)
- [Responses](alerts.md#Responses)
- [Target](alerts.md#Target)
- [agent](alerts.md#agent)
- [cloud](alerts.md#cloud)
- [container](alerts.md#container)
- [data_stream](alerts.md#data_stream)
- [destination](alerts.md#destination)
- [dll](alerts.md#dll)
- [dns](alerts.md#dns)
- [ecs](alerts.md#ecs)
- [elastic](alerts.md#elastic)
- [event](alerts.md#event)
- [file](alerts.md#file)
- [group](alerts.md#group)
- [host](alerts.md#host)
- [orchestrator](alerts.md#orchestrator)
- [process](alerts.md#process)
- [registry](alerts.md#registry)
- [rule](alerts.md#rule)
- [source](alerts.md#source)
- [threat](alerts.md#threat)
- [user](alerts.md#user)
# policy
### Sample Event
<details>
<summary>
Click to expand
</summary>

```json
{
    "agent": {
        "build": {
            "original": "version: 8.3.0-SNAPSHOT, compiled: Fri Apr 1 06:00:00 2022, branch: main, commit: f8b0ed879ad40ee1ae561ced31ec8a4027a2bf53"
        },
        "id": "4c9c9cb3-f80f-44d8-9c89-6168243b7f21",
        "type": "endpoint",
        "version": "8.3.0-SNAPSHOT"
    },
    "message": "Endpoint policy change",
    "@timestamp": "2022-04-04T18:38:15.7178887Z",
    "Endpoint": {
        "configuration": {
            "isolation": false
        },
        "state": {
            "isolation": false
        },
        "policy": {
            "applied": {
                "response": {
                    "configurations": {
                        "behavior_protection": {
                            "concerned_actions": [
                                "agent_connectivity",
                                "load_config",
                                "workflow",
                                "download_global_artifacts",
                                "download_user_artifacts",
                                "configure_file_events",
                                "configure_network_events",
                                "configure_process_events",
                                "configure_kernel",
                                "connect_kernel",
                                "configure_imageload_events",
                                "configure_dns_events",
                                "configure_security_events",
                                "configure_registry_events",
                                "configure_malicious_behavior"
                            ],
                            "status": "success"
                        },
                        "streaming": {
                            "concerned_actions": [
                                "agent_connectivity",
                                "load_config",
                                "configure_output",
                                "workflow"
                            ],
                            "status": "success"
                        },
                        "malware": {
                            "concerned_actions": [
                                "agent_connectivity",
                                "load_config",
                                "workflow",
                                "download_global_artifacts",
                                "download_user_artifacts",
                                "configure_malware",
                                "configure_kernel",
                                "detect_process_events",
                                "detect_file_write_events",
                                "connect_kernel",
                                "configure_user_notification",
                                "configure_alerts",
                                "detect_file_open_events",
                                "detect_sync_image_load_events"
                            ],
                            "status": "success"
                        },
                        "logging": {
                            "concerned_actions": [
                                "agent_connectivity",
                                "load_config",
                                "configure_logging",
                                "workflow"
                            ],
                            "status": "success"
                        },
                        "antivirus_registration": {
                            "concerned_actions": [
                                "agent_connectivity",
                                "load_config",
                                "configure_antivirus_registration",
                                "workflow"
                            ],
                            "status": "unsupported"
                        },
                        "host_isolation": {
                            "concerned_actions": [
                                "agent_connectivity",
                                "configure_host_isolation",
                                "load_config",
                                "workflow",
                                "connect_kernel",
                                "configure_user_notification"
                            ],
                            "status": "success"
                        },
                        "events": {
                            "concerned_actions": [
                                "agent_connectivity",
                                "load_config",
                                "workflow",
                                "download_global_artifacts",
                                "download_user_artifacts",
                                "detect_process_events",
                                "detect_file_write_events",
                                "detect_network_events",
                                "configure_file_events",
                                "configure_network_events",
                                "configure_process_events",
                                "configure_kernel",
                                "connect_kernel",
                                "detect_file_open_events",
                                "detect_file_access_events",
                                "detect_async_image_load_events",
                                "detect_registry_events",
                                "detect_registry_access_events",
                                "configure_imageload_events",
                                "configure_dns_events",
                                "configure_security_events",
                                "configure_registry_events"
                            ],
                            "status": "success"
                        },
                        "ransomware": {
                            "concerned_actions": [
                                "agent_connectivity",
                                "load_config",
                                "workflow",
                                "download_global_artifacts",
                                "download_user_artifacts",
                                "detect_process_events",
                                "detect_file_write_events",
                                "configure_process_events",
                                "configure_file_events",
                                "configure_ransomware",
                                "configure_kernel",
                                "connect_kernel",
                                "configure_user_notification"
                            ],
                            "status": "success"
                        },
                        "memory_protection": {
                            "concerned_actions": [
                                "agent_connectivity",
                                "configure_memory_threat",
                                "configure_process_events",
                                "download_global_artifacts",
                                "download_user_artifacts",
                                "workflow",
                                "load_config",
                                "detect_process_events",
                                "configure_kernel",
                                "connect_kernel",
                                "detect_thread_events"
                            ],
                            "status": "success"
                        },
                        "attack_surface_reduction": {
                            "concerned_actions": [
                                "agent_connectivity",
                                "configure_credential_hardening",
                                "download_global_artifacts",
                                "download_user_artifacts",
                                "workflow",
                                "load_config",
                                "configure_kernel",
                                "connect_kernel"
                            ],
                            "status": "success"
                        }
                    },
                    "diagnostic": {
                        "behavior_protection": {
                            "concerned_actions": [
                                "load_config",
                                "workflow",
                                "download_global_artifacts",
                                "download_user_artifacts",
                                "configure_file_events",
                                "configure_network_events",
                                "configure_process_events",
                                "configure_kernel",
                                "connect_kernel",
                                "configure_imageload_events",
                                "configure_dns_events",
                                "configure_security_events",
                                "configure_registry_events",
                                "configure_diagnostic_rollback",
                                "detect_process_handle_events",
                                "configure_diagnostic_malicious_behavior"
                            ],
                            "status": "success"
                        },
                        "malware": {
                            "concerned_actions": [
                                "load_config",
                                "workflow",
                                "download_global_artifacts",
                                "download_user_artifacts",
                                "configure_diagnostic_malware",
                                "detect_process_events",
                                "detect_file_write_events",
                                "connect_kernel",
                                "configure_kernel",
                                "detect_file_open_events",
                                "detect_sync_image_load_events",
                                "configure_diagnostic_rollback"
                            ],
                            "status": "success"
                        },
                        "ransomware": {
                            "concerned_actions": [
                                "load_config",
                                "workflow",
                                "download_global_artifacts",
                                "download_user_artifacts",
                                "detect_process_events",
                                "detect_file_write_events",
                                "configure_process_events",
                                "configure_file_events",
                                "configure_diagnostic_ransomware",
                                "configure_kernel",
                                "connect_kernel",
                                "configure_diagnostic_rollback"
                            ],
                            "status": "success"
                        },
                        "memory_protection": {
                            "concerned_actions": [
                                "load_config",
                                "workflow",
                                "download_global_artifacts",
                                "download_user_artifacts",
                                "detect_process_events",
                                "configure_process_events",
                                "configure_diagnostic_memory_threat",
                                "configure_kernel",
                                "connect_kernel",
                                "detect_thread_events",
                                "configure_diagnostic_rollback"
                            ],
                            "status": "success"
                        }
                    }
                },
                "name": "endpoint-1",
                "id": "b372bc3f-e9b3-4b2d-9dfe-ae677ed83933",
                "actions": [
                    {
                        "name": "configure_antivirus_registration",
                        "message": "Antivirus registration is not possible on servers",
                        "status": "unsupported"
                    },
                    {
                        "name": "configure_ransomware",
                        "message": "Successfully enabled ransomware prevention with mbr enabled and canaries enabled",
                        "status": "success"
                    },
                    {
                        "name": "configure_memory_threat",
                        "message": "Successfully enabled memory threat prevention with memory scanning enabled and shellcode protection enabled including trampoline monitoring",
                        "status": "success"
                    },
                    {
                        "name": "configure_diagnostic_memory_threat",
                        "message": "Successfully enabled memory threat detection with memory scanning enabled and shellcode protection enabled including trampoline monitoring",
                        "status": "success"
                    },
                    {
                        "name": "configure_host_isolation",
                        "message": "Host is not isolated",
                        "status": "success"
                    },
                    {
                        "name": "configure_malicious_behavior",
                        "message": "Enabled 152 out of 152 malicious behavior rules",
                        "status": "success"
                    },
                    {
                        "name": "configure_diagnostic_malicious_behavior",
                        "message": "Enabled 196 out of 196 diagnostic malicious behavior rules",
                        "status": "success"
                    },
                    {
                        "name": "configure_user_notification",
                        "message": "Successfully configured user notification",
                        "status": "success"
                    },
                    {
                        "name": "configure_malware",
                        "message": "Successfully enabled malware prevention",
                        "status": "success"
                    },
                    {
                        "name": "configure_diagnostic_malware",
                        "message": "Successfully enabled malware detection",
                        "status": "success"
                    },
                    {
                        "name": "configure_diagnostic_rollback",
                        "message": "Diagnostic system rollback is enabled",
                        "status": "success"
                    },
                    {
                        "name": "configure_kernel",
                        "message": "Successfully configured kernel",
                        "status": "success"
                    },
                    {
                        "name": "configure_output",
                        "message": "Successfully configured output connection",
                        "status": "success"
                    },
                    {
                        "name": "configure_alerts",
                        "message": "Successfully configured alerts",
                        "status": "success"
                    },
                    {
                        "name": "configure_logging",
                        "message": "Successfully configured logging",
                        "status": "success"
                    },
                    {
                        "name": "load_config",
                        "message": "Successfully parsed configuration",
                        "status": "success"
                    },
                    {
                        "name": "download_user_artifacts",
                        "message": "Successfully downloaded user artifacts",
                        "status": "success"
                    },
                    {
                        "name": "download_global_artifacts",
                        "message": "Global artifacts are available for use",
                        "status": "success"
                    },
                    {
                        "name": "connect_kernel",
                        "message": "Successfully connected to kernel",
                        "status": "success"
                    },
                    {
                        "name": "detect_process_events",
                        "message": "Successfully started process event reporting",
                        "status": "success"
                    },
                    {
                        "name": "detect_sync_image_load_events",
                        "message": "Successfully started sync image load event reporting",
                        "status": "success"
                    },
                    {
                        "name": "detect_async_image_load_events",
                        "message": "Successfully started async image load event reporting",
                        "status": "success"
                    },
                    {
                        "name": "detect_file_write_events",
                        "message": "Successfully started file write event reporting",
                        "status": "success"
                    },
                    {
                        "name": "detect_file_open_events",
                        "message": "Successfully stopped file open event reporting",
                        "status": "success"
                    },
                    {
                        "name": "detect_network_events",
                        "message": "Successfully started network event reporting",
                        "status": "success"
                    },
                    {
                        "name": "detect_registry_events",
                        "message": "Successfully started registry event reporting",
                        "status": "success"
                    },
                    {
                        "name": "detect_thread_events",
                        "message": "Successfully configured thread events",
                        "status": "success"
                    },
                    {
                        "name": "detect_file_access_events",
                        "message": "Successfully configured file access event reporting",
                        "status": "success"
                    },
                    {
                        "name": "detect_registry_access_events",
                        "message": "Successfully configured registry access event reporting",
                        "status": "success"
                    },
                    {
                        "name": "detect_process_handle_events",
                        "message": "Successfully started process handle event reporting",
                        "status": "success"
                    },
                    {
                        "name": "configure_file_events",
                        "message": "Success enabling file events; current state is enabled",
                        "status": "success"
                    },
                    {
                        "name": "configure_network_events",
                        "message": "Success enabling network events; current state is enabled",
                        "status": "success"
                    },
                    {
                        "name": "configure_process_events",
                        "message": "Success enabling process events; current state is enabled",
                        "status": "success"
                    },
                    {
                        "name": "configure_imageload_events",
                        "message": "Success enabling image load events; current state is enabled",
                        "status": "success"
                    },
                    {
                        "name": "configure_dns_events",
                        "message": "Success enabling dns events; current state is enabled",
                        "status": "success"
                    },
                    {
                        "name": "configure_registry_events",
                        "message": "Success enabling registry events; current state is enabled",
                        "status": "success"
                    },
                    {
                        "name": "configure_security_events",
                        "message": "Success enabling security events; current state is enabled",
                        "status": "success"
                    },
                    {
                        "name": "configure_diagnostic_ransomware",
                        "message": "Successfully enabled ransomware detection with mbr enabled and canaries enabled",
                        "status": "success"
                    },
                    {
                        "name": "agent_connectivity",
                        "message": "Successfully connected to Agent",
                        "status": "success"
                    },
                    {
                        "name": "workflow",
                        "message": "Successfully executed all workflows",
                        "status": "success"
                    },
                    {
                        "name": "configure_credential_hardening",
                        "message": "Successfully configured credential hardening",
                        "status": "success"
                    }
                ],
                "endpoint_policy_version": "1",
                "version": "2",
                "artifacts": {
                    "global": {
                        "channel": "stable",
                        "identifiers": [
                            {
                                "sha256": "e57a7d5638060e9655c64ac1d02f7949b87e5f5f27f2074329608db1e06d645b",
                                "name": "diagnostic-configuration-v1"
                            },
                            {
                                "sha256": "c33693fcadb720d4d37706cd2ca77b28a8c59a424ab3f251b2b07ac7975eb2f4",
                                "name": "diagnostic-endpointpe-v4-blocklist"
                            },
                            {
                                "sha256": "d47bfd600e3a8f79e290dfb0306e8abe7be11b75b36ba98132f46b8971f7f071",
                                "name": "diagnostic-endpointpe-v4-exceptionlist"
                            },
                            {
                                "sha256": "8609faa372f8761bf199a03325f56577d2fd47630d6dba386b6eb33562aef6e3",
                                "name": "diagnostic-endpointpe-v4-model"
                            },
                            {
                                "sha256": "52bc8b59292b5017bb091f97fa395881b127b07dec6182f91c4b84074ae6e7bc",
                                "name": "diagnostic-malware-signature-v1-windows"
                            },
                            {
                                "sha256": "dcbaa744fc672d8db32010a1422aafa6e0cf86816d34b1d4df9f273f106be425",
                                "name": "diagnostic-ransomware-v1-windows"
                            },
                            {
                                "sha256": "b680beed0f3ca83ae78802e972bf4bb12ecea2b1649a7aafd16e6fec8c9a0ede",
                                "name": "diagnostic-rules-windows-v1"
                            },
                            {
                                "sha256": "1d591a12ce8ae215ebdcdabc81fc912cd51162e7a8e35bcdc1676bc3125cebbf",
                                "name": "endpointpe-v4-blocklist"
                            },
                            {
                                "sha256": "b49fdcd8bf63af07ab1e74352137eb20f1e3710640dfcb1bfff3f7273ee14a7f",
                                "name": "endpointpe-v4-exceptionlist"
                            },
                            {
                                "sha256": "c05c025cce1c2b5808c180dc4986eb519c0affd30d7c27f67fdd14bde3224638",
                                "name": "endpointpe-v4-model"
                            },
                            {
                                "sha256": "b98dc812e3cd9c9aa21462bb8b2bac86158d6d2d97ea4aac6731c069f6babb4d",
                                "name": "global-configuration-v1"
                            },
                            {
                                "sha256": "7acbe147698a40c817775d471ea30c2fe4dfa7a9f54271e6dbc073131c5a3bcb",
                                "name": "global-exceptionlist-windows"
                            },
                            {
                                "sha256": "dfb2b428357b756d9f5b593c02dce99b026c9e2afeb76cdb8e8c76c6db78290a",
                                "name": "global-trustlist-windows-v1"
                            },
                            {
                                "sha256": "611a02c398c58ebe2f6d9d63621778de96263ef7fa885098ce62a22c411d67bc",
                                "name": "production-malware-signature-v1-windows"
                            },
                            {
                                "sha256": "363cb9d7bbc013d9bc171a6a29fdfe486f1c987ef2c0cdfa3c283fc4c5a4a595",
                                "name": "production-ransomware-v1-windows"
                            },
                            {
                                "sha256": "b07cf3beacd69e6922d344448a8c6d03e96ae6d5ec1e540415fe2f4804bcb631",
                                "name": "production-rules-windows-v1"
                            }
                        ],
                        "update_age": 0,
                        "snapshot": "2023-09-26",
                        "version": "1.0.261"
                    },
                    "user": {
                        "identifiers": [
                            {
                                "sha256": "d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                                "name": "endpoint-blocklist-windows-v1"
                            },
                            {
                                "sha256": "d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                                "name": "endpoint-eventfilterlist-windows-v1"
                            },
                            {
                                "sha256": "d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                                "name": "endpoint-exceptionlist-windows-v1"
                            },
                            {
                                "sha256": "d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                                "name": "endpoint-hostisolationexceptionlist-windows-v1"
                            },
                            {
                                "sha256": "d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                                "name": "endpoint-trustlist-windows-v1"
                            }
                        ],
                        "version": "1.0.0"
                    }
                },
                "status": "success"
            }
        }
    },
    "ecs": {
        "version": "1.11.0"
    },
    "data_stream": {
        "namespace": "default",
        "type": "metrics",
        "dataset": "endpoint.policy"
    },
    "host": {
        "hostname": "data-viz-win-1",
        "os": {
            "Ext": {
                "variant": "Windows Server 2019 Datacenter"
            },
            "kernel": "1809 (10.0.17763.2686)",
            "name": "Windows",
            "family": "windows",
            "type": "windows",
            "version": "1809 (10.0.17763.2686)",
            "platform": "windows",
            "full": "Windows Server 2019 Datacenter 1809 (10.0.17763.2686)"
        },
        "ip": [
            "10.201.0.13",
            "fe80::f40a:aed0:618a:972d",
            "127.0.0.1",
            "::1"
        ],
        "name": "data-viz-win-1",
        "id": "2beebb8e-e5f0-46ca-8635-97ba7bb8ccca",
        "mac": [
            "00-00-5E-00-53-23"
        ],
        "architecture": "x86_64"
    },
    "event": {
        "agent_id_status": "verified",
        "sequence": 35122,
        "ingested": "2022-04-04T18:38:16Z",
        "created": "2022-04-04T18:38:15.7178887Z",
        "kind": "state",
        "module": "endpoint",
        "action": "endpoint_policy_response",
        "id": "MYfZG00oEwD2/fqT+++++Bye",
        "category": [
            "host"
        ],
        "type": [
            "change"
        ],
        "dataset": "endpoint.policy"
    }
}
```
</details>

### [Fields](policy.md)
- [@timestamp](policy.md#@timestamp)
- [message](policy.md#message)
- [Endpoint](policy.md#Endpoint)
- [agent](policy.md#agent)
- [data_stream](policy.md#data_stream)
- [ecs](policy.md#ecs)
- [event](policy.md#event)
- [host](policy.md#host)
# registry
### Sample Event
<details>
<summary>
Click to expand
</summary>

```json
{
    "registry": {
        "hive": "HKLM",
        "path": "HKLM\\SYSTEM\\ControlSet001\\Control\\Lsa\\FipsAlgorithmPolicy\\Enabled",
        "data": {
            "strings": [],
            "type": "REG_NONE"
        },
        "value": "Enabled",
        "key": "SYSTEM\\ControlSet001\\Control\\Lsa\\FipsAlgorithmPolicy"
    },
    "agent": {
        "id": "4c9c9cb3-f80f-44d8-9c89-6168243b7f21",
        "type": "endpoint",
        "version": "8.3.0-SNAPSHOT"
    },
    "Effective_process": {
        "entity_id": "YWFhYWFhYWEtYWFhYS1hYWFhLWFhYWEtYWFhYWFhYWFhYWFhLTI3MzItMTMyOTk3MDczNDEuMjUyNTI3NDAw",
        "executable": "C:\\Windows\\System32\\wbem\\WMIC.exe",
        "name": "WMIC.exe",
        "pid": 2732
    },
    "process": {
        "Ext": {
            "ancestry": [
                "NGM5YzljYjMtZjgwZi00NGQ4LTljODktNjE2ODI0M2I3ZjIxLTYwMC0xMzI5MzU0OTExMC40NjgyMjI3MDA=",
                "NGM5YzljYjMtZjgwZi00NGQ4LTljODktNjE2ODI0M2I3ZjIxLTQ3Mi0xMzI5MzU0OTExMC4xNzIwMjY5MDA="
            ],
            "code_signature": [
                {
                    "trusted": true,
                    "subject_name": "Microsoft Windows Publisher",
                    "exists": true,
                    "status": "trusted"
                }
            ]
        },
        "code_signature": {
            "trusted": true,
            "subject_name": "Microsoft Windows Publisher",
            "exists": true,
            "status": "trusted"
        },
        "name": "svchost.exe",
        "pid": 2772,
        "entity_id": "NGM5YzljYjMtZjgwZi00NGQ4LTljODktNjE2ODI0M2I3ZjIxLTI3NzItMTMyOTM1NzE5ODguNjU3ODk4NjAw",
        "executable": "C:\\Windows\\System32\\svchost.exe",
        "thread": {
            "id": 340,
            "Ext": {
                "call_stack": [
                    {
                        "allocation_private_bytes": 16384,
                        "callsite_leading_bytes": "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
                        "callsite_trailing_bytes": "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
                        "protection": "RWX",
                        "symbol_info": "C:\\Windows\\System32\\ntdll.dll!RtlUserThreadStart+0x21"
                    }
                ],
                "call_stack_summary": "ntdll.dll|kernelbase.dll|kernel32.dll|cmd.exe|kernel32.dll|ntdll.dll",
                "hardware_breakpoint_set": true
            }
        }
    },
    "message": "Endpoint registry event",
    "@timestamp": "2022-04-04T18:53:09.1283846Z",
    "ecs": {
        "version": "1.11.0"
    },
    "data_stream": {
        "namespace": "default",
        "type": "logs",
        "dataset": "endpoint.events.registry"
    },
    "host": {
        "hostname": "data-viz-win-1",
        "os": {
            "Ext": {
                "variant": "Windows Server 2019 Datacenter"
            },
            "kernel": "1809 (10.0.17763.2686)",
            "name": "Windows",
            "family": "windows",
            "type": "windows",
            "version": "1809 (10.0.17763.2686)",
            "platform": "windows",
            "full": "Windows Server 2019 Datacenter 1809 (10.0.17763.2686)"
        },
        "ip": [
            "10.201.0.13",
            "fe80::f40a:aed0:618a:972d",
            "127.0.0.1",
            "::1"
        ],
        "name": "data-viz-win-1",
        "id": "2beebb8e-e5f0-46ca-8635-97ba7bb8ccca",
        "mac": [
            "00-00-5E-00-53-23"
        ],
        "architecture": "x86_64"
    },
    "event": {
        "agent_id_status": "verified",
        "sequence": 36271,
        "ingested": "2022-04-04T18:53:18Z",
        "created": "2022-04-04T18:53:09.1283846Z",
        "kind": "event",
        "module": "endpoint",
        "action": "query",
        "id": "MYfZG00oEwD2/fqT+++++CMy",
        "category": [
            "registry"
        ],
        "type": [
            "access"
        ],
        "dataset": "endpoint.events.registry"
    },
    "user": {
        "domain": "NT AUTHORITY",
        "name": "SYSTEM",
        "id": "S-1-5-18"
    }
}
```
</details>

### [Fields](registry.md)
- [@timestamp](registry.md#@timestamp)
- [message](registry.md#message)
- [Effective_process](registry.md#Effective_process)
- [agent](registry.md#agent)
- [data_stream](registry.md#data_stream)
- [destination](registry.md#destination)
- [ecs](registry.md#ecs)
- [event](registry.md#event)
- [group](registry.md#group)
- [host](registry.md#host)
- [process](registry.md#process)
- [registry](registry.md#registry)
- [source](registry.md#source)
- [user](registry.md#user)
# process
### Sample Event
<details>
<summary>
Click to expand
</summary>

```json
{
    "agent": {
        "id": "4c9c9cb3-f80f-44d8-9c89-6168243b7f21",
        "type": "endpoint",
        "version": "8.3.0-SNAPSHOT"
    },
    "container": {
        "id": "8d38b2f18290e973c5ea8f9ee207e970a8aa9191fa89bf3d4ea2a126f2f010a6",
        "image": {
            "name": "gke.gcr.io/csi-node-driver-registrar:v2.5.0-gke.1",
            "tag": [
                "v2.5.0-gke.1"
            ],
            "hash": {
                "all": [
                    "sha256:f7988fb6c02e0ce69257d9bd9cf37ae20a60f1df7563c3a2a6abe24160306b8d"
                ]
            }
        },
        "name": "csi-driver-registrar"
    },
    "cloud": {
        "account": {
            "id": "1234"
        },
        "instance": {
            "name": "webserver-12"
        },
        "project": {
            "id": "1234"
        },
        "provider": "aws",
        "region": "us-east-1"
    },
    "orchestrator": {
        "cluster": {
            "id": "f0cd61d5-327b-43e0-bc94-d9ea922fb4b5",
            "name": "webservers"
        },
        "namespace": "webapp",
        "resource": {
            "ip": [
                "10.1.237.155"
            ],
            "name": "pdcsi-node-6zh4j",
            "type": "pod",
            "parent": {
                "type": "DaemonSet"
            }
        }
    },
    "process": {
        "entry_leader": {
            "attested_user": {
                "id": "123",
                "name": "userA"
            },
            "attested_groups": {
                "name": "groupA"
            }
        },
        "Ext": {
            "ancestry": [
                "NGM5YzljYjMtZjgwZi00NGQ4LTljODktNjE2ODI0M2I3ZjIxLTYwMC0xMzI5MzU0OTExMC40NjgyMjI3MDA=",
                "NGM5YzljYjMtZjgwZi00NGQ4LTljODktNjE2ODI0M2I3ZjIxLTQ3Mi0xMzI5MzU0OTExMC4xNzIwMjY5MDA="
            ],
            "memfd": {
                "flag_hugetlb": false,
                "flag_allow_seal": true,
                "flags": 2,
                "name": "test_memfd",
                "flag_exec": false,
                "flag_cloexec": false,
                "flag_noexec_seal": false
            },
            "code_signature": [
                {
                    "trusted": true,
                    "subject_name": "Microsoft Windows Publisher",
                    "exists": true,
                    "status": "trusted"
                }
            ],
            "created_suspended": true,
            "mitigation_policies": [
                "Microsoft only, Opt-in to restrict to Microsoft, Windows Store and WHQL",
                "CET dynamic APIs can only be called out of proc",
                "CF Guard"
            ],
            "protection": "PsProtectedSignerAntimalware-Light",
            "device": {
                "volume_device_type": "Disk File System"
            },
            "authentication_id": "0x3e7",
            "token": {
                "integrity_level_name": "system",
                "security_attributes": [
                    "TSA://ProcUnique"
                ],
                "elevation_level": "default"
            },
            "effective_parent": {
                "entity_id": "YWFhYWFhYWEtYWFhYS1hYWFhLWFhYWEtYWFhYWFhYWFhYWFhLTI3MzItMTMyOTk3MDczNDEuMjUyNTI3NDAw",
                "executable": "C:\\Windows\\System32\\wbem\\WMIC.exe",
                "name": "WMIC.exe",
                "pid": 2732
            },
            "relative_file_creation_time": 48628704.4029488,
            "relative_file_name_modify_time": 48628704.4029488,
            "session_info": {
                "logon_type": "Interactive",
                "client_address": "127.0.0.1",
                "id": 1,
                "authentication_package": "NTLM",
                "relative_logon_time": 0.1,
                "relative_password_age": 2592000.123,
                "user_flags": [
                    "LOGON_EXTRA_SIDS",
                    "LOGON_NTLMV2_ENABLED",
                    "LOGON_WINLOGON"
                ]
            }
        },
        "parent": {
            "args": [],
            "name": "services.exe",
            "pid": 600,
            "args_count": 0,
            "entity_id": "NGM5YzljYjMtZjgwZi00NGQ4LTljODktNjE2ODI0M2I3ZjIxLTYwMC0xMzI5MzU0OTExMC40NjgyMjI3MDA=",
            "command_line": "",
            "executable": "C:\\Windows\\System32\\services.exe",
            "thread": {
                "Ext": {
                    "call_stack": [
                        {
                            "allocation_private_bytes": 16384,
                            "callsite_leading_bytes": "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
                            "callsite_trailing_bytes": "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
                            "protection": "RWX",
                            "symbol_info": "C:\\Windows\\System32\\ntdll.dll!RtlUserThreadStart+0x21"
                        }
                    ],
                    "call_stack_summary": "ntdll.dll|kernelbase.dll|kernel32.dll|cmd.exe|kernel32.dll|ntdll.dll",
                    "call_stack_contains_unbacked": true,
                    "hardware_breakpoint_set": true
                }
            }
        },
        "pid": 2772,
        "working_directory": "C:\\Windows\\system32\\",
        "end": "2022-07-18T21:05:19.9419692Z",
        "entity_id": "NGM5YzljYjMtZjgwZi00NGQ4LTljODktNjE2ODI0M2I3ZjIxLTI3NzItMTMyOTM1NzE5ODguNjU3ODk4NjAw",
        "executable": "C:\\Windows\\System32\\svchost.exe",
        "args": [
            "C:\\Windows\\System32\\svchost.exe",
            "-k",
            "WerSvcGroup"
        ],
        "code_signature": {
            "trusted": true,
            "subject_name": "Microsoft Windows Publisher",
            "exists": true,
            "status": "trusted"
        },
        "pe": {
            "original_file_name": "svchost.exe"
        },
        "name": "svchost.exe",
        "args_count": 3,
        "command_line": "C:\\Windows\\System32\\svchost.exe -k WerSvcGroup",
        "hash": {
            "sha1": "4fbfc6004084d97032837c21d3f426892d868eac",
            "sha256": "cb19fd67b1d028e01f54c426a0924528c4a8d8ed8996cfe0ee0c6e45285436a1",
            "md5": "1b280ad032268a636ecfe6f9165431b7"
        },
        "tty": {
            "char_device": {
                "major": 4,
                "minor": 1
            },
            "rows": 24,
            "columns": 80
        },
        "io": {
            "text": "helloworld",
            "total_bytes_captured": 10,
            "total_bytes_skipped": 0,
            "max_bytes_per_process_exceeded": false
        },
        "env_vars": [
            "NICK=test",
            "OTHER=why"
        ]
    },
    "message": "Endpoint process event",
    "@timestamp": "2022-04-04T18:53:08.6578986Z",
    "ecs": {
        "version": "1.11.0"
    },
    "data_stream": {
        "namespace": "default",
        "type": "logs",
        "dataset": "endpoint.events.process"
    },
    "host": {
        "hostname": "data-viz-win-1",
        "os": {
            "Ext": {
                "variant": "Windows Server 2019 Datacenter"
            },
            "kernel": "1809 (10.0.17763.2686)",
            "name": "Windows",
            "family": "windows",
            "type": "windows",
            "version": "1809 (10.0.17763.2686)",
            "platform": "windows",
            "full": "Windows Server 2019 Datacenter 1809 (10.0.17763.2686)"
        },
        "ip": [
            "10.201.0.13",
            "fe80::f40a:aed0:618a:972d",
            "127.0.0.1",
            "::1"
        ],
        "name": "data-viz-win-1",
        "id": "2beebb8e-e5f0-46ca-8635-97ba7bb8ccca",
        "mac": [
            "00-00-5E-00-53-23"
        ],
        "architecture": "x86_64"
    },
    "event": {
        "agent_id_status": "verified",
        "sequence": 36236,
        "ingested": "2022-04-04T18:53:18Z",
        "created": "2022-04-04T18:53:08.6578986Z",
        "kind": "event",
        "module": "endpoint",
        "action": "start",
        "id": "MYfZG00oEwD2/fqT+++++CLz",
        "category": [
            "process"
        ],
        "type": [
            "start"
        ],
        "dataset": "endpoint.events.process"
    },
    "user": {
        "domain": "NT AUTHORITY",
        "name": "SYSTEM",
        "id": "S-1-5-18"
    }
}
```
</details>

### [Fields](process.md)
- [@timestamp](process.md#@timestamp)
- [message](process.md#message)
- [agent](process.md#agent)
- [cloud](process.md#cloud)
- [container](process.md#container)
- [data_stream](process.md#data_stream)
- [destination](process.md#destination)
- [ecs](process.md#ecs)
- [event](process.md#event)
- [group](process.md#group)
- [host](process.md#host)
- [orchestrator](process.md#orchestrator)
- [package](process.md#package)
- [process](process.md#process)
- [source](process.md#source)
- [user](process.md#user)
# security
### Sample Event
<details>
<summary>
Click to expand
</summary>

```json
{
    "Target": {
        "process": {
            "Ext": {
                "authentication_id": "0x3e7"
            }
        }
    },
    "agent": {
        "id": "4c9c9cb3-f80f-44d8-9c89-6168243b7f21",
        "type": "endpoint",
        "version": "8.3.0-SNAPSHOT"
    },
    "file": {
        "path": "/User/admin/Downloads/application",
        "code_signature": {
            "signing_id": "com.developer.identifier",
            "team_id": "XYZABC"
        }
    },
    "process": {
        "Ext": {
            "ancestry": [
                "NGM5YzljYjMtZjgwZi00NGQ4LTljODktNjE2ODI0M2I3ZjIxLTQ3Mi0xMzI5MzU0OTExMC4xNzIwMjY5MDA="
            ],
            "authentication_id": "0x3e7",
            "code_signature": [
                {
                    "trusted": true,
                    "subject_name": "Microsoft Windows Publisher",
                    "exists": true,
                    "status": "trusted"
                }
            ]
        },
        "code_signature": {
            "trusted": true,
            "subject_name": "Microsoft Windows Publisher",
            "exists": true,
            "status": "trusted"
        },
        "name": "C:\\Windows\\System32\\services.exe",
        "entity_id": "NGM5YzljYjMtZjgwZi00NGQ4LTljODktNjE2ODI0M2I3ZjIxLTYwMC0xMzI5MzU0OTExMC40NjgyMjI3MDA=",
        "executable": "C:\\Windows\\System32\\services.exe"
    },
    "message": "Endpoint security event",
    "@timestamp": "2022-04-04T18:53:08.6510289Z",
    "ecs": {
        "version": "1.11.0"
    },
    "data_stream": {
        "namespace": "default",
        "type": "logs",
        "dataset": "endpoint.events.security"
    },
    "host": {
        "hostname": "data-viz-win-1",
        "os": {
            "Ext": {
                "variant": "Windows Server 2019 Datacenter"
            },
            "kernel": "1809 (10.0.17763.2686)",
            "name": "Windows",
            "family": "windows",
            "type": "windows",
            "version": "1809 (10.0.17763.2686)",
            "platform": "windows",
            "full": "Windows Server 2019 Datacenter 1809 (10.0.17763.2686)"
        },
        "ip": [
            "10.201.0.13",
            "fe80::f40a:aed0:618a:972d",
            "127.0.0.1",
            "::1"
        ],
        "name": "data-viz-win-1",
        "id": "2beebb8e-e5f0-46ca-8635-97ba7bb8ccca",
        "mac": [
            "00-00-5E-00-53-23"
        ],
        "architecture": "x86_64"
    },
    "event": {
        "agent_id_status": "verified",
        "sequence": 36385,
        "ingested": "2022-04-04T18:53:18Z",
        "created": "2022-04-04T18:53:08.6510289Z",
        "kind": "event",
        "module": "endpoint",
        "action": "log_on",
        "id": "MYfZG00oEwD2/fqT+++++CQ/",
        "category": [
            "authentication",
            "session"
        ],
        "type": [
            "start"
        ],
        "dataset": "endpoint.events.security",
        "outcome": "success"
    },
    "user": {
        "domain": "DESKTOP-1TK590J",
        "effective": {
            "domain": "DESKTOP-1TK590J",
            "name": "EafTestLogon80589",
            "id": "S-1-5-18",
            "email": "EafTestLogon80589@DESKTOP-1TK590J.local",
            "full_name": "EafTestLogon80589",
            "hash": "f1297b0233914ec6ebf8fc01195e8712dfd8322f5e8d9d8bbe0083a0fc1860fd"
        },
        "id": "S-1-5-21-1749029863-1064264096-968553628-1001",
        "name": "Default"
    },
    "winlog": {
        "event_data": {
            "PrivilegeList": [
                "SeSecurityPrivilege",
                "SeTakeOwnershipPrivilege",
                "SeLoadDriverPrivilege",
                "SeBackupPrivilege",
                "SeRestorePrivilege",
                "SeDebugPrivilege",
                "SeSystemEnvironmentPrivilege",
                "SeImpersonatePrivilege",
                "SeDelegateSessionUserImpersonatePrivilege"
            ]
        }
    }
}
```
</details>

### [Fields](security.md)
- [@timestamp](security.md#@timestamp)
- [message](security.md#message)
- [Target](security.md#Target)
- [agent](security.md#agent)
- [data_stream](security.md#data_stream)
- [destination](security.md#destination)
- [ecs](security.md#ecs)
- [event](security.md#event)
- [file](security.md#file)
- [group](security.md#group)
- [host](security.md#host)
- [process](security.md#process)
- [source](security.md#source)
- [user](security.md#user)
- [winlog](security.md#winlog)
# metadata
### Sample Event
<details>
<summary>
Click to expand
</summary>

```json
{
    "agent": {
        "build": {
            "original": "version: 8.3.0-SNAPSHOT, compiled: Fri Apr 1 06:00:00 2022, branch: main, commit: f8b0ed879ad40ee1ae561ced31ec8a4027a2bf53"
        },
        "id": "4c9c9cb3-f80f-44d8-9c89-6168243b7f21",
        "type": "endpoint",
        "version": "8.3.0-SNAPSHOT"
    },
    "@timestamp": "2022-04-04T12:33:36.6664577Z",
    "Endpoint": {
        "capabilities": [
            "isolation"
        ],
        "configuration": {
            "isolation": false
        },
        "state": {
            "isolation": false
        },
        "policy": {
            "applied": {
                "name": "endpoint-1",
                "id": "b372bc3f-e9b3-4b2d-9dfe-ae677ed83933",
                "status": "success"
            }
        },
        "status": "enrolled"
    },
    "ecs": {
        "version": "1.11.0"
    },
    "data_stream": {
        "namespace": "default",
        "type": "metrics",
        "dataset": "endpoint.metadata"
    },
    "elastic": {
        "agent": {
            "id": "4c9c9cb3-f80f-44d8-9c89-6168243b7f21"
        }
    },
    "host": {
        "hostname": "data-viz-win-1",
        "os": {
            "Ext": {
                "variant": "Windows Server 2019 Datacenter"
            },
            "kernel": "1809 (10.0.17763.2686)",
            "name": "Windows",
            "family": "windows",
            "type": "windows",
            "version": "1809 (10.0.17763.2686)",
            "platform": "windows",
            "full": "Windows Server 2019 Datacenter 1809 (10.0.17763.2686)"
        },
        "ip": [
            "10.201.0.13",
            "fe80::f40a:aed0:618a:972d",
            "127.0.0.1",
            "::1"
        ],
        "name": "data-viz-win-1",
        "id": "2beebb8e-e5f0-46ca-8635-97ba7bb8ccca",
        "mac": [
            "00-00-5E-00-53-23"
        ],
        "architecture": "x86_64"
    },
    "event": {
        "agent_id_status": "verified",
        "sequence": 5054,
        "ingested": "2022-04-04T12:33:37Z",
        "created": "2022-04-04T12:33:36.6664577Z",
        "kind": "metric",
        "module": "endpoint",
        "action": "endpoint_metadata",
        "id": "MYfZG00oEwD2/fqT+++++/SC",
        "category": [
            "host"
        ],
        "type": [
            "info"
        ],
        "dataset": "endpoint.metadata"
    }
}
```
</details>

### [Fields](metadata.md)
- [@timestamp](metadata.md#@timestamp)
- [Endpoint](metadata.md#Endpoint)
- [agent](metadata.md#agent)
- [data_stream](metadata.md#data_stream)
- [ecs](metadata.md#ecs)
- [elastic](metadata.md#elastic)
- [event](metadata.md#event)
- [host](metadata.md#host)
# action_responses
### Sample Event
<details>
<summary>
Click to expand
</summary>

```json
{
    "EndpointActions": {
        "completed_at": "2022-04-04T20:44:14.0Z",
        "data": {
            "comment": "Action completed successfully",
            "command": "isolate"
        },
        "action_id": "cfa1d245-24ad-4867-8043-475d4ee2a111",
        "started_at": "2022-04-04T20:44:08.0Z"
    },
    "agent": {
        "id": "c8cad7f3-9e62-43d0-94ed-8c51670fae62"
    },
    "@timestamp": "2022-04-04T20:44:14.0Z",
    "data_stream": {
        "namespace": "default",
        "type": ".logs",
        "dataset": "endpoint.action.responses"
    },
    "event": {
        "agent_id_status": "verified",
        "ingested": "2022-04-04T20:44:45Z"
    }
}
```
</details>

### [Fields](action_responses.md)
- [@timestamp](action_responses.md#@timestamp)
- [action_id](action_responses.md#action_id)
- [agent_id](action_responses.md#agent_id)
- [completed_at](action_responses.md#completed_at)
- [data.alert_id](action_responses.md#data.alert_id)
- [data.command](action_responses.md#data.command)
- [data.comment](action_responses.md#data.comment)
- [started_at](action_responses.md#started_at)
- [status](action_responses.md#status)
- [EndpointActions](action_responses.md#EndpointActions)
- [agent](action_responses.md#agent)
- [data_stream](action_responses.md#data_stream)
- [ecs](action_responses.md#ecs)
- [error](action_responses.md#error)
- [event](action_responses.md#event)
# collection
### [Fields](collection.md)
- [@timestamp](collection.md#@timestamp)
- [data_stream](collection.md#data_stream)
- [ecs](collection.md#ecs)
- [event](collection.md#event)
# library
### Sample Event
<details>
<summary>
Click to expand
</summary>

```json
{
    "agent": {
        "id": "4c9c9cb3-f80f-44d8-9c89-6168243b7f21",
        "type": "endpoint",
        "version": "8.3.0-SNAPSHOT"
    },
    "process": {
        "Ext": {
            "ancestry": [
                "NGM5YzljYjMtZjgwZi00NGQ4LTljODktNjE2ODI0M2I3ZjIxLTYwMC0xMzI5MzU0OTExMC40NjgyMjI3MDA=",
                "NGM5YzljYjMtZjgwZi00NGQ4LTljODktNjE2ODI0M2I3ZjIxLTQ3Mi0xMzI5MzU0OTExMC4xNzIwMjY5MDA="
            ],
            "code_signature": [
                {
                    "trusted": true,
                    "subject_name": "Microsoft Windows",
                    "exists": true,
                    "status": "trusted"
                }
            ],
            "protection": "PsProtectedSignerAntimalware-Light"
        },
        "code_signature": {
            "trusted": true,
            "subject_name": "Microsoft Windows",
            "exists": true,
            "status": "trusted"
        },
        "name": "VSSVC.exe",
        "pid": 4528,
        "entity_id": "NGM5YzljYjMtZjgwZi00NGQ4LTljODktNjE2ODI0M2I3ZjIxLTQ1MjgtMTMyOTM1NzEwODYuNjI4MzM0NzAw",
        "executable": "C:\\Windows\\System32\\VSSVC.exe",
        "thread": {
            "id": 340,
            "Ext": {
                "call_stack": [
                    {
                        "allocation_private_bytes": 16384,
                        "callsite_leading_bytes": "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
                        "callsite_trailing_bytes": "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
                        "protection": "RWX",
                        "symbol_info": "C:\\Windows\\System32\\ntdll.dll!RtlUserThreadStart+0x21"
                    }
                ],
                "call_stack_summary": "ntdll.dll|kernelbase.dll|kernel32.dll|cmd.exe|kernel32.dll|ntdll.dll",
                "hardware_breakpoint_set": true
            }
        }
    },
    "dll": {
        "Ext": {
            "code_signature": [
                {
                    "trusted": true,
                    "subject_name": "Microsoft Windows",
                    "exists": true,
                    "status": "trusted"
                }
            ],
            "device": {
                "volume_device_type": "Disk File System"
            },
            "load_index": 1,
            "relative_file_creation_time": 48628704.4029488,
            "relative_file_name_modify_time": 48628704.4029488,
            "size": 65536
        },
        "path": "C:\\Windows\\System32\\msxml3.dll",
        "code_signature": {
            "trusted": true,
            "subject_name": "Microsoft Windows",
            "exists": true,
            "status": "trusted"
        },
        "pe": {
            "file_version": "8.110.17763.1911",
            "imphash": "2e1d1e35c17be5497d2de33f06dc41b4",
            "original_file_name": "MSXML3.dll"
        },
        "name": "msxml3.dll",
        "hash": {
            "sha1": "02488fb2dbf679a3282338178b451da635b79b54",
            "sha256": "a9698adcf789d9e30f37dd5e6c9be0441bc37662ba7402e85071ccec2135d36c",
            "md5": "65e4fd0564411bb60c600fae12cde2f9"
        }
    },
    "message": "Endpoint DLL load event",
    "@timestamp": "2022-04-04T18:38:08.3185831Z",
    "ecs": {
        "version": "1.11.0"
    },
    "data_stream": {
        "namespace": "default",
        "type": "logs",
        "dataset": "endpoint.events.library"
    },
    "host": {
        "hostname": "data-viz-win-1",
        "os": {
            "Ext": {
                "variant": "Windows Server 2019 Datacenter"
            },
            "kernel": "1809 (10.0.17763.2686)",
            "name": "Windows",
            "family": "windows",
            "type": "windows",
            "version": "1809 (10.0.17763.2686)",
            "platform": "windows",
            "full": "Windows Server 2019 Datacenter 1809 (10.0.17763.2686)"
        },
        "ip": [
            "10.201.0.13",
            "fe80::f40a:aed0:618a:972d",
            "127.0.0.1",
            "::1"
        ],
        "name": "data-viz-win-1",
        "id": "2beebb8e-e5f0-46ca-8635-97ba7bb8ccca",
        "mac": [
            "00-00-5E-00-53-23"
        ],
        "architecture": "x86_64"
    },
    "event": {
        "agent_id_status": "verified",
        "sequence": 34339,
        "ingested": "2022-04-04T18:38:16Z",
        "created": "2022-04-04T18:38:08.3185831Z",
        "kind": "event",
        "module": "endpoint",
        "action": "load",
        "id": "MYfZG00oEwD2/fqT+++++BRi",
        "category": [
            "library"
        ],
        "type": [
            "start"
        ],
        "dataset": "endpoint.events.library"
    },
    "user": {
        "domain": "NT AUTHORITY",
        "name": "SYSTEM",
        "id": "S-1-5-18"
    },
    "Effective_process": {
        "entity_id": "YWFhYWFhYWEtYWFhYS1hYWFhLWFhYWEtYWFhYWFhYWFhYWFhLTU2NS0xNjk1MTkyOTQ3",
        "executable": "/System/Applications/Utilities/Terminal.app/Contents/MacOS/Terminal",
        "name": "Terminal",
        "pid": 565
    }
}
```
</details>

### [Fields](library.md)
- [@timestamp](library.md#@timestamp)
- [message](library.md#message)
- [Effective_process](library.md#Effective_process)
- [agent](library.md#agent)
- [data_stream](library.md#data_stream)
- [destination](library.md#destination)
- [dll](library.md#dll)
- [ecs](library.md#ecs)
- [event](library.md#event)
- [file](library.md#file)
- [group](library.md#group)
- [host](library.md#host)
- [process](library.md#process)
- [source](library.md#source)
- [user](library.md#user)
# heartbeat
### Sample Event
<details>
<summary>
Click to expand
</summary>

```json
{
    "@timestamp": "2023-07-18T20:40:09.279939Z",
    "agent": {
        "id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
    },
    "data_stream": {
        "dataset": "endpoint.heartbeat",
        "namespace": "default",
        "type": ".logs"
    },
    "message": "Endpoint heartbeat",
    "event": {
        "ingested": "2023-07-18T20:40:09.279939Z"
    },
    "billable": true
}
```
</details>

### [Fields](heartbeat.md)
- [@timestamp](heartbeat.md#@timestamp)
- [billable](heartbeat.md#billable)
- [message](heartbeat.md#message)
- [agent](heartbeat.md#agent)
- [data_stream](heartbeat.md#data_stream)
- [event](heartbeat.md#event)
# actions
### Sample Event
<details>
<summary>
Click to expand
</summary>

```json
{
    "EndpointActions": {
        "data": {
            "comment": "testing isolation",
            "command": "isolate"
        },
        "action_id": "cfa1d245-24ad-4867-8043-475d4ee2a111",
        "input_type": "endpoint",
        "expiration": "2022-04-18T20:44:07.805Z",
        "type": "INPUT_ACTION"
    },
    "agent": {
        "id": [
            "c8cad7f3-9e62-43d0-94ed-8c51670fae62"
        ]
    },
    "@timestamp": "2022-04-04T20:44:07.805Z",
    "event": {
        "agent_id_status": "auth_metadata_missing",
        "ingested": "2022-04-04T20:44:07Z"
    },
    "user": {
        "id": "user@elastic.co"
    }
}
```
</details>

### [Fields](actions.md)
- [@timestamp](actions.md#@timestamp)
- [action_id](actions.md#action_id)
- [agents](actions.md#agents)
- [data.alert_id](actions.md#data.alert_id)
- [data.command](actions.md#data.command)
- [data.comment](actions.md#data.comment)
- [expiration](actions.md#expiration)
- [input_type](actions.md#input_type)
- [type](actions.md#type)
- [user_id](actions.md#user_id)
- [EndpointActions](actions.md#EndpointActions)
- [agent](actions.md#agent)
- [data_stream](actions.md#data_stream)
- [ecs](actions.md#ecs)
- [error](actions.md#error)
- [event](actions.md#event)
- [rule](actions.md#rule)
- [user](actions.md#user)
# file
### Sample Event
<details>
<summary>
Click to expand
</summary>

```json
{
    "agent": {
        "id": "ccb7b1a1-303e-416f-b975-311737e8e125",
        "type": "endpoint",
        "version": "8.3.0-SNAPSHOT"
    },
    "Effective_process": {
        "entity_id": "YWFhYWFhYWEtYWFhYS1hYWFhLWFhYWEtYWFhYWFhYWFhYWFhLTI3MzItMTMyOTk3MDczNDEuMjUyNTI3NDAw",
        "executable": "C:\\Windows\\System32\\wbem\\WMIC.exe",
        "name": "WMIC.exe",
        "pid": 2732
    },
    "process": {
        "Ext": {
            "ancestry": [
                "Y2NiN2IxYTEtMzAzZS00MTZmLWI5NzUtMzExNzM3ZThlMTI1LTYwNC0xMzI5MzU0OTEwOS4zNTg1OTc3MDA=",
                "Y2NiN2IxYTEtMzAzZS00MTZmLWI5NzUtMzExNzM3ZThlMTI1LTQ3Mi0xMzI5MzU0OTEwOS43NjU4MjcwMA=="
            ],
            "code_signature": [
                {
                    "trusted": true,
                    "subject_name": "Elasticsearch, Inc.",
                    "exists": true,
                    "status": "trusted"
                }
            ]
        },
        "args_count": 1,
        "parent": {
            "pid": 604,
            "entity_id": "Y2NiN2IxYTEtMzAzZS00MTZmLWI5NzUtMzExNzM3ZThlMTI1LTQ1MTItMTMyOTM1NDkyODYuNzQ2MjY0MDAw",
            "group_leader": {
                "entity_id": "Y2NiN2IxYTEtMzAzZS00MTZmLWI5NzUtMzExNzM3ZThlMTI1LTQ1MTItMTMyOTM1NDkyODYuNzQ2MjY0MDAw"
            }
        },
        "entry_leader": {
            "entity_id": "Y2NiN2IxYTEtMzAzZS00MTZmLWI5NzUtMzExNzM3ZThlMTI1LTQ1MTItMTMyOTM1NDkyODYuNzQ2MjY0MDAw",
            "parent": {
                "entity_id": "Y2NiN2IxYTEtMzAzZS00MTZmLWI5NzUtMzExNzM3ZThlMTI1LTQ1MTItMTMyOTM1NDkyODYuNzQ2MjY0MDAw"
            }
        },
        "session_leader": {
            "entity_id": "Y2NiN2IxYTEtMzAzZS00MTZmLWI5NzUtMzExNzM3ZThlMTI1LTQ1MTItMTMyOTM1NDkyODYuNzQ2MjY0MDAw"
        },
        "group_leader": {
            "entity_id": "Y2NiN2IxYTEtMzAzZS00MTZmLWI5NzUtMzExNzM3ZThlMTI1LTQ1MTItMTMyOTM1NDkyODYuNzQ2MjY0MDAw"
        },
        "code_signature": {
            "trusted": true,
            "subject_name": "Elasticsearch, Inc.",
            "exists": true,
            "status": "trusted"
        },
        "name": "winlogbeat.exe",
        "pid": 4512,
        "thread": {
            "id": 340,
            "Ext": {
                "call_stack": [
                    {
                        "allocation_private_bytes": 16384,
                        "callsite_leading_bytes": "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
                        "callsite_trailing_bytes": "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
                        "protection": "RWX",
                        "symbol_info": "C:\\Windows\\System32\\ntdll.dll!RtlUserThreadStart+0x21"
                    }
                ],
                "call_stack_summary": "ntdll.dll|kernelbase.dll|kernel32.dll|cmd.exe|kernel32.dll|ntdll.dll",
                "hardware_breakpoint_set": true
            }
        },
        "entity_id": "Y2NiN2IxYTEtMzAzZS00MTZmLWI5NzUtMzExNzM3ZThlMTI1LTQ1MTItMTMyOTM1NDkyODYuNzQ2MjY0MDAw",
        "executable": "C:\\Program Files\\Winlogbeat\\winlogbeat.exe"
    },
    "message": "Endpoint file event",
    "@timestamp": "2022-04-04T18:37:01.5775771Z",
    "file": {
        "Ext": {
            "header_data": [],
            "entropy": 5.28353871945538,
            "device": {
                "volume_device_type": "Disk File System"
            },
            "header_bytes": "7570646174655f74696d653a20323032",
            "windows": {
                "zone_identifier": -1
            },
            "monotonic_id": 3526
        },
        "path": "C:\\ProgramData\\winlogbeat\\.winlogbeat.yml.new",
        "extension": "new",
        "size": 1406,
        "name": ".winlogbeat.yml.new",
        "origin_referrer_url": "https://example.com",
        "origin_url": "https://example.com/file.zip"
    },
    "ecs": {
        "version": "1.11.0"
    },
    "data_stream": {
        "namespace": "default",
        "type": "logs",
        "dataset": "endpoint.events.file"
    },
    "host": {
        "hostname": "response-win-1",
        "os": {
            "Ext": {
                "variant": "Windows Server 2019 Datacenter"
            },
            "kernel": "1809 (10.0.17763.2686)",
            "name": "Windows",
            "family": "windows",
            "type": "windows",
            "version": "1809 (10.0.17763.2686)",
            "platform": "windows",
            "full": "Windows Server 2019 Datacenter 1809 (10.0.17763.2686)"
        },
        "ip": [
            "10.201.0.9",
            "fe80::4d1:ef01:c0ed:299a",
            "127.0.0.1",
            "::1"
        ],
        "name": "response-win-1",
        "id": "bcbbe9cb-0278-43f9-aa1b-2dc9839bbf6f",
        "mac": [
            "00-00-5E-00-53-23"
        ],
        "architecture": "x86_64"
    },
    "event": {
        "agent_id_status": "verified",
        "sequence": 32114,
        "ingested": "2022-04-04T18:37:29Z",
        "created": "2022-04-04T18:37:01.5775771Z",
        "kind": "event",
        "module": "endpoint",
        "action": "creation",
        "id": "MYfZFpbNKturKgFp+++++AlT",
        "category": [
            "file"
        ],
        "type": [
            "creation"
        ],
        "dataset": "endpoint.events.file"
    },
    "user": {
        "domain": "NT AUTHORITY",
        "name": "SYSTEM",
        "id": "S-1-5-18"
    }
}
```
</details>

### [Fields](file.md)
- [@timestamp](file.md#@timestamp)
- [message](file.md#message)
- [Effective_process](file.md#Effective_process)
- [Persistence](file.md#Persistence)
- [agent](file.md#agent)
- [data_stream](file.md#data_stream)
- [destination](file.md#destination)
- [ecs](file.md#ecs)
- [event](file.md#event)
- [file](file.md#file)
- [group](file.md#group)
- [host](file.md#host)
- [process](file.md#process)
- [source](file.md#source)
- [user](file.md#user)
# api
### Sample Event
<details>
<summary>
Click to expand
</summary>

```json
{
    "@timestamp": "2023-01-09T19:38:51.5141503Z",
    "Target": {
        "process": {
            "Ext": {
                "created_suspended": true,
                "protection": "PsProtectedSignerWinTcb",
                "memory_region": {
                    "allocation_base": 1649160290304,
                    "allocation_protection": "RWX",
                    "allocation_size": 4096,
                    "allocation_type": "PRIVATE",
                    "bytes_address": 1649160290304,
                    "bytes_allocation_offset": 0,
                    "bytes_compressed": "eJztwbEJACAMALA+5uAtWnAoOPg/+EWnJO9k1bo742XuMRsEAAAA0OsD8lge9g==",
                    "bytes_compressed_present": true,
                    "hash": {
                        "sha256": "0b28b598ef70fd2377613fd88a50d52047ae31c16f2c688f3aa4e0b98d63730c"
                    },
                    "memory_pe_detected": false,
                    "region_base": 1649160290304,
                    "region_protection": "R--",
                    "region_size": 4096,
                    "region_state": "COMMIT",
                    "strings": [
                        "shellcode",
                        "seed=AAAA"
                    ]
                },
                "token": {
                    "integrity_level_name": "high"
                }
            },
            "entity_id": "YWFhYWFhYWEtYWFhYS1hYWFhLWFhYWEtYWFhYWFhYWFhYWFhLTI1NzMyLTE2OTkwMDE3NDAuOTU4NTY4MDAw",
            "executable": "C:\\Temp\\1_StayRunningWin32_x64.exe",
            "name": "1_StayRunningWin32_x64.exe",
            "pid": 25732
        }
    },
    "dll": {
        "Ext": {
            "code_signature": [
                {
                    "exists": true,
                    "status": "trusted",
                    "subject_name": "Microsoft Windows",
                    "trusted": true
                }
            ]
        },
        "hash": {
            "sha256": "8b9731a4b83e801cda7b918f8194608e91f86b3a86ffb6bb24230b1cc28e1a54"
        },
        "path": "c:\\windows\\system32\\drivers\\pktmon.sys"
    },
    "destination": {
        "ip": "2001:4860:4860::8844",
        "port": 139
    },
    "event": {
        "category": [
            "api",
            "intrusion_detection"
        ],
        "created": "2023-01-09T19:38:51.5141503Z",
        "dataset": "endpoint.events.api",
        "id": "MvlgiHxIZtj1+Abi++++++ul",
        "kind": "event",
        "module": "endpoint",
        "outcome": "success",
        "provider": "Microsoft-Windows-Threat-Intelligence",
        "sequence": 3802,
        "type": [
            "credential_access"
        ]
    },
    "host": {
        "architecture": "x86_64",
        "hostname": "DESKTOP-OCG8CR6",
        "id": "dabadaba-0000-0000-0000-000000000000",
        "ip": [
            "169.254.104.226",
            "fe80::6037:d589:2ee9:772f",
            "172.22.6.230",
            "fe80::80ea:8e8d:e1f2:6622",
            "169.254.74.35",
            "fe80::900c:a9d3:fd8:9345",
            "127.0.0.1",
            "::1"
        ],
        "mac": [
            "00-15-5D-00-09-18",
            "00-15-5D-00-09-19",
            "00-15-5D-00-09-17"
        ],
        "name": "DESKTOP-OCG8CR6",
        "os": {
            "Ext": {
                "variant": "Windows 11 Enterprise N"
            },
            "family": "windows",
            "full": "Windows 11 Enterprise N 22H2 (10.0.22621.963)",
            "kernel": "22H2 (10.0.22621.963)",
            "name": "Windows",
            "platform": "windows",
            "type": "windows",
            "version": "22H2 (10.0.22621.963)"
        }
    },
    "message": "Endpoint API event - hand-crafted with a superset of fields",
    "network": {
        "transport": "tcp",
        "type": "ipv6"
    },
    "process": {
        "Ext": {
            "ancestry": [
                "YWFhYWFhYWEtYWFhYS1hYWFhLWFhYWEtYWFhYWFhYWFhYWFhLTgxMi0xNjczMjkxNTMzLjcxNjczMTgwMA==",
                "YWFhYWFhYWEtYWFhYS1hYWFhLWFhYWEtYWFhYWFhYWFhYWFhLTQ5NjAtMTY3Mjk2NTgzMC4yODc0OTYxMDA=",
                "YWFhYWFhYWEtYWFhYS1hYWFhLWFhYWEtYWFhYWFhYWFhYWFhLTY2MjgtMTY3Mjk2NTc3Mi41MTg4MDA1MDA=",
                "YWFhYWFhYWEtYWFhYS1hYWFhLWFhYWEtYWFhYWFhYWFhYWFhLTQ2MDAtMTY3Mjk2NTcxMy40NzY1NDUyMDA="
            ],
            "api": {
                "behaviors": [
                    "cross-process",
                    "rapid_background_polling",
                    "multiple_polling_processes",
                    "pid_spoofing"
                ],
                "metadata": {
                    "target_address_name": "Unbacked",
                    "target_address_path": "c:\\windows\\system32\\ntdll.dll",
                    "return_value": 1,
                    "windows_count": 2,
                    "visible_windows_count": 0,
                    "thread_info_flags": 16,
                    "start_address_module": "C:\\Windows\\System32\\DellTPad\\ApMsgFwd.exe",
                    "start_address_allocation_protection": "RCX",
                    "procedure_symbol": "taskbar.dll",
                    "ms_since_last_keyevent": 94,
                    "background_callcount": 6021,
                    "security_descriptor": "O:BAG:SYD:P(A;;FA;;;SY)(A;;FA;;;BA)S:AI(ML;;NW;;;LW)",
                    "client_machine": "DESKTOP-EXAMPLE",
                    "client_machine_fqdn": "DESKTOP-EXAMPLE",
                    "client_process_id": 3600,
                    "client_is_local": true,
                    "amsi_filenames": [
                        "C:\\script.ps1"
                    ],
                    "amsi_logs": {
                        "entries": [
                            "[Ref].Assembly.GetType('System.Management.Automation.AmsiUtils').GetField('amsiInitFailed', 'NonPublic,Static').SetValue($null, $true);"
                        ],
                        "type": "PowerShell"
                    }
                },
                "name": "OpenProcess",
                "parameters": {
                    "desired_access": [
                        "PROCESS_QUERY_LIMITED_INFORMATION",
                        "PROCESS_VM_READ"
                    ],
                    "desired_access_numeric": 4112,
                    "handle_type": "process",
                    "address": 2904525045760,
                    "allocation_type": "COMMIT|RESERVE",
                    "protection": "R-X",
                    "protection_old": "R-X",
                    "size": 16,
                    "context_flags": 1048607,
                    "r8": 8,
                    "r9": 9,
                    "rax": 10,
                    "rbp": 3,
                    "rbx": 11,
                    "rcx": 2883351609344,
                    "rdi": 5,
                    "rdx": 13,
                    "rip": 140706538588528,
                    "rsi": 4,
                    "rsp": 2,
                    "eax": 10,
                    "ebp": 3,
                    "ebx": 11,
                    "ecx": 12,
                    "edi": 5,
                    "edx": 0,
                    "eip": 1,
                    "esi": 4,
                    "esp": 2,
                    "argument1": 2583984274656,
                    "argument2": 4105953215,
                    "argument3": 31058890,
                    "procedure": 140705553857280,
                    "usage_page": "GENERIC",
                    "usage": "KEYBOARD",
                    "flags": "INPUTSINK",
                    "hook_type": "WH_KEYBOARD_LL",
                    "hook_module": "c:\\windows\\system32\\taskbar.dll",
                    "device": "\\Device\\PktMonDev",
                    "io_control_code": 27365,
                    "event_filter_name": "ExampleFilter",
                    "event_filter_details": "__EventFilter{EventNamespace = \"root\\CimV2\"; Name = \"ExampleFilter\";};",
                    "consumer_name": "ExampleConsumer",
                    "consumer_type": "CommandLineEventConsumer",
                    "consumer_details": "CommandLineEventConsumer{Name = \"ExampleConsumer\";};",
                    "namespace": "root\\Microsoft\\Windows\\DeviceGuard",
                    "operation": "Win32_Process::Create",
                    "app_name": "PowerShell",
                    "content_name": "C:\\script.ps1",
                    "buffer": "[Ref].Assembly.GetType('System.Management.Automation.AmsiUtils').GetField('amsiInitFailed', 'NonPublic,Static').SetValue($null, $true);"
                },
                "summary": "VirtualAllocEx( charmap.exe, NULL, 0x10, COMMIT|RESERVE, R-X )"
            },
            "code_signature": [
                {
                    "exists": true,
                    "status": "errorBadDigest",
                    "subject_name": "Microsoft Windows",
                    "trusted": false
                }
            ],
            "memory_region": {
                "allocation_base": 140712018378752,
                "allocation_protection": "RCX",
                "allocation_size": 45056,
                "allocation_type": "IMAGE",
                "mapped_path": "C:\\Program Files\\Python39\\DLLs\\libffi-7.dll",
                "region_base": 140712018395136,
                "region_protection": "R-X",
                "region_size": 8192,
                "region_state": "COMMIT"
            },
            "token": {
                "integrity_level_name": "system"
            }
        },
        "code_signature": {
            "exists": true,
            "status": "errorBadDigest",
            "subject_name": "Microsoft Windows",
            "trusted": false
        },
        "command_line": "",
        "entity_id": "YWFhYWFhYWEtYWFhYS1hYWFhLWFhYWEtYWFhYWFhYWFhYWFhLTkxNi0xNjczMjkzMTMwLjk0NjAwMjAw",
        "executable": "c\\git\\endpoint-dev\\Tools\\Leia\\modules\\exe_malware\\mimikatz.exe",
        "name": "mimikatz.exe",
        "pid": 916,
        "thread": {
            "Ext": {
                "call_stack": [
                    {
                        "allocation_private_bytes": 4096,
                        "protection_provenance": "dabapi.dll",
                        "symbol_info": "c:\\windows\\system32\\ntdll.dll!ZwProtectVirtualMemory+0x14"
                    },
                    {
                        "symbol_info": "c:\\windows\\system32\\kernelbase.dll!VirtualProtect+0x36"
                    },
                    {
                        "allocation_private_bytes": 8192,
                        "callsite_leading_bytes": "c048895424204c8bc9488d0d801f0000418d500248ff15052a00000f1f4400004883c438c3cccccccccccccccccccccc4883ec2048b880bf1acaf87f0000ffd0",
                        "callsite_trailing_bytes": "4883c420c3ec48498363e800498d4320ba2500000049c743e004000000440fb7ca4c8d05d0320000ba2b000000498943d848ff15f82a00000f1f4400004883c4",
                        "protection": "RWX",
                        "protection_provenance": "eventstests.exe",
                        "symbol_info": "c:\\windows\\system32\\dabapi.dll!DabApiBufferFree+0x10"
                    },
                    {
                        "symbol_info": "Unknown"
                    }
                ],
                "call_stack_final_user_module": {
                    "allocation_private_bytes": 4096,
                    "code_signature": [
                        {
                            "exists": true,
                            "status": "trusted",
                            "subject_name": "Microsoft Windows",
                            "trusted": true
                        }
                    ],
                    "hash": {
                        "sha256": "0386c57d59ee1292bb74d9878358da7a0ba00e5b56ed52fd6171b9e6d29d85aa"
                    },
                    "name": "dabapi.dll",
                    "path": "c:\\windows\\system32\\dabapi.dll",
                    "protection": "RWX",
                    "protection_provenance": "eventstests.exe",
                    "protection_provenance_path": "c:\\dev\\eventstests.exe",
                    "reason": "ntdll.dll"
                },
                "call_stack_summary": "ntdll.dll|kernelbase.dll|kernel32.dll|cmd.exe|kernel32.dll|ntdll.dll"
            },
            "id": 11628
        }
    },
    "user": {
        "domain": "DESKTOP-OCG8CR6",
        "id": "S-1-5-21-3820246941-898183108-3095036578-1001",
        "name": "User"
    }
}
```
</details>

### [Fields](api.md)
- [@timestamp](api.md#@timestamp)
- [message](api.md#message)
- [Target](api.md#Target)
- [data_stream](api.md#data_stream)
- [destination](api.md#destination)
- [dll](api.md#dll)
- [ecs](api.md#ecs)
- [event](api.md#event)
- [host](api.md#host)
- [network](api.md#network)
- [process](api.md#process)
- [user](api.md#user)
# network
### Sample Event
<details>
<summary>
Click to expand
</summary>

```json
{
    "agent": {
        "id": "afd348c6-0ec9-4961-805e-8ed2fc4c043b",
        "type": "endpoint",
        "version": "8.3.0-SNAPSHOT"
    },
    "process": {
        "Ext": {
            "ancestry": [
                "YWZkMzQ4YzYtMGVjOS00OTYxLTgwNWUtOGVkMmZjNGMwNDNiLTYxMi0xMzI5MzU0OTEwOS43MzU5NDk3MDA=",
                "YWZkMzQ4YzYtMGVjOS00OTYxLTgwNWUtOGVkMmZjNGMwNDNiLTQ3Ni0xMzI5MzU0OTEwOS4zODExMTM3MDA="
            ],
            "code_signature": [
                {
                    "trusted": false,
                    "subject_name": "Google LLC",
                    "exists": true,
                    "status": "errorExpired"
                }
            ]
        },
        "parent": {
            "entity_id": "YWZkMzQ4YzYtMGVjOS00OTYxLTgwNWUtOGVkMmZjNGMwNDNiLTU4MC0xMzI5MzU0OTExMy40ODIyMTUwMDA=",
            "group_leader": {
                "entity_id": "YWZkMzQ4YzYtMGVjOS00OTYxLTgwNWUtOGVkMmZjNGMwNDNiLTU4MC0xMzI5MzU0OTExMy40ODIyMTUwMDA="
            }
        },
        "entry_leader": {
            "entity_id": "YWZkMzQ4YzYtMGVjOS00OTYxLTgwNWUtOGVkMmZjNGMwNDNiLTU4MC0xMzI5MzU0OTExMy40ODIyMTUwMDA=",
            "parent": {
                "entity_id": "YWZkMzQ4YzYtMGVjOS00OTYxLTgwNWUtOGVkMmZjNGMwNDNiLTU4MC0xMzI5MzU0OTExMy40ODIyMTUwMDA="
            }
        },
        "session_leader": {
            "entity_id": "YWZkMzQ4YzYtMGVjOS00OTYxLTgwNWUtOGVkMmZjNGMwNDNiLTU4MC0xMzI5MzU0OTExMy40ODIyMTUwMDA="
        },
        "group_leader": {
            "entity_id": "YWZkMzQ4YzYtMGVjOS00OTYxLTgwNWUtOGVkMmZjNGMwNDNiLTU4MC0xMzI5MzU0OTExMy40ODIyMTUwMDA="
        },
        "code_signature": {
            "trusted": false,
            "subject_name": "Google LLC",
            "exists": true,
            "status": "errorExpired"
        },
        "name": "GCEWindowsAgent.exe",
        "pid": 580,
        "entity_id": "YWZkMzQ4YzYtMGVjOS00OTYxLTgwNWUtOGVkMmZjNGMwNDNiLTU4MC0xMzI5MzU0OTExMy40ODIyMTUwMDA=",
        "executable": "C:\\Program Files\\Google\\Compute Engine\\agent\\GCEWindowsAgent.exe"
    },
    "destination": {
        "geo": {
            "continent_name": "North America",
            "country_iso_code": "US",
            "country_name": "United States",
            "location": {
                "lon": -97.822,
                "lat": 37.751
            }
        },
        "as": {
            "number": 15169,
            "organization": {
                "name": "GOOGLE"
            }
        },
        "address": "64.233.191.95",
        "port": 443,
        "bytes": 4923,
        "ip": "64.233.191.95"
    },
    "source": {
        "address": "10.201.0.32",
        "port": 54924,
        "bytes": 498,
        "ip": "10.201.0.32"
    },
    "dns": {
        "Ext": {
            "status": 123,
            "options": 9223372036854775808
        },
        "resolved_ip": [
            "10.10.10.10",
            "10.10.10.11"
        ],
        "question": {
            "name": "foo",
            "type": "A"
        }
    },
    "message": "Endpoint network event",
    "network": {
        "transport": "tcp",
        "type": "ipv4",
        "direction": "egress"
    },
    "@timestamp": "2022-04-04T18:52:00.6007809Z",
    "ecs": {
        "version": "1.11.0"
    },
    "data_stream": {
        "namespace": "default",
        "type": "logs",
        "dataset": "endpoint.events.network"
    },
    "host": {
        "hostname": "mgmt-win-1",
        "os": {
            "Ext": {
                "variant": "Windows Server 2019 Datacenter"
            },
            "kernel": "1809 (10.0.17763.2686)",
            "name": "Windows",
            "family": "windows",
            "type": "windows",
            "version": "1809 (10.0.17763.2686)",
            "platform": "windows",
            "full": "Windows Server 2019 Datacenter 1809 (10.0.17763.2686)"
        },
        "ip": [
            "10.201.0.32",
            "fe80::f8e6:a511:69ea:27c4",
            "127.0.0.1",
            "::1"
        ],
        "name": "mgmt-win-1",
        "id": "51b19c6c-27e3-4c80-ac2a-b72ed52c40c9",
        "mac": [
            "00-00-5E-00-53-23"
        ],
        "architecture": "x86_64"
    },
    "event": {
        "agent_id_status": "verified",
        "sequence": 36090,
        "ingested": "2022-04-04T18:52:21Z",
        "created": "2022-04-04T18:52:00.6007809Z",
        "kind": "event",
        "module": "endpoint",
        "action": "disconnect_received",
        "id": "MYfZG5h8j1qej16H+++++CFe",
        "category": [
            "network"
        ],
        "type": [
            "end"
        ],
        "dataset": "endpoint.events.network"
    },
    "user": {
        "domain": "NT AUTHORITY",
        "name": "SYSTEM",
        "id": "S-1-5-18"
    }
}
```
</details>

### [Fields](network.md)
- [@timestamp](network.md#@timestamp)
- [message](network.md#message)
- [agent](network.md#agent)
- [data_stream](network.md#data_stream)
- [destination](network.md#destination)
- [dns](network.md#dns)
- [ecs](network.md#ecs)
- [event](network.md#event)
- [group](network.md#group)
- [host](network.md#host)
- [http](network.md#http)
- [network](network.md#network)
- [process](network.md#process)
- [source](network.md#source)
- [user](network.md#user)
# metrics
### Sample Event
<details>
<summary>
Click to expand
</summary>

```json
{
    "agent": {
        "build": {
            "original": "version: 8.3.0-SNAPSHOT, compiled: Fri Apr 1 06:00:00 2022, branch: main, commit: f8b0ed879ad40ee1ae561ced31ec8a4027a2bf53"
        },
        "id": "4c9c9cb3-f80f-44d8-9c89-6168243b7f21",
        "type": "endpoint",
        "version": "8.3.0-SNAPSHOT"
    },
    "message": "Endpoint metrics",
    "@timestamp": "2022-04-04T18:38:15.7178887Z",
    "Endpoint": {
        "metrics": {
            "system_impact": [
                {
                    "file_events": {
                        "week_ms": 418
                    },
                    "process": {
                        "code_signature": [
                            {
                                "trusted": true,
                                "subject_name": "Microsoft Windows Publisher",
                                "exists": true,
                                "status": "trusted"
                            }
                        ],
                        "executable": "C:\\Windows\\System32\\svchost.exe"
                    },
                    "malware": {
                        "week_ms": 7483
                    },
                    "process_events": {
                        "week_ms": 78
                    },
                    "registry_events": {
                        "week_ms": 248
                    },
                    "dns_events": {
                        "week_ms": 16
                    },
                    "network_events": {
                        "week_ms": 8
                    },
                    "overall": {
                        "week_ms": 11744
                    },
                    "authentication_events": {
                        "week_ms": 155
                    },
                    "library_load_events": {
                        "week_ms": 3028
                    },
                    "cred_access_events": {
                        "week_ms": 10
                    },
                    "threat_intelligence_events": {
                        "week_ms": 250
                    },
                    "win32k_events": {
                        "week_ms": 50
                    }
                },
                {
                    "file_events": {
                        "week_ms": 46
                    },
                    "process": {
                        "code_signature": [
                            {
                                "trusted": true,
                                "subject_name": "Microsoft Windows",
                                "exists": true,
                                "status": "trusted"
                            }
                        ],
                        "executable": "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe"
                    },
                    "malware": {
                        "week_ms": 2
                    },
                    "process_events": {
                        "week_ms": 19
                    },
                    "registry_events": {
                        "week_ms": 3
                    },
                    "overall": {
                        "week_ms": 8290
                    },
                    "library_load_events": {
                        "week_ms": 7890
                    },
                    "cred_access_events": {
                        "week_ms": 20
                    },
                    "threat_intelligence_events": {
                        "week_ms": 300
                    },
                    "win32k_events": {
                        "week_ms": 10
                    }
                },
                {
                    "file_events": {
                        "week_ms": 1641
                    },
                    "process": {
                        "code_signature": [
                            {
                                "trusted": true,
                                "subject_name": "Elasticsearch, Inc.",
                                "exists": true,
                                "status": "trusted"
                            }
                        ],
                        "executable": "C:\\Program Files\\Winlogbeat\\winlogbeat.exe"
                    },
                    "malware": {
                        "week_ms": 2589
                    },
                    "process_events": {
                        "week_ms": 419
                    },
                    "registry_events": {
                        "week_ms": 1
                    },
                    "network_events": {
                        "week_ms": 32
                    },
                    "overall": {
                        "week_ms": 5046
                    },
                    "library_load_events": {
                        "week_ms": 4
                    },
                    "threat_intelligence_events": {
                        "week_ms": 360
                    }
                },
                {
                    "file_events": {
                        "week_ms": 2
                    },
                    "process": {
                        "code_signature": [
                            {
                                "trusted": true,
                                "subject_name": "Microsoft Windows Publisher",
                                "exists": true,
                                "status": "trusted"
                            }
                        ],
                        "executable": "C:\\Windows\\System32\\lsass.exe"
                    },
                    "process_events": {
                        "week_ms": 3
                    },
                    "registry_events": {
                        "week_ms": 83
                    },
                    "overall": {
                        "week_ms": 4761
                    },
                    "authentication_events": {
                        "week_ms": 3177
                    },
                    "library_load_events": {
                        "week_ms": 26
                    },
                    "cred_access_events": {
                        "week_ms": 1350
                    },
                    "threat_intelligence_events": {
                        "week_ms": 120
                    }
                },
                {
                    "process": {
                        "code_signature": [
                            {
                                "trusted": true,
                                "subject_name": "Microsoft Windows",
                                "exists": true,
                                "status": "trusted"
                            }
                        ],
                        "executable": "C:\\Windows\\System32\\conhost.exe"
                    },
                    "malware": {
                        "week_ms": 16
                    },
                    "process_events": {
                        "week_ms": 26
                    },
                    "registry_events": {
                        "week_ms": 3
                    },
                    "overall": {
                        "week_ms": 3261
                    },
                    "library_load_events": {
                        "week_ms": 2966
                    },
                    "threat_intelligence_events": {
                        "week_ms": 250
                    }
                },
                {
                    "file_events": {
                        "week_ms": 51
                    },
                    "process": {
                        "code_signature": [
                            {
                                "exists": false,
                                "status": "errorCode_endpoint: Initital state, no attempt to load signature was made"
                            }
                        ],
                        "executable": "System"
                    },
                    "malware": {
                        "week_ms": 1978
                    },
                    "overall": {
                        "week_ms": 2029
                    }
                },
                {
                    "process": {
                        "code_signature": [
                            {
                                "exists": false
                            }
                        ],
                        "executable": "C:\\Windows\\assembly\\NativeImages_v4.0.30319_64\\System.Web\\e266326169887aa7cb26b9e2aa421ee4\\System.Web.ni.dll"
                    },
                    "malware": {
                        "week_ms": 1015
                    },
                    "overall": {
                        "week_ms": 1015
                    }
                },
                {
                    "file_events": {
                        "week_ms": 8
                    },
                    "process": {
                        "code_signature": [
                            {
                                "trusted": true,
                                "subject_name": "Elasticsearch, Inc.",
                                "exists": true,
                                "status": "trusted"
                            }
                        ],
                        "executable": "C:\\Program Files\\Elastic\\Agent\\data\\elastic-agent-e80913\\install\\metricbeat-8.3.0-SNAPSHOT-windows-x86_64\\metricbeat.exe"
                    },
                    "process_events": {
                        "week_ms": 502
                    },
                    "dns_events": {
                        "week_ms": 84
                    },
                    "network_events": {
                        "week_ms": 1
                    },
                    "overall": {
                        "week_ms": 1162
                    },
                    "library_load_events": {
                        "week_ms": 417
                    },
                    "threat_intelligence_events": {
                        "week_ms": 150
                    }
                },
                {
                    "process": {
                        "code_signature": [
                            {
                                "trusted": false,
                                "subject_name": "Google LLC",
                                "exists": true,
                                "status": "errorExpired"
                            }
                        ],
                        "executable": "C:\\Program Files\\Google\\Compute Engine\\agent\\GCEWindowsAgent.exe"
                    },
                    "malware": {
                        "week_ms": 627
                    },
                    "process_events": {
                        "week_ms": 89
                    },
                    "registry_events": {
                        "week_ms": 2
                    },
                    "dns_events": {
                        "week_ms": 7
                    },
                    "network_events": {
                        "week_ms": 8
                    },
                    "overall": {
                        "week_ms": 1068
                    },
                    "library_load_events": {
                        "week_ms": 85
                    },
                    "threat_intelligence_events": {
                        "week_ms": 250
                    }
                },
                {
                    "process": {
                        "code_signature": [
                            {
                                "exists": false
                            }
                        ],
                        "executable": "C:\\Windows\\assembly\\NativeImages_v4.0.30319_64\\Microsoft.P521220ea#\\39ce4aafe1a3bc56fb1435f6550dd7a3\\Microsoft.PowerShell.Commands.Utility.ni.dll"
                    },
                    "malware": {
                        "week_ms": 760
                    },
                    "overall": {
                        "week_ms": 760
                    }
                },
                {
                    "file_events": {
                        "week_ms": 15
                    },
                    "process": {
                        "code_signature": [
                            {
                                "exists": false
                            }
                        ],
                        "executable": "C:\\Program Files\\metricbeat-7.10.0-windows-x86_64\\metricbeat.exe"
                    },
                    "malware": {
                        "week_ms": 29
                    },
                    "process_events": {
                        "week_ms": 634
                    },
                    "registry_events": {
                        "week_ms": 1
                    },
                    "dns_events": {
                        "week_ms": 8
                    },
                    "network_events": {
                        "week_ms": 4
                    },
                    "overall": {
                        "week_ms": 744
                    },
                    "library_load_events": {
                        "week_ms": 3
                    },
                    "threat_intelligence_events": {
                        "week_ms": 50
                    }
                },
                {
                    "process": {
                        "code_signature": [
                            {
                                "trusted": true,
                                "subject_name": "Microsoft Windows",
                                "exists": true,
                                "status": "trusted"
                            }
                        ],
                        "executable": "C:\\Windows\\System32\\spoolsv.exe"
                    },
                    "process_events": {
                        "week_ms": 8
                    },
                    "registry_events": {
                        "week_ms": 40
                    },
                    "overall": {
                        "week_ms": 795
                    },
                    "library_load_events": {
                        "week_ms": 627
                    },
                    "threat_intelligence_events": {
                        "week_ms": 120
                    }
                },
                {
                    "process": {
                        "code_signature": [
                            {
                                "trusted": true,
                                "subject_name": "Elasticsearch, Inc.",
                                "exists": true,
                                "status": "trusted"
                            }
                        ],
                        "executable": "C:\\Program Files\\Packetbeat\\packetbeat.exe"
                    },
                    "malware": {
                        "week_ms": 74
                    },
                    "process_events": {
                        "week_ms": 432
                    },
                    "registry_events": {
                        "week_ms": 1
                    },
                    "network_events": {
                        "week_ms": 1
                    },
                    "overall": {
                        "week_ms": 599
                    },
                    "library_load_events": {
                        "week_ms": 61
                    },
                    "threat_intelligence_events": {
                        "week_ms": 30
                    }
                },
                {
                    "file_events": {
                        "week_ms": 20
                    },
                    "process": {
                        "code_signature": [
                            {
                                "trusted": true,
                                "subject_name": "Microsoft Corporation",
                                "exists": true,
                                "status": "trusted"
                            },
                            {
                                "trusted": true,
                                "subject_name": "Microsoft Corporation",
                                "exists": true,
                                "status": "trusted"
                            }
                        ],
                        "executable": "C:\\Windows\\Microsoft.NET\\Framework64\\v4.0.30319\\csc.exe"
                    },
                    "malware": {
                        "week_ms": 350
                    },
                    "process_events": {
                        "week_ms": 19
                    },
                    "registry_events": {
                        "week_ms": 1
                    },
                    "overall": {
                        "week_ms": 480
                    },
                    "library_load_events": {
                        "week_ms": 70
                    },
                    "threat_intelligence_events": {
                        "week_ms": 20
                    }
                },
                {
                    "file_events": {
                        "week_ms": 6
                    },
                    "process": {
                        "code_signature": [
                            {
                                "trusted": true,
                                "subject_name": "Elasticsearch, Inc.",
                                "exists": true,
                                "status": "trusted"
                            }
                        ],
                        "executable": "C:\\Program Files\\Elastic\\Agent\\data\\elastic-agent-e80913\\install\\filebeat-8.3.0-SNAPSHOT-windows-x86_64\\filebeat.exe"
                    },
                    "process_events": {
                        "week_ms": 395
                    },
                    "dns_events": {
                        "week_ms": 51
                    },
                    "network_events": {
                        "week_ms": 2
                    },
                    "overall": {
                        "week_ms": 494
                    },
                    "threat_intelligence_events": {
                        "week_ms": 40
                    }
                },
                {
                    "process": {
                        "code_signature": [
                            {
                                "trusted": true,
                                "subject_name": "Google LLC",
                                "exists": true,
                                "status": "trusted"
                            }
                        ],
                        "executable": "C:\\Program Files\\Google\\Compute Engine\\vss\\GoogleVssProvider.dll"
                    },
                    "malware": {
                        "week_ms": 439
                    },
                    "overall": {
                        "week_ms": 439
                    }
                },
                {
                    "process": {
                        "code_signature": [
                            {
                                "trusted": true,
                                "subject_name": "Microsoft Windows",
                                "exists": true,
                                "status": "trusted"
                            }
                        ],
                        "executable": "C:\\Windows\\System32\\VSSVC.exe"
                    },
                    "malware": {
                        "week_ms": 45
                    },
                    "process_events": {
                        "week_ms": 13
                    },
                    "registry_events": {
                        "week_ms": 124
                    },
                    "overall": {
                        "week_ms": 476
                    },
                    "authentication_events": {
                        "week_ms": 8
                    },
                    "library_load_events": {
                        "week_ms": 216
                    },
                    "threat_intelligence_events": {
                        "week_ms": 70
                    }
                },
                {
                    "process": {
                        "code_signature": [
                            {
                                "trusted": true,
                                "subject_name": "Microsoft Windows",
                                "exists": true,
                                "status": "trusted"
                            }
                        ],
                        "executable": "C:\\Windows\\SYSTEM32\\mispace.dll"
                    },
                    "malware": {
                        "week_ms": 353
                    },
                    "overall": {
                        "week_ms": 353
                    }
                },
                {
                    "process": {
                        "code_signature": [
                            {
                                "exists": false
                            }
                        ],
                        "executable": "C:\\Windows\\assembly\\NativeImages_v4.0.30319_64\\System.Web.28b9ef5a#\\b1cbeb46534d9974961496306f2f1a28\\System.Web.Extensions.ni.dll"
                    },
                    "malware": {
                        "week_ms": 305
                    },
                    "overall": {
                        "week_ms": 305
                    }
                },
                {
                    "file_events": {
                        "week_ms": 25
                    },
                    "process": {
                        "code_signature": [
                            {
                                "trusted": true,
                                "subject_name": "Microsoft Windows",
                                "exists": true,
                                "status": "trusted"
                            }
                        ],
                        "executable": "C:\\Windows\\System32\\wbem\\WMIADAP.exe"
                    },
                    "malware": {
                        "week_ms": 247
                    },
                    "process_events": {
                        "week_ms": 4
                    },
                    "registry_events": {
                        "week_ms": 5
                    },
                    "overall": {
                        "week_ms": 345
                    },
                    "library_load_events": {
                        "week_ms": 14
                    },
                    "threat_intelligence_events": {
                        "week_ms": 50
                    }
                }
            ],
            "memory": {
                "endpoint": {
                    "private": {
                        "mean": 288590259,
                        "latest": 493723648
                    }
                }
            },
            "disks": [
                {
                    "endpoint_drive": true,
                    "total": 53564403712,
                    "free": 25891106816,
                    "device": "\\Device\\HarddiskVolume3",
                    "mount": "C:\\",
                    "fstype": "NTFS"
                },
                {
                    "total": 100663296,
                    "free": 73579520,
                    "device": "\\Device\\HarddiskVolume2",
                    "mount": "",
                    "fstype": "FAT32"
                }
            ],
            "documents_volume": {
                "file_events": {
                    "suppressed_count": 0,
                    "suppressed_bytes": 0,
                    "sent_count": 3485,
                    "sent_bytes": 7302875
                },
                "security_events": {
                    "suppressed_count": 0,
                    "suppressed_bytes": 0,
                    "sent_count": 259,
                    "sent_bytes": 422247
                },
                "library_events": {
                    "suppressed_count": 0,
                    "suppressed_bytes": 0,
                    "sent_count": 114,
                    "sent_bytes": 287954
                },
                "process_events": {
                    "suppressed_count": 0,
                    "suppressed_bytes": 0,
                    "sent_count": 201,
                    "sent_bytes": 602914
                },
                "registry_events": {
                    "suppressed_count": 0,
                    "suppressed_bytes": 0,
                    "sent_count": 605,
                    "sent_bytes": 1288593
                },
                "dns_events": {
                    "suppressed_count": 0,
                    "suppressed_bytes": 0,
                    "sent_count": 5250,
                    "sent_bytes": 11364752
                },
                "network_events": {
                    "suppressed_count": 0,
                    "suppressed_bytes": 0,
                    "sent_count": 1753,
                    "sent_bytes": 3479631
                },
                "overall": {
                    "suppressed_count": 0,
                    "suppressed_bytes": 0,
                    "sent_count": 11667,
                    "sent_bytes": 24748966
                }
            },
            "cpu": {
                "endpoint": {
                    "mean": 0.324235176435677,
                    "latest": 62.6406111450215
                }
            },
            "threads": [
                {
                    "name": "actionsAPIThread",
                    "cpu": {
                        "mean": 0.00456829602558246
                    }
                },
                {
                    "name": "stateReportThread",
                    "cpu": {
                        "mean": 0.0
                    }
                },
                {
                    "name": "KernelSyncMessageThread",
                    "cpu": {
                        "mean": 0.0
                    }
                },
                {
                    "name": "KernelSyncMessageThread",
                    "cpu": {
                        "mean": 0.0
                    }
                },
                {
                    "name": "KernelSyncMessageThread",
                    "cpu": {
                        "mean": 0.0
                    }
                },
                {
                    "name": "checkinAPIThread",
                    "cpu": {
                        "mean": 0.0365463682046597
                    }
                },
                {
                    "name": "KernelAsyncMessageQueueConsumerThread",
                    "cpu": {
                        "mean": 0.0
                    }
                },
                {
                    "name": "KernelSyncMessageThread",
                    "cpu": {
                        "mean": 0.0
                    }
                },
                {
                    "name": "KernelSyncMessageThread",
                    "cpu": {
                        "mean": 0.0
                    }
                },
                {
                    "name": "Cron",
                    "cpu": {
                        "mean": 0.0
                    }
                },
                {
                    "name": "File Cache",
                    "cpu": {
                        "mean": 0.0
                    }
                },
                {
                    "name": "FileLogThread",
                    "cpu": {
                        "mean": 0.0
                    }
                },
                {
                    "name": "LoggingLimitThread",
                    "cpu": {
                        "mean": 0.0
                    }
                },
                {
                    "name": "CredentialAccessEventDispatcherThread",
                    "cpu": {
                        "mean": 0.0
                    }
                },
                {
                    "name": "KernelPortConsumerThread",
                    "cpu": {
                        "mean": 0.00456454263282819
                    }
                },
                {
                    "name": "KernelPortConsumerThread",
                    "cpu": {
                        "mean": 0.00456454263282819
                    }
                },
                {
                    "name": "RulesEngineThread",
                    "cpu": {
                        "mean": 0.0091324200913242
                    }
                },
                {
                    "name": "KernelPortConsumerThread",
                    "cpu": {
                        "mean": 0.0
                    }
                },
                {
                    "name": "KernelAsyncMessageQueueConsumerThread",
                    "cpu": {
                        "mean": 0.00456454263282819
                    }
                },
                {
                    "name": "KernelSyncQueueConsumerThread",
                    "cpu": {
                        "mean": 0.0
                    }
                },
                {
                    "name": "KernelSyncMessageThread",
                    "cpu": {
                        "mean": 0.0
                    }
                },
                {
                    "name": "DocumentLoggingThread",
                    "cpu": {
                        "mean": 0.0
                    }
                },
                {
                    "name": "DocumentLoggingMaintenance",
                    "cpu": {
                        "mean": 0.0
                    }
                },
                {
                    "name": "BulkConsumerThread",
                    "cpu": {
                        "mean": 0.00455871626549964
                    }
                },
                {
                    "name": "DocumentLoggingConsumerThread",
                    "cpu": {
                        "mean": 0.113967906637491
                    }
                },
                {
                    "name": "DocumentLoggingLimitThread",
                    "cpu": {
                        "mean": 0.0
                    }
                },
                {
                    "name": "KernelSyncMessageThread",
                    "cpu": {
                        "mean": 0.0
                    }
                },
                {
                    "name": "KernelSyncMessageThread",
                    "cpu": {
                        "mean": 0.022822713164141
                    }
                },
                {
                    "name": "KernelSyncMessageThread",
                    "cpu": {
                        "mean": 0.0
                    }
                },
                {
                    "name": "KernelSyncMessageThread",
                    "cpu": {
                        "mean": 0.0
                    }
                },
                {
                    "name": "KernelSyncMessageThread",
                    "cpu": {
                        "mean": 0.0
                    }
                },
                {
                    "name": "KernelSyncMessageThread",
                    "cpu": {
                        "mean": 0.022822713164141
                    }
                },
                {
                    "name": "KernelSyncMessageThread",
                    "cpu": {
                        "mean": 0.0
                    }
                },
                {
                    "name": "KernelSyncMessageThread",
                    "cpu": {
                        "mean": 0.0
                    }
                },
                {
                    "name": "KernelSyncMessageThread",
                    "cpu": {
                        "mean": 0.0
                    }
                },
                {
                    "name": "KernelSyncMessageThread",
                    "cpu": {
                        "mean": 0.0
                    }
                },
                {
                    "name": "KernelSyncMessageThread",
                    "cpu": {
                        "mean": 0.0
                    }
                },
                {
                    "name": "ArtifactManifestDownload",
                    "cpu": {
                        "mean": 0.12311901504788
                    }
                },
                {
                    "name": "PolicyReloadThread",
                    "cpu": {
                        "mean": 0.0
                    }
                },
                {
                    "name": "CredentialAccessClassifierThread",
                    "cpu": {
                        "mean": 0.0
                    }
                },
                {
                    "name": "KernelPortConsumerThread",
                    "cpu": {
                        "mean": 0.0136936278984846
                    }
                },
                {
                    "name": "PerformanceMonitorWorkerThread",
                    "cpu": {
                        "mean": 0.00912200684150513
                    }
                },
                {
                    "name": "MetadataThread",
                    "cpu": {
                        "mean": 0.0
                    }
                },
                {
                    "name": "EventsQueueThread",
                    "cpu": {
                        "mean": 0.0729760547320411
                    }
                },
                {
                    "name": "DelayedAlertEnrichment",
                    "cpu": {
                        "mean": 0.0
                    }
                },
                {
                    "name": "MaintainProcessMap",
                    "cpu": {
                        "mean": 0.0
                    }
                },
                {
                    "name": "FileScoreThread",
                    "cpu": {
                        "mean": 0.0
                    }
                },
                {
                    "name": "DiagnosticMalwareThread",
                    "cpu": {
                        "mean": 0.0
                    }
                },
                {
                    "name": "QuarantineManagerWorkerThread",
                    "cpu": {
                        "mean": 0.0
                    }
                },
                {
                    "name": "EventProcessingThread",
                    "cpu": {
                        "mean": 0.0
                    }
                },
                {
                    "name": "HostIsolationMonitorThread",
                    "cpu": {
                        "mean": 0.0
                    }
                },
                {
                    "name": "serviceCommsThread",
                    "cpu": {
                        "mean": 0.0
                    }
                },
                {
                    "name": "grpcConnectionManagerThread",
                    "cpu": {
                        "mean": 0.0
                    }
                },
                {
                    "name": "RansomwareGlobalUserThread"
                },
                {
                    "name": "RansomwareProcessMonitorThread"
                },
                {
                    "name": "RansomwareFileCacheCleanupThread"
                },
                {
                    "name": "RansomwareParseUnverifiedThread"
                },
                {
                    "name": "RansomwareLuaVerifiedThread"
                }
            ],
            "uptime": {
                "endpoint": 21930,
                "system": 21992
            }
        }
    },
    "ecs": {
        "version": "1.11.0"
    },
    "data_stream": {
        "namespace": "default",
        "type": "metrics",
        "dataset": "endpoint.metrics"
    },
    "host": {
        "hostname": "data-viz-win-1",
        "os": {
            "Ext": {
                "variant": "Windows Server 2019 Datacenter"
            },
            "kernel": "1809 (10.0.17763.2686)",
            "name": "Windows",
            "family": "windows",
            "type": "windows",
            "version": "1809 (10.0.17763.2686)",
            "platform": "windows",
            "full": "Windows Server 2019 Datacenter 1809 (10.0.17763.2686)"
        },
        "ip": [
            "10.201.0.13",
            "fe80::f40a:aed0:618a:972d",
            "127.0.0.1",
            "::1"
        ],
        "name": "data-viz-win-1",
        "id": "2beebb8e-e5f0-46ca-8635-97ba7bb8ccca",
        "mac": [
            "00-00-5E-00-53-23"
        ],
        "architecture": "x86_64"
    },
    "event": {
        "agent_id_status": "verified",
        "sequence": 35124,
        "ingested": "2022-04-04T18:38:16Z",
        "created": "2022-04-04T18:38:15.7178887Z",
        "kind": "metric",
        "module": "endpoint",
        "action": "endpoint_metrics",
        "id": "MYfZG00oEwD2/fqT+++++Byi",
        "category": [
            "host"
        ],
        "type": [
            "info"
        ],
        "dataset": "endpoint.metrics"
    }
}
```
</details>

### [Fields](metrics.md)
- [@timestamp](metrics.md#@timestamp)
- [message](metrics.md#message)
- [Endpoint](metrics.md#Endpoint)
- [agent](metrics.md#agent)
- [data_stream](metrics.md#data_stream)
- [ecs](metrics.md#ecs)
- [event](metrics.md#event)
- [host](metrics.md#host)
