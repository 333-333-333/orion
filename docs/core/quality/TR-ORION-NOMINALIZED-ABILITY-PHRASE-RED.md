# TR-ORION-NOMINALIZED-ABILITY-PHRASE-RED

Spec refs: TASK-INFOSEC-PAIR-SMOKE-P007_P008; FUN-SEMANTIC-DEBUG-IR AC-3; CON-RDF-VISIBILITY AC-1; CON-SOURCE-EVIDENCE AC-1; BR-NO-NOMINALIZED-GIANT-CLASS-001.

Objetivo RED: fijar invariante genérico para no promover como clase final visible una frase nominalizada gigante ability + verb + object + context.

Caso localizado: tests/smoke/cases/infosec_p007_p008.

Texto/oración fuente: Accountability is the ability to trace actions to a specific identity.

Coverage matrix:
| Spec | Test file | Test case | Expected RED reason |
| --- | --- | --- | --- |
| BR-NO-NOMINALIZED-GIANT-CLASS-001 / FUN-SEMANTIC-DEBUG-IR AC-3 / CON-RDF-VISIBILITY AC-1 | tests/smoke/cases/infosec_p007_p008/test_infosec_p007_p008_observational_smoke.py | test_p007_p008_rdf_does_not_emit_nominalized_ability_phrase_as_visible_class | Current RDF/graph emits AbilityToTraceActionToASpecificIdentity as visible class/label. |
| BR-NO-NOMINALIZED-GIANT-CLASS-001 / FUN-SEMANTIC-DEBUG-IR AC-3 / CON-SOURCE-EVIDENCE AC-1 | tests/smoke/cases/infosec_p007_p008/test_infosec_p007_p008_observational_smoke.py | test_p007_p008_semantic_debug_ir_rejects_or_decomposes_nominalized_ability_phrase | Current semantic_debug_ir emits the giant phrase as final entity and does not preserve separate evidence-backed Ability, Action, Identity entities. |

Artifacts usados: observed_p007_p008_output.rdf, observed_p007_p008_graph_model.json, observed_p007_p008_semantic_debug_ir.json.
