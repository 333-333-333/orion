# Revisión semántica: infosec_p023_p024

## 1. Lectura independiente

### Resumen

Los dos párrafos contienen conocimiento genérico, no relatos sobre individuos concretos. **p023** enumera clases de incidentes y añade propiedades definitorias para algunos tipos. **p024** define conceptos de continuidad y recuperación, y describe qué protegen, identifican, definen o verifican. No hay nombres propios ni instancias identificadas de forma inequívoca.

La lectura se construyó antes de abrir los artifacts. Las etiquetas usadas son: **EXPLÍCITO** (afirmado literalmente), **ENTRAÑADO** (se sigue de la composición lingüística sin conocimiento externo), **PLAUSIBLE** (lectura posible pero no obligada), **NO SOPORTADO** y **CONTRADICHO**.

### Conceptos

- **p023:** malware infection, security incident, phishing attack, social engineering incident, ransomware attack, malware incident, data breach, unauthorized access, disclosure of data, data, denial-of-service attack, availability incident, access, unapproved identity, insider misuse, internal actor, lost device incident y physical and information security incident.
- **p024:** business continuity, disaster recovery, organization, major disruption, capability, critical operation, disruption, process, technology service, disruptive event, business impact analysis, critical process, dependency, recovery priority, recovery time objective, maximum acceptable time, service/restoration, recovery point objective, maximum acceptable amount of data loss, time, backup, copy of data, recovery, backup policy, backup frequency, retention, protection, restoration requirement, disaster recovery test y recovery procedure.
- **Entidades/instancias explícitas:** no hay individuos nombrados. “the organization” [p024], “an unapproved identity” [p023], “an internal actor” [p023], “a service” [p024] y “a disruptive event” [p024] son referentes genéricos o anónimos; convertirlos en individuos identificados exigiría una decisión de modelado adicional.

### Proposiciones con evidencia

| ID | Clasificación | Proposición independiente | Evidencia breve |
|---|---|---|---|
| P01 | EXPLÍCITO | Malware infection es un tipo de security incident. | “malware infection is a type of security incident” [p023] |
| P02 | EXPLÍCITO | Phishing attack es un tipo de social engineering incident. | “phishing attack is a type of social engineering incident” [p023] |
| P03 | EXPLÍCITO | Ransomware attack es un tipo de malware incident. | “ransomware attack is a type of malware incident” [p023] |
| P04 | EXPLÍCITO | Data breach es un tipo de security incident. | “data breach is a type of security incident” [p023] |
| P05 | EXPLÍCITO | El tipo descrito en P04 involucra la alternativa “unauthorized access to” o “disclosure of data”. | “that involves unauthorized access to or disclosure of data” [p023] |
| P06 | ENTRAÑADO | En la coordinación elíptica, data es el objeto compartido de unauthorized access y disclosure. | “unauthorized access to or disclosure of data” [p023] |
| P07 | EXPLÍCITO | Denial-of-service attack es un tipo de availability incident. | “denial-of-service attack is a type of availability incident” [p023] |
| P08 | EXPLÍCITO | Unauthorized access es un tipo de security incident. | “Unauthorized access is a type of security incident” [p023] |
| P09 | EXPLÍCITO | Unauthorized access involucra access. | “involving access” [p023] |
| P10 | ENTRAÑADO | En P09, unapproved identity desempeña el papel de participante/actor del access. | “access by an unapproved identity” [p023] |
| P11 | EXPLÍCITO | Insider misuse es un tipo de security incident. | “Insider misuse is a type of security incident” [p023] |
| P12 | EXPLÍCITO | Insider misuse está causado por un internal actor. | “caused by an internal actor” [p023] |
| P13 | EXPLÍCITO | Lost device incident pertenece al tipo expresado por “physical and information security incident”. | “is a type of physical and information security incident” [p023] |
| P14 | EXPLÍCITO | Business continuity y disaster recovery, como sujeto coordinado, protegen a la organización. | “Business continuity and disaster recovery protect the organization” [p024] |
| P15 | EXPLÍCITO | La protección de P14 es contra major disruptions. | “against major disruptions” [p024] |
| P16 | EXPLÍCITO | Business continuity se define como una capability. | “Business continuity is the capability” [p024] |
| P17 | EXPLÍCITO, con modalidad | El contenido de esa capability es continuar critical operations. No afirma que actualmente continúen. | “capability to continue critical operations” [p024] |
| P18 | EXPLÍCITO | La continuación de P17 está temporalmente situada during disruption. | “during disruption” [p024] |
| P19 | EXPLÍCITO | Disaster recovery se define como un process. | “Disaster recovery is the process” [p024] |
| P20 | EXPLÍCITO | El contenido del proceso es restoring technology services. | “process of restoring technology services” [p024] |
| P21 | EXPLÍCITO | La restauración de P20 sucede after a disruptive event. | “after a disruptive event” [p024] |
| P22 | EXPLÍCITO | Business impact analysis identifica critical processes. | “identifies critical processes” [p024] |
| P23 | EXPLÍCITO | Business impact analysis identifica dependencies. | “identifies … dependencies” [p024] |
| P24 | EXPLÍCITO | Business impact analysis identifica recovery priorities. | “identifies … recovery priorities” [p024] |
| P25 | EXPLÍCITO | Recovery time objective define el maximum acceptable time. | “defines the maximum acceptable time” [p024] |
| P26 | EXPLÍCITO | El tiempo de P25 se aplica a restore a service. | “time to restore a service” [p024] |
| P27 | EXPLÍCITO | Recovery point objective define el maximum acceptable amount of data loss. | “defines the maximum acceptable amount of data loss” [p024] |
| P28 | EXPLÍCITO | La cantidad de P27 se mide in time. | “measured in time” [p024] |
| P29 | EXPLÍCITO | Backup se define como a copy of data. | “A backup is a copy of data” [p024] |
| P30 | EXPLÍCITO, alcance ambiguo | Algo en el sintagma de P29 se usa for recovery; el adjunto no fija inequívocamente si modifica backup, copy o data. | “data used for recovery” [p024] |
| P31 | EXPLÍCITO | Backup policy define backup frequency. | “defines backup frequency” [p024] |
| P32 | EXPLÍCITO | Backup policy define retention. | “frequency, retention” [p024] |
| P33 | EXPLÍCITO | Backup policy define protection. | “retention, protection” [p024] |
| P34 | EXPLÍCITO | Backup policy define restoration requirements. | “restoration requirements” [p024] |
| P35 | EXPLÍCITO, con modalidad | Disaster recovery test verifica la cuestión de si recovery procedures work as expected. | “verifies whether recovery procedures work as expected” [p024] |
| P36 | NO SOPORTADO | Recovery procedures efectivamente funcionan como se espera. | El texto solo dice “verifies whether”, no afirma el resultado [p024]. |
| P37 | PLAUSIBLE | Business continuity protege por sí sola a la organización, y disaster recovery también lo hace por sí sola. | La distribución desde el sujeto coordinado de “Business continuity and disaster recovery protect…” no es obligatoria [p024]. |
| P38 | CONTRADICHO | Recovery point objective define el maximum acceptable time to restore a service. | Ese contenido se asigna a recovery **time** objective; recovery point objective define data loss [p024]. |

### Taxonomías explícitas

- **p023:** las relaciones P01, P02, P03, P04, P07, P08 y P11 son taxonomías directas inequívocas por el patrón literal “is a type of”. P13 también contiene ese patrón, pero el límite interno del supertipo coordinado es ambiguo: no autoriza dos relaciones separadas `LostDeviceIncident → PhysicalIncident` y `LostDeviceIncident → InformationSecurityIncident`.
- **p024:** hay categorizaciones definitorias explícitas —`BusinessContinuity → Capability`, `DisasterRecovery → Process` y `Backup → CopyOfData`— aunque no usan la fórmula “type of”.
- No hay base textual para convertir relaciones como `defines`, `identifies`, `protects` o `verifies` en taxonomías.

### Modalidad

- Predomina el presente genérico definitorio, sin negación ni obligación deóntica.
- “capability to continue” [p024] introduce **capacidad**, no ejecución efectiva.
- “whether … work as expected” [p024] introduce una proposición interrogada/verificada, no la verdad de esa proposición.
- “maximum acceptable” [p024] expresa un límite normativo dentro de las definiciones de RTO y RPO.
- “during” y “after” [p024] son calificadores temporales; “for recovery” [p024] expresa finalidad con adjunción ambigua.
- “or” [p023] conserva alternativas disyuntivas; “and” coordina el sujeto en P14 y componentes nominales en P13.

### Ambigüedades

- **Correferencia de “that”:** en “a type of security incident that involves…” [p023], el antecedente sintáctico inmediato es `security incident`, mientras que la lectura definitoria global atribuye la restricción a `data breach`. Esta segunda lectura es razonable, pero no debe ocultarse la ambigüedad de adjunción.
- **Elipsis coordinada:** en “unauthorized access to or disclosure of data” [p023], compartir `data` entre ambas alternativas es **ENTRAÑADO** por la coordinación, pero debe conservarse el operador `or`.
- **Coordinación del supertipo:** “physical and information security incident” [p023] puede ser un tipo compuesto o coordinación de modificadores; separar dos superclases es solo **PLAUSIBLE**.
- **Adjunción:** “a copy of data used for recovery” [p024] permite que `used for recovery` modifique `data`, `copy of data` o, por lectura funcional, `backup`. Elegir exclusivamente `Backup used_for Recovery` como hecho directo no está plenamente soportado.
- **Sujeto coordinado:** P14 afirma el sujeto compuesto; distribuirlo a cada miembro es **PLAUSIBLE**, no entrañado.
- **Referente definido:** “the organization” [p024] no remite a una organización previamente identificada; debe permanecer anónimo o no resuelto.

## 2. Resultado por etapa

Escala por dimensión: 0 = ausente/contradictorio, 1 = muy deficiente, 2 = parcial, 3 = adecuado con defectos, 4 = completo y fiel.

| Paso | Etapa | Fidelidad | Cobertura | Precisión | Trazabilidad | Coherencia | Estado |
|---:|---|---:|---:|---:|---:|---:|---|
| 01 | input_intake | 4 | 4 | 4 | 4 | 4 | OK |
| 02 | preprocessing | 4 | 4 | 4 | 4 | 4 | OK |
| 03 | sentence_segmentation | 4 | 4 | 4 | 4 | 4 | OK |
| 04 | tokenization | 4 | 4 | 4 | 4 | 4 | OK |
| 05 | linguistic_annotation | 4 | 2 | 3 | 4 | 2 | WARN |
| 06 | entity_extraction | 4 | 4 | 4 | 4 | 4 | OK |
| 07 | concept_extraction | 3 | 2 | 4 | 4 | 3 | FAIL |
| 08 | coreference_resolution | 3 | 4 | 3 | 3 | 4 | WARN |
| 09 | relation_extraction | 1 | 1 | 1 | 3 | 1 | FAIL |
| 10 | canonical_claims / semantic_claims | 4 | 4 | 4 | 4 | 4 | OK |
| 11 | semantic_debug_ir | 4 | 4 | 4 | 4 | 4 | OK |
| 12 | triple_extraction | 4 | 4 | 4 | 3 | 2 | WARN |
| 13 | taxonomy_induction | 3 | 4 | 2 | 4 | 2 | FAIL |
| 14 | type_assertion | 4 | 4 | 4 | 4 | 4 | OK |
| 15 | semantic_quality | 2 | 2 | 2 | 3 | 2 | FAIL |
| 16 | output_generation | 4 | 4 | 3 | 3 | 3 | WARN |

La ausencia de entidades en 06 y de type assertions en 14 no se penaliza: los párrafos no identifican individuos nombrados. El paso 11 sí está configurado y por eso se evalúa, no es N/A.

## 3. Hallazgos

### Q-infosec_p023_p024-05-1 — Dependencias sintácticas ausentes

- **Severidad:** MEDIA
- **Tipo:** cobertura y coherencia de anotación lingüística
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** “A malware infection is a type of security incident.” [p023]
- **Archivo y JSON Pointer:** `observed_p023_p024_05_linguistic_annotation.json`, `/tokens/0/dep` (el patrón `null` se repite en todos los tokens)
- **Evaluación razonada:** la etapa aporta lema, POS, tag y `head_text`, pero no aporta ninguna etiqueta de dependencia, pese a que su responsabilidad contractual incluye dependency. El texto contiene estructuras copulares, relativas, pasivas y coordinadas cuya interpretación depende de esa evidencia.
- **Impacto downstream:** reduce la base estructural disponible para distinguir sujeto, complemento definitorio, coordinación y alcance. No se vuelve a contar como error nuevo en 07–09; allí solo se atribuyen las degradaciones propias o amplificadas.

### Q-infosec_p023_p024-07-1 — Omisión sistemática de conceptos que son supertipos o complementos definitorios

- **Severidad:** ALTA
- **Tipo:** pérdida de cobertura conceptual
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** “A malware infection is a type of security incident.” [p023]; “Disaster recovery is the process of restoring technology services…” [p024]
- **Archivo y JSON Pointer:** `observed_p023_p024_07_concept_extraction.json`, `/concepts`
- **Evaluación razonada:** se extraen `malware infection` y otros sujetos, pero faltan candidatos explícitos como `security incident`, `social engineering incident`, `malware incident`, `availability incident`, `process` y `technology services`. En p023 esta omisión afecta precisamente a los extremos superiores de casi todas las taxonomías.
- **Impacto downstream:** deja a relation_extraction sin referencias para los objetos taxonómicos y favorece relaciones truncadas con objeto literal `type`. El paso 10 corrige después gran parte de esta pérdida mediante claims completos.

### Q-infosec_p023_p024-09-1 — Referencias cruzadas incompatibles con el texto de la propia relación

- **Severidad:** CRÍTICA
- **Tipo:** precisión referencial y coherencia estructural
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** “A denial-of-service attack is a type of availability incident.” [p023]
- **Archivo y JSON Pointer:** `observed_p023_p024_09_relation_extraction.json`, `/relations/10/subject_ref` y `/relations/10/subject_text`
- **Evaluación razonada:** la relación de la oración de denial-of-service usa como `subject_ref` el concepto de `phishing attack`, mientras el texto de sujeto queda reducido a `attack`. De forma análoga, `/relations/4/subject_ref` usa el concepto de `lost device incident` para una relación de la oración de data breach. Son referencias a conceptos de otras oraciones, no interpretaciones alternativas del párrafo.
- **Impacto downstream:** si se proyectaran directamente, fusionarían clases distintas y contaminarían taxonomía y RDF. Canonical claims en 10 las reemplaza por referencias semánticas correctas, por lo que se consideran ERROR_CORREGIDO a partir de esa etapa.

### Q-infosec_p023_p024-09-2 — Relación contradicha entre RPO y el tiempo de restauración

- **Severidad:** CRÍTICA
- **Tipo:** contenido no soportado/contradicho
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** “A recovery time objective defines the maximum acceptable time to restore a service. A recovery point objective defines the maximum acceptable amount of data loss measured in time.” [p024]
- **Archivo y JSON Pointer:** `observed_p023_p024_09_relation_extraction.json`, `/relations/9`
- **Evaluación razonada:** la relación asigna el concepto referenciado de `RecoveryPointObjective` al objeto `maximum acceptable time` dentro de la oración de RTO. Esta interpretación es **CONTRADICHA** por la siguiente oración, que reserva para RPO la cantidad aceptable de pérdida de datos.
- **Impacto downstream:** sería la principal invención semántica del pipeline intermedio. El paso 10 la elimina y genera por separado el claim correcto de RTO y el de RPO; no llega al output final.

### Q-infosec_p023_p024-09-3 — Las taxonomías se degradan a relaciones `be → type` y se pierden propiedades explícitas

- **Severidad:** ALTA
- **Tipo:** cobertura y fidelidad relacional
- **Atribución:** ERROR_AMPLIFICADO
- **Cita literal:** “A ransomware attack is a type of malware incident.” [p023]; “A disaster recovery test verifies whether recovery procedures work as expected.” [p024]
- **Archivo y JSON Pointer:** `observed_p023_p024_09_relation_extraction.json`, `/relations/2` y `/relations`
- **Evaluación razonada:** en vez de relacionar `ransomware attack` con `malware incident`, `/relations/2` produce `be` con objeto `type` y sin `object_ref`. El mismo patrón afecta las oraciones taxonómicas. Además, no aparecen relaciones para `caused by`, `during`, `after`, el tercer elemento de BIA, varios elementos de backup policy ni la proposición modal del recovery test. Parte del defecto amplifica la omisión conceptual de 07, pero la selección de `type` como objeto y la pérdida de patrones explícitos son propias de 09.
- **Impacto downstream:** el artifact relacional no puede servir por sí solo como base fiel de triples. El paso 10 actúa como reparación semántica y recupera las 31 unidades de claim necesarias.

### Q-infosec_p023_p024-12-1 — Los identificadores de términos se sustituyen de forma inconsistente por identificadores de claim

- **Severidad:** MEDIA
- **Tipo:** identidad y trazabilidad estructural
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** “A business impact analysis identifies critical processes, dependencies, and recovery priorities.” [p024]
- **Archivo y JSON Pointer:** `observed_p023_p024_12_triple_extraction.json`, `/triples/0/subject_ref`, `/triples/1/subject_ref` y `/triples/2/subject_ref`
- **Evaluación razonada:** los tres triples tienen el mismo sujeto léxico `business impact analysis`, pero cada `subject_ref` es el ID de su claim distinto. En otros triples, sujeto, predicado y objeto llegan incluso a compartir el mismo claim ID. Los SPO y sus evidencias son fieles, pero los referentes no mantienen una identidad canónica uniforme.
- **Impacto downstream:** dificulta agrupar relaciones del mismo concepto y verificar identidad entre triples. Taxonomy induction propaga este esquema de refs; output_generation lo corrige en la práctica al reconstruir IRIs léxicas estables.

### Q-infosec_p023_p024-13-1 — Una taxonomía ambigua se promueve a directa y aumenta artificialmente su confianza

- **Severidad:** ALTA
- **Tipo:** precisión, modalidad y preservación de alcance
- **Atribución:** ERROR_AMPLIFICADO
- **Cita literal:** “A lost device incident is a type of physical and information security incident.” [p023]
- **Archivo y JSON Pointer:** `observed_p023_p024_13_taxonomy_induction.json`, `/taxonomy_relations/1`
- **Evaluación razonada:** el claim previo conserva `ambiguous_coordination`, `rdf_projection: qualified_statement` y confianza 0.65. Taxonomy induction lo convierte en `subclass_of` directo, eleva la confianza a 0.95 y elimina los marcadores de ambigüedad, mientras `/conditional_taxonomy_relations` queda vacío. La etapa amplifica una incertidumbre correctamente preservada por 10–12.
- **Impacto downstream:** podría materializar un axioma OWL más fuerte que el texto. El paso 16 corrige este error: no incluye el vínculo en `subclass_facts` y lo mantiene en `/output/graph/scoped_relations/5`.

### Q-infosec_p023_p024-15-1 — El control de calidad no detecta los defectos de identidad ni la promoción taxonómica

- **Severidad:** ALTA
- **Tipo:** cobertura de control semántico
- **Atribución:** ERROR_PROPAGADO
- **Cita literal:** “A business impact analysis identifies…” [p024] y “physical and information security incident” [p023]
- **Archivo y JSON Pointer:** `observed_p023_p024_15_semantic_quality.json`, `/semantic_quality_report/semantic_integrity_checks/claim_term_references_distinct`, `/semantic_quality_report/semantic_integrity_issues` y `/semantic_quality_report/rdf_readiness`
- **Evaluación razonada:** el reporte declara `claim_term_references_distinct: true`, no registra issues y marca RDF readiness, aunque 12 fragmenta la identidad del mismo sujeto entre claim IDs y 13 promovió el supertipo ambiguo. Sí detecta correctamente las dos ambigüedades originales, pero no comprueba su tratamiento en taxonomy induction.
- **Impacto downstream:** no crea otro error semántico; deja pasar los ya documentados en Q-12-1 y Q-13-1. Output_generation aplica salvaguardas propias y corrige la promoción ambigua.

### Q-infosec_p023_p024-16-1 — El modelo final conserva los claims, pero duplica estructuras de esquema

- **Severidad:** MEDIA
- **Tipo:** duplicación y coherencia del output
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** “A business impact analysis identifies critical processes, dependencies, and recovery priorities.” [p024]
- **Archivo y JSON Pointer:** `observed_p023_p024_16_output_generation.json`, `/output/graph/classes` y `/output/graph/schema/classes`
- **Evaluación razonada:** ambos arrays de clases son idénticos; por ejemplo, la representación de `BusinessImpactAnalysis` aparece en `/output/graph/classes/6` y `/output/graph/schema/classes/6`. También coexisten vistas repetidas de uso de propiedades en `facts`, `object_property_facts`, `object_property_schema` y `schema/object_properties`. La proyección de los 31 claim IDs es completa y no contiene la falsa relación RPO–maximum acceptable time, pero el payload no cumple estrictamente el requisito de ausencia de duplicación.
- **Impacto downstream:** consumidores que no conozcan qué vista es autoritativa pueden contar dos veces clases o hechos observados. Es un defecto estructural final, no una nueva proposición de dominio.

## 4. Diagnóstico

- **Primera degradación:** el primer incumplimiento observable aparece en 05, donde todas las dependencias son `null`. La primera pérdida semántica sustantiva aparece en 07 al omitir supertipos y complementos definitorios explícitos.
- **Principal pérdida:** 09 pierde la mayor parte de las taxonomías completas y varias propiedades/qualifiers de p023–p024, sustituyendo algunas por `be → type`. Esta pérdida es intermedia: 10 la corrige de forma amplia y trazable.
- **Principal contenido no soportado:** en 09 se vincula RecoveryPointObjective con `maximum acceptable time`, interpretación **CONTRADICHA** por p024. Se elimina en 10 y no llega al output.
- **Errores que llegan a RDF/OWL:** no llega ninguna contradicción proposicional identificada. La promoción directa del tipo ambiguo de lost device en 13 es **ERROR_CORREGIDO** en 16 mediante una scoped relation. Sí llega la duplicación estructural de clases/esquema, y queda como incertidumbre de modelado —no como hecho explícito— la representación como clases RDF de términos genéricos como `Data`, `Retention` o `Protection`.
- **Aciertos:** 01–04 preservan exactamente texto, oraciones, offsets y tokens; 06 y 14 son conservadores ante la ausencia de individuos nombrados; 08 conserva una resolución relativa trazable; 10 reconstruye 31 claims, conserva disyunción, coordinación, finalidad, temporalidad, capacidad, interrogación y ambigüedad; 11 y 12 mantienen esos contenidos; 16 contabiliza los 31 claim IDs, separa hechos directos, alternativas y scoped relations, y evita materializar el supertipo ambiguo de lost device.
- **Incertidumbres:** la adjunción de “used for recovery” [p024], el antecedente semántico de “that” [p023], la estructura interna de “physical and information security incident” [p023] y la distributividad del sujeto coordinado [p024]. El conservadurismo de 10 y 16 ante estas lecturas es correcto y no se penaliza.

## 5. Veredicto

- **Calidad global:** **86/100**.
- **Output final:** **parcialmente fiel**. Es completo y proposicionalmente fiel, y corrige los errores semánticos intermedios más graves; no alcanza “fiel” bajo el criterio estricto solicitado porque duplica estructuras del modelo final y su trazabilidad RDF es en parte indirecta.
- **Tres correcciones prioritarias:**
  1. Extraer en 07 todos los supertipos y complementos definitorios explícitos, con spans y referencias canónicas propias.
  2. Restringir en 09 las referencias al contexto de la oración, resolver correctamente `type of`, coordinaciones, pasivas y complementos, y prohibir referencias cruzadas incompatibles como PhishingAttack/DenialOfServiceAttack o RPO/RTO.
  3. Mantener IDs canónicos de términos, confianza y scope desde 12 hasta 16; hacer que 15 valide taxonomy induction y publicar una sola vista autoritativa de clases, hechos y esquema sin duplicación.

Siguiente caso pendiente: infosec_p025_p026.
