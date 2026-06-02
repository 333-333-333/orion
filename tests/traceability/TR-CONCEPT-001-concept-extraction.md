# TR-CONCEPT-001 concept extraction

Scope: TB-CONCEPT-001 RED tests only. Production code intentionally untouched.

Test Files
- tests/unit/pipeline/step_007_concept_extraction/test_noun_chunks_to_concepts.py
- tests/unit/pipeline/step_007_concept_extraction/test_entity_label_to_concepts.py
- tests/unit/pipeline/step_007_concept_extraction/test_dedup_deterministic.py
- tests/unit/pipeline/step_007_concept_extraction/test_offsets_sentence_mapping.py
- tests/unit/pipeline/step_007_concept_extraction/test_empty_concepts_and_payload_preservation.py
- tests/unit/test_concept_extraction_observability.py
- tests/integration/test_pipeline_full_concept_extraction.py

Coverage Matrix (tests -> specs)
- test_noun_chunks_generate_concepts_with_required_fields_and_sources
  -> UC-CONCEPT-001 MF-1, FUN-CONCEPT-001 AC-1, BR-CONCEPT-001, TB-CONCEPT-001
- test_entity_labels_are_projected_to_concepts_source_entity_label
  -> UC-CONCEPT-001 AF-1, FUN-CONCEPT-001 AC-2, BR-CONCEPT-002, TB-CONCEPT-001
- test_concept_generation_is_deterministic_and_deduplicates_normalized_lemma_text
  -> UC-CONCEPT-002 MF-1, NFR-CONCEPT-001 AC-1, BR-CONCEPT-003, TB-CONCEPT-001
- test_concepts_use_preprocessed_offsets_and_sentence_mapping
  -> UC-CONCEPT-003 MF-1, CON-CONCEPT-001 AC-1, BR-CONCEPT-004, TB-CONCEPT-001
- test_empty_candidates_return_empty_concepts_and_preserve_payload_full
  -> UC-CONCEPT-001 AF-2, FUN-CONCEPT-001 AC-3, BR-CONCEPT-005, TB-CONCEPT-001
- test_concept_extraction_events_started_completed_and_no_raw_text_memory_sink
  -> UC-CONCEPT-004 MF-1, FUN-014 AC-2, FUN-016 AC-1, NFR-007 AC-2, BR-CONCEPT-006, TB-CONCEPT-001
- test_concept_extraction_failed_event_and_no_raw_text_jsonl
  -> UC-CONCEPT-004 EF-1, FUN-014 AC-3, FUN-016 AC-2, NFR-007 AC-2, BR-CONCEPT-006, TB-CONCEPT-001
- test_orion_process_runs_concept_extraction_after_entity_extraction_and_preserves_payload
  -> UC-CONCEPT-001 MF-1, UC-CONCEPT-002 MF-1, FUN-CONCEPT-001 AC-1, FUN-CONCEPT-001 AC-2, FUN-CONCEPT-001 AC-3, TB-CONCEPT-001
