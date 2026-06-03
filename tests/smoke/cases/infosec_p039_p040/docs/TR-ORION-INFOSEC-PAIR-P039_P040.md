# TR-ORION-INFOSEC-PAIR-P039_P040

Spec refs: TASK-INFOSEC-PAIR-SMOKE-P039_P040; FUN-INFOSEC-PAIR-SMOKE AC-1..3; CON-NO-INFOSEC-3K AC-1; BR-INFOSEC-PAIR-SMOKE-001..003.

Objetivo: medir precisión observada de pipeline actual para párrafos p039, p040 sin expected domain inventado.

Fixtures leídos:
- p039: A phishing scenario illustrates how threats, vulnerabilities, controls, and incidents relate to each other. A threat actor sends a phishing email to an employee. The phishing email contains a malicious link. The employee clicks the malicious link and submits a password. The submitted password become...
- p040: A ransomware scenario illustrates the importance of backups, monitoring, and response. Malware encrypts files on a file server. The file server becomes unavailable to business users. The event affects availability and may affect integrity. Endpoint detection and response may detect the malware activ...

Artifacts esperados: observed_p039_p040_semantic_claims.json, observed_p039_p040_graph_model.json, observed_p039_p040_output.rdf, observed_p039_p040_metrics.json.
