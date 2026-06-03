# TR-ORION-INFOSEC-PAIR-P021_P022

Spec refs: TASK-INFOSEC-PAIR-SMOKE-P021_P022; FUN-INFOSEC-PAIR-SMOKE AC-1..3; CON-NO-INFOSEC-3K AC-1; BR-INFOSEC-PAIR-SMOKE-001..003.

Objetivo: medir precisión observada de pipeline actual para párrafos p021, p022 sin expected domain inventado.

Fixtures leídos:
- p021: A security information and event management system collects, normalizes, correlates, and analyzes security logs. Log collection gathers records from systems and applications. Log normalization converts different log formats into a common structure. Log correlation identifies relationships between ev...
- p022: Incident response is the process of preparing for, detecting, analyzing, containing, eradicating, and recovering from security incidents. Preparation establishes plans, tools, roles, and communication channels. Detection identifies potential incidents. Analysis determines the scope, cause, and impac...

Artifacts esperados: observed_p021_p022_semantic_claims.json, observed_p021_p022_graph_model.json, observed_p021_p022_output.rdf, observed_p021_p022_metrics.json.
