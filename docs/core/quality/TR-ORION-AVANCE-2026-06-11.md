---
id: TR-ORION-AVANCE-2026-06-11
type: TR
title: Presentación de avance ORION
status: draft
version: 0
created_at: 2026-06-11
updated_at: 2026-06-11
summary: Presentación breve de qué puede y qué no puede hacer ORION hoy.
tags:
  - report
  - presentation
  - progress
  - library-only
domain: orion
capability: boundary
actors:
  - Host Application
systems:
  - ORION
source: README.md
related_ucs:
  - UC-001
  - UC-002
  - UC-003
  - UC-004
  - UC-005
  - UC-006
related_reqs:
  - FUN-001
  - FUN-002
  - FUN-003
  - FUN-004
  - FUN-005
  - FUN-006
  - FUN-007
  - FUN-008
  - FUN-009
  - FUN-010
  - FUN-011
  - FUN-012
  - FUN-013
  - CON-001
  - CON-002
  - CON-003
  - CON-004
  - CON-005
  - CON-006
  - CON-007
  - CON-008
  - NFR-001
  - NFR-002
  - NFR-003
  - NFR-004
  - NFR-005
  - NFR-006
  - NFR-008
owner: herodotus
---

# ORION — Presentación de avance

**Fecha:** 11 de junio de 2026

---

## 1. Qué es ORION

- Librería Python, no producto CLI.
- Corre dentro del proceso del host.
- Extrae elementos ontológicos desde texto natural.
- Produce salidas RDF/OWL orientadas y trazables.

---

## 2. Qué sí puede hacer

- Recibir `str` o ruta a `.txt`.
- Procesar texto con pipeline determinista.
- Extraer candidatos ontológicos, relaciones, claims semánticos y triples.
- Separar triples deterministas de triples inferidos.
- Devolver objetos Python y serializaciones.
- Exportar `ttl`, `rdfxml`, `jsonld` y `nt`.
- Mantener trazabilidad por entidad, propiedad y triple.
- Funcionar embebido en una app host, incluso backend REST propio del host.

---

## 3. Qué no puede hacer

- No es CLI.
- No es REST API.
- No es servicio HTTP propio.
- No acepta cualquier formato de archivo: hoy el input base es `str` o `.txt`.
- No promete soporte abierto e ilimitado de idiomas.
- No debe depender de configuraciones globales opacas.
- No debe romper la separación entre salidas deterministas e inferidas.
- No debe ser nondeterminista si inputs, config y dependencias quedan fijados.

---

## 4. Límites de alcance hoy

- Idioma por config; default inglés.
- Soporte inicial basado en spaCy: inglés y español.
- Tamaño de modelo configurable; default `lg`.
- Dependencias y modelos deben ir pinneados.
- YAML no es el formato principal de config.

---

## 5. Avance técnico actual

- Pipeline ordenado: `semantic_claims` → triples → RDF.
- Smoke modular por caso bajo `tests/smoke/cases/...`.
- Un runner único: `python3 tests/smoke/run_infosec_smoke_suite.py`.
- Última validación conocida: smoke suite verde.

---

## 6. Riesgo / cuidado

- La verdad del contrato vive en docs y tests, no en hardcode.
- Los artefactos observados se regeneran con la suite.
- Hay basura local posible: `__pycache__`, `.DS_Store`, temporales.
- Las capacidades públicas deben seguir alineadas con README y requisitos.

---

## 7. Cierre

ORION ya hace bien trabajo de librería determinista, trazable y embebible.
ORION no debe venderse como CLI, API HTTP o caja mágica multiformato.

Referencias:
- `README.md`
- `docs/requirements/*`
- `docs/use-cases/*`
- `docs/core/quality/TR-ORION-INFOSEC-FULL-TEXT-SMOKE.md`
