# TR-TYPE-001 type assertion

Scope: TB-TYPE-001 GREEN. Tests implemented. Production code implemented.
Verification: pytest -q -> GREEN (97 passed).

Test Files
- tests/unit/pipeline/step_011_type_assertion/test_copula_pattern.py
- tests/unit/pipeline/step_011_type_assertion/test_entity_label_mapping.py
- tests/unit/pipeline/step_011_type_assertion/test_no_subclass_false_positive.py
- tests/unit/pipeline/step_011_type_assertion/test_dedupe_determinism.py
- tests/unit/pipeline/step_011_type_assertion/test_empty_type_assertions_and_payload_preservation.py
- tests/unit/observability/test_type_assertion_events.py
- tests/integration/test_pipeline_type_assertion.py

Coverage Matrix (tests -> specs)
- test_extracts_instance_of_from_copula_john_is_a_person
  -> UC-TYPE-001 MF-1, FUN-TYPE-001 AC-1, BR-TYPE-001, TB-TYPE-001
- test_entity_label_mapping_generates_person_and_org_type_assertions
  -> UC-TYPE-001 AF-1, FUN-TYPE-001 AC-2, BR-TYPE-002, BR-TYPE-003, TB-TYPE-001
- test_does_not_emit_subclass_or_subclass_of_from_taxonomic_sentence
  -> UC-TYPE-002 EF-1, CON-TYPE-001 AC-1, BR-TYPE-004, TB-TYPE-001
- test_type_assertions_are_deduplicated_deterministic_and_stable_order
  -> UC-TYPE-003 MF-1, NFR-TYPE-001 AC-1, BR-TYPE-005, TB-TYPE-001
- test_no_signal_returns_empty_type_assertions_and_preserves_full_previous_payload
  -> UC-TYPE-002 AF-1, FUN-TYPE-001 AC-3, BR-TYPE-006, TB-TYPE-001
- test_type_assertion_events_started_completed_and_no_raw_text_memory_sink
  -> UC-TYPE-004 MF-1, FUN-014 AC-2, FUN-016 AC-1, NFR-007 AC-2, BR-TYPE-007, TB-TYPE-001
- test_type_assertion_failed_event_and_no_raw_text_jsonl
  -> UC-TYPE-004 EF-1, FUN-014 AC-3, FUN-016 AC-2, NFR-007 AC-2, BR-TYPE-007, TB-TYPE-001
- test_orion_process_runs_type_assertion_after_taxonomy_induction_and_preserves_payload
  -> UC-TYPE-005 MF-1, FUN-TYPE-002 AC-1, FUN-TYPE-001 AC-3, TB-TYPE-001
