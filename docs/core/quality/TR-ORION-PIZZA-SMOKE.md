# TR-ORION-PIZZA-SMOKE

Spec refs: TASK-PIZZA-SMOKE-001; TASK-PIZZA-RED-001; FUN-PIZZA-SMOKE AC-1..3; FUN-PIZZA-PRONOUN AC-1..2; CON-NO-INFOSEC-3K AC-1; CON-SOURCE-EVIDENCE AC-1; CON-RDF-VISIBILITY AC-1..3; BR-PIZZA-SMOKE-001..003; BR-PIZZA-PRONOUN-001..003; BR-PIZZA-CONNECTOR-001.

Objetivo: validar un smoke modular con texto propio de pizzas de aproximadamente 500 palabras, sin reactivar legacy infosec 3k y sin tocar src productivo.

Fixture leído:
- pizza_001: texto modular sobre Mario's Pizzeria, Vesuvio pie, proveedores, horno Dante, Luigi Bianchi, Central Cafe, Nina Patel y orden CAFE-17.

Coverage matrix:
- FUN-PIZZA-SMOKE AC-1 / CON-NO-INFOSEC-3K AC-1 / BR-PIZZA-SMOKE-001 -> test_pizza_short_observed_artifacts_are_generated_case_local
- FUN-PIZZA-SMOKE AC-2 / CON-SOURCE-EVIDENCE AC-1 / BR-PIZZA-SMOKE-002 -> test_pizza_short_semantic_claims_preserve_source_evidence
- FUN-PIZZA-SMOKE AC-3 / CON-RDF-VISIBILITY AC-1 / BR-PIZZA-SMOKE-003 -> test_pizza_short_rdf_projection_has_visible_structure
- TASK-PIZZA-RED-001 / CON-RDF-VISIBILITY AC-2 / BR-PIZZA-PRONOUN-001 -> test_task_pizza_red_001_pronoun_he_is_not_visible_as_rdf_node_or_class
- TASK-PIZZA-RED-001 / CON-RDF-VISIBILITY AC-3 / BR-PIZZA-CONNECTOR-001 -> test_task_pizza_red_001_connector_prefixes_are_not_visible_classes
- TASK-PIZZA-RED-001 / FUN-PIZZA-PRONOUN AC-1 / BR-PIZZA-PRONOUN-002 -> test_task_pizza_red_001_reaches_central_cafe_uses_luigi_not_he
- TASK-PIZZA-RED-001 / FUN-PIZZA-PRONOUN AC-2 / BR-PIZZA-PRONOUN-003 -> test_task_pizza_red_001_pronoun_claims_rewrite_or_stay_unresolved_internal

Artifactual esperado: observed_pizza_short_semantic_claims.json, observed_pizza_short_graph_model.json, observed_pizza_short_output.rdf, observed_pizza_short_metrics.json.

Notas de alcance: fixture case-local; legacy infosec_3k no se reactiva; artifacts observados se regeneran por harness; TASK-PIZZA-RED-001 es RED intencional y solo valida el fixture concreto pizza_short, sin exigir lógica productiva hardcodeada.
