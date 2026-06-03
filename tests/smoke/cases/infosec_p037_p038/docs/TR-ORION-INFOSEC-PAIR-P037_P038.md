# TR-ORION-INFOSEC-PAIR-P037_P038

Spec refs: TASK-INFOSEC-PAIR-SMOKE-P037_P038; FUN-INFOSEC-PAIR-SMOKE AC-1..3; CON-NO-INFOSEC-3K AC-1; BR-INFOSEC-PAIR-SMOKE-001..003.

Objetivo: medir precisión observada de pipeline actual para párrafos p037, p038 sin expected domain inventado.

Fixtures leídos:
- p037: For example, a customer database stores personal data and financial data. The customer database is hosted on a database server. The database server runs inside a production network. The production network is protected by a firewall. The firewall enforces network access rules. The customer database i...
- p038: Another example involves remote access. A remote employee uses a laptop to access a corporate application. The laptop is an endpoint. The corporate application is a web application. The remote employee authenticates through multi-factor authentication. The identity provider verifies the employee ide...

Artifacts esperados: observed_p037_p038_semantic_claims.json, observed_p037_p038_graph_model.json, observed_p037_p038_output.rdf, observed_p037_p038_metrics.json.
