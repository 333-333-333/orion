# TR-TRIPLE-001 triple extraction

Scope: TB-TRIPLE-001 final GREEN. Tests implemented and production implementation completed. Latest verification: pytest -q => 84 passed.

Test Files
- tests/unit/pipeline/step_009_triple_extraction/test_relation_to_triple.py
- tests/unit/pipeline/step_009_triple_extraction/test_dedup_determinism.py
- tests/unit/pipeline/step_009_triple_extraction/test_empty_triples_and_payload_preservation.py
- tests/unit/test_triple_extraction_observability.py
- tests/integration/test_pipeline_full_triple_extraction.py

Coverage Matrix (tests -> specs)
- test_valid_relation_maps_to_triple_with_required_fields_and_refs_fallback
  -> UC-TRIPLE-001 MF-1, FUN-TRIPLE-001 AC-1, BR-TRIPLE-001, BR-TRIPLE-002, TB-TRIPLE-001
- test_triple_generation_is_deterministic_deduplicated_and_stable_order
  -> UC-TRIPLE-002 MF-1, NFR-TRIPLE-001 AC-1, BR-TRIPLE-003, TB-TRIPLE-001
- test_no_relations_returns_empty_triples_and_preserves_previous_payload_complete
  -> UC-TRIPLE-001 AF-1, FUN-TRIPLE-001 AC-2, BR-TRIPLE-004, TB-TRIPLE-001
- test_orion_process_runs_triple_extraction_after_relation_extraction_and_preserves_payload
  -> UC-TRIPLE-003 MF-1, FUN-TRIPLE-002 AC-1, FUN-TRIPLE-001 AC-1, FUN-TRIPLE-001 AC-2, TB-TRIPLE-001
- test_triple_extraction_events_started_completed_and_no_raw_text_memory_sink
  -> UC-TRIPLE-004 MF-1, FUN-014 AC-2, FUN-016 AC-1, NFR-007 AC-2, BR-TRIPLE-005, TB-TRIPLE-001
- test_triple_extraction_failed_event_and_no_raw_text_jsonl
  -> UC-TRIPLE-004 EF-1, FUN-014 AC-3, FUN-016 AC-2, NFR-007 AC-2, BR-TRIPLE-005, TB-TRIPLE-001
