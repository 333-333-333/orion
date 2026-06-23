---
title: "ORION — Presentación de avance"
subtitle: "11 de junio de 2026"
author: "ORION"
date: "2026-06-11"
---

# ORION

- Librería Python.
- No CLI.
- Corre dentro del proceso del host.
- Extrae elementos ontológicos desde texto natural.
- Produce salidas RDF/OWL con trazabilidad.

---

# Qué sí puede hacer

- Recibir `str` o ruta a `.txt`.
- Procesar texto con pipeline determinista.
- Extraer candidatos ontológicos, relaciones, claims semánticos y triples.
- Separar triples deterministas de triples inferidos.
- Devolver objetos Python y serializaciones.
- Exportar `ttl`, `rdfxml`, `jsonld` y `nt`.

---

# Qué no puede hacer

- No es CLI.
- No es REST API.
- No es servicio HTTP propio.
- No acepta cualquier formato de archivo.
- No promete soporte abierto e ilimitado de idiomas.
- No debe depender de configuraciones globales opacas.

---

# Reglas transversales

- Identificadores estables.
- Dedupe estable.
- Trazabilidad por entidad, propiedad y triple.
- Contrato en docs y tests, no en hardcode.
- Determinismo con inputs, config y dependencias fijas.

---

# Pipeline completa

1. Input intake
2. Preprocessing
3. Sentence segmentation
4. Tokenization
5. Linguistic annotation
6. Entity extraction
7. Concept extraction
8. Coreference + relations
9. Canonical claims + triples
10. Taxonomy induction
11. Type assertion
12. Semantic quality
13. Output generation

---

# 1. Input intake

- Acepta `str` o `.txt`.
- Construye `source_text_id` estable.
- Guarda metadatos de origen.
- Rechaza contrato fuera del boundary de librería.

---

# 2. Preprocessing

- Normaliza Unicode a NFC.
- Colapsa espacios repetidos.
- Normaliza saltos de línea.
- Si queda vacío, falla.

---

# 3. Sentence segmentation

- Corta por `.`, `?`, `!`.
- Usa offsets limpios.
- Cada oración recibe `sentence_id` estable.
- No inventa texto nuevo.

---

# 4. Tokenization

- Tokeniza con regex: palabra o puntuación.
- Conserva offsets por token.
- Cada token recibe `token_id` estable.
- Sirve de base para los pasos lingüísticos.

---

# 5. Linguistic annotation

- Alinea tokens del pipeline con spaCy.
- Extrae lemma, POS, tag, dependencia y head.
- Si no hay match exacto, usa fallback estable.
- No cambia los tokens base.

---

# 6. Entity extraction

- Usa soporte de entidades con offsets normalizados.
- Mantiene `entity_id` estable con hash.
- Resuelve sentence_id por span.
- Hoy NER genérico queda apagado; ORION usa evidencia lingüística.

---

# 7. Concept extraction

- Saca candidatos desde noun chunks, labels y tokens.
- Limpia artículos y conectores.
- Expande frases a izquierda y derecha.
- Da confianza distinta según origen.
- Evita ruido de frases largas o fragmentos raros.

---

# 8. Coreference + relations

- Coref solo para relativos como `that`, `which`, `who`.
- Elige antecedente por distancia y posición.
- Si confianza baja, deja unresolved.
- Relaciones sale de SVO y copulativas.
- Dedupe estable.
- Filtra instrucción meta tipo “ORION should be able to...”.

---

# 9. Canonical claims + triples

- Normaliza texto con reglas de frase.
- Reescribe objetos nominalizados cuando toca.
- Desarma listas y temporales.
- Construye claims canónicos con evidencia.
- Convierte claims y relations a triples estables.

---

# 10. Taxonomy induction

- Busca `subclass_of` desde patrones copulares.
- También usa `such as` e `including`.
- Canonicaliza cabeza y padre.
- Evita scaffolds taxonómicos falsos.

---

# 11. Type assertion

- Busca `instance_of` desde copulas.
- Usa labels de entidad.
- Usa patrones de relación.
- Usa sujetos taxonómicos cortos.
- Dedupe estable.

---

# 12. Semantic quality

- Marca ruido de entidades y conceptos.
- Detecta texto largo sin relaciones o triples.
- Calcula `rdf_readiness`.
- Produce `quality_score`.
- Devuelve advertencias, no magia.

---

# 13. Output generation

- Valida base IRI y prefixes.
- Elige estrategia RDF u OWL.
- Proyecta SVO explícito cuando hace falta.
- Devuelve serialización visible y estable.

---

# Límites de alcance hoy

- Idioma por config; default inglés.
- Soporte inicial: inglés y español.
- Tamaño de modelo configurable; default `lg`.
- Dependencias y modelos pinneados.
- YAML no es el formato principal de config.

---

# Avance técnico actual

- Pipeline ordenado: `semantic_claims` → triples → RDF.
- Smoke modular por caso.
- Un runner único: `python3 tests/smoke/run_infosec_smoke_suite.py`.
- Última validación conocida: smoke suite verde.

---

# Cierre

ORION ya hace bien trabajo de librería determinista, trazable y embebible.

ORION no debe venderse como CLI, API HTTP o caja mágica multiformato.
