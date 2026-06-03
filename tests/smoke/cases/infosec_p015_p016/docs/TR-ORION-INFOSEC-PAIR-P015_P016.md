# TR-ORION-INFOSEC-PAIR-P015_P016

Spec refs: TASK-INFOSEC-PAIR-SMOKE-P015_P016; FUN-INFOSEC-PAIR-SMOKE AC-1..3; CON-NO-INFOSEC-3K AC-1; BR-INFOSEC-PAIR-SMOKE-001..003.

Objetivo: medir precisión observada de pipeline actual para párrafos p015, p016 sin expected domain inventado.

Fixtures leídos:
- p015: Application security protects software systems throughout their lifecycle. A software vulnerability is a weakness in application code, configuration, or design. Input validation prevents malicious or malformed data from entering an application. Output encoding reduces the risk of injection and cross...
- p016: A web application is a type of application. A mobile application is a type of application. An API is a type of application interface. A database is a type of data storage system. A web server hosts web applications. An application server executes business logic. A database server stores structured d...

Artifacts esperados: observed_p015_p016_semantic_claims.json, observed_p015_p016_graph_model.json, observed_p015_p016_output.rdf, observed_p015_p016_metrics.json.
