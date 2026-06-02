# TR-TOK-001 tokenization

Scope: TB-TOK-001 RED tests only. Production code intentionally untouched.

Test Files
- tests/unit/pipeline/step_004_tokenization/test_split.py
- tests/unit/pipeline/step_004_tokenization/test_offsets.py
- tests/integration/test_pipeline_tokenization.py

Coverage Matrix (tests -> specs)
- test_tokenization_splits_words_and_punctuation_deterministically_and_preserves_sentence_order
  -> UC-002 MF-4, UC-003 MF-4, FUN-017 AC-1, FUN-017 AC-2, CON-010 AC-1, BR-TOK-001
- test_tokenization_is_deterministic_with_stable_token_ids_and_indices
  -> UC-006 AF-2, FUN-018 AC-1, NFR-001 AC-2, NFR-002 AC-2, BR-TOK-001
- test_token_offsets_are_relative_to_preprocessed_text_and_match_spans
  -> UC-006 MF-6, FUN-018 AC-2, NFR-005 AC-2, CON-006 AC-2, BR-TOK-002
- test_each_token_exposes_required_contract_fields
  -> UC-002 EF-2, FUN-017 AC-3, BR-TOK-002
- test_orion_process_includes_tokenization_output_and_preserves_previous_phase_data
  -> UC-002 MF-1/MF-2/MF-3/MF-4, FUN-017 AC-1, FUN-017 AC-2
- test_tokenization_events_started_completed_failed_exist_and_do_not_expose_raw_text
  -> UC-006 MF-7, FUN-014 AC-2, NFR-006 AC-2, NFR-007 AC-2, NFR-008 AC-2, CON-010 AC-2


JSONL Tokenization Coverage
- test_tokenization_events_persist_jsonl_with_pipeline_order_and_without_raw_text
  -> UC-006 MF-7, FUN-016 AC-1, FUN-016 AC-2, NFR-006 AC-2, NFR-007 AC-2, CON-011 AC-1
- test_tokenization_failed_event_persists_jsonl_without_raw_text
  -> UC-006 EF-1, FUN-014 AC-3, FUN-016 AC-2, NFR-006 AC-6, NFR-007 AC-2, CON-011 AC-1

BR Coverage Minimum
- BR-TOK-001 satisfaction: split deterministic words/punctuation
- BR-TOK-001 violation-attempt: deterministic replay asserts no drift
- BR-TOK-002 satisfaction: offsets map exact span in preprocessed_text
- BR-TOK-002 violation-attempt: required token fields and offsets consistency enforced
