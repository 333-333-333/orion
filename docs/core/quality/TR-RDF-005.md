# TR-RDF-005 Ontology Contract Not Everything Is Subclass RED

## Contract

Todo `rdfs:subClassOf` generado por ORION debe tener diferenciador evidence-backed frente al padre.

Diferenciador válido:
- propiedad o relación nueva soportada por texto fuente;
- restricción o valor explícito soportado por texto fuente;
- contraste explícito entre hermanos o categorías soportado por texto fuente.

Si una frase solo define, etiqueta, parafrasea o introduce alias/type-only sin propiedad/restricción/valor/relación/contraste nuevo frente al padre, ORION debe conservarla como `rdfs:label`, `rdfs:comment` o definición, pero no debe crear `owl:Class` ni `rdfs:subClassOf` redundante.

## Traceability

- UC-SMOKE-001 AF-9 -> test_infosec_3k_ontology_contract_not_everything_is_subclass_and_class_only_modeling
- FUN-SMOKE-001 AC-11 -> test_infosec_3k_ontology_contract_not_everything_is_subclass_and_class_only_modeling
- CON-SMOKE-RDF-004 AC-1 -> test_infosec_3k_ontology_contract_not_everything_is_subclass_and_class_only_modeling
- BR-SMOKE-012 -> test_infosec_3k_ontology_contract_not_everything_is_subclass_and_class_only_modeling
- BR-SMOKE-013 -> test_infosec_3k_ontology_contract_not_everything_is_subclass_and_class_only_modeling
- TASK-ONT-001 -> TR-RDF-005 invariant evidence-backed subclass differentiator
- TASK-ONT-002 -> tests/smoke/cases/infosec_p001_p002/test_infosec_p001_p002_modular_contract_smoke.py::test_p001_p002_modular_contract_rejects_alias_only_subclass_taxonomy
- TASK-ONT-003 -> tests/smoke/cases/infosec_p003_p004/test_infosec_p003_p004_canonical_rdf_smoke.py::test_p003_p004_rdf_rejects_definition_only_taxonomy_without_differentiator
- TASK-ONT-004 -> tests/smoke/test_rdf_visible_no_isolated_nodes_smoke.py::test_rdf_output_contract_visible_classes_have_evidence_backed_differentiator_red

## Coverage Matrix

| Spec | Test id | Expected RED signal |
| --- | --- | --- |
| TASK-ONT-001 | TR-RDF-005 | Contract declares evidence-backed differentiator invariant. |
| TASK-ONT-002 | test_p001_p002_modular_contract_rejects_alias_only_subclass_taxonomy | Alias-only definitional parent cannot leak as `owl:Class` or `subClassOf`. |
| TASK-ONT-003 | test_p003_p004_rdf_rejects_definition_only_taxonomy_without_differentiator | Definition/comment-only taxonomy cannot create redundant subclass hierarchy. |
| TASK-ONT-004 | test_rdf_output_contract_visible_classes_have_evidence_backed_differentiator_red | Visible RDF classes must have non-taxonomic evidence, not isolated subclass-only aliases. |

## RED expectation

The current implementation may still promote definitional/type-only wording into visible `owl:Class` nodes and direct `rdfs:subClassOf` pairs. In Themis RED, tests must fail until RDF projection degrades those cases to label/comment/definition only.


## Themis RED Result 2026-06-03

Command: `python3 tests/smoke/run_infosec_smoke_suite.py`

Result: RED, 4 failed / 85 passed.

Expected failures:
- `test_p001_p002_modular_contract_has_exact_small_deterministic_classes`: unexpected `foundational-model` class.
- `test_p001_p002_modular_contract_rejects_alias_only_subclass_taxonomy`: `foundational-model` leaked as `owl:Class`.
- `test_p003_p004_rdf_has_exact_small_class_contract`: unexpected `advisory-document`, `control-document`, `formal-document`, `minimum-set-of-controls`, `operational-document` classes.
- `test_p003_p004_rdf_rejects_definition_only_taxonomy_without_differentiator`: definition-only taxonomy leaked as `owl:Class`.

Scope gap:
- `tests/smoke/test_rdf_visible_no_isolated_nodes_smoke.py` was hardened for TASK-ONT-004 but is not selected by `tests/smoke/run_infosec_smoke_suite.py`; it was syntax-checked only, not runner-executed.
