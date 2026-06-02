# TR-REL-001 relation extraction

Scope: TB-REL-001 RED tests only. Production code intentionally untouched.

Test Files
- tests/unit/pipeline/step_008_relation_extraction/test_svo_relations.py
- tests/unit/pipeline/step_008_relation_extraction/test_copula_relations.py
- tests/unit/pipeline/step_008_relation_extraction/test_relation_entity_concept_mapping.py
- tests/unit/pipeline/step_008_relation_extraction/test_relation_determinism_dedupe.py
- tests/unit/pipeline/step_008_relation_extraction/test_empty_relations_and_payload_preservation.py
- tests/unit/test_relation_extraction_observability.py
- tests/integration/test_pipeline_full_relation_extraction.py

Coverage Matrix (tests -> specs)
- test_extracts_basic_svo_relation_with_required_fields_from_enriched_tokens
  -> UC-REL-001 MF-1, FUN-REL-001 AC-1, BR-REL-001, TB-REL-001
- test_extracts_simple_copula_relation_x_is_y
  -> UC-REL-001 AF-1, FUN-REL-001 AC-2, BR-REL-002, TB-REL-001
- test_subject_object_refs_map_to_existing_entity_or_concept_when_available
  -> UC-REL-002 MF-1, CON-REL-001 AC-1, BR-REL-003, TB-REL-001
- test_relation_generation_is_deterministic_deduplicated_and_stable_order
  -> UC-REL-003 MF-1, NFR-REL-001 AC-1, BR-REL-004, TB-REL-001
- test_no_relation_candidates_returns_empty_relations_and_preserves_payload
  -> UC-REL-001 AF-2, FUN-REL-001 AC-3, BR-REL-005, TB-REL-001
- test_relation_extraction_events_started_completed_and_no_raw_text_memory_sink
  -> UC-REL-005 MF-1, FUN-014 AC-2, FUN-016 AC-1, NFR-007 AC-2, BR-REL-006, TB-REL-001
- test_relation_extraction_failed_event_and_no_raw_text_jsonl
  -> UC-REL-005 EF-1, FUN-014 AC-3, FUN-016 AC-2, NFR-007 AC-2, BR-REL-006, TB-REL-001
- test_orion_process_runs_relation_extraction_after_concept_extraction_and_preserves_payload
  -> UC-REL-004 MF-1, FUN-REL-002 AC-1, FUN-REL-001 AC-1, FUN-REL-001 AC-3, TB-REL-001
