# Revisión semántica: infosec_p035_p036

## 1. Lectura independiente

### Resumen

`p035` presenta la arquitectura segura como integración de seguridad en el diseño, enumera mecanismos o enfoques y expresa una obligación de alineación. `p036` presenta doce relaciones genéricas y modales entre clases de elementos de seguridad.

No hay personas, organizaciones, productos, sistemas concretos ni otras instancias nombradas. Los sintagmas indefinidos de `p036` —por ejemplo, “A security control” y “An incident”— expresan tipos genéricos; tratarlos como individuos concretos sería **NO SOPORTADO**.

### Conceptos

- `p035`: secure architecture, security, design, systems, environments, defense in depth, layers of security controls, zero trust, security model, implicit trust, network location, network segmentation, lateral movement, strong authentication, access points, encryption, data at rest, data in transit, monitoring, suspicious activity, backup, recovery, resilience, business requirements, risk appetite y regulatory obligations.
- `p036`: security control/control, asset, risk, threat, vulnerability, system, information asset, user, role, permission, policy, requirement, incident y response procedure.
- Definición explícita: “Zero trust is a security model” (`p035`).
- Caracterización funcional explícita: “Secure architecture integrates security into the design of systems and environments” (`p035`). No está formulada como equivalencia ni como definición necesaria y suficiente.
- “Defense in depth applies multiple layers of security controls” (`p035`) describe una relación funcional; no declara una taxonomía.
- “Control” y “security control” podrían ser correferentes conceptuales, pero su identidad es solo **PLAUSIBLE** (`p035`, `p036`).
- “Information asset” podría ser una clase más específica de “asset”, pero esa taxonomía es **NO SOPORTADA**: `p036` usa ambos términos sin declarar relación `is-a`.

### Proposiciones con evidencia

1. **EXPLÍCITO** — La arquitectura segura integra seguridad en el diseño de sistemas y entornos: “Secure architecture integrates security into the design of systems and environments.” (`p035`)
2. **EXPLÍCITO** — La defensa en profundidad aplica múltiples capas de controles de seguridad: “Defense in depth applies multiple layers of security controls.” (`p035`)
3. **EXPLÍCITO** — Zero trust es un modelo de seguridad: “Zero trust is a security model” (`p035`).
4. **EXPLÍCITO** — El modelo descrito no asume confianza implícita basada en la ubicación de red: “that assumes no implicit trust based on network location” (`p035`).
5. **CONTRADICHO** — La lectura positiva “Zero trust assumes implicit trust” contradice “assumes no implicit trust” (`p035`).
6. **EXPLÍCITO** — La segmentación de red limita el movimiento lateral: “Network segmentation limits lateral movement.” (`p035`)
7. **EXPLÍCITO** — La autenticación fuerte protege puntos de acceso: “Strong authentication protects access points.” (`p035`)
8. **EXPLÍCITO** — El cifrado protege datos en reposo y en tránsito: “Encryption protects data at rest and in transit.” (`p035`)
9. **ENTRAÑADO** — Del objeto coordinado anterior se obtienen ambas condiciones: protección de datos en reposo y protección de datos en tránsito (`p035`).
10. **EXPLÍCITO** — La monitorización detecta actividad sospechosa: “Monitoring detects suspicious activity.” (`p035`)
11. **EXPLÍCITO** — Backup y recuperación, como sujeto coordinado, apoyan la resiliencia: “Backup and recovery support resilience.” (`p035`)
12. **PLAUSIBLE**, no entrañado — Que backup por separado apoye la resiliencia y que recovery por separado la apoye; el texto permite una lectura colectiva (`p035`).
13. **EXPLÍCITO** — La arquitectura segura debe alinearse conjuntamente con requisitos de negocio, apetito de riesgo y obligaciones regulatorias: “must align with business requirements, risk appetite, and regulatory obligations” (`p035`).
14. **ENTRAÑADO** — Bajo la distribución ordinaria de la coordinación, la obligación alcanza a cada uno de los tres objetos de alineación (`p035`).
15. **EXPLÍCITO** — Un control de seguridad puede proteger uno o más activos: “A security control can protect one or more assets.” (`p036`)
16. **EXPLÍCITO** — Un activo puede verse afectado por uno o más riesgos: “An asset can be affected by one or more risks.” (`p036`)
17. **EXPLÍCITO** — Un riesgo puede ser reducido por uno o más controles: “A risk can be reduced by one or more controls.” (`p036`)
18. **EXPLÍCITO** — Una amenaza puede explotar una o más vulnerabilidades: “A threat can exploit one or more vulnerabilities.” (`p036`)
19. **EXPLÍCITO** — Una vulnerabilidad puede afectar uno o más sistemas: “A vulnerability can affect one or more systems.” (`p036`)
20. **EXPLÍCITO** — Un sistema puede procesar uno o más activos de información: “A system can process one or more information assets.” (`p036`)
21. **EXPLÍCITO** — Un usuario puede acceder a uno o más sistemas: “A user can access one or more systems.” (`p036`)
22. **EXPLÍCITO** — Un rol puede incluir uno o más permisos: “A role can include one or more permissions.” (`p036`)
23. **EXPLÍCITO** — Una política puede definir uno o más requisitos: “A policy can define one or more requirements.” (`p036`)
24. **EXPLÍCITO** — Un requisito puede ser satisfecho por uno o más controles: “A requirement can be satisfied by one or more controls.” (`p036`)
25. **EXPLÍCITO** — Un incidente puede afectar uno o más activos: “An incident can affect one or more assets.” (`p036`)
26. **EXPLÍCITO** — Un incidente puede activar uno o más procedimientos de respuesta: “An incident can trigger one or more response procedures.” (`p036`)
27. **NO SOPORTADO** — Convertir cualquiera de los enunciados con “can” en un hecho actual o universal sin modalidad (`p036`).

### Taxonomías explícitas

- La única categorización lingüística explícita es “Zero trust is a security model” (`p035`).
- Su proyección como `ZeroTrust rdfs:subClassOf SecurityModel` es **PLAUSIBLE**, pero no inequívoca: la misma forma lingüística admite una lectura de pertenencia/tipado. El texto no decide si `ZeroTrust` debe modelarse como clase o como individuo conceptual (`p035`).
- No se declaran jerarquías entre asset/information asset, control/security control, system/environment ni entre los demás conceptos (`p035`, `p036`).

### Modalidad

- Los primeros ocho enunciados de `p035` son genéricos en indicativo.
- “must align” expresa obligación y debe conservar alcance sobre los tres objetos coordinados (`p035`).
- “no implicit trust” expresa polaridad negativa; “based on network location” restringe aquello cuya asunción se niega (`p035`).
- Los doce enunciados de `p036` usan “can”: expresan posibilidad o capacidad, no actualidad ni necesidad.
- “one or more” está dentro del alcance de “can”; preserva una cardinalidad mínima condicional. No afirma por sí solo que existan actualmente tales objetos (`p036`).

### Ambigüedades

- “that” en “a security model that assumes…” se refiere explícitamente al sintagma “security model”; como este predica de Zero trust, atribuir la relativa a Zero trust es **ENTRAÑADO** (`p035`).
- “Backup and recovery” puede tener alcance colectivo; distribuir `supports` a cada miembro es solo **PLAUSIBLE** (`p035`).
- “data at rest and in transit” contiene elipsis: la expansión a dos estados de `data` es **ENTRAÑADA** (`p035`).
- “Control” = “security control” es **PLAUSIBLE**, no explícito (`p035`, `p036`).
- Las menciones repetidas de asset, risk, system, requirement e incident en `p036` refieren a las mismas clases léxicas, no necesariamente al mismo individuo.
- La formalización de “Zero trust is a security model” como subclase o como instancia permanece abierta (`p035`).

## 2. Resultado por etapa

Escala: 0 = ausente/contradictorio; 4 = completo y fiel para la responsabilidad propia de la etapa.

| Paso | Etapa | Fidelidad | Cobertura | Precisión | Trazabilidad | Coherencia | Estado |
|---:|---|---:|---:|---:|---:|---:|---|
| 01 | input_intake | 4 | 4 | 4 | 4 | 4 | OK |
| 02 | preprocessing | 4 | 4 | 4 | 4 | 4 | OK |
| 03 | sentence_segmentation | 4 | 4 | 4 | 4 | 4 | OK |
| 04 | tokenization | 4 | 4 | 4 | 4 | 4 | OK |
| 05 | linguistic_annotation | 3 | 4 | 3 | 4 | 3 | WARN |
| 06 | entity_extraction | 4 | 4 | 4 | 4 | 4 | OK |
| 07 | concept_extraction | 3 | 3 | 3 | 4 | 2 | WARN |
| 08 | coreference_resolution | 4 | 4 | 4 | 4 | 4 | OK |
| 09 | relation_extraction | 2 | 2 | 2 | 3 | 2 | FAIL |
| 10 | canonical_claims / semantic_claims | 4 | 4 | 4 | 4 | 3 | OK |
| 11 | semantic_debug_ir | 2 | 2 | 2 | 4 | 3 | WARN |
| 12 | triple_extraction | 3 | 3 | 4 | 4 | 3 | WARN |
| 13 | taxonomy_induction | 3 | 4 | 3 | 4 | 4 | WARN |
| 14 | type_assertion | 4 | 4 | 4 | 4 | 4 | OK |
| 15 | semantic_quality | 2 | 2 | 2 | 3 | 2 | WARN |
| 16 | output_generation | 3 | 4 | 3 | 3 | 3 | WARN |

## 3. Hallazgos

### Q-infosec_p035_p036-05-1

- **Severidad:** alta
- **Tipo:** anotación lingüística incorrecta con absorción del predicado
- **Atribución:** ERROR_ORIGEN en 05; ERROR_PROPAGADO en 07 y 09; ERROR_CORREGIDO en 10
- **Clasificación:** CONTRADICHO por la estructura literal
- **Cita literal:** “Backup and recovery support resilience.” (`p035`)
- **Archivo:** `tests/smoke/cases/infosec_p035_p036/artifacts/pipeline_outputs/observed_p035_p036_05_linguistic_annotation.json`
- **JSON Pointer:** `/tokens/64`, `/tokens/66`, `/tokens/67`, `/tokens/68`
- **Evaluación razonada:** `support` queda anotado como `NOUN` y `compound` de `resilience`; `resilience` queda como raíz nominal. El texto, en cambio, contiene el verbo plural `support` con sujeto coordinado y objeto `resilience`. La consecuencia se ve una sola vez, no como errores nuevos: 07 absorbe toda la proposición en `/concepts/20`, 09 no produce la relación y 15 excluye ese concepto ruidoso.
- **Impacto downstream:** pérdida de la proposición en la extracción relacional automática. La etapa 10 la reconstruye fielmente y evita que la pérdida alcance el output final.

### Q-infosec_p035_p036-09-1

- **Severidad:** crítica
- **Tipo:** inversión semántica por pérdida de negación y restricción
- **Atribución:** ERROR_ORIGEN en 09; ERROR_CORREGIDO en 10
- **Clasificación:** CONTRADICHO
- **Cita literal:** “assumes no implicit trust based on network location” (`p035`)
- **Archivo:** `tests/smoke/cases/infosec_p035_p036/artifacts/pipeline_outputs/observed_p035_p036_09_relation_extraction.json`
- **JSON Pointer:** `/relations/13`
- **Evaluación razonada:** la relación observada expresa `security model —assume→ implicit trust`, sin `no` ni “based on network location”. Leída como relación positiva afirma lo contrario del párrafo y pierde el alcance de la base.
- **Impacto downstream:** habría creado una afirmación falsa. La etapa 10 corrige sujeto, polaridad y base; 16 conserva esos datos en una relación scoped.

### Q-infosec_p035_p036-09-2

- **Severidad:** alta
- **Tipo:** pérdida sistemática de modalidad, cardinalidad y alcance coordinado
- **Atribución:** ERROR_ORIGEN en 09; ERROR_CORREGIDO en 10
- **Clasificación:** las relaciones nucleares son ENTRAÑADAS, pero las versiones no modales son NO SOPORTADAS
- **Cita literal:** “Secure architecture must align with business requirements, risk appetite, and regulatory obligations.” (`p035`); “A security control can protect one or more assets.” (`p036`)
- **Archivo:** `tests/smoke/cases/infosec_p035_p036/artifacts/pipeline_outputs/observed_p035_p036_09_relation_extraction.json`
- **JSON Pointer:** `/relations`, en particular `/relations/1`
- **Evaluación razonada:** no se extrae ninguna relación `align` del último enunciado de `p035`. En `p036`, las relaciones reducen “can … one or more” a predicados simples y objetos como “one asset”, sin campos de modalidad ni cuantificador. La etapa 09 no debe afirmar actualidad cuando el párrafo solo expresa capacidad.
- **Impacto downstream:** pérdida masiva de alcance lógico si 09 se consumiera directamente. 10 recupera `must`, los tres objetos, `can`, `one_or_more` y la voz.

### Q-infosec_p035_p036-09-3

- **Severidad:** alta
- **Tipo:** relación pasiva incompleta
- **Atribución:** ERROR_ORIGEN en 09; ERROR_CORREGIDO en 10
- **Clasificación:** NO SOPORTADO como representación completa
- **Cita literal:** “A requirement can be satisfied by one or more controls.” (`p036`)
- **Archivo:** `tests/smoke/cases/infosec_p035_p036/artifacts/pipeline_outputs/observed_p035_p036_09_relation_extraction.json`
- **JSON Pointer:** `/relations/19`
- **Evaluación razonada:** se produce `requirement —be→ satisfied`, con `object_ref` vacío, y se omite el agente `controls`, la modalidad y la cardinalidad. “Satisfied” tampoco es el objeto semántico del verbo copulativo en el sentido requerido por el párrafo.
- **Impacto downstream:** rompe la conexión requirement–control. La claim `Requirement canBeSatisfiedBy Control` de 10 corrige el error antes de RDF.

### Q-infosec_p035_p036-10-1

- **Severidad:** positiva
- **Tipo:** recuperación semántica y de trazabilidad
- **Atribución:** ERROR_CORREGIDO
- **Clasificación:** EXPLÍCITO
- **Cita literal:** “Backup and recovery support resilience.” (`p035`); “A requirement can be satisfied by one or more controls.” (`p036`)
- **Archivo:** `tests/smoke/cases/infosec_p035_p036/artifacts/pipeline_outputs/observed_p035_p036_10_canonical_claims.json`
- **JSON Pointer:** `/canonical_claims/claims/8`, `/canonical_claims/claims/21`
- **Evaluación razonada:** 10 restaura la coordinación de Backup/Recovery y la relación pasiva Requirement/Control. También conserva `must`, `can`, `one_or_more`, polaridad negativa, base de red y estados de los datos en las claims correspondientes. Las 24 claims cubren las proposiciones y expansiones coordinadas necesarias.
- **Impacto downstream:** corta la propagación de los errores principales de 05 y 09 y suministra una base semántica mayoritariamente fiel para 12 y 16.

### Q-infosec_p035_p036-11-1

- **Severidad:** media
- **Tipo:** sidecar de depuración semánticamente incompleto
- **Atribución:** ERROR_ORIGEN en 11; no propagado al output final
- **Clasificación:** CONTRADICHO para la relación positiva; parcial para los estados
- **Cita literal:** “assumes no implicit trust based on network location” y “data at rest and in transit” (`p035`)
- **Archivo:** `tests/smoke/cases/infosec_p035_p036/artifacts/pipeline_outputs/observed_p035_p036_11_semantic_debug_ir.json`
- **JSON Pointer:** `/artifacts/semantic_debug_ir/relations/3`, `/artifacts/semantic_debug_ir/relations/6`
- **Evaluación razonada:** la IR de depuración elimina `polarity: negative` y `basis` de `assumes`, y elimina `states` de la relación de cifrado. Por ello el sidecar no permite depurar fielmente la proyección de esas claims, aunque conserve la evidencia literal.
- **Impacto downstream:** riesgo de diagnóstico humano erróneo; no contamina 16 porque el output usa `semantic_claims`.

### Q-infosec_p035_p036-12-1

- **Severidad:** media
- **Tipo:** pérdida de calificadores al convertir claims en triples
- **Atribución:** ERROR_ORIGEN en 12; ERROR_CORREGIDO en 16
- **Clasificación:** representación parcial
- **Cita literal:** “assumes no implicit trust based on network location” y “Encryption protects data at rest and in transit.” (`p035`)
- **Archivo:** `tests/smoke/cases/infosec_p035_p036/artifacts/pipeline_outputs/observed_p035_p036_12_triple_extraction.json`
- **JSON Pointer:** `/triples/17`, `/triples/22`
- **Evaluación razonada:** el triple de Zero trust conserva la polaridad pero no `basis: NetworkLocation`; el triple de cifrado conserva coordinación pero no los estados. El SPO nuclear es fiel, pero no toda la claim.
- **Impacto downstream:** una proyección basada exclusivamente en triples perdería alcance. 16 recupera ambos calificadores desde las claims.

### Q-infosec_p035_p036-13-1

- **Severidad:** media
- **Tipo:** compromiso ontológico más fuerte que la lectura inequívoca
- **Atribución:** ERROR_ORIGEN en 13; ERROR_PROPAGADO a 16
- **Clasificación:** PLAUSIBLE, no EXPLÍCITO como `rdfs:subClassOf`
- **Cita literal:** “Zero trust is a security model” (`p035`)
- **Archivo:** `tests/smoke/cases/infosec_p035_p036/artifacts/pipeline_outputs/observed_p035_p036_13_taxonomy_induction.json`
- **JSON Pointer:** `/taxonomy_relations/0`
- **Evaluación razonada:** el enunciado categoriza Zero trust como modelo de seguridad, pero no resuelve por sí solo la decisión clase–instancia. `subclass_of` es una formalización razonable, aunque no la única entrañada por la frase.
- **Impacto downstream:** 16 materializa la decisión como `rdfs:subClassOf`; consumidores OWL reciben un compromiso taxonómico que debería declararse como interpretación.

### Q-infosec_p035_p036-15-1

- **Severidad:** media
- **Tipo:** evaluación de calidad internamente inconsistente
- **Atribución:** ERROR_ORIGEN en 15
- **Clasificación:** NO SOPORTADO para “unstructured_disjunction”; contradicho por los triples para “claim_scope_preserved”
- **Cita literal:** “data at rest and in transit” y “based on network location” (`p035`); “one or more” (`p036`)
- **Archivo:** `tests/smoke/cases/infosec_p035_p036/artifacts/pipeline_outputs/observed_p035_p036_15_semantic_quality.json`
- **JSON Pointer:** `/semantic_quality_report/relation_gaps/0`, `/semantic_quality_report/semantic_integrity_checks/claim_scope_preserved_in_triples`
- **Evaluación razonada:** se informa `unstructured_disjunction` sin localizar una alternativa lógica no estructurada; “one or more” es una expresión cardinal modal, no evidencia suficiente de una disyunción ontológica. A la vez se marca `claim_scope_preserved_in_triples: true` aunque 12 perdió `basis` y `states`.
- **Impacto downstream:** el `rdf_readiness: false` es prudente, pero sus razones no diagnostican con precisión las pérdidas reales.

### Q-infosec_p035_p036-16-1

- **Severidad:** media
- **Tipo:** referencia scoped no integrada estructuralmente en el grafo
- **Atribución:** ERROR_ORIGEN en 16
- **Clasificación:** el contenido es EXPLÍCITO; su proyección es estructuralmente parcial
- **Cita literal:** “based on network location” (`p035`)
- **Archivo:** `tests/smoke/cases/infosec_p035_p036/artifacts/pipeline_outputs/observed_p035_p036_16_output_generation.json`
- **JSON Pointer:** `/output/graph/scoped_relations/0/basis`, `/output/graph/classes`
- **Evaluación razonada:** la relación negativa final recupera `basis: "NetworkLocation"`, pero no existe `orion:NetworkLocation` en `classes` y el valor no usa IRI. La semántica es legible, pero queda una referencia sin nodo RDF/OWL coherente.
- **Impacto downstream:** consultas por el concepto NetworkLocation no pueden enlazarlo con la relación; la base funciona como literal auxiliar, no como recurso del modelo.

## 4. Diagnóstico

- **Primera degradación:** 05, al analizar “Backup and recovery support resilience” como sintagma nominal en vez de proposición verbal (`p035`).
- **Principal pérdida:** 09 elimina negación, modalidad, cardinalidad y alcance, y omite relaciones completas como `must align` (`p035`, `p036`). Es la etapa semánticamente más débil. 10 corrige esas pérdidas.
- **Principal contenido no soportado:** el diagnóstico `unstructured_disjunction` de 15 no está sustentado por los párrafos; “one or more” expresa cardinalidad bajo `can` (`p036`). En el modelo final no se observa una invención de dominio comparable; el mayor exceso es la interpretación **PLAUSIBLE** de ZeroTrust como subclase (`p035`).
- **Errores que llegan a RDF/OWL:** llega el compromiso `ZeroTrust rdfs:subClassOf SecurityModel`, que es plausible pero no inequívoco (`p035`), y llega `NetworkLocation` como base no enlazada a una clase/IRI (`p035`). La falsa lectura positiva de implicit trust y las pérdidas de `can`/`must` no llegan: 10 y 16 las corrigen.
- **Aciertos:** intake, normalización, 21 segmentos y tokens son fieles; 06 es conservador ante la ausencia de entidades nombradas; 08 resuelve correctamente “that”; 10 ofrece cobertura y evidencia por párrafo; 14 evita inventar individuos; 16 conserva las doce relaciones modales de `p036` como scoped relations, la obligación triple de alineación, la coordinación Backup/Recovery, la negación y los estados de los datos.
- **Incertidumbres:** clase frente a instancia para ZeroTrust (`p035`); lectura colectiva o distributiva de Backup/Recovery (`p035`); identidad entre Control y SecurityControl (`p035`, `p036`). El conservadurismo frente a estas ambigüedades no debe penalizarse.

## 5. Veredicto

- **Calidad global:** **84/100**.
- **Output final:** **parcialmente fiel**. Conserva prácticamente todas las proposiciones, modalidades, cuantificadores y evidencias, sin que los errores críticos de 09 se materialicen como hechos positivos. No alcanza “fiel” por el compromiso taxonómico no inequívoco y por la referencia `NetworkLocation` no integrada en el grafo.
- **Tres correcciones prioritarias:**
  1. Preservar negación, modalidad, cardinalidad, voz, coordinación y calificadores desde 09, sin depender de una reparación posterior (`p035`, `p036`).
  2. Corregir la anotación verbal de “Backup and recovery support resilience” y evitar absorber proposiciones completas como conceptos (`p035`).
  3. En RDF/OWL, modelar `NetworkLocation` como recurso trazable y hacer explícita —o dejar abierta— la decisión clase–instancia para ZeroTrust (`p035`).

Siguiente caso pendiente: infosec_p037_p038.
