# TR-ORION-INFOSEC-PAIR-P041_P042

Spec refs: TASK-INFOSEC-PAIR-SMOKE-P041_P042; FUN-INFOSEC-PAIR-SMOKE AC-1..3; CON-NO-INFOSEC-3K AC-1; BR-INFOSEC-PAIR-SMOKE-001..003.

Objetivo: medir precisión observada de pipeline actual para párrafos p041, p042 sin expected domain inventado.

Fixtures leídos:
- p041: A data breach scenario illustrates the importance of access control and data protection. An unauthorized user accesses a restricted document repository. The restricted document repository stores confidential information and personal data. The unauthorized access violates the access control policy. A...
- p042: ORION should be able to identify security concepts, classify hierarchical relationships, and extract meaningful relationships from this text. Information asset, security control, security incident, authentication factor, threat actor, compliance requirement, cloud workload, endpoint, and supplier ar...

Artifacts esperados: observed_p041_p042_semantic_claims.json, observed_p041_p042_graph_model.json, observed_p041_p042_output.rdf, observed_p041_p042_metrics.json.
