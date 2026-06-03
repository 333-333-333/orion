# TR-ORION-INFOSEC-PAIR-P023_P024

Spec refs: TASK-INFOSEC-PAIR-SMOKE-P023_P024; FUN-INFOSEC-PAIR-SMOKE AC-1..3; CON-NO-INFOSEC-3K AC-1; BR-INFOSEC-PAIR-SMOKE-001..003.

Objetivo: medir precisión observada de pipeline actual para párrafos p023, p024 sin expected domain inventado.

Fixtures leídos:
- p023: A malware infection is a type of security incident. A phishing attack is a type of social engineering incident. A ransomware attack is a type of malware incident. A data breach is a type of security incident that involves unauthorized access to or disclosure of data. A denial-of-service attack is a ...
- p024: Business continuity and disaster recovery protect the organization against major disruptions. Business continuity is the capability to continue critical operations during disruption. Disaster recovery is the process of restoring technology services after a disruptive event. A business impact analysi...

Artifacts esperados: observed_p023_p024_semantic_claims.json, observed_p023_p024_graph_model.json, observed_p023_p024_output.rdf, observed_p023_p024_metrics.json.
