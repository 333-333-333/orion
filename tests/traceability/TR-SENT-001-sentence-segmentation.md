# TR-SENT-001 sentence segmentation

Scope: TB-SENT-001 RED tests only. Production code intentionally untouched.

Test Files
- tests/unit/pipeline/step_003_sentence_segmentation/test_sentence_segmentation_split_basic.py
- tests/unit/pipeline/step_003_sentence_segmentation/test_sentence_segmentation_offsets_determinism.py
- tests/integration/test_process_sentence_segmentation.py

Coverage Matrix (tests -> specs)
- test_sentence_segmentation_splits_by_dot_question_exclamation_no_empty_and_keeps_order
  -> UC-002, UC-003, US-003, US-004, FUN-003, FUN-004, FUN-013, NFR-001, NFR-002, CON-010
- test_sentence_segmentation_is_deterministic_with_stable_sentence_ids_and_offsets_on_preprocessed_text
  -> UC-006, US-013, US-027, FUN-015, NFR-001, NFR-002, NFR-005, CON-006
- test_orion_process_runs_input_intake_then_preprocessing_then_sentence_segmentation_and_preserves_raw_text
  -> UC-002, UC-003, US-003, FUN-003, FUN-013, NFR-006, NFR-008
- test_sentence_segmentation_events_started_completed_failed_exist_and_never_expose_raw_text
  -> UC-006, US-004, US-013, FUN-014, FUN-015, NFR-007, NFR-008, CON-010

Requested Trace IDs presence
- UC-002 covered
- UC-003 covered
- UC-006 covered
- US-003 covered
- US-004 covered
- US-013 covered
- US-027 covered
- FUN-003 covered
- FUN-004 covered
- FUN-013 covered
- FUN-014 covered
- FUN-015 covered
- NFR-001 covered
- NFR-002 covered
- NFR-005 covered
- NFR-006 covered
- NFR-007 covered
- NFR-008 covered
- CON-006 covered
- CON-010 covered
