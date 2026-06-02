# TR-SQ-001 semantic quality

Scope: TB-SQ-001 RED. Tests exigen nuevo step_012_semantic_quality y corrimiento output_generation a step_013.
Verification: pytest -q -> RED esperado hasta implementar contrato.

Test Files
- tests/unit/pipeline/step_012_semantic_quality/test_semantic_quality_contract.py
- tests/unit/pipeline/step_013_output_generation/test_rdf_output_strategy_semantic_quality.py
- tests/integration/test_pipeline_semantic_quality_order.py
- tests/integration/test_pipeline_output_generation.py
- tests/smoke/test_infosec_3k_pipeline_smoke.py

Coverage Matrix
- test_semantic_quality_report_detects_entity_acronym_noise_and_preserves_original_payload
  -> UC-SQ-001 MF-1, FUN-SQ-001 AC-1, BR-SQ-001, BR-SQ-002, TB-SQ-001
- test_semantic_quality_report_detects_concept_noise_and_long_text_warnings
  -> UC-SQ-001 AF-1, FUN-SQ-001 AC-2, BR-SQ-003, BR-SQ-004, TB-SQ-001
- test_semantic_quality_report_sets_rdf_readiness_true_when_semantic_signal_exists
  -> UC-SQ-001 AF-2, FUN-SQ-001 AC-3, BR-SQ-005, TB-SQ-001
- test_semantic_quality_report_exposes_relation_gaps_key_even_when_empty
  -> UC-SQ-001 EF-1, FUN-SQ-001 AC-4, BR-SQ-006, TB-SQ-001
- test_rdf_output_generation_step_013_filters_excluded_acronyms_and_keeps_payload
  -> UC-SQ-002 MF-1, FUN-SQ-002 AC-1, CON-SQ-001 AC-1, BR-SQ-007, TB-SQ-001
- test_orion_process_runs_semantic_quality_between_type_assertion_and_output_generation
  -> UC-SQ-003 MF-1, FUN-SQ-003 AC-1, BR-SQ-008, TB-SQ-001
- test_orion_process_runs_output_generation_after_type_assertion_and_preserves_payload_plus_output
  -> UC-OUT-005 MF-1, FUN-OUT-004 AC-1, TB-SQ-001
- test_infosec_3k_pipeline_stage_log_artifact_has_12_stages_order_and_useful_snapshots
  -> UC-SMOKE-001 AF-4, FUN-SMOKE-001 AC-6, BR-SQ-008, TB-SQ-001

Untestable
- none
