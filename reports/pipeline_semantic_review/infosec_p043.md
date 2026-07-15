# Revisión semántica: infosec_p043

## 1. Lectura independiente

- **Resumen**
  - **Tema:** requisitos semánticos para una ontología de seguridad de la información y para el grafo RDF u OWL generado a partir de ella.
  - **Lectura central:** el párrafo no afirma sin más que todas las relaciones de dominio sean hechos del mundo. Afirma que la ontología **debería representarlas**. Esa modalidad y ese alcance deben conservarse.
  - **Entidades/instancias explícitas:** no hay nombres propios ni individuos de dominio identificados. Sí hay dos referentes definidos del discurso: “The resulting ontology”/“The ontology” (la misma ontología, **ENTRAÑADO**) y “the generated RDF or OWL graph” (un grafo generado concreto, aunque sin nombre). “These relationships” refiere anafóricamente al conjunto de relaciones precedentes.
  - **Definiciones:** no hay definiciones explícitas del tipo «X es Y» ni equivalencias definitorias.

- **Conceptos**
  - Referentes del artefacto: resulting ontology, ontology, generated graph, RDF, OWL, relationships.
  - Actores o agentes genéricos: users, suppliers, auditors.
  - Objetos y estructuras de acceso/control: systems, roles, permissions, controls, policies, requirements, services.
  - Riesgo y seguridad: risks, threats, vulnerabilities, incidents, assets, information assets, compliance.
  - Mecanismos y propiedades: encryption, confidentiality, backups, availability, logging, accountability, monitoring, suspicious activity.
  - Usos del grafo: querying, validation, reasoning, mining.
  - Los sustantivos plurales son genéricos; el texto no fija si expresan universalidad, existencia o solo una firma de relación ontológica.

- **Proposiciones con evidencia**

| ID | Proposición literal | Evidencia breve de p043 | Clasificación |
|---|---|---|---|
| P01 | La ontología debería representar que los usuarios acceden a sistemas. | “users access systems” | EXPLÍCITO, bajo `should represent` |
| P02 | La ontología debería representar que los roles incluyen permisos. | “roles include permissions” | EXPLÍCITO, bajo `should represent` |
| P03 | La ontología debería representar que los controles reducen riesgos. | “controls reduce risks” | EXPLÍCITO, bajo `should represent` |
| P04 | La ontología debería representar que las amenazas explotan vulnerabilidades. | “threats exploit vulnerabilities” | EXPLÍCITO, bajo `should represent` |
| P05 | La ontología debería representar que los incidentes afectan activos. | “incidents affect assets” | EXPLÍCITO, bajo `should represent` |
| P06 | La ontología debería representar que los sistemas procesan activos de información. | “systems process information assets” | EXPLÍCITO, bajo `should represent` |
| P07 | La ontología debería representar que las políticas definen requisitos. | “policies define requirements” | EXPLÍCITO, bajo `should represent` |
| P08 | La ontología debería representar que los requisitos son satisfechos por controles. | “requirements are satisfied by controls” | EXPLÍCITO, bajo `should represent`; voz pasiva |
| P09 | La ontología debería representar que los proveedores proporcionan servicios. | “suppliers provide services” | EXPLÍCITO, bajo `should represent` |
| P10 | La ontología debería representar que los auditores evalúan el cumplimiento. | “auditors evaluate compliance” | EXPLÍCITO, bajo `should represent` |
| P11 | La ontología debería representar que el cifrado protege la confidencialidad. | “encryption protects confidentiality” | EXPLÍCITO, bajo `should also represent` |
| P12 | La ontología debería representar que las copias de respaldo apoyan la disponibilidad. | “backups support availability” | EXPLÍCITO, bajo `should also represent` |
| P13 | La ontología debería representar que el registro apoya la rendición de cuentas. | “logging supports accountability” | EXPLÍCITO, bajo `should also represent` |
| P14 | La ontología debería representar que la monitorización detecta actividad sospechosa. | “monitoring detects suspicious activity” | EXPLÍCITO, bajo `should also represent` |
| P15 | Estas relaciones hacen que el grafo generado RDF u OWL sea adecuado para consultas. | “These relationships make … suitable for querying” | EXPLÍCITO |
| P16 | Estas relaciones hacen que el grafo generado RDF u OWL sea adecuado para validación. | “suitable for … validation” | EXPLÍCITO por coordinación |
| P17 | Estas relaciones hacen que el grafo generado RDF u OWL sea adecuado para razonamiento. | “suitable for … reasoning” | EXPLÍCITO por coordinación |
| P18 | Estas relaciones hacen que el grafo generado RDF u OWL sea adecuado para minería. | “suitable for … mining” | EXPLÍCITO por coordinación |

- **Taxonomías explícitas**
  - No hay relaciones explícitas de subclase, superclase o pertenencia taxonómica.
  - “information assets” es un sintagma nominal compuesto; inferir `InformationAsset subClassOf Asset` es **PLAUSIBLE**, pero no **EXPLÍCITO** ni **ENTRAÑADO**.
  - “roles include permissions” expresa una relación `include`, no una taxonomía.
  - “RDF or OWL graph” clasifica de forma disyuntiva al grafo concreto por su formato; no establece una jerarquía entre RDF, OWL y Graph.

- **Modalidad**
  - P01–P14 están bajo la modalidad deóntica/desiderativa “should represent”. Son contenido requerido de la ontología, no hechos categóricos no modalizados.
  - “also” añade P11–P14 al mismo alcance modal.
  - P15–P18 están en presente declarativo mediante “make”; expresan una consecuencia atribuida colectivamente a las relaciones.
  - “RDF or OWL” conserva una alternativa. Elegir solo RDF, solo OWL o afirmar ambos formatos sería **NO SOPORTADO**.
  - La coordinación final con “and” incluye los cuatro usos; no expresa alternativas entre ellos.

- **Ambigüedades**
  - **Correferencia:** “The ontology” = “The resulting ontology” es **ENTRAÑADO** por continuidad discursiva. “These relationships” refiere a las relaciones enumeradas antes; el alcance más natural incluye P01–P14, aunque el texto no enumera formalmente el conjunto.
  - **`that`:** en “represent that …” introduce una cláusula y no es una mención referencial. Resolverlo contra “ontology” es **CONTRADICHO** por su función en la construcción.
  - **Cuantificación:** interpretar “users access systems” como «todo usuario accede a todo sistema» es **NO SOPORTADO**. Una lectura de relación genérica entre los conceptos User y System es **PLAUSIBLE**.
  - **Naturaleza de los nodos:** tratar todos los sustantivos como clases OWL es **PLAUSIBLE**, pero no está explícitamente declarado. Es especialmente dudoso para el referente definido “the generated … graph” y para los usos Querying, Validation, Reasoning y Mining.
  - **Causalidad:** reducir “These relationships make the … graph suitable” a `GeneratedGraph suitableFor X` es **ENTRAÑADO** como resultado, pero pierde parte de la causalidad explícita si no se conserva el antecedente colectivo.
  - **Interpretaciones ajenas:** `Role includes Control`, `Incident affects InformationAsset` y `Encryption backup Availability` son **NO SOPORTADAS**; el párrafo coordina proposiciones distintas y no afirma esas relaciones.

## 2. Resultado por etapa

| Paso | Etapa | Fidelidad | Cobertura | Precisión | Trazabilidad | Coherencia | Estado |
|---:|---|---:|---:|---:|---:|---:|---|
| 01 | input_intake | 4 | 4 | 4 | 4 | 4 | OK |
| 02 | preprocessing | 4 | 4 | 4 | 4 | 4 | OK |
| 03 | sentence_segmentation | 4 | 4 | 4 | 4 | 4 | OK |
| 04 | tokenization | 4 | 4 | 4 | 4 | 4 | OK |
| 05 | linguistic_annotation | 2 | 4 | 2 | 4 | 2 | FAIL |
| 06 | entity_extraction | 4 | 4 | 4 | 4 | 4 | OK |
| 07 | concept_extraction | 2 | 2 | 2 | 4 | 2 | FAIL |
| 08 | coreference_resolution | 0 | 0 | 0 | 4 | 1 | FAIL |
| 09 | relation_extraction | 1 | 2 | 2 | 2 | 1 | FAIL |
| 10 | canonical_claims / semantic_claims | 4 | 4 | 4 | 3 | 4 | OK |
| 11 | semantic_debug_ir | 4 | 4 | 4 | 4 | 4 | OK |
| 12 | triple_extraction | 4 | 4 | 4 | 3 | 4 | OK |
| 13 | taxonomy_induction | 4 | 4 | 4 | 4 | 4 | OK |
| 14 | type_assertion | 2 | 2 | 4 | 2 | 3 | WARN |
| 15 | semantic_quality | 3 | 3 | 4 | 4 | 4 | WARN |
| 16 | output_generation | 3 | 3 | 3 | 4 | 2 | FAIL |

## 3. Hallazgos

### Q-infosec_p043-05-1
- **Severidad:** alta.
- **Tipo:** precisión lingüística y coherencia sintáctica.
- **Atribución:** ERROR_ORIGEN.
- **Cita literal (p043):** “users access systems”; “systems process information assets”; “backups support availability”.
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p043/artifacts/pipeline_outputs/observed_p043_05_linguistic_annotation.json`; `/tokens/6`, `/tokens/7`, `/tokens/8`, `/tokens/26`, `/tokens/27`, `/tokens/60`, `/tokens/61`.
- **Evaluación razonada:** `users` y `access` quedan como compuestos nominales de `systems`; `systems` y `process` quedan absorbidos en otro compuesto; `backups` se etiqueta como verbo y `support` como nombre. Las anotaciones invierten o borran límites sujeto–predicado explícitos. La interpretación correcta es **EXPLÍCITA** en p043; la anotación observada no es una ambigüedad semántica legítima.
- **Impacto downstream:** origina los conceptos-cláusula de 07 y varias relaciones falsas u omitidas de 09. El error se corrige en 10, por lo que no debe volver a contarse como origen en 07, 09, 12 o 16.

### Q-infosec_p043-07-1
- **Severidad:** alta.
- **Tipo:** cobertura y granularidad conceptual.
- **Atribución:** ERROR_AMPLIFICADO, misma línea causal que Q-infosec_p043-05-1.
- **Cita literal (p043):** “users access systems”, “systems process information assets” y “backups support availability”.
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p043/artifacts/pipeline_outputs/observed_p043_07_concept_extraction.json`; `/concepts/9`, `/concepts/19`, `/concepts/28`.
- **Evaluación razonada:** se proponen con alta confianza los falsos conceptos “systems process information assets” y “support availability”, y también “users access systems” como un solo concepto. A la vez faltan candidatos atómicos adecuados para System, Backup y Logging en sus funciones literales. Las cláusulas completas no son conceptos explícitos; contienen predicados absorbidos.
- **Impacto downstream:** degrada referencias de argumentos y favorece relaciones espurias en 09. La exclusión posterior de estos cuatro conceptos en 15 es un **ERROR_CORREGIDO** y evita su proyección final directa.

### Q-infosec_p043-08-1
- **Severidad:** alta.
- **Tipo:** correferencia, precisión y cobertura.
- **Atribución:** ERROR_ORIGEN.
- **Cita literal (p043):** “represent that users access systems” y “These relationships make the generated RDF or OWL graph suitable”.
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p043/artifacts/pipeline_outputs/observed_p043_08_coreference_resolution.json`; `/coreferences/0`, `/coreferences/1`, `/coreferences`.
- **Evaluación razonada:** las dos ocurrencias de `that` son introductores de cláusula, no menciones, pero se resuelven respectivamente a “resulting ontology” y “ontology”. En cambio, la anáfora real “These relationships” no aparece. Las dos resoluciones producidas son **CONTRADICHAS** por la construcción sintáctica; la anáfora omitida sí está explícita.
- **Impacto downstream:** el artifact de correferencia queda semánticamente inútil. No obstante, 10 reconstruye `antecedent_scope: represented_relationships`, de modo que este error no llega como falsa correferencia al modelo final.

### Q-infosec_p043-09-1
- **Severidad:** alta.
- **Tipo:** fidelidad, cobertura y precisión relacional.
- **Atribución:** ERROR_AMPLIFICADO, principalmente desde Q-infosec_p043-05-1 y Q-infosec_p043-07-1.
- **Cita literal (p043):** “roles include permissions, controls reduce risks”; “incidents affect assets, systems process information assets”; “encryption protects confidentiality, backups support availability”.
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p043/artifacts/pipeline_outputs/observed_p043_09_relation_extraction.json`; `/relations/0`, `/relations/5`, `/relations/8`, `/relations/11`.
- **Evaluación razonada:** se generan `Encryption—backup→support availability`, `Role—include→Control` e `Incident—affect→process information asset`, todas **NO SOPORTADAS**. La pasiva de requisitos se reduce a `Requirement—be→satisfied` y pierde “by controls”. Además faltan relaciones explícitas como User–access–System, Control–reduce–Risk, System–process–InformationAsset y Logging–support–Accountability.
- **Impacto downstream:** si se proyectaran estas candidatas, introducirían relaciones falsas y omisiones graves. 10 no las propaga: reconstruye las 14 relaciones modales y las cuatro consecuencias, por lo que 09 es la amplificación terminal de esta línea de error.

### Q-infosec_p043-09-2
- **Severidad:** baja.
- **Tipo:** trazabilidad.
- **Atribución:** ERROR_ORIGEN.
- **Cita literal (p043):** “roles include permissions” dentro de la primera oración completa.
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p043/artifacts/pipeline_outputs/observed_p043_09_relation_extraction.json`; `/relations/3/evidence_span`, `/relations/4/evidence_span`, `/relations/7/evidence_span`.
- **Evaluación razonada:** varias relaciones usan como evidencia toda la oración 0–342, aunque la frase justificativa es local. La oración permite rastreo general, pero no localiza qué coordinación respalda cada relación.
- **Impacto downstream:** 10 y 12 conservan la oración y los IDs, pero también mantienen evidencia a nivel de oración; la verificabilidad manual es menor sin alterar por sí sola el significado final.

### Q-infosec_p043-10-1
- **Severidad:** informativa; acierto crítico.
- **Tipo:** recuperación semántica, modalidad y discurso.
- **Atribución:** ERROR_CORREGIDO respecto de 05, 07, 08 y 09.
- **Cita literal (p043):** “The resulting ontology should represent that …”; “These relationships make the generated RDF or OWL graph suitable for querying, validation, reasoning, and mining.”
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p043/artifacts/pipeline_outputs/observed_p043_10_canonical_claims.json`; `/semantic_claims/claims`, en particular `/semantic_claims/claims/0`–`/semantic_claims/claims/17`.
- **Evaluación razonada:** las 18 descomposiciones fieles están presentes. P01–P14 conservan `modality: should`, `scope: ResultingOntology` y `relation_role: represented_content`; P15–P18 conservan el alcance discursivo, la coordinación y la alternativa `RDF,OWL`. No sobreviven las relaciones falsas de 09.
- **Impacto downstream:** proporciona una base semántica completa y precisa para 11 y 12 y protege el output final de la mayoría de errores tempranos.

### Q-infosec_p043-14-1
- **Severidad:** media.
- **Tipo:** cobertura de tipado y distinción clase–instancia.
- **Atribución:** ERROR_ORIGEN.
- **Cita literal (p043):** “the generated RDF or OWL graph”.
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p043/artifacts/pipeline_outputs/observed_p043_14_type_assertion.json`; `/type_assertions`.
- **Evaluación razonada:** el sintagma definido introduce un grafo generado concreto y lo caracteriza disyuntivamente como RDF u OWL. La lista vacía no representa ninguna pertenencia de tipo ni una alternativa condicionada. No se exige escoger una rama: hacerlo sería **NO SOPORTADO**; sí debería conservarse la clasificación disyuntiva del referente.
- **Impacto downstream:** 16 termina promoviendo `GeneratedGraph` a clase y no produce una instancia ni una alternativa lógica, amplificando la pérdida de categoría semántica.

### Q-infosec_p043-15-1
- **Severidad:** media-baja.
- **Tipo:** cobertura del control de calidad.
- **Atribución:** ERROR_CORREGIDO parcial.
- **Cita literal (p043):** “users access systems”, “systems process information assets” y “backups support availability”.
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p043/artifacts/pipeline_outputs/observed_p043_15_semantic_quality.json`; `/semantic_quality_report/concept_noise`, `/excluded_concepts`, `/semantic_quality_report/warnings`.
- **Evaluación razonada:** identifica correctamente los cuatro conceptos con predicado absorbido y declara `rdf_readiness: false`. Es una corrección efectiva del ruido de 07. La cobertura es parcial porque el informe solo advierte `concept_noise_detected` y no registra las falsas correferencias de 08 ni las candidatas relacionales falsas de 09, aunque estas últimas ya no alimentan la proyección desde semantic claims.
- **Impacto downstream:** los conceptos ruidosos no llegan al grafo final. La omisión diagnóstica restante afecta observabilidad más que contenido, pues 16 usa `semantic_claims`.

### Q-infosec_p043-16-1
- **Severidad:** alta.
- **Tipo:** fidelidad del modelo final y distinción clase–instancia.
- **Atribución:** ERROR_AMPLIFICADO desde Q-infosec_p043-14-1.
- **Cita literal (p043):** “These relationships make the generated RDF or OWL graph suitable for querying, validation, reasoning, and mining.”
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p043/artifacts/pipeline_outputs/observed_p043_16_output_generation.json`; `/output/graph/classes/9`, `/output/graph/instance_facts`, `/output/graph/logical_alternatives`, `/output/graph/object_property_schema/12`, `/output/graph/scoped_relations/14`–`/output/graph/scoped_relations/17`.
- **Evaluación razonada:** el grafo concreto `GeneratedGraph` se modela como clase y `suitableFor` como firma de propiedad con dominio/rango; no hay hecho de instancia ni alternativa lógica RDF/OWL. Los metadatos de `scoped_relations` conservan la evidencia, el antecedente y `RDF,OWL`, por lo que no hay pérdida total, pero la proyección RDF/OWL estándar es más esquemática y más general que la proposición definida del párrafo. La lectura de clase es **PLAUSIBLE**, no **EXPLÍCITA**.
- **Impacto downstream:** consultas sobre el artifact completo pueden recuperar el claim, pero consultas RDF/OWL de instancia no recuperarán que el grafo generado concreto es adecuado para esos cuatro usos ni su tipo alternativo.

### Q-infosec_p043-16-2
- **Severidad:** baja.
- **Tipo:** coherencia estructural y duplicación.
- **Atribución:** ERROR_ORIGEN.
- **Cita literal (p043):** “The resulting ontology should represent…” y “the generated RDF or OWL graph”.
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p043/artifacts/pipeline_outputs/observed_p043_16_output_generation.json`; `/output/graph/classes` frente a `/output/graph/schema/classes`, y `/output/graph/object_property_schema` frente a `/output/graph/schema/object_properties`.
- **Evaluación razonada:** clases y propiedades se repiten en dos vistas casi equivalentes. No se observan dobles `scoped_relations`, por lo que la duplicación es estructural, no una duplicación lógica demostrada; aun así incumple el criterio estricto de un output sin redundancia y puede inducir doble conteo en consumidores ingenuos.
- **Impacto downstream:** aumenta el riesgo de divergencia entre vistas y de contabilización duplicada, aunque el contenido semántico actual coincide.

## 4. Diagnóstico

- **Primera degradación:** paso 05. La anotación lingüística interpreta varios verbos coordinados como nombres o compuestos, pese a que los límites relacionales son literales.
- **Principal pérdida:** la pérdida temprana de User–access–System, Control–reduce–Risk, System–process–InformationAsset, Backup–support–Availability y Logging–support–Accountability se corrige en 10. La pérdida que sí persiste parcialmente es la condición de “the generated … graph” como referente concreto y su clasificación alternativa RDF/OWL; 16 lo proyecta como clase/esquema.
- **Principal contenido no soportado:** en etapas intermedias, `Role includes Control`, `Incident affects process information asset` y la falsa relación de Encryption con Backup. Ninguna llega a los semantic claims ni al output. En el modelo final, la promoción general de los usos y del grafo generado a clases es solo **PLAUSIBLE**, no explícita.
- **Errores que llegan a RDF/OWL:** llega la distorsión clase–instancia de `GeneratedGraph`, no una falsa relación de dominio. También llega redundancia estructural entre las vistas de esquema. No llegan las correferencias falsas de `that`, los conceptos-cláusula excluidos ni las relaciones espurias de 09.
- **Aciertos:** texto, offsets, tres oraciones y tokens son fieles; no se inventan taxonomías ni individuos de dominio; 10 recupera las 18 proposiciones y conserva modalidad, alcance, pasiva, coordinación, antecedente discursivo y alternativa RDF/OWL; 12 mantiene las 18 correspondencias claim–triple; 15 excluye exactamente los cuatro conceptos con predicados absorbidos.
- **Incertidumbres legítimas:** cuantificación de los plurales genéricos, lectura de “information assets” como clase especializada, inclusividad de `or`, y formalización OWL de Querying/Validation/Reasoning/Mining. El conservadurismo ante estas cuestiones no debe penalizarse; sí debe evitarse convertir una lectura plausible en compromiso ontológico silencioso.

## 5. Veredicto

- **Calidad global:** **80/100**.
- **Output final:** **parcialmente fiel**. Contiene todas las relaciones semánticas en `scoped_relations`, con buena evidencia y sin las invenciones de 09, pero no satisface completamente el criterio estricto de ausencia de pérdida, duplicación e invención: el grafo definido se generaliza como clase/esquema, su alternativa de tipo no se materializa y existen vistas estructurales duplicadas.
- **Tres correcciones prioritarias:**
  1. Corregir el análisis de coordinaciones para mantener sujetos, verbos y objetos atómicos en 05–09, evitando conceptos-cláusula y relaciones cruzadas.
  2. Rechazar `that` como mención y resolver “These relationships” al conjunto de relaciones representadas, con trazas locales por proposición.
  3. Proyectar “the generated RDF or OWL graph” como referente de instancia con tipado alternativo explícito y relaciones `suitableFor` de instancia; evitar promociones de clase no justificadas y eliminar vistas duplicadas del esquema.

Siguiente caso pendiente: ninguno; auditoría inicial completa.
