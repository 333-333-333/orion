# TR-ORION-SEMANTIC-DEBUG-IR-RED: Semantic debug IR smoke RED

## Metadata
- ID: TR-ORION-SEMANTIC-DEBUG-IR-RED
- Phase: RED
- Date: 2026-06-04
- Scope: smoke semantic debug intermediate artifact

## Contract added
Each smoke case should be able to emit `observed_{case_id}_semantic_debug_ir.json`. Minimal IR contract: top-level `entities` array and `relations` array; optional `contexts` and `rejected`. Each entity has `id`, `label`/`canonical`/equivalent, and source/source_sentence when available. Each relation has `subject`, `predicate`, `object`, and source_sentence/evidence.

## Coverage matrix
| Spec ID | Test file | Test case | Expected RED reason |
| --- | --- | --- | --- |
| TASK-SEMANTIC-DEBUG-IR-001 / FUN-SEMANTIC-DEBUG-IR AC-1 / CON-SEMANTIC-DEBUG-IR-SHAPE AC-1 / BR-SEMANTIC-DEBUG-IR-001 | tests/smoke/cases/infosec_p015_p016/test_infosec_p015_p016_observational_smoke.py | test_p015_p016_semantic_debug_ir_contract_shape | `observed_p015_p016_semantic_debug_ir.json` missing until implementation emits IR |
| TASK-SEMANTIC-DEBUG-IR-001 / FUN-SEMANTIC-DEBUG-IR AC-2 / CON-SOURCE-EVIDENCE AC-1 / BR-SEMANTIC-DEBUG-IR-002 | tests/smoke/cases/infosec_p015_p016/test_infosec_p015_p016_observational_smoke.py | test_p015_p016_semantic_debug_ir_load_balancer_relation_is_evidence_backed | Requires evidence-backed `LoadBalancer distributes Traffic` relation |
| TASK-SEMANTIC-DEBUG-IR-001 / FUN-SEMANTIC-DEBUG-IR AC-3 / CON-NO-INVENTED-PROPERTY AC-1 / BR-SEMANTIC-DEBUG-IR-003 | tests/smoke/cases/infosec_p015_p016/test_infosec_p015_p016_observational_smoke.py | test_p015_p016_semantic_debug_ir_does_not_promote_across_phrase_noise | Forbids invented `flowsAcross`; compound `TrafficAcrossMultipleServer` cannot be final entity |

## Runner
Validation command: `python3 tests/smoke/run_infosec_smoke_suite.py`. The p015/p016 case is already selected by the smoke runner.
