# TR-ORION-P043-TASK-001

Spec refs: TASK-001 p043; FUN-P043-SVO AC-1..3; CON-P043-EXPLICIT-SVO AC-1..2; CON-P043-NO-COMPOUND-CLASS AC-1; BR-P043-SVO-001..003.

Fase: Themis RED. No fixes productivos.

Invariant: p043 explicit text must produce separate SVO resources and predicates for users access systems; roles include permissions; controls reduce risks; threats exploit vulnerabilities; incidents affect assets; systems process information assets; policies define requirements; requirements are satisfied by controls; suppliers provide services; auditors evaluate compliance.

Coverage Matrix:

| Spec/BR | Test file | Test id | Expected RED reason |
| --- | --- | --- | --- |
| FUN-P043-SVO AC-1; CON-P043-EXPLICIT-SVO AC-1; BR-P043-SVO-001 | tests/smoke/cases/infosec_p043/test_infosec_p043_observational_smoke.py | test_p043_task_001_explicit_svo_entities_are_separate_classes | Current graph emits compound relation classes instead of separate Users/System/etc. |
| FUN-P043-SVO AC-2; CON-P043-EXPLICIT-SVO AC-2; BR-P043-SVO-002 | tests/smoke/cases/infosec_p043/test_infosec_p043_observational_smoke.py | test_p043_task_001_access_is_object_property_between_users_and_systems | Current graph lacks users --access/accesses--> systems object property. |
| FUN-P043-SVO AC-3; CON-P043-NO-COMPOUND-CLASS AC-1; BR-P043-SVO-003 | tests/smoke/cases/infosec_p043/test_infosec_p043_observational_smoke.py | test_p043_task_001_no_compound_relation_classes_or_meta_hub | Current graph includes AccessSystem/ControlReduceRisk/ThreatExploitVulnerability and ResultingOntologyShouldRepresent hub. |

Validation command: python3 tests/smoke/run_infosec_smoke_suite.py
