# Revisión semántica: infosec_p031_p032

## 1. Lectura independiente

### Resumen

Los dos párrafos presentan descripciones genéricas, no casos individuales:

- **p031** describe la gestión del ciclo de vida de la información y varias operaciones sobre la información, desde su creación hasta su eliminación, incluyendo clasificación y reglas de manejo.
- **p032** describe la gestión de cambios, tres clases de cambio, una violación de control y funciones de solicitud, aprobación, prueba y reversión.

No aparecen nombres propios, organizaciones, productos ni individuos identificados. Los sintagmas con artículo indefinido —«a repository», «another party», «a change», «a modification», «a previous state»— son menciones genéricas; modelarlos como instancias concretas sería **NO SOPORTADO**.

### Conceptos

- **p031:** Data lifecycle management, information, creation, disposal, data creation, new information, data storage, repository, data processing, data transmission, systems, people, data sharing, party, data archival, long-term retention, retention, secure deletion, recovery of disposed data, data classification, labels, data handling rules y classification level.
- **p032:** Change management, modification, systems, applications, infrastructure, configurations, change request, standard change, pre-approved low-risk change, normal change, change, assessment, approval, emergency change, urgent issues, change approval, acceptability of a change, change testing, working as intended, change rollback, previous state, failed change, unauthorized change, control violation, poor change management y vulnerabilities.
- **Entidades/instancias explícitas:** ninguna. Todos los referentes son tipos, actividades, estados, resultados o participantes genéricos.
- **Definiciones funcionales explícitas:** las oraciones de p031 describen qué hace cada actividad; p032 define expresamente con «is a type of» a StandardChange, NormalChange, EmergencyChange y UnauthorizedChange.

### Proposiciones con evidencia

1. **EXPLÍCITO [p031]:** la gestión del ciclo de vida protege información durante el intervalo indicado: «protects information from creation to disposal».
2. **EXPLÍCITO [p031]:** la creación de datos produce información nueva: «Data creation produces new information».
3. **EXPLÍCITO [p031]:** el almacenamiento conserva información en un repositorio: «keeps information in a repository».
4. **EXPLÍCITO [p031]:** el procesamiento transforma **o** usa información: «transforms or uses information». La proposición literal es disyuntiva; afirmar ambas ramas conjuntamente es **NO SOPORTADO**.
5. **EXPLÍCITO [p031]:** la transmisión mueve información entre sistemas **o** personas: «moves information between systems or people». La coordinación debe conservarse.
6. **EXPLÍCITO [p031]:** compartir datos proporciona información a otra parte: «provides information to another party».
7. **EXPLÍCITO [p031]:** el archivado almacena información con finalidad de retención a largo plazo: «stores information for long-term retention».
8. **EXPLÍCITO [p031]:** la eliminación retira información bajo la condición temporal «when retention expires».
9. **EXPLÍCITO [p031]:** la eliminación segura impide «recovery of disposed data».
10. **EXPLÍCITO [p031]:** la clasificación aplica etiquetas a información: «applies labels to information».
11. **EXPLÍCITO [p031]:** las reglas de manejo definen cómo debe protegerse cada nivel: «each classification level must be protected».
12. **EXPLÍCITO [p032]:** la gestión de cambios controla modificaciones «to systems, applications, infrastructure, and configurations».
13. **EXPLÍCITO [p032]:** una solicitud de cambio propone una modificación: «A change request proposes a modification».
14. **EXPLÍCITO [p032]:** StandardChange es un tipo de PreApprovedLowRiskChange: «a type of pre-approved low-risk change».
15. **EXPLÍCITO [p032]:** NormalChange es un tipo de Change y requiere Assessment y Approval: «a type of change that requires assessment and approval».
16. **EXPLÍCITO [p032]:** EmergencyChange es un tipo de Change implementado rápidamente con la finalidad de resolver problemas urgentes: «implemented rapidly to resolve urgent issues».
17. **EXPLÍCITO [p032]:** ChangeApproval verifica que un cambio sea aceptable: «verifies that a change is acceptable».
18. **EXPLÍCITO [p032]:** ChangeTesting verifica que un cambio funcione según lo previsto: «verifies that a change works as intended».
19. **EXPLÍCITO [p032]:** ChangeRollback restaura un estado anterior bajo la condición «if a change fails».
20. **EXPLÍCITO [p032]:** UnauthorizedChange es un tipo de ControlViolation: «is a type of control violation».
21. **EXPLÍCITO [p032]:** PoorChangeManagement puede introducir vulnerabilidades: «can introduce vulnerabilities»; no es una afirmación categórica de que siempre las introduzca.

Interpretaciones derivadas controladas:

- **ENTRAÑADO [p032]:** las modificaciones controladas tienen como objetivos los cuatro elementos coordinados, porque el texto dice «modifications to systems, applications, infrastructure, and configurations».
- **ENTRAÑADO [p032]:** NormalChange y EmergencyChange son subclases de Change; StandardChange lo es de PreApprovedLowRiskChange; UnauthorizedChange lo es de ControlViolation.
- **PLAUSIBLE, no explícito [p032]:** identificar el sustantivo aislado «approval» de la oración de NormalChange con el concepto posterior completo ChangeApproval.
- **NO SOPORTADO [p031]:** interpretar «from creation to disposal» como que la gestión protege *contra* Creation o *contra* Disposal.
- **CONTRADICHO por la modalidad [p032]:** convertir «can introduce vulnerabilities» en «introduces vulnerabilities» sin posibilidad.

### Taxonomías explícitas

- **EXPLÍCITO [p032]:** StandardChange `subclass_of` PreApprovedLowRiskChange.
- **EXPLÍCITO [p032]:** NormalChange `subclass_of` Change.
- **EXPLÍCITO [p032]:** EmergencyChange `subclass_of` Change.
- **EXPLÍCITO [p032]:** UnauthorizedChange `subclass_of` ControlViolation.
- **NO SOPORTADO [p031]:** inducir una taxonomía de etapas del ciclo de vida solo por la enumeración funcional; p031 no usa una relación literal de tipo/subtipo.

### Modalidad

- **Disyunción [p031]:** «transforms or uses» y «systems or people».
- **Obligación [p031]:** «must be protected»; además aparece el cuantificador distributivo «each».
- **Condición temporal [p031]:** «when retention expires».
- **Condición [p032]:** «if a change fails».
- **Posibilidad [p032]:** «can introduce vulnerabilities».
- **Finalidad y manera [p032]:** «implemented rapidly to resolve urgent issues».
- El resto son enunciados declarativos genéricos en presente.

### Ambigüedades

- **[p031] «from creation to disposal»:** **EXPLÍCITO** como alcance temporal; la lectura de Creation como amenaza es **NO SOPORTADO**.
- **[p031] «between systems or people»:** puede significar entre sistemas o entre personas; no especifica extremos concretos. Conservar la alternativa es más fiel que escoger una rama.
- **[p031] «another party»:** el referente de comparación no está identificado; resolver una parte concreta sería **NO SOPORTADO**.
- **[p031] «disposed data»:** está relacionado semánticamente con datos objeto de disposición, pero no identifica una instancia previa concreta.
- **[p032] «that» en NormalChange:** es relativo y su antecedente textual es «change»; esta correferencia es **EXPLÍCITA**.
- **[p032] «that» tras «verifies»:** en las oraciones de aprobación y prueba funciona como complementizador, no como mención correferencial.
- **[p032] «approval»:** vincularlo con ChangeApproval es **PLAUSIBLE**, pero el texto no declara identidad léxica.
- **[p032] «a change» en aprobación, prueba y reversión:** es un referente genérico de la clase Change, no una misma instancia compartida entre oraciones.

## 2. Resultado por etapa

Escala: 0 = ausente/incorrecto; 1 = deficiente; 2 = parcial; 3 = sólido con defectos; 4 = completo y fiel.

| Paso | Etapa | Fidelidad | Cobertura | Precisión | Trazabilidad | Coherencia | Estado |
|---:|---|---:|---:|---:|---:|---:|---|
| 01 | input_intake | 4 | 4 | 4 | 4 | 4 | OK |
| 02 | preprocessing | 4 | 4 | 4 | 4 | 4 | OK |
| 03 | sentence_segmentation | 4 | 4 | 4 | 4 | 4 | OK |
| 04 | tokenization | 4 | 4 | 4 | 4 | 4 | OK |
| 05 | linguistic_annotation | 3 | 4 | 3 | 4 | 3 | WARN |
| 06 | entity_extraction | 4 | 4 | 4 | 4 | 4 | OK |
| 07 | concept_extraction | 2 | 2 | 2 | 4 | 2 | FAIL |
| 08 | coreference_resolution | 1 | 4 | 1 | 4 | 3 | FAIL |
| 09 | relation_extraction | 1 | 1 | 1 | 3 | 1 | FAIL |
| 10 | canonical_claims / semantic_claims | 3 | 4 | 3 | 4 | 4 | WARN |
| 11 | semantic_debug_ir | 4 | 4 | 4 | 4 | 4 | OK |
| 12 | triple_extraction | 4 | 4 | 4 | 4 | 4 | OK |
| 13 | taxonomy_induction | 4 | 4 | 4 | 4 | 4 | OK |
| 14 | type_assertion | 4 | 4 | 4 | 4 | 4 | OK |
| 15 | semantic_quality | 3 | 2 | 3 | 3 | 2 | WARN |
| 16 | output_generation | 3 | 4 | 3 | 3 | 3 | WARN |

La puntuación 4 de los pasos 11 y 12 evalúa su responsabilidad local: ambos proyectan fielmente las claims recibidas y conservan sus metadatos. El contenido discutible que reciben se atribuye al paso 10, no se vuelve a contar como error de origen.

## 3. Hallazgos

### Q-infosec_p031_p032-05-1

- **Severidad:** alta
- **Tipo:** anotación lingüística incorrecta
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** [p031] «Data archival stores information for long-term retention.»
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p031_p032/artifacts/pipeline_outputs/observed_p031_p032_05_linguistic_annotation.json`, `/tokens/50`
- **Evaluación razonada:** «stores» aparece como `pos: NOUN`, `tag: NNS`, `dependency: compound` y con cabeza `information`, aunque en la oración realiza la predicación verbal. La interpretación del predicado como verbo es **EXPLÍCITA** por la estructura literal.
- **Impacto downstream:** origina el sintagma proposicional espurio del paso 07 y contribuye a que el paso 09 no extraiga la relación de archivado. La claim canónica posterior lo corrige.

### Q-infosec_p031_p032-07-1

- **Severidad:** alta
- **Tipo:** absorción de predicado en concepto
- **Atribución:** ERROR_AMPLIFICADO
- **Cita literal:** [p031] «Data archival stores information» dentro de «Data archival stores information for long-term retention.»
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p031_p032/artifacts/pipeline_outputs/observed_p031_p032_07_concept_extraction.json`, `/concepts/17`
- **Evaluación razonada:** se propone como concepto completo `Data archival stores information`, con confianza 0.95. Es una proposición, no un concepto nominal. El paso amplifica el error originado en 05 y no obtiene limpiamente DataArchival e Information en esa ocurrencia.
- **Impacto downstream:** degrada la extracción relacional; el paso 15 termina excluyendo este ruido y las claims del paso 10 reconstruyen la semántica correcta. Es la misma cadena de error de Q-05-1, no un segundo origen independiente.

### Q-infosec_p031_p032-07-2

- **Severidad:** media
- **Tipo:** cobertura conceptual incompleta
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** [p032] «pre-approved low-risk change» y «control violation».
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p031_p032/artifacts/pipeline_outputs/observed_p031_p032_07_concept_extraction.json`, `/concepts`
- **Evaluación razonada:** no hay candidatos para PreApprovedLowRiskChange ni ControlViolation, pese a ser objetos explícitos de definiciones taxonómicas. También se agrupan «assessment and approval» y se duplica la misma mención de [p031] «another party» como `another party` y `party` (`/concepts/16` y `/concepts/53`).
- **Impacto downstream:** el paso 09 produce objetos `type` sin referencia y pierde los supertipos. El paso 10 corrige las taxonomías a partir de evidencia literal.

### Q-infosec_p031_p032-08-1

- **Severidad:** alta
- **Tipo:** correferencia espuria
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** [p032] «Change approval verifies that a change is acceptable» y «Change testing verifies that a change works as intended».
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p031_p032/artifacts/pipeline_outputs/observed_p031_p032_08_coreference_resolution.json`, `/coreferences/1` y `/coreferences/2`
- **Evaluación razonada:** ambos `that` son complementizadores y no menciones anafóricas. Resolverlos a ChangeApproval y ChangeTesting es **NO SOPORTADO**. En contraste, `/coreferences/0` resuelve correctamente el `that` relativo de NormalChange a «change».
- **Impacto downstream:** introduce evidencia correferencial falsa, aunque no se observa materialización directa de esas dos resoluciones en el modelo final.

### Q-infosec_p031_p032-09-1

- **Severidad:** crítica
- **Tipo:** conflación de sujetos entre párrafos y clases
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** [p032] «Change management controls modifications…», «A normal change… requires assessment and approval» y «Poor change management can introduce vulnerabilities.»
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p031_p032/artifacts/pipeline_outputs/observed_p031_p032_09_relation_extraction.json`, `/relations/4/subject_ref`, `/relations/17/subject_ref`, `/relations/20/subject_ref` y `/relations/21/subject_ref`
- **Evaluación razonada:** ChangeManagement y PoorChangeManagement apuntan al identificador de DataLifecycleManagement; las dos relaciones de NormalChange apuntan al identificador de StandardChange. Estas identidades están **CONTRADICHAS** por los sujetos literales de p032 y además cruzan indebidamente p031/p032.
- **Impacto downstream:** contaminaría triples y RDF si se proyectaran estas relaciones. El paso 10 las reemplaza por sujetos canónicos correctos, por lo que el error queda corregido antes de RDF.

### Q-infosec_p031_p032-09-2

- **Severidad:** crítica
- **Tipo:** pérdida de relaciones, argumentos y modalidad
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** [p031] «moves information between systems or people», «stores information for long-term retention», «define how each classification level must be protected»; [p032] «implemented rapidly to resolve urgent issues», «verifies that a change works as intended» y «if a change fails».
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p031_p032/artifacts/pipeline_outputs/observed_p031_p032_09_relation_extraction.json`, `/relations`
- **Evaluación razonada:** faltan por completo o quedan truncadas la transmisión, el archivado, la regla de protección, la finalidad y manera del cambio de emergencia, la verificación de testing y las condiciones de disposal/rollback. También se pierde `can` en PoorChangeManagement y `transforms` en la disyunción de procesamiento. Los objetos taxonómicos se reducen a `type`.
- **Impacto downstream:** este es el mayor colapso local de cobertura. No llega al RDF porque el paso 10 reconstruye 32 claims desde evidencia literal; sin esa corrección, el modelo sería no fiel.

### Q-infosec_p031_p032-09-3

- **Severidad:** alta
- **Tipo:** rol semántico no soportado
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** [p031] «protects information from creation to disposal».
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p031_p032/artifacts/pipeline_outputs/observed_p031_p032_09_relation_extraction.json`, `/relations/7` y `/relations/9`
- **Evaluación razonada:** `management protect_from creation` y `management protect_to disposal` convierten límites de alcance en objetos de protección. Esa lectura es **NO SOPORTADA**; el objeto protegido es Information y Creation/Disposal delimitan el alcance.
- **Impacto downstream:** el paso 10 lo corrige con `scope_from` y `scope_to`, evitando que estas dos relaciones espurias lleguen al output.

### Q-infosec_p031_p032-10-1

- **Severidad:** informativa (acierto decisivo)
- **Tipo:** recuperación semántica y de trazabilidad
- **Atribución:** ERROR_CORREGIDO
- **Cita literal:** [p031] «Data processing transforms or uses information»; [p032] «Poor change management can introduce vulnerabilities.»
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p031_p032/artifacts/pipeline_outputs/observed_p031_p032_10_canonical_claims.json`, `/canonical_claims/claims`
- **Evaluación razonada:** las 32 claims recuperan las 21 proposiciones y sus descomposiciones justificadas: disyunciones, condiciones, finalidad, manera, cuantificador, obligación, posibilidad, participantes y cuatro definiciones. Cada claim conserva párrafo, oración, texto probatorio y `source_text_id`.
- **Impacto downstream:** corrige los principales errores de 05/07/09 y permite que triples, taxonomía y output sean ampliamente fieles.

### Q-infosec_p031_p032-10-2

- **Severidad:** media
- **Tipo:** especialización plausible pero no entrañada
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** [p032] «A normal change is a type of change that requires assessment and approval.»
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p031_p032/artifacts/pipeline_outputs/observed_p031_p032_10_canonical_claims.json`, `/canonical_claims/claims/23/object`
- **Evaluación razonada:** la claim usa `ChangeApproval`, mientras la evidencia de esa oración solo dice `approval`. La vinculación con el concepto de la oración siguiente es **PLAUSIBLE**, pero no está declarada como identidad. La representación conservadora sería Approval, manteniendo un posible enlace separado y marcado como incierto.
- **Impacto downstream:** esta especialización sí llega a triples, facts y esquema RDF como rango de `requires`.

### Q-infosec_p031_p032-10-3

- **Severidad:** baja
- **Tipo:** nominalización proposicional defectuosa
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** [p032] «a change works as intended».
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p031_p032/artifacts/pipeline_outputs/observed_p031_p032_10_canonical_claims.json`, `/canonical_claims/claims/28`
- **Evaluación razonada:** `Change works Intended` trata `intended` como objeto/concepto, aunque «as intended» expresa una manera o criterio. La claim principal anterior conserva correctamente `evaluated_outcome: works_as_intended`; esta segunda claim es semánticamente mal formada.
- **Impacto downstream:** se propaga al debug IR y a un triple, pero queda marcado `projection_scope: evidence_only` y no se materializa como hecho RDF; por ello su impacto final es limitado.

### Q-infosec_p031_p032-15-1

- **Severidad:** media
- **Tipo:** control de calidad semántica incompleto
- **Atribución:** ERROR_AMPLIFICADO
- **Cita literal:** [p032] «requires assessment and approval» y «works as intended».
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p031_p032/artifacts/pipeline_outputs/observed_p031_p032_15_semantic_quality.json`, `/semantic_quality_report/semantic_ambiguities`, `/semantic_quality_report/semantic_integrity_issues` y `/semantic_quality_report/rdf_readiness`
- **Evaluación razonada:** el paso detecta correctamente el ruido «Data archival stores information», pero declara vacías las ambigüedades y los problemas de integridad pese a la especialización Approval→ChangeApproval y a `Change works Intended`. Además fija `rdf_readiness: false` sin explicar una barrera adicional al ruido ya excluido.
- **Impacto downstream:** no origina los defectos de las claims, pero no los filtra ni los marca antes de la proyección y deja una señal de readiness poco accionable.

### Q-infosec_p031_p032-16-1

- **Severidad:** media
- **Tipo:** contenido no soportado propagado a RDF
- **Atribución:** ERROR_PROPAGADO
- **Cita literal:** [p032] «requires assessment and approval».
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p031_p032/artifacts/pipeline_outputs/observed_p031_p032_16_output_generation.json`, `/output/graph/facts/15` y `/output/graph/object_property_schema/15`
- **Evaluación razonada:** el modelo afirma NormalChange `requires` ChangeApproval y declara ese rango observado. Es la misma especialización **PLAUSIBLE** originada en Q-10-2, no un error nuevo de output.
- **Impacto downstream:** consumidores RDF pueden interpretar como explícita una identidad que el párrafo no asegura.

### Q-infosec_p031_p032-16-2

- **Severidad:** media
- **Tipo:** duplicación estructural del modelo
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** [p031] «Data lifecycle management…» y [p032] «Change management…», representados en ambos inventarios.
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p031_p032/artifacts/pipeline_outputs/observed_p031_p032_16_output_generation.json`, `/output/graph/classes`, `/output/graph/schema/classes`, `/output/graph/subclass_facts` y `/taxonomy_relations`
- **Evaluación razonada:** los 46 elementos de `classes` se repiten exactamente en `schema/classes`; las cuatro taxonomías también aparecen como dos vistas equivalentes. No inventa hechos, pero incumple el criterio estricto de modelo final sin duplicación y puede inducir doble conteo si el consumidor no conoce las vistas.
- **Impacto downstream:** aumenta redundancia y riesgo de inconsistencias futuras, aunque en este artifact las copias coinciden.

### Q-infosec_p031_p032-16-3

- **Severidad:** informativa (acierto)
- **Tipo:** preservación de alcance y modalidad
- **Atribución:** ERROR_CORREGIDO
- **Cita literal:** [p031] «transforms or uses», «when retention expires», «must be protected»; [p032] «implemented rapidly to resolve», «if a change fails» y «can introduce».
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p031_p032/artifacts/pipeline_outputs/observed_p031_p032_16_output_generation.json`, `/output/graph/logical_alternatives` y `/output/graph/scoped_relations`
- **Evaluación razonada:** el output evita materializar como categóricas las alternativas, condiciones, obligación, finalidad y posibilidad. Conserva evidencia literal y metadatos de alcance. Las cuatro taxonomías explícitas aparecen correctamente y `type_assertions` permanece vacío, acorde con la ausencia de instancias.
- **Impacto downstream:** evita que la fuerte degradación del paso 09 contamine el RDF final y conserva todas las proposiciones literales en alguna estructura del modelo.

## 4. Diagnóstico

- **Primera degradación:** paso 05, al analizar «stores» de [p031] como nombre y absorber el predicado en el sintagma nominal.
- **Principal pérdida:** paso 09. Pierde relaciones completas, argumentos coordinados, condiciones y modalidades; además confunde DataLifecycleManagement, ChangeManagement, PoorChangeManagement, StandardChange y NormalChange.
- **Principal contenido no soportado:** la identificación de [p032] `approval` con `ChangeApproval`. Es plausible por proximidad temática, pero no está explícitamente declarada.
- **Errores que llegan a RDF/OWL:** llega la especialización NormalChange→requires→ChangeApproval. No llegan las correferencias espurias, los sujetos cruzados del paso 09, `protect_from/protect_to` ni `Change works Intended`. También llega redundancia estructural de inventarios, no una falsedad factual.
- **Aciertos:** intake, normalización, segmentación y tokens son íntegros; la ausencia de entidades nombradas y type assertions es conservadora; las claims recuperan la semántica perdida; la taxonomía contiene exactamente las cuatro relaciones explícitas; el output preserva disyunción, condiciones, obligación, posibilidad, finalidad, manera, participantes y evidencia.
- **Incertidumbres:** «between systems or people» admite más de una lectura de los extremos; «another party» carece de antecedente concreto; `approval` puede referir a ChangeApproval, pero solo con grado **PLAUSIBLE**. El conservadurismo ante estos puntos no debe penalizarse.

## 5. Veredicto

- **Calidad global:** **80/100**.
- **Output final:** **parcialmente fiel**. Conserva la cobertura proposicional completa y evita la mayoría de las falsas materializaciones, pero contiene una especialización no entrañada y duplicación estructural exacta.
- **Tres correcciones prioritarias:**
  1. Corregir la extracción relacional para conservar sujetos completos, argumentos coordinados, condiciones, disyunciones y modalidad sin conflar identificadores entre oraciones o párrafos.
  2. Mantener `Approval` como concepto literal salvo que la identidad con `ChangeApproval` se marque explícitamente como incierta; eliminar la claim proposicional `Change works Intended`.
  3. Emitir una sola vista canónica de clases y taxonomías, con trazabilidad directa por claim y una explicación coherente de `rdf_readiness` antes de proyectar RDF.

Siguiente caso pendiente: infosec_p033_p034.
