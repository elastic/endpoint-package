# Elastic Defend Integration

Elastic Defend provides organizations with prevention, detection, and response capabilities across Windows, macOS, and Linux operating systems running on both traditional endpoints and public cloud environments. ​​Use Elastic Defend to:

- **Prevent complex attacks** - Prevent malware (Windows, macOS, Linux) and ransomware (Windows) from executing, and stop advanced threats with malicious behavior (Windows, macOS, Linux), memory threat (Windows, macOS, Linux), and credential hardening (Windows) protections. All powered by [Elastic Labs](https://www.elastic.co/security-labs/) and our global community.
- **Alert in high fidelity** - Bolster team efficacy by detecting threats centrally and minimizing false positives via extensive corroboration.
- **Detect threats in high fidelity** - Elastic Defend facilitates deep visibility by instrumenting the process, file, and network data in your environments with minimal data collection overhead.
- **Triage and respond rapidly** - Quickly analyze detailed data from across your hosts. Examine host-based activity with interactive visualizations. Invoke remote response actions across distributed endpoints. Extend investigation capabilities even further with the Osquery integration, fully integrated into Elastic Security workflows.
- **Secure your cloud workloads** - Stop threats targeting cloud workloads and cloud-native applications. Gain real-time visibility and control with a lightweight user-space agent, powered by eBPF. Automate the identification of cloud threats with detection rules and machine learning (ML). Achieve rapid time-to-value with MITRE ATT&CK-aligned detections honed by Elastic Security Labs. 
- **View terminal sessions** - Give your security team a unique and powerful investigative tool for digital forensics and incident response (DFIR), reducing the mean time to respond (MTTR). Session view provides a time-ordered series of process executions in your Linux workloads in the form of a terminal shell, as well as the ability to replay the terminal session.

**Installation guide**
For in-depth, step-by-step instructions to help you get started with Elastic Defend, read through our [installation guide](https://www.elastic.co/guide/en/security/current/install-endpoint.html). For macOS endpoints, we recommend reviewing our documentation on [enabling full disk access](https://www.elastic.co/guide/en/security/current/deploy-elastic-endpoint.html#enable-fda-endpoint).

## Compatibility

For compatibility information view our [documentation](https://www.elastic.co/guide/en/security/current/index.html).

## Logs

The log type of documents are stored in the `logs-endpoint.*` indices. The following sections define the mapped fields
sent by the endpoint.

### alerts

{{fields "alerts"}}

### file

{{fields "file"}}

### library

{{fields "library"}}

### network

{{fields "network"}}

### process

{{fields "process"}}

### registry

{{fields "registry"}}

### security

{{fields "security"}}

## Metrics

The metrics type of documents are stored in `metrics-endpoint.*` indices. The following sections define the mapped fields
sent by the endpoint.

### metadata

{{fields "metadata"}}

### metrics

Metrics documents contain performance information about the endpoint executable and the host it is running on.

{{fields "metrics"}}

### policy response

{{fields "policy"}}
