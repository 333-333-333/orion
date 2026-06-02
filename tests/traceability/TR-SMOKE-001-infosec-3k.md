# TR-SMOKE-001 infosec 3k pipeline smoke

Scope: Smoke permanente para texto sintético largo de seguridad de la información, con artefactos persistentes de input, log sanitizado, output RDF y stage log de pipeline.
Verification: pytest -q -> GREEN.

Persisted Paths
- Input fixture: tests/smoke/fixtures/infosec_3k_input.txt
- Sanitized log artifact: tests/smoke/artifacts/infosec_3k_orion_events.jsonl
- RDF output artifact (required): tests/smoke/artifacts/infosec_3k_output.rdf
- RDF debug artifact (optional): tests/smoke/artifacts/infosec_3k_rdf_output.json
- Pipeline stage results artifact (required): tests/smoke/artifacts/infosec_3k_pipeline_stage_results.jsonl
- Smoke test: tests/smoke/test_infosec_3k_pipeline_smoke.py

Coverage Matrix (spec -> tests)
- UC-SMOKE-001 MF-1, FUN-SMOKE-001 AC-1, NFR-SMOKE-001 AC-1, CON-SMOKE-001 AC-1, BR-SMOKE-001
  -> test_infosec_3k_fixture_exists_and_word_count_is_about_3000
- UC-SMOKE-001 AF-1, FUN-SMOKE-001 AC-2, NFR-SMOKE-001 AC-2, CON-SMOKE-001 AC-2, BR-SMOKE-002
  -> test_infosec_3k_pipeline_no_crash_common_output_and_reasonable_counts[rdf]
  -> test_infosec_3k_pipeline_no_crash_common_output_and_reasonable_counts[owl]
- UC-SMOKE-001 EF-1, FUN-SMOKE-001 AC-3, NFR-SMOKE-SEC-001 AC-1, CON-SMOKE-SEC-001 AC-1, BR-SMOKE-003
  -> test_infosec_3k_persisted_artifact_log_is_sanitized_and_stable_shape
- UC-SMOKE-001 AF-2, FUN-SMOKE-001 AC-4, NFR-SMOKE-001 AC-3, CON-SMOKE-001 AC-3, BR-SMOKE-004
  -> test_infosec_3k_persisted_rdf_output_artifact_exists_and_is_real_rdf_xml_sanitized
- UC-SMOKE-001 AF-3, FUN-SMOKE-001 AC-5, CON-SMOKE-001 AC-4, BR-SMOKE-005
  -> test_infosec_3k_debug_json_artifact_optional_when_present_is_not_sensitive
- UC-SMOKE-001 AF-4, FUN-SMOKE-001 AC-6, NFR-SMOKE-001 AC-4, CON-SMOKE-001 AC-5, BR-SMOKE-006
  -> test_infosec_3k_pipeline_stage_log_artifact_has_12_stages_order_and_useful_snapshots
- UC-SMOKE-001 AF-5, FUN-SMOKE-001 AC-7, BR-SMOKE-007
  -> test_infosec_3k_stage_results_show_relation_gap_against_concept_signal
- UC-SMOKE-001 AF-6, FUN-SMOKE-001 AC-8, BR-SMOKE-008
  -> test_infosec_3k_taxonomy_candidates_must_reach_rdf_as_subclassof

Stage order contract
1. input_intake
2. preprocessing
3. sentence_segmentation
4. tokenization
5. linguistic_annotation
6. entity_extraction
7. concept_extraction
8. relation_extraction
9. triple_extraction
10. taxonomy_induction
11. type_assertion
12. output_generation

Result
- Status: GREEN
- Untestable: none
