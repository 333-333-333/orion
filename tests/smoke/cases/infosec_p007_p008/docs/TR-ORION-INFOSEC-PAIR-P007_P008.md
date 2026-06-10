# TR-ORION-INFOSEC-PAIR-P007_P008

Spec refs: TASK-INFOSEC-PAIR-SMOKE-P007_P008; FUN-INFOSEC-PAIR-SMOKE AC-1..3; FUN-SEMANTIC-DEBUG-IR AC-3; CON-NO-INFOSEC-3K AC-1; CON-RDF-VISIBILITY AC-1; CON-SOURCE-EVIDENCE AC-1; BR-INFOSEC-PAIR-SMOKE-001..003; BR-NO-NOMINALIZED-GIANT-CLASS-001.

Objetivo: medir precisión observada de pipeline actual para párrafos p007, p008 sin expected domain inventado y proteger invariante genérico: frases nominalizadas gigantes ability + verb + object + context no salen como clase final visible.

Fixtures leídos:
- p007: Information classification helps organizations apply appropriate protection levels to different kinds of information. Public information is a type of information that can be disclosed without causing harm. Internal information is a type of information intended for use inside the organization. Confid...
- p008: Access control regulates who can access which resource and under which conditions. Identification is the process of claiming an identity. Authentication is the process of verifying an identity. Authorization is the process of determining what actions an authenticated identity may perform. Accountabi...

Oración fuente localizada: Accountability is the ability to trace actions to a specific identity.

Artifacts esperados: observed_p007_p008_semantic_claims.json, observed_p007_p008_graph_model.json, observed_p007_p008_semantic_debug_ir.json, observed_p007_p008_output.rdf, observed_p007_p008_metrics.json.

Coverage matrix:
- BR-NO-NOMINALIZED-GIANT-CLASS-001 -> test_p007_p008_rdf_does_not_emit_nominalized_ability_phrase_as_visible_class; test_p007_p008_semantic_debug_ir_rejects_or_decomposes_nominalized_ability_phrase.
- FUN-SEMANTIC-DEBUG-IR AC-3 / CON-RDF-VISIBILITY AC-1 / CON-SOURCE-EVIDENCE AC-1 -> mismos tests, usando observed_p007_p008_semantic_debug_ir.json cuando existe.
