# TR-NS-001 namespace config

Scope: TB-NS-001 GREEN final. Tests implementados y producción implementada.
Verification: pytest -q -> GREEN (120 passed).

Test Files
- tests/unit/pipeline/step_012_output_generation/test_namespace_config.py
- tests/unit/pipeline/step_012_output_generation/test_namespace_validation.py
- tests/unit/pipeline/step_012_output_generation/test_namespace_helpers.py
- tests/unit/pipeline/step_012_output_generation/test_rdf_owl_namespaces.py
- tests/integration/test_namespace_pipeline.py

Coverage Matrix (tests -> specs)
- test_orion_config_sets_namespace_defaults_when_not_provided
  -> UC-NS-001 MF-1, FUN-NS-001 AC-1, CON-NS-001 AC-1, BR-NS-001, TB-NS-001
- test_orion_config_accepts_custom_base_iri_and_custom_prefixes_preserving_reserved
  -> UC-NS-001 AF-1, FUN-NS-001 AC-2, CON-NS-001 AC-2, BR-NS-001, BR-NS-004, TB-NS-001
- test_orion_config_from_mapping_supports_base_iri_and_prefixes
  -> UC-NS-001 EF-1, FUN-NS-001 AC-3, CON-NS-001 AC-3, BR-NS-001, BR-NS-003, TB-NS-001
- test_orion_config_rejects_empty_base_iri
  -> UC-NS-002 EF-1, FUN-NS-002 AC-1, CON-NS-002 AC-1, BR-NS-002, TB-NS-001
- test_orion_config_rejects_non_absolute_or_non_http_base_iri
  -> UC-NS-002 EF-2, FUN-NS-002 AC-2, CON-NS-002 AC-2, BR-NS-002, TB-NS-001
- test_orion_config_rejects_empty_prefixes_map_and_empty_prefix_values
  -> UC-NS-002 EF-3, FUN-NS-002 AC-3, CON-NS-002 AC-3, BR-NS-004, TB-NS-001
- test_orion_config_rejects_overriding_reserved_prefixes_with_invalid_values
  -> UC-NS-002 EF-4, FUN-NS-002 AC-4, CON-NS-002 AC-4, BR-NS-003, TB-NS-001
- test_slugify_iri_part_supports_pascal_case_camel_case_and_individual_style
  -> UC-NS-003 MF-1, FUN-NS-003 AC-1, BR-NS-005, TB-NS-001
- test_make_iri_builds_stable_class_predicate_individual_iris
  -> UC-NS-003 AF-1, FUN-NS-003 AC-2, BR-NS-006, TB-NS-001
- test_compact_iri_uses_known_prefixes_and_keeps_unknown_full_iri
  -> UC-NS-003 EF-1, FUN-NS-003 AC-3, BR-NS-007, TB-NS-001
- test_rdf_output_uses_stable_iris_and_compact_reserved_predicates
  -> UC-NS-004 MF-1, FUN-NS-004 AC-1, BR-NS-008, BR-NS-009, TB-NS-001
- test_owl_output_uses_namespace_aware_iris_for_classes_individuals_and_properties
  -> UC-NS-004 AF-1, FUN-NS-004 AC-2, NFR-NS-001 AC-1, BR-NS-010, TB-NS-001
- test_orion_process_accepts_namespace_config_and_emits_namespace_aware_output
  -> UC-NS-005 MF-1, FUN-NS-005 AC-1, CON-NS-003 AC-1, BR-NS-011, TB-NS-001
