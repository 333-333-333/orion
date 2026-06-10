# TR-ORION-README-PUBLIC-LIBRARY-CONTRACT-RED

Spec refs: README-PUBLIC-API; FUN-README-PUBLIC-API AC-1, AC-2; CON-README-CONFIG AC-1; CON-README-OUTPUT AC-1; BR-README-CONTRACT-001; BR-README-CONTRACT-002.

Objetivo RED: fijar el contrato público README de ORION como librería Python embebible, aunque GREEN pueda romper compatibilidad vieja basada en dict interno.

Coverage matrix:
| Spec | Test file | Test case | Expected RED reason |
| --- | --- | --- | --- |
| FUN-README-PUBLIC-API AC-1 / CON-README-CONFIG AC-1 / BR-README-CONTRACT-001 | tests/smoke/test_readme_public_library_contract_red.py | test_readme_public_api_accepts_documented_library_config | ORION debe aceptar config README con language, spacy_model_size, output_formats ttl/rdfxml/jsonld/nt, traceability. |
| FUN-README-PUBLIC-API AC-2 / CON-README-OUTPUT AC-1 / BR-README-CONTRACT-002 | tests/smoke/test_readme_public_library_contract_red.py | test_readme_public_api_process_returns_documented_result_object | Implementación actual devuelve dict y no objeto con ontology, serialized, deterministic_triples, inferred_triples; serialized multiformato no existe. |

Untestable items: ninguno.

Validación RED esperada: python3 tests/smoke/run_infosec_smoke_suite.py falla en test_readme_public_api_process_returns_documented_result_object por missing_attrs con los atributos públicos README.
