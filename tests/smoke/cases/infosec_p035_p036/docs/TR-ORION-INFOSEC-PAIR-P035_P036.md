# TR-ORION-INFOSEC-PAIR-P035_P036

Spec refs: TASK-INFOSEC-PAIR-SMOKE-P035_P036; FUN-INFOSEC-PAIR-SMOKE AC-1..3; CON-NO-INFOSEC-3K AC-1; BR-INFOSEC-PAIR-SMOKE-001..003.

Objetivo: medir precisión observada de pipeline actual para párrafos p035, p036 sin expected domain inventado.

Fixtures leídos:
- p035: Secure architecture integrates security into the design of systems and environments. Defense in depth applies multiple layers of security controls. Zero trust is a security model that assumes no implicit trust based on network location. Network segmentation limits lateral movement. Strong authentica...
- p036: A security control can protect one or more assets. An asset can be affected by one or more risks. A risk can be reduced by one or more controls. A threat can exploit one or more vulnerabilities. A vulnerability can affect one or more systems. A system can process one or more information assets. A us...

Artifacts esperados: observed_p035_p036_semantic_claims.json, observed_p035_p036_graph_model.json, observed_p035_p036_output.rdf, observed_p035_p036_metrics.json.
