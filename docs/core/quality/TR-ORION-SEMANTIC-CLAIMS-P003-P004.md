---
id: TR-ORION-SEMANTIC-CLAIMS-P003-P004
type: test-report
status: red
spec_ref: TASK-SEMANTIC-CLAIMS-P003-P004
created: 2026-06-03
---

# TR-ORION-SEMANTIC-CLAIMS-P003-P004 — RED semantic_claims p003+p004

## Scope
Valida fixtures reales p003 y p004 con smoke modular aislado en tests/smoke/cases/infosec_p003_p004/. Contrato exige semantic_claims antes de triples/RDF.

## Coverage Matrix
| Spec | Test file | Test case | Expected status |
|---|---|---|---|
| TASK-SEMANTIC-CLAIMS-P003-P004; FUN AC-1; CON AC-1; BR-001 | tests/smoke/cases/infosec_p003_p004/test_infosec_p003_p004_semantic_claims_smoke.py | test_p003_p004_semantic_claims_exist_before_triples_or_rdf | RED/GREEN |
| TASK-SEMANTIC-CLAIMS-P003-P004; FUN AC-2; CON AC-2; BR-002 | tests/smoke/cases/infosec_p003_p004/test_infosec_p003_p004_semantic_claims_smoke.py | test_p003_p004_semantic_claims_have_explicit_spo_source_and_resolved_references | RED/GREEN |
| TASK-SEMANTIC-CLAIMS-P003-P004; FUN AC-3; CON AC-3; BR-003/BR-004 | tests/smoke/cases/infosec_p003_p004/test_infosec_p003_p004_semantic_claims_smoke.py | test_p003_p004_semantic_contract_expected_claims_and_no_chunk_residue | RED/GREEN |
| TASK-SEMANTIC-CLAIMS-P003-P004; FUN AC-4; CON AC-4; BR-005 | tests/smoke/cases/infosec_p003_p004/test_infosec_p003_p004_semantic_claims_smoke.py | test_p003_p004_definitions_are_separate_from_relations | RED/GREEN |
| TASK-SEMANTIC-CLAIMS-P003-P004; FUN AC-5; CON AC-5; BR-006 | tests/smoke/cases/infosec_p003_p004/test_infosec_p003_p004_semantic_claims_smoke.py | test_p003_p004_ontology_projection_uses_semantic_claims_not_noun_chunks | RED/GREEN |

## Contract
Expected contract: tests/smoke/cases/infosec_p003_p004/expected_semantic_contract.json
Observed artifact: tests/smoke/cases/infosec_p003_p004/artifacts/observed_p003_p004_semantic_claims.json

## 3k guard
Runner must select p001+p002 modular tests and p003+p004 semantic modular test only. Full infosec 3k tests stay disabled.

## RED result
python3 tests/smoke/run_infosec_smoke_suite.py => returncode 1; 13 collected; 8 passed, 5 failed. p001+p002 passed. p003+p004 failed usefully because semantic_claims stage is not present before triples/RDF; observed artifact shows observed_stage=canonical_claims, stage=canonical_claims, claim_count=5, all p003, zero p004, and residue MinimumSetOfControlRequired.

## 3k execution guard evidence after run
selected_tests = tests/smoke/cases/infosec_p001_p002/test_infosec_p001_p002_canonical_claims_red_smoke.py, tests/smoke/cases/infosec_p001_p002/test_infosec_p001_p002_modular_contract_smoke.py, tests/smoke/cases/infosec_p003_p004/test_infosec_p003_p004_semantic_claims_smoke.py. disabled_infosec_3k_tests includes test_infosec_3k_pipeline_smoke.py, test_infosec_3k_paragraphs_smoke.py, test_infosec_paragraph_semantics_smoke.py.
