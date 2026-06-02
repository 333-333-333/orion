# TR-RDF-007 Semantic Core Coverage from infosec_3k RED

- UC-SMOKE-001 AF-11 -> test_infosec_3k_min_semantic_core_coverage_from_full_fixture_document
- FUN-SMOKE-001 AC-13 -> test_infosec_3k_min_semantic_core_coverage_from_full_fixture_document
- CON-SMOKE-RDF-006 AC-1 -> test_infosec_3k_min_semantic_core_coverage_from_full_fixture_document
- BR-SMOKE-016 -> test_infosec_3k_min_semantic_core_coverage_from_full_fixture_document
- BR-SMOKE-017 -> test_infosec_3k_min_semantic_core_coverage_from_full_fixture_document
- BR-SMOKE-018 -> test_infosec_3k_min_semantic_core_coverage_from_full_fixture_document
- BR-SMOKE-019 -> test_infosec_3k_min_semantic_core_coverage_from_full_fixture_document
- BR-SMOKE-020 -> test_infosec_3k_min_semantic_core_coverage_from_full_fixture_document
- BR-SMOKE-021 -> test_infosec_3k_min_semantic_core_coverage_from_full_fixture_document
- BR-SMOKE-022 -> test_infosec_3k_min_semantic_core_coverage_from_full_fixture_document
- BR-SMOKE-023 -> test_infosec_3k_min_semantic_core_coverage_from_full_fixture_document
- BR-SMOKE-023 relation-chain -> threat exploits vulnerability + threat affects asset (texto explícito fixture)
- UC-SMOKE-001 AF-12 -> test_infosec_3k_strict_full_document_semantic_contract_red_gate
- FUN-SMOKE-001 AC-14 -> test_infosec_3k_strict_full_document_semantic_contract_red_gate
- NFR-SMOKE-SEC-002 AC-1 -> test_infosec_3k_strict_full_document_semantic_contract_red_gate
- CON-SMOKE-RDF-007 AC-1 -> test_infosec_3k_strict_full_document_semantic_contract_red_gate
- BR-SMOKE-024 -> test_infosec_3k_strict_full_document_semantic_contract_red_gate
- BR-SMOKE-025 -> test_infosec_3k_strict_full_document_semantic_contract_red_gate
- BR-SMOKE-026 -> test_infosec_3k_strict_full_document_semantic_contract_red_gate
- BR-SMOKE-027 -> test_infosec_3k_strict_full_document_semantic_contract_red_gate
- BR-SMOKE-028 -> test_infosec_3k_strict_full_document_semantic_contract_red_gate
- BR-SMOKE-029 -> test_infosec_3k_strict_full_document_semantic_contract_red_gate

- CON-SMOKE-RDF-007 AC-2 -> hallazgo_coverage_ratio >= 0.85 (core infosec, auditoría, SIEM/logging, retention, remediation, backup/recovery, MFA/password/key/token, encryption/data, cloud bucket, API, vendor, training/awareness, physical/camera/office, properties/domain/range inferibles desde graph.object_property_schema declarado, prohibiciones WebVOWL)
- NFR-SMOKE-SEC-002 AC-2 -> fail gate when hallazgo_coverage_ratio < 0.85

- CON-SMOKE-RDF-007 AC-3 -> facts_count>=500 y relation_extraction_count>=450 quedan en modo diagnóstico/advisory (no hard fail de contrato)

- UC-SMOKE-001 AF-13 -> test_infosec_3k_rdfxml_blocks_canonical_duplicate_entities_by_casing_or_namespace_role_conflict
- FUN-SMOKE-001 AC-15 -> test_infosec_3k_rdfxml_blocks_canonical_duplicate_entities_by_casing_or_namespace_role_conflict
- CON-SMOKE-RDF-008 AC-1 -> test_infosec_3k_rdfxml_blocks_canonical_duplicate_entities_by_casing_or_namespace_role_conflict
- BR-SMOKE-030 -> test_infosec_3k_rdfxml_blocks_canonical_duplicate_entities_by_casing_or_namespace_role_conflict
- BR-SMOKE-031 -> test_infosec_3k_rdfxml_blocks_canonical_duplicate_entities_by_casing_or_namespace_role_conflict

- UC-SMOKE-001 AF-14 -> test_infosec_3k_risk_must_not_be_semantically_isolated_when_present
- FUN-SMOKE-001 AC-16 -> test_infosec_3k_risk_must_not_be_semantically_isolated_when_present
- CON-SMOKE-RDF-009 AC-1 -> test_infosec_3k_risk_must_not_be_semantically_isolated_when_present
- BR-SMOKE-032 -> test_infosec_3k_risk_must_not_be_semantically_isolated_when_present
- BR-SMOKE-033 -> test_infosec_3k_risk_must_not_be_semantically_isolated_when_present
- AF-14 criterio actualizado: Risk no aislado si hay enlace OWL o facts RDF reales con predicado textual observado; sin allowlist semántica inventada.

- UC-SMOKE-001 AF-15 -> test_infosec_3k_log_and_logging_must_stay_distinct_but_explicitly_connected
- FUN-SMOKE-001 AC-17 -> test_infosec_3k_log_and_logging_must_stay_distinct_but_explicitly_connected
- CON-SMOKE-RDF-010 AC-1 -> test_infosec_3k_log_and_logging_must_stay_distinct_but_explicitly_connected
- BR-SMOKE-034 -> test_infosec_3k_log_and_logging_must_stay_distinct_but_explicitly_connected
- BR-SMOKE-035 -> test_infosec_3k_log_and_logging_must_stay_distinct_but_explicitly_connected

- UC-SMOKE-001 AF-16 -> test_infosec_3k_webvowl_min_labels_and_restriction_identifiability_contract_red_smoke
- FUN-SMOKE-001 AC-18 -> test_infosec_3k_webvowl_min_labels_and_restriction_identifiability_contract_red_smoke
- CON-SMOKE-RDF-011 AC-1 -> test_infosec_3k_webvowl_min_labels_and_restriction_identifiability_contract_red_smoke
- BR-SMOKE-036 -> test_infosec_3k_webvowl_min_labels_and_restriction_identifiability_contract_red_smoke
- BR-SMOKE-037 -> test_infosec_3k_webvowl_min_labels_and_restriction_identifiability_contract_red_smoke

- UC-SMOKE-001 AF-17 -> test_infosec_3k_webvowl_restriction_domain_contract_no_top_level_orphans_red_smoke
- FUN-SMOKE-001 AC-19 -> test_infosec_3k_webvowl_restriction_domain_contract_no_top_level_orphans_red_smoke
- CON-SMOKE-RDF-012 AC-1 -> test_infosec_3k_webvowl_restriction_domain_contract_no_top_level_orphans_red_smoke
- BR-SMOKE-038 -> test_infosec_3k_webvowl_restriction_domain_contract_no_top_level_orphans_red_smoke
- BR-SMOKE-039 -> test_infosec_3k_webvowl_restriction_domain_contract_no_top_level_orphans_red_smoke


- UC-SMOKE-001 AF-18 -> test_infosec_3k_webvowl_no_duplicated_visible_domain_edges_by_modeling_style_red_smoke
- FUN-SMOKE-001 AC-20 -> test_infosec_3k_webvowl_no_duplicated_visible_domain_edges_by_modeling_style_red_smoke
- CON-SMOKE-RDF-013 AC-1 -> test_infosec_3k_webvowl_no_duplicated_visible_domain_edges_by_modeling_style_red_smoke
- BR-SMOKE-040 -> test_infosec_3k_webvowl_no_duplicated_visible_domain_edges_by_modeling_style_red_smoke
- BR-SMOKE-041 -> test_infosec_3k_webvowl_no_duplicated_visible_domain_edges_by_modeling_style_red_smoke


- UC-SMOKE-001 AF-19 -> test_infosec_3k_webvowl_visual_contract_reified_statements_must_be_named_and_meaningful_red_smoke
- FUN-SMOKE-001 AC-21 -> test_infosec_3k_webvowl_visual_contract_reified_statements_must_be_named_and_meaningful_red_smoke
- CON-SMOKE-RDF-017 AC-1 -> test_infosec_3k_webvowl_visual_contract_reified_statements_must_be_named_and_meaningful_red_smoke
- BR-SMOKE-049 -> test_infosec_3k_webvowl_visual_contract_reified_statements_must_be_named_and_meaningful_red_smoke
- BR-SMOKE-050 -> test_infosec_3k_webvowl_visual_contract_reified_statements_must_be_named_and_meaningful_red_smoke

- UC-SMOKE-001 AF-20 -> test_infosec_3k_webvowl_reified_context_nodes_must_have_visual_name_contract_red_smoke
- FUN-SMOKE-001 AC-22 -> test_infosec_3k_webvowl_reified_context_nodes_must_have_visual_name_contract_red_smoke
- CON-SMOKE-RDF-018 AC-1 -> test_infosec_3k_webvowl_reified_context_nodes_must_have_visual_name_contract_red_smoke
- BR-SMOKE-051 -> test_infosec_3k_webvowl_reified_context_nodes_must_have_visual_name_contract_red_smoke
- BR-SMOKE-052 -> test_infosec_3k_webvowl_reified_context_nodes_must_have_visual_name_contract_red_smoke
