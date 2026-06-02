# TR-LING-001 linguistic-annotation

Scope: TB-LING-001 RED tests only. Production code untouched.

Test Files
- tests/unit/test_orion_config.py
- tests/unit/test_spacy_model_loading.py
- tests/unit/test_linguistic_annotation_output.py
- tests/integration/test_pipeline_full_linguistic_annotation.py
- tests/unit/test_linguistic_annotation_observability.py

Coverage Matrix (spec/BR -> tests)
- UC-001 MF-2 | FUN-002 AC-1 | CON-008 AC-1 | BR-LING-001
  -> test_orion_config_uses_en_core_web_lg_when_spacy_model_is_none
- UC-001 EF-1 | FUN-013 AC-1 | CON-008 AC-2 | BR-LING-001
  -> test_orion_config_rejects_empty_spacy_model_string
- UC-001 AF-1 | FUN-002 AC-1 | CON-008 AC-3 | BR-LING-001
  -> test_orion_config_accepts_non_empty_spacy_model_string
- UC-001 EF-2 | FUN-013 AC-1 | CON-005 AC-1 | BR-LING-002
  -> test_spacy_model_load_missing_raises_orion_exception_not_raw_import_or_os_error
- UC-002 MF-5 | FUN-LING-001 AC-1 | BR-LING-003
  -> test_linguistic_annotation_enriches_each_token_and_preserves_token_contract
- UC-002 MF-5 | FUN-LING-001 AC-2 | BR-LING-004
  -> test_linguistic_annotation_keeps_offsets_relative_to_preprocessed_text
- UC-002 MF-1..MF-5 | FUN-LING-001 AC-1
  -> test_orion_process_runs_linguistic_annotation_after_tokenization_and_preserves_payload
- UC-006 MF-8 | FUN-014 AC-2 | FUN-016 AC-1 | NFR-007 AC-2 | BR-LING-005
  -> test_linguistic_annotation_events_started_completed_and_no_raw_text_memory_sink
- UC-006 EF-2 | FUN-014 AC-3 | FUN-016 AC-2 | NFR-007 AC-2 | BR-LING-005
  -> test_linguistic_annotation_failed_event_and_no_raw_text_jsonl

BR Coverage Minimum
- BR-LING-001 satisfaction: None defaults to en_core_web_lg
- BR-LING-001 violation-attempt: empty string fails validation
- BR-LING-002 satisfaction: valid model path allowed for setup
- BR-LING-002 violation-attempt: missing model cannot leak raw ImportError/OSError
- BR-LING-003 satisfaction: tokens enriched with lemma/pos/tag/dependency
- BR-LING-003 violation-attempt: missing enriched fields fails contract assertions
- BR-LING-004 satisfaction: offsets still map preprocessed_text spans
- BR-LING-004 violation-attempt: offset mismatch fails
- BR-LING-005 satisfaction: started/completed events emitted sanitized
- BR-LING-005 violation-attempt: failed event emitted sanitized
