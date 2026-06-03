# TR-ORION-INFOSEC-PAIR-P011_P012

Spec refs: TASK-INFOSEC-PAIR-SMOKE-P011_P012; FUN-INFOSEC-PAIR-SMOKE AC-1..3; CON-NO-INFOSEC-3K AC-1; BR-INFOSEC-PAIR-SMOKE-001..003.

Objetivo: medir precisión observada de pipeline actual para párrafos p011, p012 sin expected domain inventado.

Fixtures leídos:
- p011: The principle of least privilege states that an identity must receive only the permissions required to perform its duties. A permission grants an action over a resource. A role is a collection of permissions. A user group is a collection of identities that share common permissions. A role assignment...
- p012: Identity and access management controls the lifecycle of identities, accounts, roles, permissions, and credentials. User provisioning creates a new user account. User deprovisioning disables or removes access for a user who no longer requires it. Access modification changes the permissions assigned ...

Artifacts esperados: observed_p011_p012_semantic_claims.json, observed_p011_p012_graph_model.json, observed_p011_p012_output.rdf, observed_p011_p012_metrics.json.
