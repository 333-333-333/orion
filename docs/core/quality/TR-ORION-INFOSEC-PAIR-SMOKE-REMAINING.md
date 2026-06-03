# TR-ORION-INFOSEC-PAIR-SMOKE-REMAINING
## Metadata
- ID: TR-ORION-INFOSEC-PAIR-SMOKE-REMAINING
- Scope: fixtures p005..p043 en pares modulares
- Tester: sisyphus-tester
- Runner: python3 tests/smoke/run_infosec_smoke_suite.py
- Result: GREEN, 82 passed in 10.65s
## Coverage Matrix

| Spec | Cases | Tests | Status |
| --- | --- | --- | --- |
| FUN-INFOSEC-PAIR-SMOKE AC-1 | p005..p043 | observed_artifacts_are_generated_case_local | GREEN |
| FUN-INFOSEC-PAIR-SMOKE AC-2 | p005..p043 | semantic_claims_preserve_source_evidence | GREEN |
| FUN-INFOSEC-PAIR-SMOKE AC-3 | p005..p043 | rdf_projection_has_visible_structure | GREEN |
| CON-NO-INFOSEC-3K AC-1 | runner selected_tests | run_infosec_smoke_suite denylist + selected cases only | GREEN |
| BR-INFOSEC-PAIR-SMOKE-001 | p005..p043 | artifact generation | GREEN |
| BR-INFOSEC-PAIR-SMOKE-002 | p005..p043 | source evidence support proxy | GREEN |
| BR-INFOSEC-PAIR-SMOKE-003 | p005..p043 | RDF visible structure | GREEN |
## Observed Metrics

| Pair | Claims | Evidence proxy | Classes | Object properties | RDF |
| --- | ---: | ---: | ---: | ---: | --- |
| p005_p006 | 29 | 1.0 | 39 | 15 | True |
| p007_p008 | 22 | 1.0 | 36 | 8 | True |
| p009_p010 | 17 | 1.0 | 23 | 3 | True |
| p011_p012 | 24 | 1.0 | 35 | 17 | True |
| p013_p014 | 32 | 1.0 | 44 | 18 | True |
| p015_p016 | 26 | 1.0 | 43 | 20 | True |
| p017_p018 | 32 | 1.0 | 41 | 19 | True |
| p019_p020 | 25 | 1.0 | 36 | 17 | True |
| p021_p022 | 32 | 1.0 | 49 | 30 | True |
| p023_p024 | 23 | 1.0 | 34 | 9 | True |
| p025_p026 | 35 | 1.0 | 48 | 27 | True |
| p027_p028 | 25 | 1.0 | 40 | 25 | True |
| p029_p030 | 25 | 1.0 | 43 | 14 | True |
| p031_p032 | 25 | 1.0 | 43 | 20 | True |
| p033_p034 | 34 | 1.0 | 44 | 25 | True |
| p035_p036 | 15 | 1.0 | 25 | 14 | True |
| p037_p038 | 21 | 1.0 | 38 | 15 | True |
| p039_p040 | 24 | 1.0 | 35 | 24 | True |
| p041_p042 | 20 | 1.0 | 35 | 20 | True |
| p043 | 19 | 1.0 | 22 | 19 | True |

## Notes
No se inventan expected domain claims. Cada case tiene expected_semantic_contract.json con shape/artifacts/fixture hashes derivados del texto leído. Precisión domain se mide como proxy: claims con evidence presente en fixture / claims totales.

## Untestable / límites
Precisión semántica completa requiere gold expected por párrafo leído y curado; no se generó para 39 párrafos por riesgo de baja calidad manual. P043 quedó single por impar final y se documenta como decisión.
