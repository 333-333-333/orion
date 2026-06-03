# TR-ORION-INFOSEC-PAIR-P009_P010

Spec refs: TASK-INFOSEC-PAIR-SMOKE-P009_P010; FUN-INFOSEC-PAIR-SMOKE AC-1..3; CON-NO-INFOSEC-3K AC-1; BR-INFOSEC-PAIR-SMOKE-001..003.

Objetivo: medir precisión observada de pipeline actual para párrafos p009, p010 sin expected domain inventado.

Fixtures leídos:
- p009: A credential is evidence used to prove an identity. A password is a type of credential. A certificate is a type of cryptographic credential. An access token is a type of temporary credential. An API key is a type of credential used by applications to authenticate requests. A private key is a type of...
- p010: Multi-factor authentication improves authentication strength by requiring more than one verification factor. A knowledge factor is a type of authentication factor based on something the user knows. A possession factor is a type of authentication factor based on something the user has. An inherence f...

Artifacts esperados: observed_p009_p010_semantic_claims.json, observed_p009_p010_graph_model.json, observed_p009_p010_output.rdf, observed_p009_p010_metrics.json.
