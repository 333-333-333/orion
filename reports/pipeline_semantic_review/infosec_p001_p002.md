# Revisión semántica: infosec_p001_p002

## 1. Lectura independiente

### Resumen

Los dos párrafos definen la seguridad de la información, los activos de información y el modelo CIA. El primer párrafo caracteriza la seguridad de la información como disciplina orientada a proteger activos frente a amenazas y define qué condiciones puede satisfacer un activo de información; además enumera siete clases de activo. El segundo presenta como propósito de la disciplina preservar confidencialidad, integridad y disponibilidad, define esas tres propiedades y afirma que juntas forman la tríada CIA, un modelo fundacional para la seguridad de la información.

### Conceptos

- **Seguridad de la información**: disciplina y tema principal.
- **Activo de información** y **recurso**.
- **Valor para una organización**.
- **Información** y las operaciones de almacenarla, procesarla, transmitirla o representarla.
- **Amenazas internas y externas**.
- Clases de activo: **documento confidencial**, **base de datos corporativa**, **registro de cliente**, **repositorio de código fuente**, **archivo de configuración de sistema**, **archivo de respaldo** e **informe empresarial**.
- **Confidencialidad**, **integridad** y **disponibilidad** como propiedades de seguridad.
- **Entidad autorizada**, **modificación no autorizada**, **sistema** y condición de necesidad.
- **Tríada CIA** y **modelo fundacional**.

No aparecen individuos concretos, organizaciones nombradas ni instancias del mundo real. Los sintagmas anteriores designan clases o conceptos genéricos; “CIA triad” es el nombre de un modelo conceptual, no una instancia operativa descrita en el texto.

### Proposiciones con evidencia

Todas las proposiciones siguientes son **EXPLÍCITAS**, salvo indicación contraria:

1. La seguridad de la información es una disciplina. Evidencia: “**Information security is a discipline**”.
2. Esa disciplina está enfocada en proteger activos de información frente a amenazas internas y externas. Evidencia: “**focused on protecting information assets against internal and external threats**”. “Estar enfocada” expresa orientación, no garantiza que la protección se logre.
3. Un activo de información es un recurso. Evidencia: “**An information asset is any resource**”.
4. El recurso definido tiene valor para una organización. Evidencia: “**that has value for an organization**”.
5. El recurso definido almacena, procesa, transmite **o** representa información. Evidencia: “**stores, processes, transmits, or represents information**”. Es una sola condición disyuntiva; el texto no autoriza a convertirla en cuatro propiedades obligatorias simultáneas.
6. Un documento confidencial es un tipo de activo de información. Evidencia: “**A confidential document is a type of information asset**”.
7. Una base de datos corporativa es un tipo de activo de información. Evidencia: “**A corporate database is a type of information asset**”.
8. Un registro de cliente es un tipo de activo de información. Evidencia: “**A customer record is a type of information asset**”.
9. Un repositorio de código fuente es un tipo de activo de información. Evidencia: “**A source code repository is a type of information asset**”.
10. Un archivo de configuración de sistema es un tipo de activo de información. Evidencia: “**A system configuration file is a type of information asset**”.
11. Un archivo de respaldo es un tipo de activo de información. Evidencia: “**A backup archive is a type of information asset**”.
12. Un informe empresarial es un tipo de activo de información. Evidencia: “**A business report is a type of information asset**”.
13. El propósito de la seguridad de la información es preservar confidencialidad, integridad y disponibilidad. Evidencia: “**The purpose of information security is to preserve confidentiality, integrity, and availability**”. Es una finalidad, no la afirmación factual de que siempre las preserve.
14. La confidencialidad es una propiedad de seguridad. Evidencia: “**Confidentiality is a security property**”.
15. La confidencialidad asegura que la información sea accesible solo para entidades autorizadas. Evidencia: “**ensures information is accessible only to authorized entities**”.
16. La integridad es una propiedad de seguridad. Evidencia: “**Integrity is a security property**”.
17. La integridad asegura que la información sea exacta. Evidencia: “**ensures information is accurate**”.
18. La integridad asegura que la información sea completa. Evidencia: “**information is accurate, complete**”.
19. La integridad asegura que la información esté protegida frente a modificación no autorizada. Evidencia: “**protected against unauthorized modification**”.
20. La disponibilidad es una propiedad de seguridad. Evidencia: “**Availability is a security property**”.
21. La disponibilidad asegura que la información y los sistemas sean accesibles cuando se necesiten. Evidencia: “**ensures information and systems are accessible when needed**”.
22. Confidencialidad, integridad y disponibilidad forman la tríada CIA. Evidencia: “**Confidentiality, integrity, and availability form the CIA triad**”.
23. La tríada CIA es un modelo fundacional para la seguridad de la información. Evidencia: “**The CIA triad is a foundational model for information security**”.

### Taxonomías explícitas

- `InformationSecurity` es una clase de `Discipline`.
- `InformationAsset` es una clase de `Resource`.
- `ConfidentialDocument`, `CorporateDatabase`, `CustomerRecord`, `SourceCodeRepository`, `SystemConfigurationFile`, `BackupArchive` y `BusinessReport` son clases de `InformationAsset`.
- `Confidentiality`, `Integrity` y `Availability` son clases de `SecurityProperty`.
- `CIATriad` es una clase de `FoundationalModel`.

“Internal threats” y “external threats” permite **ENTRAÑAR** categorías de amenaza calificadas como internas y externas, pero el texto no contiene una fórmula taxonómica explícita del tipo “InternalThreat is a type of Threat”.

### Modalidad

- **Finalidad/teleología**: “purpose ... is to preserve”. No equivale a cumplimiento efectivo.
- **Orientación**: “focused on protecting”. No equivale a una garantía de protección.
- **Disyunción**: “stores, processes, transmits, **or** represents”. No debe proyectarse como conjunción.
- **Exclusividad**: “accessible **only** to authorized entities”. El alcance de “only” es esencial.
- **Condición temporal/contextual**: “accessible **when needed**”.
- **Aserción definitoria fuerte**: “ensures” caracteriza lo que garantiza cada propiedad según el texto.
- No hay obligación, recomendación ni prohibición de un actor.

### Referencias y correferencias

- Los dos “that” de la definición de activo remiten inequívocamente a “resource” y, por la definición copular, al activo de información caracterizado.
- En las tres definiciones de propiedades, “that” modifica inequívocamente “security property”; semánticamente introduce la característica de confidencialidad, integridad o disponibilidad, respectivamente.
- No hay pronombres personales ni referencias interoracionales ambiguas.

### Ambigüedades

- No se especifica si el “or” de las cuatro operaciones es inclusivo o exclusivo; sí es inequívoco que no es una conjunción de cuatro requisitos.
- “Internal” y “external” pueden modelarse como clases de amenaza o como calificadores, sin que el texto fuerce una de esas dos representaciones.
- “When needed” no identifica quién determina la necesidad ni el contexto temporal.
- “Authorized entities” no especifica el mecanismo ni la autoridad que concede autorización.
- “Model for information security” no define una semántica formal de la relación `models`.

## 2. Resultado inicial por etapa

| Paso | Etapa | Fidelidad | Cobertura | Precisión | Trazabilidad | Coherencia | Estado |
|------|-------|-----------|-----------|-----------|--------------|------------|--------|
| 01 | input_intake | 4 | 4 | 4 | 3 | 4 | OK |
| 02 | preprocessing | 4 | 4 | 4 | 4 | 4 | OK |
| 03 | sentence_segmentation | 4 | 4 | 4 | 4 | 4 | OK |
| 04 | tokenization | 4 | 4 | 4 | 4 | 4 | OK |
| 05 | linguistic_annotation | 3 | 4 | 2 | 4 | 3 | WARN |
| 06 | entity_extraction | 4 | 4 | 4 | 4 | 4 | OK |
| 07 | concept_extraction | 2 | 3 | 1 | 4 | 2 | FAIL |
| 08 | coreference_resolution | 3 | 1 | 4 | 4 | 2 | FAIL |
| 09 | relation_extraction | 1 | 1 | 1 | 3 | 1 | FAIL |
| 10 | canonical_claims / semantic_claims | 2 | 4 | 2 | 4 | 3 | WARN |
| 11 | semantic_debug_ir | N/A | N/A | N/A | N/A | N/A | N/A |
| 12 | triple_extraction | 1 | 1 | 1 | 3 | 1 | FAIL |
| 13 | taxonomy_induction | 2 | 3 | 2 | 4 | 2 | FAIL |
| 14 | type_assertion | 4 | 4 | 4 | 4 | 4 | OK |
| 15 | semantic_quality | 3 | 3 | 3 | 4 | 3 | WARN |
| 16 | output_generation | 2 | 2 | 2 | 3 | 3 | FAIL |

Observaciones de atribución global:

- Los pasos 01–04 preservan texto, fronteras, puntuación y offsets.
- El paso 05 introduce el primer error lingüístico relevante.
- El paso 10 corrige gran parte del ruido de relaciones del paso 09, pero introduce errores propios de modalidad y disyunción.
- El paso 12 vuelve a usar las relaciones defectuosas y no los claims corregidos, amplificando el problema.
- El paso 15 detecta correctamente la desconexión total entre claims y triples.
- El paso 16 vuelve a partir de `canonical_claims` y, por ello, corrige mucho del ruido de los pasos 12–13; no obstante, conserva o amplifica varias distorsiones de los claims y excluye hechos válidos.

## 3. Hallazgos

### Q-infosec_p001_p002-05-1
- Severidad: alta
- Tipo: distorsión
- Atribución: ERROR_ORIGEN
- Evidencia del texto: “**that stores, processes, transmits, or represents information**”.
- Evidencia del output: `observed_p001_p002_05_linguistic_annotation.json`, `/tokens/30`, `/tokens/32`, `/tokens/34` y `/tokens/37`.
- Evaluación razonada: `stores` y `processes` son verbos coordinados con `transmits` y `represents`. El output etiqueta `stores` como `NOUN/NNS` y `nsubj`, y `processes` como `NOUN/NNS` y `appos`; solo `transmits` y `represents` quedan como verbos. Además, el segundo “that” queda como `mark` de `transmits`, en lugar de sujeto relativo del grupo coordinado. La anotación contradice la estructura sintáctica explícita.
- Impacto downstream: origina los conceptos espurios `stores` y `processes`, impide reconstruir correctamente la disyunción y contribuye a relaciones con sujetos y predicados invertidos.

### Q-infosec_p001_p002-05-2
- Severidad: media
- Tipo: distorsión
- Atribución: ERROR_ORIGEN
- Evidencia del texto: “**Confidentiality is a security property that ensures information is accessible only to authorized entities**”.
- Evidencia del output: `observed_p001_p002_05_linguistic_annotation.json`, `/tokens/134`–`/tokens/140`.
- Evaluación razonada: `information` se anota como objeto directo de `ensures` y el segundo `is` como coordinación de la cópula principal. La lectura correcta es una completiva: la propiedad asegura que **information is accessible**. La estructura observada separa el paciente de su propiedad y debilita el alcance de `only to authorized entities`.
- Impacto downstream: facilita relaciones falsas como `information authorize authorized entity` y pierde quién es accesible y bajo qué restricción.

### Q-infosec_p001_p002-07-1
- Severidad: alta
- Tipo: granularidad
- Atribución: ERROR_AMPLIFICADO
- Evidencia del texto: “**Information security is a discipline focused on protecting information assets against internal and external threats**”.
- Evidencia del output: `observed_p001_p002_07_concept_extraction.json`, `/concepts/1`, `/concepts/2`, `/concepts/3`, `/concepts/29` y `/concepts/30`.
- Evaluación razonada: se proponen como conceptos `a discipline focused`, `discipline focused` y `protecting information assets`. Los dos primeros son duplicados solapados y fragmentos que incorporan un participio; el tercero convierte una acción con su objeto en concepto. `a foundational model` y `foundational model` también se duplican. No se obtiene un candidato limpio `Discipline` en la primera oración.
- Impacto downstream: produce nodos artificiales como `discipline focused` y permite jerarquías mal formadas, incluida `InformationSecurity subclass_of discipline focused`.

### Q-infosec_p001_p002-07-2
- Severidad: media
- Tipo: granularidad
- Atribución: ERROR_AMPLIFICADO
- Evidencia del texto: “**An information asset is any resource that has value for an organization and that stores, processes, transmits, or represents information**”.
- Evidencia del output: `observed_p001_p002_07_concept_extraction.json`, `/concepts/5`–`/concepts/11`, `/concepts/31`–`/concepts/33` y `/concepts/43`–`/concepts/44`.
- Evaluación razonada: la etapa duplica `information asset`, `resource` y `organization`, promueve los verbos `stores`, `processes` y `transmits` a conceptos y crea `represents information` como concepto verbal. Esto mezcla participantes, predicados y frases completas sin una granularidad ontológica estable.
- Impacto downstream: la extracción de relaciones selecciona estos candidatos como sujetos u objetos y crea relaciones no soportadas.

### Q-infosec_p001_p002-08-1
- Severidad: alta
- Tipo: correferencia
- Atribución: ERROR_ORIGEN
- Evidencia del texto: “**any resource that has value for an organization and that stores, processes, transmits, or represents information**”.
- Evidencia del output: `observed_p001_p002_08_coreference_resolution.json`, `/coreferences/0` y `/coreferences/1`.
- Evaluación razonada: ambos relativos se marcan `unresolved` con `no_antecedent_for_that`, aunque su antecedente gramatical explícito es `resource`. La resolución conservadora sería apropiada ante ambigüedad real, pero aquí no la hay.
- Impacto downstream: aparecen relaciones cuyo sujeto literal es `that`, y las propiedades de valor y operación no se atribuyen al recurso/activo.

### Q-infosec_p001_p002-08-2
- Severidad: media
- Tipo: correferencia
- Atribución: ERROR_ORIGEN
- Evidencia del texto: “**Confidentiality is a security property that ensures**”, “**Integrity is a security property that ensures**” y “**Availability is a security property that ensures**”.
- Evidencia del output: `observed_p001_p002_08_coreference_resolution.json`, `/coreferences/2`, `/coreferences/3` y `/coreferences/4`.
- Evaluación razonada: los tres relativos tienen el antecedente local explícito `security property`, caracterizado en cada oración por el sujeto copular. Marcar los tres como carentes de antecedente omite una referencia inequívoca.
- Impacto downstream: la relación `ensures` queda sin el sujeto semántico correcto o se sustituye por relaciones parciales basadas en proximidad.

### Q-infosec_p001_p002-09-1
- Severidad: crítica
- Tipo: distorsión
- Atribución: ERROR_AMPLIFICADO
- Evidencia del texto: “**A corporate database is a type of information asset**”.
- Evidencia del output: `observed_p001_p002_09_relation_extraction.json`, `/relations/2`, `/relations/3` y `/relations/4`.
- Evaluación razonada: la relación explícita debería ser `corporate database —type_of→ information asset`. El output produce `type —information→ asset`, `database —type→ information` y `database —be→ type`. Se pierde el objeto compuesto `information asset` y se materializan palabras funcionales como nodos semánticos.
- Impacto downstream: los triples heredan `corporate database type information` y la taxonomía induce tanto la jerarquía válida por otra ruta como la falsa `database subclass_of type`.

### Q-infosec_p001_p002-09-2
- Severidad: crítica
- Tipo: alucinación
- Atribución: ERROR_AMPLIFICADO
- Evidencia del texto: “**resource that has value for an organization and that stores, processes, transmits, or represents information**”.
- Evidencia del output: `observed_p001_p002_09_relation_extraction.json`, `/relations/9`–`/relations/13`.
- Evaluación razonada: relaciones como `value —organization→ store`, `asset —resource→ value`, `store —represent→ information` y `that —have→ value` no expresan ninguna proposición del texto. Al mismo tiempo, faltan la atribución correcta de valor al recurso y la estructura disyuntiva de las cuatro operaciones.
- Impacto downstream: el paso 12 convierte todas estas relaciones en triples con alta confianza; la señal de confianza no refleja su invalidez semántica.

### Q-infosec_p001_p002-10-1
- Severidad: alta
- Tipo: distorsión
- Atribución: ERROR_ORIGEN
- Evidencia del texto: “**stores, processes, transmits, or represents information**”.
- Evidencia del output: `observed_p001_p002_10_canonical_claims.json`, `/canonical_claims/claims/6`–`/canonical_claims/claims/9`.
- Evaluación razonada: los claims convierten una condición con `or` en cuatro afirmaciones independientes e incondicionales: todo `InformationAsset` almacena, procesa, transmite y representa información. Esa conjunción es más fuerte que el texto. Una proyección fiel debe conservar la disyunción o marcar cada alternativa como posibilidad, no como hecho universal separado.
- Impacto downstream: las cuatro afirmaciones llegan como hechos y restricciones RDF en el paso 16.

### Q-infosec_p001_p002-10-2
- Severidad: alta
- Tipo: distorsión
- Atribución: ERROR_ORIGEN
- Evidencia del texto: “**The purpose of information security is to preserve confidentiality, integrity, and availability**”.
- Evidencia del output: `observed_p001_p002_10_canonical_claims.json`, `/canonical_claims/claims/17`–`/canonical_claims/claims/19`.
- Evaluación razonada: `InformationSecurity preserves ...` elimina la modalidad teleológica “the purpose ... is to”. El texto declara un objetivo de la disciplina; no asegura que la preservación ocurra de hecho. Los claims son atómicos y trazables, pero su modalidad es incorrecta.
- Impacto downstream: el RDF presenta una relación factual `preserves`, sin indicador de propósito o finalidad.

### Q-infosec_p001_p002-10-3
- Severidad: alta
- Tipo: distorsión
- Atribución: ERROR_ORIGEN
- Evidencia del texto: “**focused on protecting information assets against internal and external threats**”.
- Evidencia del output: `observed_p001_p002_10_canonical_claims.json`, `/canonical_claims/claims/1`–`/canonical_claims/claims/3`.
- Evaluación razonada: el claim `focused_on_protecting InformationAsset` conserva parte de la orientación, pero los dos claims `InformationSecurity protects against InternalThreat/ExternalThreat` convierten el complemento de la actividad focal en protección efectiva y omiten el paciente `InformationAsset`.
- Impacto downstream: el paso 16 materializa `protects` y `protectsAgainst` como hechos de clase, perdiendo el matiz “focused on”.

### Q-infosec_p001_p002-10-4
- Severidad: alta
- Tipo: granularidad
- Atribución: ERROR_ORIGEN
- Evidencia del texto: “**Confidentiality, integrity, and availability form the CIA triad**”.
- Evidencia del output: `observed_p001_p002_10_canonical_claims.json`, `/canonical_claims/claims/29`.
- Evaluación razonada: aunque el campo `members` conserva los tres miembros, el sujeto del claim normalizado es `SecurityProperty`. El texto no afirma que la clase genérica de todas las propiedades de seguridad forme la tríada; afirma que la forman exactamente tres propiedades nombradas.
- Impacto downstream: el output final materializa `SecurityProperty —forms→ CIATriad`, ampliando el sujeto más allá de la evidencia.

### Q-infosec_p001_p002-12-1
- Severidad: crítica
- Tipo: proyección
- Atribución: ERROR_AMPLIFICADO
- Evidencia del texto: “**A corporate database is a type of information asset**” y “**An information asset is any resource that has value for an organization**”.
- Evidencia del output: `observed_p001_p002_12_triple_extraction.json`, `/triples/2`–`/triples/4` y `/triples/8`–`/triples/13`.
- Evaluación razonada: existiendo 32 claims canónicos, la etapa emite 54 triples derivados de las relaciones defectuosas. Reaparecen `corporate database —type→ information`, `type —information→ protect information asset`, `that —have→ value` y `value —organization→ store`. Los triples llevan `relation_id`/`predicate_ref`, pero ningún `claim_id`.
- Impacto downstream: amplifica los errores del paso 09 y provoca la desconexión total `claims_without_triples:32` / `triples_without_claims:54`. Estos triples concretos no llegan al RDF porque el paso 16 vuelve a los claims canónicos.

### Q-infosec_p001_p002-13-1
- Severidad: alta
- Tipo: taxonomía
- Atribución: ERROR_AMPLIFICADO
- Evidencia del texto: “**A confidential document is a type of information asset**”, junto con las seis formulaciones análogas.
- Evidencia del output: `observed_p001_p002_13_taxonomy_induction.json`, `/taxonomy_relations/1`, `/taxonomy_relations/3`, `/taxonomy_relations/5`, `/taxonomy_relations/10`, `/taxonomy_relations/11`, `/taxonomy_relations/14` y `/taxonomy_relations/16`.
- Evaluación razonada: además de varias jerarquías válidas, se inducen `database`, `report`, `document`, `record`, `repository`, `file` y `archive` como subclases de `type`. “Type” es parte del patrón lingüístico “is a type of”, no la superclase semántica.
- Impacto downstream: contamina la taxonomía intermedia con siete clases superiores espurias. El paso 16 corrige este error al reconstruir la taxonomía desde claims canónicos.

### Q-infosec_p001_p002-13-2
- Severidad: media
- Tipo: omisión
- Atribución: ERROR_PROPAGADO
- Evidencia del texto: “**An information asset is any resource**” y “**The CIA triad is a foundational model**”.
- Evidencia del output: `observed_p001_p002_13_taxonomy_induction.json`, `/taxonomy_relations`.
- Evaluación razonada: no se inducen `InformationAsset subclass_of Resource` ni `CIATriad subclass_of FoundationalModel`, pese a ser relaciones copulares explícitas. La primera ya fue dañada en relaciones/triples; la segunda tampoco se recupera.
- Impacto downstream: el paso 16 recupera `InformationAsset subclass_of Resource`, pero no recupera `CIATriad subclass_of FoundationalModel`.

### Q-infosec_p001_p002-15-1
- Severidad: media
- Tipo: omisión
- Atribución: ERROR_PROPAGADO
- Evidencia del texto: “**focused on protecting information assets**” y “**stores, processes, transmits, or represents information**”.
- Evidencia del output: `observed_p001_p002_15_semantic_quality.json`, `/semantic_quality_report/concept_noise`, `/excluded_concepts`, `/semantic_quality_report/relation_gaps` y `/semantic_quality_report/rdf_readiness`.
- Evaluación razonada: la etapa acierta al declarar `rdf_readiness: false` y detectar todos los claims y triples desconectados. Sin embargo, declara `concept_noise: []` y no excluye conceptos pese a fragmentos como `discipline focused`, `protecting information assets`, `stores` y `processes`. Tampoco identifica semánticamente cuáles de los 54 triples no son proyectables; solo detecta su desconexión estructural.
- Impacto downstream: aporta una alerta global útil, pero no suministra exclusiones finas. El paso 16 genera RDF pese a la falta de readiness.

### Q-infosec_p001_p002-16-1
- Severidad: crítica
- Tipo: proyección
- Atribución: ERROR_PROPAGADO
- Evidencia del texto: “**stores, processes, transmits, or represents information**”.
- Evidencia del output: `observed_p001_p002_16_output_generation.json`, `/output/graph/facts/3`–`/output/graph/facts/6` y `/output/graph/restrictions/7`, `/output/graph/restrictions/10`–`/output/graph/restrictions/12`.
- Evaluación razonada: el grafo materializa las cuatro alternativas como cuatro hechos/restricciones simultáneos de `InformationAsset`. La disyunción del original desaparece por completo.
- Impacto downstream: el RDF/OWL afirma una caracterización más fuerte que la fuente y puede hacer inferencias falsas sobre cualquier clase de activo.

### Q-infosec_p001_p002-16-2
- Severidad: crítica
- Tipo: proyección
- Atribución: ERROR_AMPLIFICADO
- Evidencia del texto: “**The purpose of information security is to preserve confidentiality, integrity, and availability**”.
- Evidencia del output: `observed_p001_p002_16_output_generation.json`, `/output/graph/facts/7` y `/output/graph/projection/claim_dispositions/17`–`/output/graph/projection/claim_dispositions/19`.
- Evaluación razonada: el paso hereda la pérdida de modalidad del claim y además sustituye los tres objetos explícitos por la superclase `SecurityProperty`. Tres claims distintos se colapsan en `InformationSecurity —preserves→ SecurityProperty`; no queda ni la finalidad ni la enumeración CIA.
- Impacto downstream: el RDF amplía el alcance a cualquier propiedad de seguridad y pierde los tres objetivos concretos del texto.

### Q-infosec_p001_p002-16-3
- Severidad: alta
- Tipo: proyección
- Atribución: ERROR_ORIGEN
- Evidencia del texto: “**An information asset is any resource that has value for an organization**”.
- Evidencia del output: `observed_p001_p002_16_output_generation.json`, `/output/graph/facts/2` y `/output/graph/projection/claim_dispositions/5`.
- Evaluación razonada: el claim tenía como sujeto `InformationAsset`, pero la proyección lo transforma en `Resource —hasValueFor→ Organization`. El texto define que los recursos que son activos de información tienen valor; no afirma que todo recurso genérico lo tenga.
- Impacto downstream: la restricción se aplica a una superclase más amplia y genera una generalización no soportada.

### Q-infosec_p001_p002-16-4
- Severidad: alta
- Tipo: omisión
- Atribución: ERROR_ORIGEN
- Evidencia del texto: “**information is accurate, complete, and protected against unauthorized modification**” y “**information and systems are accessible when needed**”.
- Evidencia del output: `observed_p001_p002_16_output_generation.json`, `/output/graph/projection/claim_dispositions/24`, `/output/graph/projection/claim_dispositions/25` y `/output/graph/projection/claim_dispositions/27`.
- Evaluación razonada: se excluyen como no proyectables tres hechos explícitos y válidos: completitud, protección frente a modificación no autorizada y disponibilidad de la información. Se conserva exactitud y disponibilidad de sistemas, por lo que las definiciones quedan incompletas y asimétricas.
- Impacto downstream: el RDF reduce integridad a exactitud y reduce disponibilidad a sistemas, omitiendo partes centrales de ambas definiciones.

### Q-infosec_p001_p002-16-5
- Severidad: alta
- Tipo: omisión
- Atribución: ERROR_ORIGEN
- Evidencia del texto: “**The CIA triad is a foundational model for information security**”.
- Evidencia del output: `observed_p001_p002_16_output_generation.json`, `/output/graph/projection/claim_dispositions/30`, `/output/graph/classes` y `/output/graph/subclass_facts`.
- Evaluación razonada: el claim `CIATriad is a FoundationalModel` queda como `evidence_only`; no existe la clase `FoundationalModel` ni la jerarquía correspondiente. Sí se conserva `CIATriad —models→ InformationSecurity`, pero esa relación no sustituye la clasificación explícita.
- Impacto downstream: el modelo final pierde una definición taxonómica literal de la tríada CIA.

### Q-infosec_p001_p002-16-6
- Severidad: alta
- Tipo: distorsión
- Atribución: ERROR_AMPLIFICADO
- Evidencia del texto: “**ensures information is accessible only to authorized entities**”.
- Evidencia del output: `observed_p001_p002_16_output_generation.json`, `/output/graph/facts/8` y `/output/graph/restrictions/0`.
- Evaluación razonada: `Confidentiality —ensuresAccessibleTo→ AuthorizedEntity` omite el paciente `Information` y la exclusividad `only`. El resultado puede leerse como una relación directa entre confidencialidad y entidades autorizadas, no como la condición de acceso de la información.
- Impacto downstream: el RDF no puede distinguir acceso exclusivo de mero acceso ni identificar qué recurso es accesible.

### Q-infosec_p001_p002-16-7
- Severidad: alta
- Tipo: proyección
- Atribución: ERROR_PROPAGADO
- Evidencia del texto: “**Confidentiality, integrity, and availability form the CIA triad**”.
- Evidencia del output: `observed_p001_p002_16_output_generation.json`, `/output/graph/facts/11` y `/output/graph/restrictions/3`.
- Evaluación razonada: el grafo materializa `SecurityProperty —forms→ CIATriad`. La fuente restringe el sujeto a tres miembros explícitos; la superclase incluye potencialmente otras propiedades no mencionadas.
- Impacto downstream: cualquier consumidor puede inferir una relación genérica entre toda propiedad de seguridad y la tríada, contenido no soportado por el párrafo.

## 4. Diagnóstico inicial

- **Primera etapa donde se degrada el significado**: `05 linguistic_annotation`, al analizar `stores` y `processes` como sustantivos y romper la completiva de confidencialidad. Los pasos 01–04 son fieles.
- **Principal pérdida semántica**: la modalidad y el alcance lógico. Se pierde la disyunción `or`, la finalidad de `purpose`, la orientación de `focused on`, la exclusividad de `only` y partes explícitas de integridad y disponibilidad.
- **Principal contenido no soportado**: las generalizaciones de clase `Resource —hasValueFor→ Organization`, `SecurityProperty —preserves→ SecurityProperty` implícita por rango y, especialmente, `SecurityProperty —forms→ CIATriad`; también son no soportados los cuatro requisitos simultáneos para todo activo.
- **Errores que alcanzan el RDF/OWL**: las cuatro operaciones convertidas en conjunción; la preservación convertida de propósito en hecho y colapsada a `SecurityProperty`; el valor trasladado de `InformationAsset` a `Resource`; la formación de la tríada atribuida a toda `SecurityProperty`; la pérdida de `only` y del paciente `Information`; y las omisiones de completitud, modificación no autorizada, disponibilidad de información y `FoundationalModel`.
- **Errores que no alcanzan el RDF/OWL**: los triples léxicamente corruptos del paso 12 y las falsas subclases de `type` del paso 13 son corregidos por el paso 16, cuya proyección declara `source_stage: canonical_claims`.
- **Aspectos correctamente preservados**: texto y offsets completos; 15 oraciones correctas; tokenización íntegra; ausencia justificada de entidades nombradas e instancias; las siete subclases de activo; `InformationAsset subclass_of Resource`; las tres propiedades CIA como subclases de `SecurityProperty`; las clases de amenazas interna/externa; almacenamiento/procesamiento/transmisión/representación como vocabulario; relación de la tríada con seguridad de la información; y trazabilidad por claim y evidencia literal en buena parte del grafo.
- **Incertidumbres del auditor**: el texto no decide si “internal/external threats” deben ser clases o calificadores; tampoco define una formalización única de “model for”. Estas elecciones conservadoras no se penalizan por sí mismas. La crítica a las cuatro operaciones no presupone si `or` es inclusivo o exclusivo: solo observa que no equivale a cuatro afirmaciones universales simultáneas.

## 5. Veredicto inicial

- **Calidad global inicial: 56/100**
- **Output final inicial: parcialmente fiel**
- **Tres correcciones prioritarias iniciales**:
  1. Hacer que triples, taxonomía y RDF se proyecten de los claims canónicos con identidad de claim, conservando modalidad, disyunción, participantes y alcance; no volver a las relaciones ruidosas.
  2. Representar explícitamente `purpose`, `focused on`, `or`, `only` y `when needed`, evitando transformar finalidades o alternativas en hechos universales.
  3. Eliminar generalizaciones de superclase no soportadas y proyectar todos los hechos explícitos válidos: completitud, protección contra modificación no autorizada, disponibilidad de información y `CIATriad subclass_of FoundationalModel`.

## 6. Iteración de corrección

### Cambios aplicados

1. `triple_extraction` consume ahora `semantic_claims` o `canonical_claims`, conserva `claim_id`, evidencia, modalidad, paciente, condición, cuantificador y coordinación, y solo usa relaciones si no hay claims.
2. Los claims de p001–p002 conservan:
   - finalidad mediante `has_purpose_to_preserve` y `modality: purpose`;
   - orientación mediante `focused_on_protecting` / `focused_on_protecting_against`;
   - disyunción mediante un `alternative_group` con `coordination: or`;
   - exclusividad mediante `ensures_accessible_only_to`, `patient: Information` y `quantifier: only`;
   - condición mediante `condition: when_needed`;
   - composición de la tríada mediante tres relaciones `CIATriad has_member ...`.
3. `taxonomy_induction` deriva las jerarquías de claims canónicos. Desaparecen las siete falsas subclases de `type` y se recuperan `InformationAsset → Resource` y `CIATriad → FoundationalModel`.
4. La proyección RDF deja de elevar `hasValueFor` a `Resource`, no colapsa los tres objetivos CIA a `SecurityProperty`, conserva objetos concretos y materializa completitud, modificación no autorizada y disponibilidad de información.
5. Las cuatro operaciones alternativas ya no se publican como cuatro hechos simultáneos: aparecen en `/output/graph/logical_alternatives/0` bajo `operator: or`.
6. La resolución de relativos sigue la cadena de dependencias y resuelve los cinco `that` a `resource` o `security property` con trazabilidad.
7. `concept_extraction` elimina los principales fragmentos con límites verbales y `semantic_quality` verifica la identidad claim–triple y la readiness RDF.

### Resultado final por etapa

| Paso | Etapa | Fidelidad | Cobertura | Precisión | Trazabilidad | Coherencia | Estado |
|------|-------|-----------|-----------|-----------|--------------|------------|--------|
| 01 | input_intake | 4 | 4 | 4 | 3 | 4 | OK |
| 02 | preprocessing | 4 | 4 | 4 | 4 | 4 | OK |
| 03 | sentence_segmentation | 4 | 4 | 4 | 4 | 4 | OK |
| 04 | tokenization | 4 | 4 | 4 | 4 | 4 | OK |
| 05 | linguistic_annotation | 3 | 4 | 2 | 4 | 3 | WARN |
| 06 | entity_extraction | 4 | 4 | 4 | 4 | 4 | OK |
| 07 | concept_extraction | 3 | 3 | 3 | 4 | 3 | WARN |
| 08 | coreference_resolution | 4 | 4 | 4 | 4 | 4 | OK |
| 09 | relation_extraction | 2 | 2 | 2 | 3 | 2 | FAIL |
| 10 | canonical_claims / semantic_claims | 4 | 4 | 4 | 4 | 4 | OK |
| 11 | semantic_debug_ir | N/A | N/A | N/A | N/A | N/A | N/A |
| 12 | triple_extraction | 4 | 4 | 4 | 4 | 4 | OK |
| 13 | taxonomy_induction | 4 | 4 | 4 | 4 | 4 | OK |
| 14 | type_assertion | 4 | 4 | 4 | 4 | 4 | OK |
| 15 | semantic_quality | 3 | 3 | 3 | 4 | 3 | WARN |
| 16 | output_generation | 4 | 3 | 4 | 4 | 3 | WARN |

### Evidencia de mejora

- `/triples` contiene 34 triples y cada `relation_id` corresponde a un claim; no quedan claims sin triple ni triples ajenos a claims.
- `/semantic_quality_report/relation_gaps` está vacío y `/semantic_quality_report/rdf_readiness` es `true`.
- `/taxonomy_relations` contiene 13 taxonomías canónicas, todas justificadas por una definición literal.
- `/output/graph/facts` conserva finalidad, foco, miembros CIA, completitud, paciente, exclusividad y condición.
- `/output/graph/subclass_facts` incluye las 15 jerarquías justificadas, incluidas amenazas calificadas y `FoundationalModel`.
- `/output/graph/logical_alternatives/0/alternatives` conserva exactamente `stores`, `processes`, `transmits` y `represents` bajo un único `or`.

### Estado de los hallazgos iniciales

- **Resueltos**: Q-08-1, Q-08-2, Q-10-1 a Q-10-4, Q-12-1, Q-13-1, Q-13-2 y Q-16-2 a Q-16-7.
- **Parcialmente resueltos**: Q-05-1, Q-05-2, Q-07-1, Q-07-2, Q-09-1, Q-09-2, Q-15-1 y Q-16-1.
- **Riesgo residual principal**: `stores` y `processes` aún aparecen como conceptos por el análisis POS observado, la extracción intermedia de relaciones continúa siendo ruidosa y el contenedor de alternativas está explícito en el modelo de grafo, pero su serialización RDF estándar aún no expresa toda la lógica disyuntiva ni todos los calificadores del sidecar.

### Veredicto tras la iteración

- **Calidad global final: 86/100**
- **Output final: parcialmente fiel, sin las distorsiones críticas iniciales**
- **Umbral solicitado: alcanzado (≥80/100)**
- **Correcciones siguientes, no bloqueantes**:
  1. Sustituir la heurística de relaciones por extracción coordinada basada en dependencias/roles.
  2. Serializar `logical_alternatives` y calificadores como estructuras RDF reificadas o axiomas OWL.
  3. Hacer coincidir plenamente la limpieza de conceptos observada en runtime con los artifacts incrementales por etapa.

Siguiente caso pendiente: `infosec_p003_p004`.
