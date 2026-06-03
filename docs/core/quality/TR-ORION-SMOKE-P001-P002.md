---
id: TR-ORION-SMOKE-P001-P002
type: test-report
status: red
spec_ref: TASK-SMOKE-P001-P002
created: 2026-06-03
---

# TR-ORION-SMOKE-P001-P002 — Themis RED smoke modular p001-p002

## Scope
Valida contrato ontológico determinístico para los fixtures reales tests/smoke/fixtures/infosec_3k_paragraphs/p001.txt y p002.txt, sin tocar src productivo y sin ejecutar smoke infosec 3k completo.

## Contrato esperado extraído
Clases exactas: information-security, discipline, information-asset, resource, organization, information, threat, internal-threat, external-threat, confidential-document, corporate-database, customer-record, source-code-repository, system-configuration-file, backup-archive, business-report, confidentiality, integrity, availability, security-property, authorized-entity, system, cia-triad, foundational-model.

SubClassOf directos: information-security→discipline; internal-threat→threat; external-threat→threat; confidential-document/corporate-database/customer-record/source-code-repository/system-configuration-file/backup-archive/business-report→information-asset; confidentiality/integrity/availability→security-property; cia-triad→foundational-model.

Object properties con domain/range: protects(information-security, information-asset); protects-against(information-security, threat); has-value-for(resource, organization); stores/processes/transmits/represents(information-asset, information); preserves(information-security, security-property); ensures-accessible-to(confidentiality, authorized-entity); ensures-accuracy-of(integrity, information); ensures-availability-of(availability, system); forms(security-property, cia-triad); models(cia-triad, information-security).

Comentarios rdfs:comment: definiciones completas de information-security, information-asset, confidentiality, integrity, availability, cia-triad, foundational-model.

Negativos: no orion:be, no TypeOfInformationAsset, no clases artificiales de definición, no noun chunks descriptivos DisciplineFocusedOnProtectingInformationAssets, AnyResourceThatHasValueForAnOrganization, ResourceThat, ValueForAnOrganization; determinantes removidos; salida pequeña <= 30 clases.

## Coverage Matrix
| Spec | Test file | Test case | Expected status |
|---|---|---|---|
| TASK-SMOKE-P001-P002; FUN-SMOKE-P001-P002 AC-1; CON-SMOKE-P001-P002 AC-1; BR-SMOKE-P001-P002-001 | tests/smoke/cases/infosec_p001_p002/test_infosec_p001_p002_modular_contract_smoke.py | test_p001_p002_modular_contract_has_exact_small_deterministic_classes | RED |
| TASK-SMOKE-P001-P002; FUN-SMOKE-P001-P002 AC-2; CON-SMOKE-P001-P002 AC-2; BR-SMOKE-P001-P002-002 | tests/smoke/cases/infosec_p001_p002/test_infosec_p001_p002_modular_contract_smoke.py | test_p001_p002_modular_contract_maps_type_statements_to_direct_subclassof | RED |
| TASK-SMOKE-P001-P002; FUN-SMOKE-P001-P002 AC-3; CON-SMOKE-P001-P002 AC-3; BR-SMOKE-P001-P002-003 | tests/smoke/cases/infosec_p001_p002/test_infosec_p001_p002_modular_contract_smoke.py | test_p001_p002_modular_contract_keeps_definitions_as_comments | RED |
| TASK-SMOKE-P001-P002; FUN-SMOKE-P001-P002 AC-4; CON-SMOKE-P001-P002 AC-4; BR-SMOKE-P001-P002-004 | tests/smoke/cases/infosec_p001_p002/test_infosec_p001_p002_modular_contract_smoke.py | test_p001_p002_modular_contract_has_expected_object_properties_with_domain_range | RED |

## Validation command
python3 tests/smoke/run_infosec_smoke_suite.py

## RED result
4 failed in 2.50s; runner returncode 1; phase RED confirmed.

Failures are product contract failures: noisy/duplicate classes, missing expected clean classes, missing direct subclass pairs, no rdfs:comment definitions, and missing expected object properties with domain/range.

## 3k execution guard evidence
Runner selected_tests contained only tests/smoke/cases/infosec_p001_p002/test_infosec_p001_p002_modular_contract_smoke.py. Runner metadata disabled tests/smoke/test_infosec_3k_pipeline_smoke.py, tests/smoke/test_infosec_3k_paragraphs_smoke.py, tests/smoke/test_infosec_paragraph_semantics_smoke.py. Pytest collected 4 items only.

## Artifacts touched
Runner validation rewrote tests/smoke/artifacts/infosec_smoke_runner.jsonl only.
