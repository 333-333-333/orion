# TR-TAX-001 taxonomy induction

Scope: TB-TAX-001 final GREEN. Tests implemented and production code implemented.
Verification: pytest -q -> 89 passed.

Test Files
- tests/unit/pipeline/step_010_taxonomy_induction/test_patterns.py
- tests/unit/pipeline/step_010_taxonomy_induction/test_dedupe_payload.py
- tests/integration/test_pipeline_taxonomy_induction.py
- tests/unit/observability/test_taxonomy_induction_events.py

Coverage Matrix (tests -> specs)
- test_extracts_taxonomy_relations_from_supported_patterns_and_rejects_instance_case
  -> UC-TAX-001 MF-1, UC-TAX-001 AF-1, UC-TAX-001 AF-2, FUN-TAX-001 AC-1, FUN-TAX-001 AC-2, BR-TAX-001, BR-TAX-002, BR-TAX-003, TB-TAX-001
- test_taxonomy_is_deterministic_deduplicated_stable_and_preserves_payload_when_no_signal
  -> UC-TAX-002 MF-1, UC-TAX-001 AF-3, FUN-TAX-001 AC-3, FUN-TAX-001 AC-4, NFR-TAX-001 AC-1, BR-TAX-004, BR-TAX-005, TB-TAX-001
- test_orion_process_runs_taxonomy_induction_after_triple_extraction_and_preserves_payload
  -> UC-TAX-003 MF-1, FUN-TAX-002 AC-1, FUN-TAX-001 AC-4, TB-TAX-001
- test_taxonomy_induction_events_started_completed_and_no_raw_text_memory_sink
  -> UC-TAX-004 MF-1, FUN-014 AC-2, FUN-016 AC-1, NFR-007 AC-2, BR-TAX-006, TB-TAX-001
- test_taxonomy_induction_failed_event_and_no_raw_text_jsonl
  -> UC-TAX-004 EF-1, FUN-014 AC-3, FUN-016 AC-2, NFR-007 AC-2, BR-TAX-006, TB-TAX-001
