---
id: TR-ORION-CANONICAL-CLAIMS-P001-P002
type: test-report
status: red
spec_ref: TASK-CANONICAL-CLAIMS-P001-P002
created: 2026-06-02
---

# TR-ORION-CANONICAL-CLAIMS-P001-P002 — Themis RED canonical_claims p001-p002

## Scope
Valida nueva etapa intermedia canonical_claims para los fixtures reales tests/smoke/fixtures/infosec_3k_paragraphs/p001.txt y p002.txt. La etapa debe existir antes de extracción de tripletas y antes de RDF, preservar assets por párrafo y exponer statements normalizados explícitos, no RDF.

## Contrato claims esperado
p001: InformationSecurity is a Discipline; InformationSecurity is focused on protecting InformationAsset; InformationSecurity protects against InternalThreat; InformationSecurity protects against ExternalThreat; InformationAsset is a Resource; InformationAsset has value for Organization; InformationAsset stores Information; InformationAsset processes Information; InformationAsset transmits Information; InformationAsset represents Information; ConfidentialDocument is a type of InformationAsset; CorporateDatabase is a type of InformationAsset; CustomerRecord is a type of InformationAsset; SourceCodeRepository is a type of InformationAsset; SystemConfigurationFile is a type of InformationAsset; BackupArchive is a type of InformationAsset; BusinessReport is a type of InformationAsset.

p002: InformationSecurity preserves Confidentiality; InformationSecurity preserves Integrity; InformationSecurity preserves Availability; Confidentiality is a SecurityProperty; Integrity is a SecurityProperty; Availability is a SecurityProperty; Confidentiality ensures Information is accessible only to AuthorizedEntity; Integrity ensures Information is accurate; Integrity ensures Information is complete; Integrity protects Information against UnauthorizedModification; Availability ensures Information is accessible when needed; Availability ensures System is accessible when needed; SecurityProperty forms CIATriad; CIATriad is a FoundationalModel; CIATriad is a model for InformationSecurity.

## Coverage Matrix
| Spec | Test file | Test case | Expected status |
|---|---|---|---|
| TASK-CANONICAL-CLAIMS-P001-P002; FUN-CANONICAL-CLAIMS-P001-P002 AC-1; CON-CANONICAL-CLAIMS-P001-P002 AC-1; BR-CANONICAL-CLAIMS-P001-P002-001 | tests/smoke/cases/infosec_p001_p002/test_infosec_p001_p002_canonical_claims_red_smoke.py | test_p001_p002_canonical_claims_stage_exists_before_triples_and_rdf | RED |
| TASK-CANONICAL-CLAIMS-P001-P002; FUN-CANONICAL-CLAIMS-P001-P002 AC-2; CON-CANONICAL-CLAIMS-P001-P002 AC-2; BR-CANONICAL-CLAIMS-P001-P002-002 | tests/smoke/cases/infosec_p001_p002/test_infosec_p001_p002_canonical_claims_red_smoke.py | test_p001_p002_canonical_claims_are_explicit_normalized_statements_not_rdf | RED |
| TASK-CANONICAL-CLAIMS-P001-P002; FUN-CANONICAL-CLAIMS-P001-P002 AC-3; CON-CANONICAL-CLAIMS-P001-P002 AC-3; BR-CANONICAL-CLAIMS-P001-P002-003 | tests/smoke/cases/infosec_p001_p002/test_infosec_p001_p002_canonical_claims_red_smoke.py | test_p001_p002_canonical_claims_preserve_paragraph_assets | RED |

## Validation command
python3 tests/smoke/run_infosec_smoke_suite.py

## RED result
3 failed in 2.12s; runner returncode 1; phase RED confirmed. All failures are the intended contract failure: canonical_claims stage payload missing; pipeline is still deriving downstream output directly without canonical_claims.

## 3k execution guard evidence
Runner selected_tests contained only tests/smoke/cases/infosec_p001_p002/test_infosec_p001_p002_canonical_claims_red_smoke.py. Runner metadata disabled tests/smoke/test_infosec_3k_pipeline_smoke.py, tests/smoke/test_infosec_3k_paragraphs_smoke.py, tests/smoke/test_infosec_paragraph_semantics_smoke.py. Pytest collected 3 items only.

## Artifacts touched
Runner validation rewrote tests/smoke/artifacts/infosec_smoke_runner.jsonl. Test expects tests/smoke/cases/infosec_p001_p002/artifacts/observed_p001_p002_canonical_claims.json produced by the canonical_claims stage; artifact remains absent in RED.
