# Elastic Defend integration

## Overview

Elastic Defend provides endpoint security capabilities including prevention, detection, investigation, and response for Windows, macOS, and Linux hosts. It protects endpoints while collecting high-fidelity system telemetry.

This telemetry is analyzed within Elastic’s security analytics platform, allowing security teams to monitor endpoint activity and investigate threats as part of their broader security operations workflows. Elastic Defend forms a core component of Elastic Security’s XDR capabilities.

With Elastic Defend, teams can:

* Prevent malware, ransomware, and behavioral threats
* Detect advanced attacker techniques using high-fidelity endpoint telemetry
* Investigate threats with full process, file, and network visibility
* Respond quickly with integrated response actions
* Correlate endpoint activity with cloud, network, and identity telemetry with Elastic Security XDR

## How Elastic Defend powers XDR

Elastic Defend supports Elastic Security’s XDR capabilities by feeding deep endpoint telemetry into Elastic’s security analytics platform. Because endpoint data is stored alongside cloud, identity, and network telemetry, security teams can correlate activity across domains and detect attacks that span multiple systems.

Defend enables this by:

* Providing kernel level host telemetry (process, file, memory, network) that captures activity at the point of execution
* Automatically mapping endpoint activity to the Elastic Common Schema (ECS), allowing for immediate correlation with identity, network, and cloud provider signals
* Supporting detection of multi-stage attacks across users, hosts, and cloud services
* Enriching alerts with endpoint context and visualizations—like process trees and timelines—to reconstruct full attack activity
* Integrating response actions—like host isolation and process termination—directly into detection workflows to reduce time-to-resolution

## Capabilities 

### Prevention 

Elastic Defend applies a layered defense strategy at the endpoint, combining signature-based and behavioral protections to disrupt attacks at every stage. Rather than relying on a single detection approach, multiple protective layers work together to maintain resilience as attacker tradecraft evolves. Protections are continuously refined to stay ahead of emerging threats and include:

* Kernel-level visibility and enforcement
* Malware and ransomware protection
* Behavior-based threat prevention
* Memory threat protection

### Detection 

Elastic Defend delivers high-confidence detection by unifying deep endpoint telemetry with Elastic Security’s analytics platform. Behavioral detections, machine learning, and cross-domain correlation work together to uncover advanced threats that span users, hosts, cloud, and network environments. This approach is built on:

* Rich endpoint telemetry, including process, file, and network activity
* Behavior-based detections aligned to MITRE ATT&CK
* Integration with Elastic Security detection rules and machine learning
* Correlation with signals from other data sources

### Investigation & response 

When a threat is detected, Elastic Defend helps security teams investigate attacker activity and respond quickly to minimize impact. Capabilities include:

* Centralized alert triage and investigation
* Visual reconstruction of attack activity through process tree and timeline views
* Host isolation to contain active threats
* Process termination to disrupt malicious activity
* Remote response actions across distributed endpoints

Elastic Security also includes built-in forensic capabilities that allow responders to collect investigative artifacts directly from affected hosts during an incident. Analysts can capture memory snapshots using Elastic Defend or leverage [Osquery Manager](https://www.elastic.co/docs/solutions/security/investigate/osquery) to retrieve critical host artifacts such as system logs, process listings, startup items, and other execution evidence used in incident response.

Elastic extends [Osquery’s](https://www.elastic.co/docs/reference/integrations/osquery_manager) capabilities with additional artifact-focused tables for evidence such as browser history, AMCache data, and jumplists, along with prebuilt forensic queries that help investigators quickly gather relevant artifacts across Windows, macOS, and Linux systems.

## How it works 

Elastic Defend runs as part of [Elastic Agent](https://www.elastic.co/docs/reference/fleet) and sends endpoint telemetry to Elasticsearch, where it is analyzed and correlated with other security data.

Elastic Defend uses the Elastic Common Schema (ECS), allowing endpoint data to efficiently correlate with other telemetry sources. This unified data model enables cross-domain detections, streamlined investigations, and integrated response within a single platform.

## Data collected

Elastic Defend collects selective data on system activities to detect and prevent as many threats as possible, while balancing storage and performance overhead.

* Process execution events
* File creation and modification
* Network connections
* Security alerts and detections
* Host metadata

Data is stored in indices such as:
* `logs-endpoint.events.*`
* `logs-endpoint.alerts.*`

For additional insight into Elastic Defend’s data collection and events captured, see [Event capture and Elastic Defend](https://www.elastic.co/docs/solutions/security/manage-elastic-defend/event-capture-elastic-defend).

## Requirements and installation

### Compatibility 
> **Note:**
> Elastic Defend does not support deployment within an Elastic Agent DaemonSet in Kubernetes. For these use cases, use [Defend for Containers](https://www.elastic.co/docs/reference/integrations/cloud_defend).

For system requirements information, [refer to our documentation](https://www.elastic.co/docs/solutions/security/configure-elastic-defend/elastic-defend-requirements).

### Installation

To install Elastic Defend, follow these steps: 

1. From Kibana, click **Add integrations**. 
2. Select **Elastic Defend**.  
3. Add the integration to an agent policy. 
4. Enroll Elastic Agent on your hosts.  
5. Verify endpoint telemetry in the Elastic Security app.   

For in-depth, step-by-step instructions to help you get started with Elastic Defend, read through [our installation guide](https://www.elastic.co/docs/solutions/security/configure-elastic-defend/install-elastic-defend).

## Licensing 

### Elastic Cloud Hosted 

| Capability | Free and open - Basic | Platinum | Enterprise |
|---|---|---|---|
| Elastic Defend enabled telemetry and event collection | ✅ | ✅ | ✅ |
| Malware prevention | ✅ | ✅ | ✅ |
| Admin defined endpoint blocklist | ✅ | ✅ | ✅ |
| Ransomware prevention | - | ✅ | ✅ |
| Malicious behavior protection | - | ✅ | ✅ |
| Memory threat protection | - | ✅ | ✅ |
| Self healing | - | ✅ | ✅ |
| Per Policy configuration | - | ✅ | ✅ |
| Host isolation | - | ✅ | ✅ |
| Tamper Protection | - | ✅ | ✅ |
| Interactive Response Console | - | - | ✅ |
| Device Control | - | - | ✅ |
| Artifact upgrade control | - | - | ✅ |

### Serverless

| Capability | Security Complete (No endpoint add on) | Endpoint Protection Essentials | Endpoint Protection Complete |
|---|---|---|---|
| Elastic Defend enabled telemetry and event collection | ✅ | ✅ | ✅ |
| Malware prevention | - | ✅ | ✅ |
| Admin defined endpoint blocklist | - | ✅ | ✅ |
| Ransomware prevention | - | ✅ | ✅ |
| Malicious behavior protection | - | ✅ | ✅ |
| Memory threat protection | - | ✅ | ✅ |
| Self healing | - | ✅ | ✅ |
| Per Policy configuration | - | ✅ | ✅ |
| Host isolation | - | ✅ | ✅ |
| Tamper Protection | - | - | ✅ |
| Interactive Response Console | - | - | ✅ |
| Device Control | - | - | ✅ |
| Artifact upgrade control | - | - | ✅ |

## Logs

The log type of documents are stored in the `logs-endpoint.*` indices. The following sections define the mapped fields
sent by the endpoint.

### alerts

<dropdown title="Exported fields">

{{fields "alerts"}}

</dropdown>

### file

<dropdown title="Exported fields">

{{fields "file"}}

</dropdown>

### library

<dropdown title="Exported fields">

{{fields "library"}}

</dropdown>

### network

<dropdown title="Exported fields">

{{fields "network"}}

</dropdown>

### process

<dropdown title="Exported fields">

{{fields "process"}}

</dropdown>

### registry

<dropdown title="Exported fields">

{{fields "registry"}}

</dropdown>

### security

<dropdown title="Exported fields">

{{fields "security"}}

</dropdown>

## Metrics

The metrics type of documents are stored in `metrics-endpoint.*` indices. The following sections define the mapped fields
sent by the endpoint.

### metadata

<dropdown title="Exported fields">

{{fields "metadata"}}

</dropdown>

### metrics

Metrics documents contain performance information about the endpoint executable and the host it is running on.

<dropdown title="Exported fields">

{{fields "metrics"}}

</dropdown>

### policy response

<dropdown title="Exported fields">

{{fields "policy"}}

</dropdown>
