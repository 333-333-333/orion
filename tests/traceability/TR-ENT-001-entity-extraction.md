# TR-ENT-001 entity extraction

Scope: TB-ENT-001 RED tests only. Production code intentionally untouched.

Test Files
- tests/unit/pipeline/step_006_entity_extraction/test_extract_entities_from_doc.py
- tests/unit/pipeline/step_006_entity_extraction/test_entity_offsets_sentence_mapping.py
- tests/unit/pipeline/step_006_entity_extraction/test_entity_id_determinism.py
- tests/unit/pipeline/step_006_entity_extraction/test_empty_entities.py
- tests/unit/test_entity_extraction_observability.py
- tests/integration/test_pipeline_full_entity_extraction.py

Coverage Matrix (tests -> specs)
- test_extract_entities_from_doc_adds_entities_and_preserves_existing_payload_fields
  -> UC-002 MF-6, FUN-ENT-001 AC-1, BR-ENT-001, TB-ENT-001
- test_entities_use_offsets_relative_to_preprocessed_text_and_map_to_sentence_id_by_span
  -> UC-006 MF-9, FUN-ENT-001 AC-2, BR-ENT-002, TB-ENT-001
- test_entity_id_is_deterministic_for_same_payload_and_doc_entities
  -> UC-004 MF-3, NFR-001 AC-1, BR-ENT-003, TB-ENT-001
- test_extract_entities_from_doc_returns_empty_entities_when_doc_has_no_entities
  -> UC-002 AF-2, FUN-ENT-001 AC-3, BR-ENT-004, TB-ENT-001
- test_entity_extraction_events_started_completed_and_no_raw_text_memory_sink
  -> UC-006 MF-10, FUN-014 AC-2, FUN-016 AC-1, NFR-007 AC-2, BR-ENT-005, TB-ENT-001
- test_entity_extraction_failed_event_and_no_raw_text_jsonl
  -> UC-006 EF-3, FUN-014 AC-3, FUN-016 AC-2, NFR-007 AC-2, BR-ENT-005, TB-ENT-001
- test_orion_process_runs_entity_extraction_after_linguistic_annotation_and_preserves_payload
  -> UC-002 MF-6, FUN-ENT-001 AC-1, FUN-ENT-001 AC-2, FUN-ENT-001 AC-3, TB-ENT-001
