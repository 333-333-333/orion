# TR-ORION-INFOSEC-FULL-TEXT-SMOKE
## Metadata
- ID: TR-ORION-INFOSEC-FULL-TEXT-SMOKE
- Scope: fixtures p001..p043 como texto completo modular por directorio de caso
- Tester: sisyphus-tester
- Runner: python3 tests/smoke/run_infosec_smoke_suite.py
- Result: GREEN, 87 passed in 61.96s
- Note: semantic_claims va antes de triple extraction/RDF. smoke/proxy; no gold semántico completo manual.

## Coverage Matrix
| Spec | Case | Tests | Status |
| --- | --- | --- | --- |
| FUN-INFOSEC-FULL-TEXT-SMOKE AC-1 | infosec_full_text | pipeline_generates_case_local_artifacts | GREEN |
| FUN-INFOSEC-FULL-TEXT-SMOKE AC-2 | infosec_full_text | has_semantic_claims_for_every_paragraph | GREEN |
| FUN-INFOSEC-FULL-TEXT-SMOKE AC-3 | infosec_full_text | evidence_proxy_and_projection_are_consistent | GREEN |
| FUN-INFOSEC-FULL-TEXT-SMOKE AC-4 | infosec_full_text | rdf_object_properties_have_domain_and_range | GREEN |
| FUN-INFOSEC-FULL-TEXT-SMOKE AC-5 | infosec_full_text | no_known_noun_chunk_residues_and_reasonable_metrics | GREEN |
| CON-NO-SRC-CHANGE AC-1 | infosec_full_text | test-only smoke/harness/runner changes | GREEN |
| CON-FULL-TEXT-FIXTURES AC-1 | infosec_full_text | p001..p043 ordered fixture load | GREEN |
| CON-NO-INFOSEC-3K AC-1 | runner selected_tests | legacy infosec_3k denylist remains disabled | GREEN |
| BR-INFOSEC-FULL-TEXT-SMOKE-001 | infosec_full_text | artifact generation | GREEN |
| BR-INFOSEC-FULL-TEXT-SMOKE-002 | infosec_full_text | claims for each paragraph | GREEN |
| BR-INFOSEC-FULL-TEXT-SMOKE-003 | infosec_full_text | source evidence/projection consistency | GREEN |
| BR-INFOSEC-FULL-TEXT-SMOKE-004 | infosec_full_text | RDF object properties domain/range | GREEN |
| BR-INFOSEC-FULL-TEXT-SMOKE-005 | infosec_full_text | noun-chunk residue and metrics proxy | GREEN |

## Observed Metrics
| Case | Paragraphs | Claims | Evidence proxy | Classes | Object properties | Subclass facts | RDF bytes | RDF |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| infosec_full_text | 43 | 573 | 1.0 | 722 | 408 | 154 | 387036 | True |

## Artifacts
- tests/smoke/cases/infosec_full_text/artifacts/observed_infosec_full_text_semantic_claims.json
- tests/smoke/cases/infosec_full_text/artifacts/observed_infosec_full_text_graph_model.json
- tests/smoke/cases/infosec_full_text/artifacts/observed_infosec_full_text_output.rdf
- tests/smoke/cases/infosec_full_text/artifacts/observed_infosec_full_text_metrics.json

## Limits
Smoke/proxy only. No se creó gold semántico completo manual porque 43 párrafos requieren curación humana para precisión semántica real. Validación mide shape, consistencia, cobertura por párrafo, evidencia textual, RDF visible, projection.source_stage semantic_claims, domain/range y residuos conocidos. Contratos estrictos quedan en p001-p002 y p003-p004; el resto se trata como observacional/proxy.
