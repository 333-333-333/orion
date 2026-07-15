# Revisión semántica: infosec_p029_p030

## 1. Lectura independiente

- **Resumen**
  - `p029` presenta el cumplimiento como satisfacción de requisitos legales, regulatorios, contractuales e internos; define esos tipos y relaciona evidencia, auditoría, controles, no conformidad y acción correctiva.
  - `p030` presenta la privacidad como protección de datos personales y derechos; define roles y prácticas de tratamiento, e introduce límites de finalidad, minimización, conservación y supresión.
  - No hay vínculo explícito entre ambos temas. Tampoco hay nombres propios ni individuos concretos identificados: los sintagmas denotan conceptos, roles o participantes genéricos. “the organization” puede aludir a una organización discursivamente determinada, pero no está nombrada.

- **Conceptos**
  - `p029`: compliance, organization, requirement, legal requirement, regulatory requirement, contractual requirement, internal requirement, obligation, law, regulator, agreement, evidence, demonstration of compliance, audit, control, nonconformity, failure, corrective action.
  - `p030`: privacy, personal data, individual right, data subject, person, data controller, purpose, means, processing, data processor, controller, privacy notice, processing activity, consent, lawful basis, context, data minimization, necessity, purpose limitation, defined purpose, retention limitation, storage duration, data deletion.
  - Relaciones literales: ensures, meets, is/type-of, must be satisfied, derived from, imposed by, defined in/by, supports, evaluates whether, satisfies, fails to meet, addresses, protects, is processed, determines, processes on behalf of, informs about, is a basis for, limits to, restricts to, restricts duration, removes when.
  - Entidades/instancias explícitas: hay participantes genéricos (“the organization”, “a regulator”, “controls”, “individuals”, “a controller”), pero ninguna instancia nombrada. No se justifica convertirlos en individuos concretos únicos.

- **Proposiciones con evidencia**
  1. **EXPLÍCITO (`p029`)**: Compliance asegura la proposición de que la organización satisface cuatro clases de requisitos: “Compliance ensures that the organization meets legal, regulatory, contractual, and internal requirements.” La coordinación distribuye `meets` sobre legal, regulatory, contractual e internal requirements.
  2. **EXPLÍCITO (`p029`)**: Un requisito de cumplimiento es una obligación y esa obligación debe satisfacerse: “A compliance requirement is an obligation that must be satisfied.”
  3. **EXPLÍCITO (`p029`)**: Un requisito legal es un tipo de requisito de cumplimiento y deriva de la ley: “A legal requirement is a type of compliance requirement derived from law.”
  4. **EXPLÍCITO (`p029`)**: Un requisito regulatorio es un tipo de requisito de cumplimiento y lo impone un regulador: “A regulatory requirement is a type of compliance requirement imposed by a regulator.”
  5. **EXPLÍCITO (`p029`)**: Un requisito contractual es un tipo de requisito de cumplimiento y se define en un acuerdo: “A contractual requirement is a type of compliance requirement defined in an agreement.”
  6. **EXPLÍCITO (`p029`)**: Un requisito interno es un tipo de requisito de cumplimiento y lo define la organización: “An internal requirement is a type of compliance requirement defined by the organization.”
  7. **EXPLÍCITO (`p029`)**: La evidencia apoya la demostración del cumplimiento: “Evidence supports the demonstration of compliance.”
  8. **EXPLÍCITO (`p029`)**: Una auditoría evalúa la cuestión de si los controles satisfacen requisitos: “An audit evaluates whether controls satisfy requirements.” **NO SOPORTADO**: afirmar sin el alcance de `whether` que los controles efectivamente los satisfacen.
  9. **EXPLÍCITO (`p029`)**: Una no conformidad es un fallo en satisfacer un requisito: “A nonconformity is a failure to meet a requirement.”
  10. **EXPLÍCITO (`p029`)**: Una acción correctiva aborda una no conformidad: “A corrective action addresses a nonconformity.”
  11. **EXPLÍCITO (`p030`)**: La privacidad protege dos objetos coordinados, los datos personales y los derechos de los individuos: “Privacy protects personal data and the rights of individuals.”
  12. **EXPLÍCITO (`p030`)**: Un interesado es una persona cuyos datos personales son tratados: “A data subject is a person whose personal data is processed.”
  13. **EXPLÍCITO (`p030`)**: Un responsable determina tanto los fines como los medios del tratamiento de datos personales: “A data controller determines the purposes and means of processing personal data.”
  14. **EXPLÍCITO (`p030`)**: Un encargado trata datos personales por cuenta de un responsable: “A data processor processes personal data on behalf of a controller.”
  15. **EXPLÍCITO (`p030`)**: Un aviso de privacidad informa a los interesados acerca de actividades de tratamiento: “A privacy notice informs data subjects about processing activities.”
  16. **EXPLÍCITO (`p030`)**: El consentimiento es una base lícita para el tratamiento, con alcance limitado a algunos contextos: “Consent is a lawful basis for processing in some contexts.” **NO SOPORTADO**: universalizarlo a todo contexto.
  17. **EXPLÍCITO (`p030`)**: La minimización limita los datos personales a lo necesario: “Data minimization limits personal data to what is necessary.”
  18. **EXPLÍCITO (`p030`)**: La limitación de finalidad restringe el tratamiento a fines definidos: “Purpose limitation restricts processing to defined purposes.”
  19. **EXPLÍCITO (`p030`)**: La limitación de conservación restringe cuánto tiempo se almacenan los datos personales: “Retention limitation restricts how long personal data is stored.”
  20. **EXPLÍCITO (`p030`)**: La supresión elimina los datos personales bajo la condición de que ya no sean necesarios: “Data deletion removes personal data when it is no longer needed.” **NO SOPORTADO**: convertirla en una eliminación incondicional.
  - **ENTRAÑADO**: legal, regulatory, contractual e internal requirement están incluidos bajo compliance requirement por la fórmula literal “is a type of”.
  - **ENTRAÑADO**: en `p030`, “it” en “when it is no longer needed” retoma `personal data`; preservar esa correferencia es necesario para conservar la condición.
  - **PLAUSIBLE**, no literal: normalizar “how long personal data is stored” como `StorageDuration` y “rights of individuals” como `IndividualRight`, siempre que se mantenga la cita y no se añada contenido.
  - **CONTRADICHO por la estructura textual**: interpretar el primer “that” de `p029` como mención correferente a `Compliance`; introduce una subordinada completiva, no reemplaza un referente nominal.

- **Taxonomías explícitas**
  - `p029`: `LegalRequirement → ComplianceRequirement`; `RegulatoryRequirement → ComplianceRequirement`; `ContractualRequirement → ComplianceRequirement`; `InternalRequirement → ComplianceRequirement`, todas **EXPLÍCITAS** mediante “a type of”.
  - Clasificaciones definicionales también explícitas: `ComplianceRequirement → Obligation`, `Nonconformity → Failure` (`p029`) y `DataSubject → Person` (`p030`).
  - `Consent → LawfulBasis` (`p030`) solo está soportado con la condición “in some contexts”; no es una subclase universal incondicional.
  - No se expresa una taxonomía entre data controller, data processor y controller; solo se describen funciones y una relación “on behalf of”.

- **Modalidad**
  - `p029`: `must` impone necesidad de satisfacción; `whether` marca contenido evaluado y no asertado como verdadero.
  - `p030`: `in some contexts` restringe el alcance de la base lícita; `what is necessary` introduce un criterio sin especificar su medida; `defined purposes` restringe el destino; `how long` expresa dimensión temporal; `when it is no longer needed` condiciona la supresión y contiene negación temporal (`no longer`).
  - El presente simple formula caracterizaciones generales, no eventos individuales fechados.

- **Ambigüedades**
  - `p029`: “the organization” puede ser una entidad discursiva concreta o el rol genérico organización; no hay identidad nominal suficiente para crear una instancia única. La segunda aparición es correferente de forma plausible, no identificada por nombre.
  - `p029`: “requirements” aparece en plural genérico; no se enumeran instancias concretas. En la primera oración, los cuatro modificadores comparten el núcleo coordinado `requirements`.
  - `p029`: “whether controls satisfy requirements” es el objeto de evaluación; su verdad queda abierta.
  - `p030`: `whose` vincula los datos personales con `person`, que en la cópula caracteriza al data subject. `it` tiene como antecedente textual natural `personal data`.
  - `p030`: no se especifican cuáles son “some contexts”, qué cuenta como “necessary”, cuáles son los “defined purposes” ni una duración concreta. El conservadurismo ante esas ausencias es correcto.

## 2. Resultado por etapa

Escala: 0 = ausente/contrario; 1 = grave; 2 = parcial; 3 = bueno con defecto localizado; 4 = completo y fiel. Las puntuaciones no vuelven a penalizar errores meramente heredados.

| Paso | Etapa | Fidelidad | Cobertura | Precisión | Trazabilidad | Coherencia | Estado |
|---:|---|---:|---:|---:|---:|---:|---|
| 01 | input_intake | 4 | 4 | 4 | 4 | 4 | OK |
| 02 | preprocessing | 4 | 4 | 4 | 4 | 4 | OK |
| 03 | sentence_segmentation | 4 | 4 | 4 | 4 | 4 | OK |
| 04 | tokenization | 4 | 4 | 4 | 4 | 4 | OK |
| 05 | linguistic_annotation | 3 | 2 | 3 | 4 | 2 | FAIL |
| 06 | entity_extraction | 4 | 4 | 4 | 4 | 4 | OK |
| 07 | concept_extraction | 2 | 3 | 2 | 4 | 2 | WARN |
| 08 | coreference_resolution | 1 | 1 | 1 | 4 | 2 | FAIL |
| 09 | relation_extraction | 2 | 2 | 2 | 4 | 2 | FAIL |
| 10 | canonical_claims / semantic_claims | 3 | 4 | 3 | 4 | 4 | WARN |
| 11 | semantic_debug_ir | 3 | 2 | 3 | 3 | 3 | WARN |
| 12 | triple_extraction | 4 | 4 | 4 | 1 | 3 | FAIL |
| 13 | taxonomy_induction | 4 | 4 | 4 | 3 | 4 | OK |
| 14 | type_assertion | 4 | 4 | 4 | 4 | 4 | OK |
| 15 | semantic_quality | 1 | 1 | 1 | 2 | 1 | FAIL |
| 16 | output_generation | 3 | 4 | 3 | 3 | 4 | FAIL |

## 3. Hallazgos

### Q-infosec_p029_p030-05-1
- **Severidad:** alta
- **Tipo:** anotación lingüística incompleta e inconsistente
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** `p029`, “An audit evaluates whether controls satisfy requirements.”
- **Archivo:** `tests/smoke/cases/infosec_p029_p030/artifacts/pipeline_outputs/observed_p029_p030_05_linguistic_annotation.json`
- **JSON Pointer:** `/tokens/94/pos`, `/tokens/94/tag`, `/tokens/0/dep` (el campo `dep` es nulo en todos los tokens)
- **Evaluación razonada:** `satisfy` se anota como `NOUN/NN` aunque ocupa el núcleo predicativo de la subordinada; además, la etapa no aporta ninguna etiqueta de dependencia, pese a que esa evidencia forma parte de su responsabilidad. `head_text` no sustituye la relación de dependencia ausente.
- **Impacto downstream:** favorece sintagmas espurios y dificulta distinguir subordinación, coordinación, modalidad y argumentos. Es la primera degradación observable; no se vuelve a contar como error nuevo cuando se manifiesta en conceptos.

### Q-infosec_p029_p030-07-1
- **Severidad:** media
- **Tipo:** candidatos conceptuales que incorporan estructura predicativa o palabras funcionales
- **Atribución:** ERROR_AMPLIFICADO
- **Cita literal:** `p029`, “An audit evaluates whether controls satisfy requirements.”; `p030`, “Retention limitation restricts how long personal data is stored.”
- **Archivo:** `tests/smoke/cases/infosec_p029_p030/artifacts/pipeline_outputs/observed_p029_p030_07_concept_extraction.json`
- **JSON Pointer:** `/concepts/16`, `/concepts/43`, `/concepts/48`
- **Evaluación razonada:** se proponen como conceptos `controls satisfy requirements`, `what` y `long personal data`. El primero absorbe un predicado dentro del supuesto sintagma nominal; el segundo es una forma relativa sin contenido conceptual autónomo; el tercero incorpora erróneamente `long` a `personal data` en vez de conservar la dimensión “how long … is stored”. Son candidatos trazables, pero semánticamente ruidosos y todos reciben confianza alta (0.95).
- **Impacto downstream:** contamina la entrada de correferencia y relaciones. La capa de claims corrige estos casos, por lo que no llegan como tales al modelo final.

### Q-infosec_p029_p030-08-1
- **Severidad:** alta
- **Tipo:** correferencia falsa y cobertura insuficiente
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** `p029`, “Compliance ensures that the organization meets …”; `p030`, “Data deletion removes personal data when it is no longer needed.”
- **Archivo:** `tests/smoke/cases/infosec_p029_p030/artifacts/pipeline_outputs/observed_p029_p030_08_coreference_resolution.json`
- **JSON Pointer:** `/coreferences/0`, `/coreferences`
- **Evaluación razonada:** el primer `that` se resuelve a `Compliance`, aunque es el introductor de la proposición subordinada. En cambio, la lista completa no contiene resoluciones para `whose` ni para `it → personal data`. La resolución del segundo `that → obligation` sí es fiel.
- **Impacto downstream:** puede alterar el alcance de `ensures` y perder la condición de supresión. Las claims de la etapa 10 reconstruyen ambas estructuras, por lo que este error queda corregido antes de triples.

### Q-infosec_p029_p030-09-1
- **Severidad:** alta
- **Tipo:** relaciones truncadas, lematización defectuosa y pérdida de alcance
- **Atribución:** ERROR_AMPLIFICADO
- **Cita literal:** `p029`, “A legal requirement is a type of compliance requirement derived from law.” y “A compliance requirement is an obligation that must be satisfied.”; `p030`, “A data controller determines the purposes and means of processing personal data.”
- **Archivo:** `tests/smoke/cases/infosec_p029_p030/artifacts/pipeline_outputs/observed_p029_p030_09_relation_extraction.json`
- **JSON Pointer:** `/relations/16`, `/relations/2`, `/relations/18`, `/relations/19`, `/relations/20`
- **Evaluación razonada:** las cuatro definiciones taxonómicas quedan como `X be type`, sin objeto `compliance requirement` ni sus relaciones `derived_from`, `imposed_by`, `defined_in` o `defined_by`; la modalidad se fragmenta como `that be satisfied`; la primera coordinación se reduce a `organization meet legal requirement`; y `purposes` aparece mutilado como `purpos`. También faltan relaciones completas para auditoría, conservación y varios complementos/condiciones de `p030`.
- **Impacto downstream:** esta es la mayor pérdida semántica intermedia. No obstante, la etapa 10 la corrige casi por completo mediante claims explícitas; por ello no se atribuye otra vez a triples o taxonomía.

### Q-infosec_p029_p030-10-1
- **Severidad:** alta
- **Tipo:** objeto incorrecto para un operador proposicional
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** `p029`, “Compliance ensures that the organization meets legal, regulatory, contractual, and internal requirements.”
- **Archivo:** `tests/smoke/cases/infosec_p029_p030/artifacts/pipeline_outputs/observed_p029_p030_10_canonical_claims.json`
- **JSON Pointer:** `/canonical_claims/claims/0` y `/semantic_claims/claims/0`
- **Evaluación razonada:** `Compliance ensures Organization` no es la proposición literal: el objeto semántico de `ensures` es que la organización satisface los cuatro tipos de requisitos. `relation_role: proposition_wrapper` y `proposition_group` preservan que hay alcance proposicional, pero no corrigen que el campo `object` sea `Organization`. La interpretación binaria es **NO SOPORTADA**.
- **Impacto downstream:** el triple correspondiente hereda el objeto incorrecto; el output evita materializarlo como hecho simple, pero lo conserva como relación acotada y lo amplía a esquema de propiedad.

### Q-infosec_p029_p030-10-2
- **Severidad:** informativa
- **Tipo:** recuperación semántica sustancial
- **Atribución:** ERROR_CORREGIDO
- **Cita literal:** `p029`, “An audit evaluates whether controls satisfy requirements.”; `p030`, “Consent is a lawful basis for processing in some contexts.”
- **Archivo:** `tests/smoke/cases/infosec_p029_p030/artifacts/pipeline_outputs/observed_p029_p030_10_canonical_claims.json`
- **JSON Pointer:** `/canonical_claims/claims`, `/semantic_claims/claims`
- **Evaluación razonada:** las 35 claims cubren las 20 oraciones y restauran las cuatro taxonomías, `must`, el alcance de `whether`, `on_behalf_of`, `topics`, `necessary`, `DefinedPurpose`, `StorageDuration` y la condición negativa de supresión. Canonical y semantic claims son coherentes e idénticas, y cada claim incluye párrafo, oración y evidencia literal.
- **Impacto downstream:** evita que la mayor parte del ruido de 07–09 alcance triples y el modelo final. La excepción es el wrapper indicado en el hallazgo anterior.

### Q-infosec_p029_p030-11-1
- **Severidad:** baja
- **Tipo:** proyección de depuración incompleta
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** `p030`, “A data processor processes personal data on behalf of a controller.” y “Data minimization limits personal data to what is necessary.”
- **Archivo:** `tests/smoke/cases/infosec_p029_p030/artifacts/pipeline_outputs/observed_p029_p030_11_semantic_debug_ir.json`
- **JSON Pointer:** `/artifacts/semantic_debug_ir/relations/27`, `/artifacts/semantic_debug_ir/relations/31`
- **Evaluación razonada:** el IR conserva los SPO y la evidencia, pero omite metadatos de claims como `on_behalf_of` en la relación 27 y `constraint: necessary` en la 31; también omite `processing_state` en la relación relativa. Para depurar la proyección semántica, esos campos son evidencia relevante.
- **Impacto downstream:** ninguno sobre RDF, porque esta etapa es un sidecar; el impacto se limita a diagnóstico incompleto.

### Q-infosec_p029_p030-12-1
- **Severidad:** alta
- **Tipo:** ruptura de identidad y trazabilidad de fuente
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** `p029`, “A corrective action addresses a nonconformity.”
- **Archivo:** `tests/smoke/cases/infosec_p029_p030/artifacts/pipeline_outputs/observed_p029_p030_12_triple_extraction.json` (comparado con etapas 01 y 03)
- **JSON Pointer:** `/triples/0/source_text_id`, `/triples/0/sentence_id`; referencia de entrada: etapa 01 `/source_text_id` y etapa 03 `/sentences/9/sentence_id`
- **Evaluación razonada:** el triple usa `source_text_id = b54b…` y `sentence_id = sent-0a3f…`, mientras la fuente de intake es `bab0…` y la oración segmentada correspondiente es `sent-7f08…`. El patrón afecta a los triples pese a que offsets y evidencia siguen apuntando al texto correcto. Los `claim_id` sí se conservan.
- **Impacto downstream:** taxonomía hereda los identificadores sustituidos y el output final ya no expone una cadena directa hasta la identidad de intake. No se penaliza de nuevo a la etapa 13 por limitarse a propagar la entrada recibida.

### Q-infosec_p029_p030-15-1
- **Severidad:** alta
- **Tipo:** control de calidad incapaz de detectar errores presentes
- **Atribución:** ERROR_AMPLIFICADO
- **Cita literal:** `p029`, “Compliance ensures that the organization meets …”; `p030`, “Retention limitation restricts how long personal data is stored.”
- **Archivo:** `tests/smoke/cases/infosec_p029_p030/artifacts/pipeline_outputs/observed_p029_p030_15_semantic_quality.json`
- **JSON Pointer:** `/semantic_quality_report/quality_score`, `/semantic_quality_report/warnings`, `/semantic_quality_report/concept_noise`, `/semantic_quality_report/semantic_integrity_checks`
- **Evaluación razonada:** declara `quality_score: 1.0`, `rdf_readiness: true`, cero warnings y cero ruido, aunque siguen presentes el wrapper `Compliance ensures Organization`, conceptos como `long personal data` y la ruptura de IDs de fuente. `logical_scope_structured: true` solo reconoce la estructura formal, no la incorrección del objeto del wrapper.
- **Impacto downstream:** no crea el error semántico, pero amplifica su riesgo al certificarlo sin reserva y permitir su proyección final.

### Q-infosec_p029_p030-16-1
- **Severidad:** alta
- **Tipo:** contenido no soportado amplificado a esquema RDF/OWL
- **Atribución:** ERROR_AMPLIFICADO
- **Cita literal:** `p029`, “Compliance ensures that the organization meets legal, regulatory, contractual, and internal requirements.”
- **Archivo:** `tests/smoke/cases/infosec_p029_p030/artifacts/pipeline_outputs/observed_p029_p030_16_output_generation.json`
- **JSON Pointer:** `/output/graph/scoped_relations/0`, `/output/graph/object_property_schema/6`
- **Evaluación razonada:** el modelo conserva `Compliance ensures Organization` como relación acotada y declara para `orion:ensures` dominio `Compliance` y rango acotado `Organization`. El grupo proposicional enlaza las cuatro relaciones `Organization meets …`, pero el rango sigue representando al sujeto interno como si fuera el objeto de `ensures`. No hay pérdida de los cuatro requisitos, pero sí una aridad/selección semántica incorrecta.
- **Impacto downstream:** es el principal contenido no soportado que llega al modelo RDF/OWL. Puede inducir consultas o consumidores a interpretar una relación directa Compliance–Organization que el párrafo no afirma.

## 4. Diagnóstico

- **Primera degradación:** etapa 05. La ausencia total de dependencias y el POS incorrecto de `satisfy` deterioran la evidencia lingüística antes de la extracción semántica.
- **Principal pérdida:** en la ruta intermedia, etapa 09 pierde taxonomías, complementos, modalidad y alcance. Esa pérdida queda **ERROR_CORREGIDO** en 10. La principal pérdida persistente es la identidad de fuente/oración sustituida en 12.
- **Principal contenido no soportado:** `Compliance ensures Organization`, originado en 10. El texto solo soporta que Compliance asegura una proposición cuyo sujeto interno es la organización.
- **Errores que llegan a RDF/OWL:** (1) el wrapper anterior llega como `scoped_relation` y como esquema acotado de `orion:ensures`; (2) la trazabilidad ya no mantiene los IDs de intake/segmentación. Los conceptos ruidosos de 07, la falsa correferencia de 08 y la mayoría de pérdidas de 09 no llegan al grafo final gracias a 10.
- **Aciertos:** intake, normalización, segmentación y tokens son exactos; la ausencia de entidades NER y de type assertions es conservadora y adecuada al no haber individuos nombrados; las claims cubren las 20 oraciones; taxonomía separa correctamente la clasificación condicional de Consent; triples y output conservan `must`, `whether`, contextos, temas, finalidad, duración, tratamiento por cuenta de y condición de supresión; la proyección evita materializar como hechos incondicionales los contenidos acotados.
- **Incertidumbres:** la lectura como clases de los participantes genéricos es razonable, pero “the organization” admite lectura de entidad discursiva. `IndividualRight`, `RequirementSatisfaction` y `StorageDuration` son abstracciones entrañadas o plausibles, no términos literales; son aceptables solo por conservar evidencia y alcance. No se penaliza no crear instancias ni completar contextos, necesidades, fines o duraciones que el texto deja indeterminados.

## 5. Veredicto

- **Calidad global:** **81/100**.
- **Output final:** **parcialmente fiel**. Conserva casi toda la semántica literal, incluidas coordinaciones, taxonomías y condiciones, pero incumple la exigencia de ausencia de invención por el wrapper `Compliance ensures Organization` y presenta trazabilidad de fuente incompleta/inconsistente.
- **Tres correcciones prioritarias:**
  1. Representar el objeto de `ensures` como la proposición completa —o conservar solo el grupo proposicional—, nunca como `Organization`; impedir además que esa aproximación genere rango de propiedad.
  2. Preservar sin sustitución `source_text_id` y `sentence_id` desde intake/segmentación hasta triples, taxonomía y output, exponiendo el enlace en la proyección final.
  3. Reparar y validar la cadena 05→09: dependencias no nulas, POS correcto, conceptos sin cláusulas/palabras funcionales y relaciones con complementos, coordinación, modalidad y condiciones; la etapa 15 debe detectar y advertir estas anomalías antes de declarar RDF readiness.

Siguiente caso pendiente: infosec_p031_p032.
