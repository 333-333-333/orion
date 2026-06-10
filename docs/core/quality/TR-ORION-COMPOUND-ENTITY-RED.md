# TR-ORION-COMPOUND-ENTITY-RED

Spec refs: TB-ORION-COMPOUND-ENTITY-RED; FUN-COMPOUND-ENTITY AC-1..2; CON-RDF-VISIBILITY AC-1..2; BR-COMPOUND-ENTITY-001..002.

Objetivo RED: fijar Themis smoke para entidades compuestas rotas en NLP/RDF sin ampliar ontología completa, sin reificación y sin arreglo global.

Caso localizado: tests/smoke/cases/infosec_compound_entities_red.

Texto/oración fuente: p044 fixture con identity and access management, physical access, unauthorized access, recovery point objective, key management service.

Coverage matrix:
| Spec | Test file | Test case | Expected RED reason |
| --- | --- | --- | --- |
| BR-COMPOUND-ENTITY-001 / FUN-COMPOUND-ENTITY AC-1 / CON-RDF-VISIBILITY AC-1 | tests/smoke/cases/infosec_compound_entities_red/test_infosec_compound_entities_red_smoke.py | test_compound_entities_are_atomic_in_semantic_and_graph_layers | Current NLP/graph may split compounds or promote clause residues instead of atomic compound entities. |
| BR-COMPOUND-ENTITY-002 / FUN-COMPOUND-ENTITY AC-2 / CON-RDF-VISIBILITY AC-2 | tests/smoke/cases/infosec_compound_entities_red/test_infosec_compound_entities_red_smoke.py | test_compound_entities_emit_direct_visible_rdf_triples_not_split_nodes | Current RDF/Turtle may miss direct triples for compound entities or expose split residue nodes. |

Artifacts generados por harness: observed_compound_entities_red_semantic_claims.json, observed_compound_entities_red_graph_model.json, observed_compound_entities_red_output.rdf, observed_compound_entities_red_output.ttl.
