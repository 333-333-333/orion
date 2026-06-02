# TR-PRP-001 preprocessing

Scope: TB-PRP-001 RED tests only. Production code intentionally untouched.

Test Files
- tests/unit/pipeline/step_002_preprocessing/test_contract.py
- tests/unit/pipeline/step_002_preprocessing/test_normalization.py
- tests/unit/pipeline/step_002_preprocessing/test_empty_cleanup.py
- tests/unit/pipeline/step_002_preprocessing/test_operations.py
- tests/integration/test_process_preprocessing.py
- tests/fixtures/preprocessing/sample_input.txt

Coverage Matrix (tests -> specs)
- test_preprocessing_contract_preserves_raw_text_and_source_metadata_and_adds_outputs
  -> UC-002, UC-003, FUN-003, FUN-004, FUN-013, US-003, US-004
- test_preprocessing_contract_keeps_case_intact_and_does_not_lowercase_text
  -> UC-002, UC-006, NFR-001, NFR-002, US-019
- test_preprocessing_unicode_normalization_is_deterministic_and_repeatable
  -> UC-002, FUN-003, NFR-001, NFR-005, US-027
- test_preprocessing_collapses_repeated_spaces_and_normalizes_newlines_only
  -> UC-002, FUN-003, NFR-005, NFR-008
- test_preprocessing_does_not_do_tokenization_segmentation_or_lemmatization_side_effects
  -> UC-002, FUN-013, CON-010, NFR-007
- test_preprocessing_raises_orion_error_when_cleanup_results_in_empty_text
  -> UC-002, FUN-013, US-013
- test_preprocessing_operations_applied_reports_expected_operations_in_order
  -> UC-006, FUN-015, NFR-006
- test_preprocessing_failed_event_omits_raw_text_from_event_payload_when_error_happens
  -> UC-002, NFR-007, CON-010, US-019
- test_orion_process_string_runs_input_intake_then_preprocessing_and_preserves_contract
  -> UC-002, FUN-003, NFR-001, NFR-002, US-003
- test_orion_process_path_runs_preprocessing_and_keeps_source_text_id_and_raw_text
  -> UC-003, FUN-004, CON-006, US-004

Requested Trace IDs presence
- UC-002 covered
- UC-003 covered
- UC-006 covered
- US-003 covered
- US-004 covered
- US-013 covered
- US-019 covered
- US-027 covered
- FUN-003 covered
- FUN-004 covered
- FUN-013 covered
- FUN-014 covered (event expectations in integration/unit preprocessing logging checks)
- FUN-015 covered
- NFR-001 covered
- NFR-002 covered
- NFR-005 covered
- NFR-006 covered
- NFR-007 covered
- NFR-008 covered
- CON-006 covered
- CON-010 covered
