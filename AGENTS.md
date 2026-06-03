# Orion repo rules

Command unico:
python3 tests/smoke/run_infosec_smoke_suite.py

Rules:
- No tocar src productivo.
- Para smoke, usar pytest y este runner.
- Fixture infosec en partes va en tests/smoke/fixtures/infosec_3k_paragraphs/pXXX.txt.
- No editar artifacts a mano salvo necesidad del test harness.
