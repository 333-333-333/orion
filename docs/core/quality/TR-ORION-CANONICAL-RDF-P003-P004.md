---
id: TR-ORION-CANONICAL-RDF-P003-P004
type: test-report
status: red
spec_ref: TASK-CANONICAL-RDF-P003-P004
created: 2026-06-02
updated: 2026-06-03
---

# TR-ORION-CANONICAL-RDF-P003-P004 — Themis RED RDF quality p003-p004

## Scope
Valida fixtures reales p003+p004 con smoke modular en tests/smoke/cases/infosec_p003_p004/. Contrato test-only para completitud relacional RDF. No cambia src productivo.

## Contrato estricto
- RDF artifact case-local obligatorio.
- Vocabulario válido no se prohíbe por nombre: Control, Expectation, GoodPractice, Resource, Rule permitidos si vienen del texto.
- Clases RDF deben coincidir con contrato semántico derivado de p003+p004 y max_class_count=48.
- Taxonomía mínima: definiciones explícitas "type of" de p003 deben mapear a subClassOf; no se exige taxonomía inventada para roles p004.
- Definiciones deben aparecer como rdfs:comment en graph y RDF serializado.
- Object properties deben tener predicate/domain/range en graph y RDF serializado, cubriendo relaciones expresadas: implements, defines, protects, recommends, required-for, approves, allocates, supports, coordinates, classifies, operates, maintains, stores, processes, manages, monitors, investigates, evaluates, checked-against, accesses, follows.
- Entidades centrales derivadas de relaciones p003+p004 deben quedar conectadas por object properties; max_unjustified_connectivity_orphans=0.
- projection.source_stage debe ser semantic_claims y claim_ids deben coincidir con semantic_claims.
- Noun-chunk residues prohibidos: type-of*, resource-for-security-initiative, rules-and-expectations, minimum-set-of-controls-required, technical-environment-that-stores.

## Coverage Matrix
| Spec | Test file | Test case | Expected status |
|---|---|---|---|
| TASK-CANONICAL-RDF-P003-P004; FUN-CANONICAL-RDF-P003-P004 AC-1; CON-CANONICAL-RDF-P003-P004 AC-1; BR-CANONICAL-RDF-P003-P004-001 | tests/smoke/cases/infosec_p003_p004/test_infosec_p003_p004_canonical_rdf_smoke.py | test_p003_p004_canonical_claims_are_deterministic_and_asset_scoped | GREEN |
| TASK-CANONICAL-RDF-P003-P004; FUN-CANONICAL-RDF-P003-P004 AC-2; CON-CANONICAL-RDF-P003-P004 AC-2; BR-CANONICAL-RDF-P003-P004-002 | tests/smoke/cases/infosec_p003_p004/test_infosec_p003_p004_canonical_rdf_smoke.py | test_p003_p004_rdf_artifact_is_generated_case_local | GREEN |
| TASK-CANONICAL-RDF-P003-P004; FUN-CANONICAL-RDF-P003-P004 AC-2; CON-CANONICAL-RDF-P003-P004 AC-2; BR-CANONICAL-RDF-P003-P004-002 | tests/smoke/cases/infosec_p003_p004/test_infosec_p003_p004_canonical_rdf_smoke.py | test_p003_p004_rdf_has_exact_small_class_contract | RED if class contract drifts |
| TASK-CANONICAL-RDF-P003-P004; FUN-CANONICAL-RDF-P003-P004 AC-3; CON-CANONICAL-RDF-P003-P004 AC-3; BR-CANONICAL-RDF-P003-P004-003 | tests/smoke/cases/infosec_p003_p004/test_infosec_p003_p004_canonical_rdf_smoke.py | test_p003_p004_rdf_maps_type_definitions_to_direct_subclassof | RED if explicit type taxonomy missing |
| TASK-CANONICAL-RDF-P003-P004; FUN-CANONICAL-RDF-P003-P004 AC-4; CON-CANONICAL-RDF-P003-P004 AC-4; BR-CANONICAL-RDF-P003-P004-004 | tests/smoke/cases/infosec_p003_p004/test_infosec_p003_p004_canonical_rdf_smoke.py | test_p003_p004_rdf_preserves_definition_sentences_as_comments | RED |
| TASK-CANONICAL-RDF-P003-P004; FUN-CANONICAL-RDF-P003-P004 AC-5; CON-CANONICAL-RDF-P003-P004 AC-5; BR-CANONICAL-RDF-P003-P004-004 | tests/smoke/cases/infosec_p003_p004/test_infosec_p003_p004_canonical_rdf_smoke.py | test_p003_p004_rdf_has_expected_object_properties_with_domain_range | RED |
| TASK-CANONICAL-RDF-P003-P004; FUN-CANONICAL-RDF-P003-P004 AC-5; CON-CANONICAL-RDF-P003-P004 AC-5; BR-CANONICAL-RDF-P003-P004-004 | tests/smoke/cases/infosec_p003_p004/test_infosec_p003_p004_canonical_rdf_smoke.py | test_p003_p004_rdf_keeps_central_entities_relation_connected | RED |
| TASK-CANONICAL-RDF-P003-P004; FUN-CANONICAL-RDF-P003-P004 AC-6; CON-CANONICAL-RDF-P003-P004 AC-6; BR-CANONICAL-RDF-P003-P004-005 | tests/smoke/cases/infosec_p003_p004/test_infosec_p003_p004_canonical_rdf_smoke.py | test_p003_p004_rdf_projection_comes_only_from_semantic_claims | GREEN |
| TASK-CANONICAL-RDF-P003-P004; FUN-CANONICAL-RDF-P003-P004 AC-7; CON-CANONICAL-RDF-P003-P004 AC-7; BR-CANONICAL-RDF-P003-P004-006 | tests/smoke/cases/infosec_p003_p004/test_infosec_p003_p004_canonical_rdf_smoke.py | test_p003_p004_rdf_has_no_noun_chunk_residue | GREEN |

## Validation command
python3 tests/smoke/run_infosec_smoke_suite.py

## Artifacts
Expected contract: tests/smoke/cases/infosec_p003_p004/expected_contract.json
Observed semantic_claims: tests/smoke/cases/infosec_p003_p004/artifacts/observed_p003_p004_semantic_claims.json
Observed RDF: tests/smoke/cases/infosec_p003_p004/artifacts/observed_p003_p004_output.rdf

## 3k guard
Runner selects only modular p001+p002, p003+p004 semantic, and p003+p004 RDF tests. Full infosec 3k smoke files remain disabled.

## RED expectation
python3 tests/smoke/run_infosec_smoke_suite.py => returncode 1; 22 collected; 20 passed, 2 failed. RED útil por faltantes relacionales serializados y comments, no por ban duro de vocabulario válido.

## RED evidence
- Object property contract debe fallar si faltan relaciones derivadas en graph o RDF serializado: Organization implements SecurityPolicy/SecurityProcedure/Control, SecurityPolicy defines Rule/Expectation, SecurityPolicy protects Information, SeniorManagement allocates Resource, Resource supports SecurityInitiative, Compliance checked_against SecurityRequirement.
- Connectivity debe fallar si entidades centrales quedan sin object-property link.
- Comments debe fallar hasta que definiciones p003+p004 estén como rdfs:comment.
- Noun-chunk/artificial residue sigue prohibido: MinimumSetOfControlRequired/minimum-set-of-controls-required y fragmentos compuestos no ontológicos.

## 3k execution guard evidence after run
selected_tests = tests/smoke/cases/infosec_p001_p002/test_infosec_p001_p002_canonical_claims_red_smoke.py, tests/smoke/cases/infosec_p001_p002/test_infosec_p001_p002_modular_contract_smoke.py, tests/smoke/cases/infosec_p003_p004/test_infosec_p003_p004_semantic_claims_smoke.py, tests/smoke/cases/infosec_p003_p004/test_infosec_p003_p004_canonical_rdf_smoke.py. disabled_infosec_3k_tests includes test_infosec_3k_pipeline_smoke.py, test_infosec_3k_paragraphs_smoke.py, test_infosec_paragraph_semantics_smoke.py.
