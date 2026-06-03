# TR-ORION-INFOSEC-PAIR-P017_P018

Spec refs: TASK-INFOSEC-PAIR-SMOKE-P017_P018; FUN-INFOSEC-PAIR-SMOKE AC-1..3; CON-NO-INFOSEC-3K AC-1; BR-INFOSEC-PAIR-SMOKE-001..003.

Objetivo: medir precisión observada de pipeline actual para párrafos p017, p018 sin expected domain inventado.

Fixtures leídos:
- p017: Cloud security protects cloud services, cloud infrastructure, cloud workloads, and cloud data. A cloud account is an administrative boundary for cloud resources. A cloud workload is a type of computing resource hosted in a cloud environment. A virtual machine is a type of cloud workload. A container...
- p018: Cryptography protects information through mathematical techniques. Encryption is a cryptographic mechanism that protects confidentiality. Decryption is the process that converts encrypted data back into readable data. A cryptographic key is a value used by a cryptographic algorithm. Symmetric encryp...

Artifacts esperados: observed_p017_p018_semantic_claims.json, observed_p017_p018_graph_model.json, observed_p017_p018_output.rdf, observed_p017_p018_metrics.json.
