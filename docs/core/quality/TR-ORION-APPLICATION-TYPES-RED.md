# TR-ORION-APPLICATION-TYPES-RED

Spec refs: TASK-APP-TYPES-RED-001; FUN-APP-TYPES AC-1..4; CON-SMOKE-MODULAR AC-1; CON-SOURCE-EVIDENCE AC-1; CON-APP-TAXONOMY AC-1..2; BR-APP-TYPES-001..004.

Fase: Themis RED. No fixes productivos.

Invariant: exact/equivalent text "A web application is a type of application. A mobile application is a type of application." must produce Application, WebApplication subClassOf Application, MobileApplication subClassOf Application, and must not produce MobileApplication subClassOf WebApplication or WebApplication subClassOf MobileApplication.

Coverage Matrix:

| Spec/BR | Test file | Test id | Expected RED reason |
| --- | --- | --- | --- |
| FUN-APP-TYPES AC-1; CON-SMOKE-MODULAR AC-1; BR-APP-TYPES-001 | tests/smoke/cases/application_types_minimal/test_application_types_minimal_observational_smoke.py | test_application_types_minimal_observed_artifacts_are_generated_case_local | Harness must generate case-local observed artifacts. |
| FUN-APP-TYPES AC-2; CON-SOURCE-EVIDENCE AC-1; BR-APP-TYPES-002 | tests/smoke/cases/application_types_minimal/test_application_types_minimal_observational_smoke.py | test_application_types_minimal_preserves_source_evidence | Claims must remain evidence-backed by fixture text. |
| FUN-APP-TYPES AC-3; CON-APP-TAXONOMY AC-1; BR-APP-TYPES-003 | tests/smoke/cases/application_types_minimal/test_application_types_minimal_observational_smoke.py | test_application_types_minimal_emits_application_taxonomy | Current bug may miss Application or direct type-of subClassOf taxonomy. |
| FUN-APP-TYPES AC-4; CON-APP-TAXONOMY AC-2; BR-APP-TYPES-004 | tests/smoke/cases/application_types_minimal/test_application_types_minimal_observational_smoke.py | test_application_types_minimal_does_not_cross_subclass_siblings | Current bug may infer sibling cross-subClassOf relations between WebApplication and MobileApplication. |

Validation command: python3 tests/smoke/run_infosec_smoke_suite.py
