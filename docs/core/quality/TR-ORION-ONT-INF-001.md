---
id: TR-ORION-ONT-INF-001
type: test-report
status: red
spec_ref: TB-ORION-ONT-INF-001
created: 2026-06-02
---

# TR-ORION-ONT-INF-001 — Themis RED ontology infosec

## Scope
Valida contrato RED de TB-ORION-ONT-INF-001 sin tocar src productivo.

## Coverage Matrix
| Spec | Test file | Test case | Expected status |
|---|---|---|---|
| TB-ORION-ONT-INF-001 TASK-001/TASK-002; CON-ONT-INF-001 AC-1; BR-ONT-INF-001/002 | tests/smoke/test_infosec_3k_pipeline_smoke.py | test_tb_orion_ont_inf_001_closed_infosec_ontology_blocks_generic_ner_and_scaffolds_red | RED |
| TB-ORION-ONT-INF-001 TASK-003; FUN-ONT-INF-001 AC-1; BR-ONT-INF-003/004 | tests/smoke/test_infosec_3k_pipeline_smoke.py | test_tb_orion_ont_inf_001_taxonomy_direction_and_definition_comments_red | RED |
| TB-ORION-ONT-INF-001 TASK-004; FUN-ONT-INF-002 AC-1; CON-ONT-INF-002 AC-1; BR-ONT-INF-005 | tests/smoke/test_infosec_3k_pipeline_smoke.py | test_tb_orion_ont_inf_001_expected_infosec_relations_have_domain_range_red | RED |

## Validation command
python3 tests/smoke/run_infosec_smoke_suite.py

## RED result
Command: python3 tests/smoke/run_infosec_smoke_suite.py
Result: 5 failed, 66 passed in 261.75s (0:04:21); phase RED confirmed.
Relevant TB failures:
- test_tb_orion_ont_inf_001_closed_infosec_ontology_blocks_generic_ner_and_scaffolds_red: recursos gramaticales prohibidos visibles: ['resource-that']
- test_tb_orion_ont_inf_001_taxonomy_direction_and_definition_comments_red: TypeOf* scaffolding visible, e.g. orion:AccessToken->orion:TypeOfTemporaryCredential
- test_tb_orion_ont_inf_001_expected_infosec_relations_have_domain_range_red: missing expected domain/range for accesses/includes/exploits/reduces/affects
