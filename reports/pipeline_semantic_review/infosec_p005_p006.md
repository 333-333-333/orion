# Revisión semántica: infosec_p005_p006

## 1. Lectura independiente

### Resumen

Los dos párrafos presentan un vocabulario definicional sobre gestión del riesgo y controles de seguridad. `p005` define riesgo, amenaza, vulnerabilidad, impacto, probabilidad, escenario de riesgo y control, además de sus relaciones y modalidades. `p006` explicita una taxonomía de cuatro tipos de control de seguridad, describe su función y clasifica cuatro ejemplos genéricos.

La lectura distingue cinco niveles:

- **EXPLÍCITO**: expresado literalmente por el texto.
- **ENTRAÑADO**: consecuencia necesaria de la forma lingüística, sin conocimiento externo.
- **PLAUSIBLE**: lectura posible, pero no necesaria.
- **NO SOPORTADO**: no se deriva del texto.
- **CONTRADICHO**: incompatible con una afirmación o condición literal.

### Conceptos

- **Tema general — EXPLÍCITO:** gestión del riesgo en seguridad de la información y controles de seguridad. Evidencia: “Risk management is a core process in information security” (`p005`) y “A preventive control is a type of security control” (`p006`).
- **Conceptos de `p005` — EXPLÍCITO:** `RiskManagement`, `CoreProcess`, `InformationSecurity`, `Risk`, `Possibility`, `Threat`, `Vulnerability`, `Harm`, `Asset`, `PotentialCause`, `UnwantedIncident`, `Weakness`, `Impact`, `Consequence`, `SecurityEvent`, `Incident`, `Likelihood`, `Probability`, `RiskScenario`, `Control` y `SecurityWeakness`.
- **Conceptos de `p006` — EXPLÍCITO:** `PreventiveControl`, `DetectiveControl`, `CorrectiveControl`, `CompensatingControl`, `SecurityControl`, `ProbabilityOfAnIncident`, `SuspiciousActivity`, `PolicyViolation`, `NormalOperations`, `AlternativeProtectionMechanism`, `PrimaryControl`, `AccessControl`, `Logging`, `BackupRestoration`, `ManualApproval` y `AutomatedEnforcement`.
- **Entidades o instancias individuales explícitas:** ninguna. Las expresiones “Access control”, “Logging”, “Backup restoration” y “Manual approval” designan categorías o prácticas genéricas en estas oraciones, no individuos identificados. Tratarlas como clases es **ENTRAÑADO/razonable por la forma genérica**; tratarlas como individuos concretos sería **NO SOPORTADO**.
- La equivalencia entre `Control` y `SecurityControl` es **PLAUSIBLE**, pero no está afirmada. `p005` usa “A control”, mientras `p006` usa “security control”; fusionarlos sin marca de incertidumbre sería **NO SOPORTADO**.
- Que los cuatro tipos de `p006` formen una partición exhaustiva o disjunta de `SecurityControl` es **NO SOPORTADO**: el texto enumera cuatro tipos, pero no dice que sean los únicos ni que no se solapen.

### Proposiciones con evidencia

| ID | Clasificación | Proposición literal | Evidencia breve |
|---|---|---|---|
| P005-01 | EXPLÍCITO | La gestión del riesgo es un proceso central en seguridad de la información. | “Risk management is a core process in information security” (`p005`). |
| P005-02 | EXPLÍCITO | Un riesgo es la posibilidad de cierto contenido proposicional. | “A risk is the possibility that…” (`p005`). |
| P005-03 | EXPLÍCITO, bajo posibilidad | Una amenaza explota una vulnerabilidad dentro del contenido que define el riesgo. | “a threat exploits a vulnerability” (`p005`). |
| P005-04 | EXPLÍCITO, bajo posibilidad | La misma amenaza causa daño a un activo dentro del contenido que define el riesgo. | “and causes harm to an asset” (`p005`). |
| P005-05 | EXPLÍCITO | Una amenaza es una causa potencial de un incidente no deseado. | “A threat is a potential cause of an unwanted incident” (`p005`). |
| P005-06 | EXPLÍCITO | Una vulnerabilidad es una debilidad. | “A vulnerability is a weakness” (`p005`). |
| P005-07 | EXPLÍCITO, modal | Esa debilidad puede ser explotada por una amenaza. | “that can be exploited by a threat” (`p005`). |
| P005-08 | EXPLÍCITO | Un impacto es la consecuencia indicada. | “An impact is the consequence” (`p005`). |
| P005-09 | EXPLÍCITO, disyuntivo | La consecuencia puede ser producida por un evento de seguridad o por un incidente. | “produced by a security event or incident” (`p005`). |
| P005-10 | EXPLÍCITO | Una probabilidad (`likelihood`) es la probabilidad de un evento. | “A likelihood is the probability that…” (`p005`). |
| P005-11 | EXPLÍCITO, bajo probabilidad | El evento medido es que ocurra un escenario de riesgo. | “a risk scenario occurs” (`p005`). |
| P005-12 | EXPLÍCITO | Un escenario de riesgo describe cómo puede desarrollarse una secuencia. | “A risk scenario describes how…” (`p005`). |
| P005-13 | EXPLÍCITO, modal | Una amenaza puede explotar una vulnerabilidad en el escenario descrito. | “a threat may exploit a vulnerability” (`p005`). |
| P005-14 | EXPLÍCITO, modal y coordinado | La misma amenaza puede afectar un activo en el escenario descrito. | “and affect an asset” (`p005`). |
| P005-15 | EXPLÍCITO | Un control reduce el riesgo. | “A control reduces risk” (`p005`). |
| P005-16 | EXPLÍCITO, medio alternativo | Prevenir debilidades de seguridad es un medio de reducir el riesgo. | “by preventing… security weaknesses” (`p005`). |
| P005-17 | EXPLÍCITO, medio alternativo | Detectar debilidades de seguridad es un medio de reducir el riesgo. | “detecting… security weaknesses” (`p005`). |
| P005-18 | EXPLÍCITO, medio alternativo | Corregir debilidades de seguridad es un medio de reducir el riesgo. | “correcting… security weaknesses” (`p005`). |
| P005-19 | EXPLÍCITO, medio alternativo | Compensar debilidades de seguridad es un medio de reducir el riesgo. | “compensating for security weaknesses” (`p005`). |
| P006-01 | EXPLÍCITO | Un control preventivo es un tipo de control de seguridad. | “A preventive control is a type of security control” (`p006`). |
| P006-02 | EXPLÍCITO | El control preventivo reduce la probabilidad de un incidente. | “reduces the probability of an incident” (`p006`). |
| P006-03 | EXPLÍCITO | Un control detectivo es un tipo de control de seguridad. | “A detective control is a type of security control” (`p006`). |
| P006-04 | EXPLÍCITO, disyuntivo | El control detectivo identifica actividad sospechosa o infracciones de políticas. | “identifies suspicious activity or policy violations” (`p006`). |
| P006-05 | EXPLÍCITO | Un control correctivo es un tipo de control de seguridad. | “A corrective control is a type of security control” (`p006`). |
| P006-06 | EXPLÍCITO, temporal | El control correctivo restaura operaciones normales después de un incidente. | “restores normal operations after an incident” (`p006`). |
| P006-07 | EXPLÍCITO | Un control compensatorio es un tipo de control de seguridad. | “A compensating control is a type of security control” (`p006`). |
| P006-08 | EXPLÍCITO, condicional y negativo | Proporciona un mecanismo alternativo cuando un control primario no puede implementarse. | “provides an alternative protection mechanism when a primary control cannot be implemented” (`p006`). |
| P006-09 | EXPLÍCITO | El control de acceso es un control preventivo. | “Access control is a preventive control” (`p006`). |
| P006-10 | EXPLÍCITO | El registro (`Logging`) es un control detectivo. | “Logging is a detective control” (`p006`). |
| P006-11 | EXPLÍCITO | La restauración de copias de seguridad es un control correctivo. | “Backup restoration is a corrective control” (`p006`). |
| P006-12 | EXPLÍCITO, condicional y negativo | La aprobación manual es un control compensatorio cuando la aplicación automatizada no está disponible. | “Manual approval is a compensating control when automated enforcement is not available” (`p006`). |

Interpretaciones de control:

- El sujeto omitido de “causes” es la misma amenaza que el de “exploits”: **ENTRAÑADO** por coordinación en `p005`.
- El sujeto omitido de “affect” es la misma amenaza que el de “exploit”: **ENTRAÑADO** por coordinación en `p005`.
- Proyectar “Threat exploits Vulnerability” o “Threat affects Asset” como hechos incondicionales es **NO SOPORTADO**, porque `p005` los sitúa bajo “possibility” o “may”.
- Proyectar “ManualApproval is_a CompensatingControl” sin la condición es **NO SOPORTADO**, porque `p006` restringe la clasificación con “when automated enforcement is not available”.
- Afirmar que la aplicación automatizada está disponible en esa condición es **CONTRADICHO** por “is not available” (`p006`).
- Afirmar que el control primario puede implementarse en la condición descrita es **CONTRADICHO** por “cannot be implemented” (`p006`).

### Taxonomías explícitas

| Subclase o concepto definido | Superclase o categoría | Alcance | Clasificación y evidencia |
|---|---|---|---|
| `RiskManagement` | `CoreProcess` | en `InformationSecurity` | EXPLÍCITO: “core process in information security” (`p005`). |
| `Risk` | `Possibility` | contenido definitorio | EXPLÍCITO: “risk is the possibility” (`p005`). |
| `Threat` | `PotentialCause` | modalidad potencial; objetivo `UnwantedIncident` | EXPLÍCITO: “threat is a potential cause” (`p005`). |
| `Vulnerability` | `Weakness` | — | EXPLÍCITO: “vulnerability is a weakness” (`p005`). |
| `Impact` | `Consequence` | — | EXPLÍCITO: “impact is the consequence” (`p005`). |
| `Likelihood` | `Probability` | evento `RiskScenario occurs` | EXPLÍCITO: “likelihood is the probability” (`p005`). |
| `PreventiveControl` | `SecurityControl` | — | EXPLÍCITO: “type of security control” (`p006`). |
| `DetectiveControl` | `SecurityControl` | — | EXPLÍCITO: “type of security control” (`p006`). |
| `CorrectiveControl` | `SecurityControl` | — | EXPLÍCITO: “type of security control” (`p006`). |
| `CompensatingControl` | `SecurityControl` | — | EXPLÍCITO: “type of security control” (`p006`). |
| `AccessControl` | `PreventiveControl` | — | EXPLÍCITO: “is a preventive control” (`p006`). |
| `Logging` | `DetectiveControl` | — | EXPLÍCITO: “is a detective control” (`p006`). |
| `BackupRestoration` | `CorrectiveControl` | — | EXPLÍCITO: “is a corrective control” (`p006`). |
| `ManualApproval` | `CompensatingControl` | solo cuando `AutomatedEnforcement` no está disponible | EXPLÍCITO y condicional (`p006`). |

Por transitividad, `AccessControl`, `Logging` y `BackupRestoration` quedan bajo `SecurityControl`: **ENTRAÑADO** por las dos clasificaciones explícitas de cada cadena. La misma inferencia para `ManualApproval` solo es válida bajo su condición.

### Modalidad

- **Posibilidad definitoria:** “possibility that a threat exploits…” (`p005`). No licencia hechos actuales.
- **Potencialidad:** “potential cause” (`p005`). No equivale a causa efectiva.
- **Capacidad:** “can be exploited” (`p005`). No equivale a explotación ocurrida.
- **Posibilidad modal:** “may exploit… and affect” (`p005`). El modal alcanza ambos verbos coordinados.
- **Probabilidad:** “probability that a risk scenario occurs” (`p005`). El escenario es el evento medido, no un hecho ocurrido.
- **Disyunción:** “security event or incident” (`p005`), los cuatro medios unidos por “or” (`p005`) y “suspicious activity or policy violations” (`p006`). No se especifica si la disyunción es exclusiva.
- **Temporalidad:** “after an incident” (`p006`) restringe la restauración.
- **Condición negativa:** “when a primary control cannot be implemented” y “when automated enforcement is not available” (`p006`).

### Ambigüedades

- En “the possibility that…” y “the probability that…”, `that` es complementizador no referencial (`p005`).
- En “a weakness that can be exploited”, `that` refiere a `weakness`; dado que la oración define `Vulnerability` como esa debilidad, aplicar la capacidad a la vulnerabilidad es **ENTRAÑADO** (`p005`).
- En las cuatro fórmulas “a type of security control that…”, el antecedente superficial más cercano de `that` es `security control`, pero la oración completa caracteriza al subtipo definido. Atribuir la función a `PreventiveControl`, `DetectiveControl`, `CorrectiveControl` o `CompensatingControl` es **ENTRAÑADO**; generalizarla a todo `SecurityControl` es **NO SOPORTADO** (`p006`).
- “or” puede ser inclusivo o exclusivo; el texto no lo resuelve (`p005`, `p006`). Conservar una agrupación disyuntiva sin exclusividad es la opción más fiel.
- “normal operations” aparece en plural; normalizarlo a `NormalOperation` singular es **PLAUSIBLE**, no una identidad morfológica literal (`p006`).
- “security weaknesses” puede compartir objeto con “preventing, detecting, correcting” por coordinación; es una lectura **ENTRAÑADA** de la construcción, aunque solo “compensating” lleva explícitamente `for` (`p005`).
- No se especifica si “Access control”, “Logging”, “Backup restoration” y “Manual approval” son tipos exhaustivos, ejemplos típicos o realizaciones concretas; solo sus clasificaciones son explícitas (`p006`).

## 2. Resultado por etapa

Escala: 0 = ausente o inválido; 1 = deficiente; 2 = parcial; 3 = adecuado con defectos; 4 = completo y fiel. No hay pasos N/A: `semantic_debug_ir` está configurado.

| Paso | Etapa | Fidelidad | Cobertura | Precisión | Trazabilidad | Coherencia | Estado |
|---:|---|---:|---:|---:|---:|---:|---|
| 01 | `input_intake` | 4 | 4 | 4 | 4 | 4 | OK |
| 02 | `preprocessing` | 4 | 4 | 4 | 4 | 4 | OK |
| 03 | `sentence_segmentation` | 4 | 4 | 4 | 4 | 4 | OK |
| 04 | `tokenization` | 4 | 4 | 4 | 4 | 4 | OK |
| 05 | `linguistic_annotation` | 3 | 3 | 3 | 4 | 3 | WARN |
| 06 | `entity_extraction` | 4 | 4 | 4 | 4 | 4 | OK |
| 07 | `concept_extraction` | 3 | 3 | 2 | 4 | 2 | WARN |
| 08 | `coreference_resolution` | 4 | 4 | 4 | 4 | 4 | OK |
| 09 | `relation_extraction` | 1 | 1 | 1 | 3 | 2 | FAIL |
| 10 | `canonical_claims` / `semantic_claims` | 4 | 4 | 4 | 4 | 4 | OK |
| 11 | `semantic_debug_ir` | 4 | 4 | 4 | 4 | 4 | OK |
| 12 | `triple_extraction` | 4 | 4 | 4 | 4 | 4 | OK |
| 13 | `taxonomy_induction` | 4 | 4 | 4 | 4 | 4 | OK |
| 14 | `type_assertion` | 4 | 4 | 4 | 4 | 4 | OK |
| 15 | `semantic_quality` | 3 | 3 | 3 | 4 | 4 | WARN |
| 16 | `output_generation` | 3 | 4 | 3 | 4 | 2 | FAIL |

La etapa 06 no se penaliza por producir `entities: []`: los párrafos no contienen individuos o entidades nombradas inequívocas; su contenido es conceptual y genérico (`p005`, `p006`). La etapa 14 tampoco se penaliza por `type_assertions: []` por la misma razón.

## 3. Hallazgos

### Q-infosec_p005_p006-05-1

- **Severidad:** media.
- **Tipo:** anotación lingüística incompleta.
- **Atribución:** ERROR_ORIGEN.
- **Cita literal:** “when a primary control cannot be implemented” (`p006`).
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p005_p006/artifacts/pipeline_outputs/observed_p005_p006_05_linguistic_annotation.json`, `/tokens/179`.
- **Evaluación razonada:** el token `cannot` conserva texto y offsets, pero deja vacíos `lemma`, `pos`, `tag`, `dependency` y `head_text`. La negación/modalidad es semánticamente decisiva para la condición. La etapa 05 debía aportar evidencia lingüística completa, no decidir todavía la relación.
- **Impacto downstream:** riesgo de perder la imposibilidad o convertir la condición en positiva. No se cuenta otra vez en pasos posteriores porque la etapa 10 reconstruye correctamente `condition_modality: "cannot"` y `condition_polarity: "negative"`; queda **corregido downstream**.

### Q-infosec_p005_p006-05-2

- **Severidad:** baja.
- **Tipo:** análisis defectuoso de coordinación nominal.
- **Atribución:** ERROR_ORIGEN.
- **Cita literal:** “identifies suspicious activity or policy violations” (`p006`).
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p005_p006/artifacts/pipeline_outputs/observed_p005_p006_05_linguistic_annotation.json`, `/tokens/138/dependency` y `/tokens/141/dependency`.
- **Evaluación razonada:** `activity` se anota como `nmod` de `violations`, mientras solo `violations` queda como `dobj` de `identifies`. La superficie contiene dos objetos coordinados alternativos, no una modificación de uno por el otro.
- **Impacto downstream:** podía omitir `SuspiciousActivity` o fusionarla con `PolicyViolation`. La etapa 10 lo corrige al crear dos claims enlazados por el mismo `alternative_group`; no se vuelve a contar como error nuevo.

### Q-infosec_p005_p006-07-1

- **Severidad:** media.
- **Tipo:** identidad conceptual inconsistente y ruido de candidato.
- **Atribución:** ERROR_ORIGEN.
- **Cita literal:** “causes harm to an asset” y “affect an asset” (`p005`).
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p005_p006/artifacts/pipeline_outputs/observed_p005_p006_07_concept_extraction.json`, `/concepts/8` y `/concepts/25`.
- **Evaluación razonada:** las dos menciones normalizadas como `asset` reciben IDs diferentes (`con-5bad…` y `con-a995…`). Además, la lista incluye candidatos solapados como `potential cause` y `potential cause of an unwanted incident`, y convierte el adjetivo `available` en concepto. La etapa propone candidatos, por lo que cierto conservadurismo es aceptable, pero IDs distintos para el mismo texto normalizado reducen coherencia y precisión.
- **Impacto downstream:** podría fragmentar un único concepto o proyectar recursos de andamiaje. Los claims canónicos unifican `Asset` y no proyectan `Available`; el error no llega como duplicación conceptual al modelo final.

### Q-infosec_p005_p006-09-1

- **Severidad:** alta.
- **Tipo:** pérdida de taxonomía explícita.
- **Atribución:** ERROR_ORIGEN.
- **Cita literal:** “A preventive control is a type of security control”, con la misma forma para detective, corrective y compensating (`p006`).
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p005_p006/artifacts/pipeline_outputs/observed_p005_p006_09_relation_extraction.json`, `/relations/1`, `/relations/7`, `/relations/13` y `/relations/20`.
- **Evaluación razonada:** las relaciones candidatas reducen las definiciones a `subtype be type`, con `object_text: "type"` y sin objeto `security control`. Esto no expresa la relación taxonómica literal y deja cuatro objetos sin referencia conceptual.
- **Impacto downstream:** de propagarse, impediría inducir la jerarquía central de `p006`. La etapa 10 lo **corrige** mediante cuatro claims `is_a SecurityControl`, y las etapas 12–13 conservan esos claims; por ello no se contabiliza como cuatro errores propagados adicionales.

### Q-infosec_p005_p006-09-2

- **Severidad:** alta.
- **Tipo:** colapso de modalidad y contexto proposicional.
- **Atribución:** ERROR_ORIGEN.
- **Cita literal:** “A risk scenario describes how a threat may exploit a vulnerability and affect an asset” (`p005`).
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p005_p006/artifacts/pipeline_outputs/observed_p005_p006_09_relation_extraction.json`, `/relations/3` y `/relations/4`.
- **Evaluación razonada:** se extraen `Threat exploit Vulnerability` y `Threat affect Asset` sin campos para `may`, sin el contexto `RiskScenario` y sin indicar que son eventos descritos. Como hechos simples serían **NO SOPORTADOS**.
- **Impacto downstream:** habría convertido posibilidades descritas en hechos incondicionales. La etapa 10 lo corrige con `modality: "may"`, `context: "RiskScenario"` y `proposition_role: "described_event"`; las etapas 12 y 16 preservan esa estructura en vez de materializar los hechos.

### Q-infosec_p005_p006-09-3

- **Severidad:** alta.
- **Tipo:** relación semánticamente mal formada.
- **Atribución:** ERROR_ORIGEN.
- **Cita literal:** “a threat exploits a vulnerability and causes harm to an asset” (`p005`).
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p005_p006/artifacts/pipeline_outputs/observed_p005_p006_09_relation_extraction.json`, `/relations/9`.
- **Evaluación razonada:** `Threat cause_to Asset` pierde el objeto directo `Harm` y convierte el destino introducido por `to` en objeto de un predicado sintético. La proposición literal es que la amenaza causa daño, con `Asset` como destino del daño, todo bajo la posibilidad que define `Risk`.
- **Impacto downstream:** podría inventar una relación directa de “causar un activo”. La etapa 10 la corrige a `Threat causes Harm`, conserva `target: Asset` y añade `modality: possibility` y `context: Risk`.

### Q-infosec_p005_p006-09-4

- **Severidad:** alta.
- **Tipo:** referencia conceptual incompatible con su etiqueta.
- **Atribución:** ERROR_ORIGEN.
- **Cita literal:** “A compensating control is a type of security control that provides an alternative protection mechanism…” (`p006`).
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p005_p006/artifacts/pipeline_outputs/observed_p005_p006_09_relation_extraction.json`, `/relations/0/subject_ref`.
- **Evaluación razonada:** `subject_text` dice `security control`, pero `subject_ref` es `con-07004191b72a7ac3`, que en la etapa 07 identifica `information security`. La misma estrategia de antecedente, además, atribuye las funciones al genérico `security control`, cuando la oración completa caracteriza el subtipo concreto; generalizar la función a todo control de seguridad es **NO SOPORTADO**.
- **Impacto downstream:** amenaza tanto la trazabilidad como la precisión de dominio. La etapa 10 no reutiliza esa referencia defectuosa y crea el claim correcto con sujeto `CompensatingControl`; el error queda corregido antes de triples y RDF.

### Q-infosec_p005_p006-15-1

- **Severidad:** baja.
- **Tipo:** control de ruido incompleto.
- **Atribución:** ERROR_PROPAGADO desde Q-infosec_p005_p006-07-1; no incrementa el conteo de errores de origen.
- **Cita literal:** “automated enforcement is not available” (`p006`).
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p005_p006/artifacts/pipeline_outputs/observed_p005_p006_15_semantic_quality.json`, `/semantic_quality_report/concept_noise` y `/excluded_concepts`.
- **Evaluación razonada:** el reporte declara `concept_noise: []` y no excluye conceptos, aunque la etapa 07 creó `available` como candidato independiente y mantuvo candidatos nominales solapados. El adjetivo participa en una condición negativa; no funciona aquí como concepto autónomo.
- **Impacto downstream:** limitado, porque la proyección usa claims canónicos y no crea una clase `Available`. El control de calidad acierta al no perder la condición, pero sobreestima la limpieza del conjunto completo de candidatos.

### Q-infosec_p005_p006-16-1

- **Severidad:** media.
- **Tipo:** recurso referenciado pero no declarado.
- **Atribución:** ERROR_ORIGEN.
- **Cita literal:** “Risk management is a core process in information security” (`p005`).
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p005_p006/artifacts/pipeline_outputs/observed_p005_p006_16_output_generation.json`, `/output/graph/scoped_relations/0/scope` y `/output/graph/classes`.
- **Evaluación razonada:** la relación acotada usa `orion:InformationSecurity`, pero `InformationSecurity` no aparece en `graph.classes` ni en `graph.schema.classes`. El contenido de alcance se conserva, pero el grafo queda estructuralmente incompleto respecto de uno de sus recursos explícitos.
- **Impacto downstream:** consumidores RDF/OWL pueden encontrar un IRI sin declaración o etiqueta, y la navegación del alcance de `RiskManagement` queda degradada. No se inventa una proposición, pero sí se pierde parte de la representación del concepto explícito.

### Q-infosec_p005_p006-16-2

- **Severidad:** media.
- **Tipo:** duplicación estructural del modelo final.
- **Atribución:** ERROR_ORIGEN.
- **Cita literal:** “Access control is a preventive control” y “Backup restoration is a corrective control” (`p006`).
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p005_p006/artifacts/pipeline_outputs/observed_p005_p006_16_output_generation.json`, `/output/graph/classes` frente a `/output/graph/schema/classes`, y `/output/graph/subclass_facts` frente a `/taxonomy_relations`.
- **Evaluación razonada:** las clases se repiten en dos ramas completas y las taxonomías vuelven a emitirse en dos formas. En RDF la repetición de una terna puede ser idempotente, pero el contrato observado es un modelo JSON y la etapa 16 debía evitar duplicación. Tampoco se declara cuál rama es canónica.
- **Impacto downstream:** riesgo de doble conteo, divergencia futura entre copias y serializaciones inconsistentes. Los hechos repetidos siguen siendo fieles, por lo que el defecto es estructural, no una invención semántica.

### Q-infosec_p005_p006-16-3

- **Severidad:** baja.
- **Tipo:** resumen de esquema ambiguo.
- **Atribución:** ERROR_ORIGEN.
- **Cita literal:** “Risk management is a core process in information security” (`p005`), “A threat is a potential cause…” (`p005`) y “Manual approval is a compensating control when…” (`p006`).
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p005_p006/artifacts/pipeline_outputs/observed_p005_p006_16_output_generation.json`, `/output/graph/object_property_schema/8`.
- **Evaluación razonada:** el esquema agregado de `orion:isA` reúne tres dominios y tres rangos en listas independientes. Las relaciones acotadas conservan correctamente cada pareja, pero el resumen puede leerse como una combinación cruzada no expresada por los párrafos. Es **NO SOPORTADO** inferir, por ejemplo, que cualquier dominio listado mantiene `isA` con cualquier rango listado.
- **Impacto downstream:** no hay triples cruzados materializados, de modo que no es una invención efectiva en este artifact; sí existe riesgo de que un consumidor interprete esas listas como restricciones globales.

## 4. Diagnóstico

- **Primera degradación:** paso 05, donde `cannot` queda sin anotación lingüística y se analiza mal la coordinación “suspicious activity or policy violations” (`p006`). La primera degradación conceptual aparece en 07 con la fragmentación de `Asset` (`p005`). La degradación semántica más grave se concentra en 09.
- **Principal pérdida:** en 09 se pierden temporalmente la taxonomía `*Control -> SecurityControl` (`p006`), el alcance modal de “may” (`p005`) y varios argumentos o condiciones. La etapa 10 recupera esas pérdidas con 32 claims explícitos y trazables.
- **Principal contenido no soportado:** no hay un hecho final materializado claramente inventado. El mayor riesgo no soportado es estructural: interpretar las listas agregadas de dominio/rango de `orion:isA` como combinaciones cruzadas (`p005`, `p006`).
- **Errores que llegan a RDF/OWL:** llegan el IRI `orion:InformationSecurity` sin declaración de clase (`p005`), la duplicación de clases y taxonomías (`p006`) y la ambigüedad del resumen agregado de `isA` (`p005`, `p006`). Los errores graves de 09 no llegan como hechos incondicionales porque 10 los corrige y 16 usa `scoped_relations` o `logical_alternatives`.
- **Aciertos:** intake, normalización, segmentación, tokenización y offsets son completos; la ausencia de entidades nombradas y de type assertions es conservadora; la correferencia distingue complementizadores y relativos; los claims canónicos preservan modalidad, disyunción, condición, temporalidad, voz, destino y evidencia; triples y taxonomía mantienen 32 claims y las 14 clasificaciones explícitas, incluida la clasificación condicional de `ManualApproval` (`p005`, `p006`).
- **Incertidumbres:** no debe decidirse si `Control` equivale a `SecurityControl`, si las disyunciones son exclusivas, si los cuatro tipos son exhaustivos o si los ejemplos son individuos. El pipeline final evita esas inferencias, lo cual es un acierto conservador (`p005`, `p006`).

## 5. Veredicto

- **Calidad global:** **88/100**.
- **Output final:** **parcialmente fiel**. Representa todas las proposiciones canónicas sin convertir modalidades o condiciones en hechos simples, pero incumple el criterio estricto de modelo final sin pérdida ni duplicación por el recurso `InformationSecurity` no declarado y por las ramas repetidas del grafo.
- **Tres correcciones prioritarias:**
  1. Declarar y etiquetar todos los recursos usados por relaciones acotadas, empezando por `orion:InformationSecurity`, y validar que ningún IRI quede colgante (`p005`).
  2. Elegir una representación canónica única para clases y taxonomías, evitando duplicar `graph.classes`/`graph.schema.classes` y `subclass_facts`/`taxonomy_relations` (`p006`).
  3. Preservar pares de sujeto–objeto en los resúmenes de propiedades y endurecer la validación previa contra referencias incompatibles, modalidades perdidas y objetos `type` incompletos (`p005`, `p006`).

Siguiente caso pendiente: infosec_p007_p008.
