# Revisión semántica: infosec_p027_p028

## 1. Lectura independiente

### Resumen

Los dos párrafos presentan, sin aportar conocimiento externo, controles y responsabilidades de seguridad vinculados al empleo y a la concienciación. `p027` describe el alcance temporal de la seguridad de recursos humanos, varias prácticas o procedimientos y tres obligaciones explícitas de los empleados. `p028` describe el efecto de la concienciación, cinco contenidos de concienciación, campañas y dos mecanismos de medición.

La lectura distingue entre una acción efectivamente afirmada y una acción que solo constituye contenido enseñado. Por ejemplo, `p028` afirma que la concienciación enseña a los usuarios a proteger dispositivos; no afirma sin ese alcance que los usuarios efectivamente los protejan.

### Conceptos

- **Ámbito de empleo (`p027`):** human resource security, security responsibilities, employment, background check, candidate, confidentiality agreement, obligations, sensitive information, disciplinary process, policy violations, termination procedure y access.
- **Formación y conducta (`p027`):** security awareness training, users, policies, threats, expected behavior, role-based training, specialized security knowledge y specific responsibilities.
- **Sujetos y objetos de obligación (`p027`):** employees, credentials, suspected incidents y acceptable use policies.
- **Concienciación (`p028`):** security awareness, human-related security risks, phishing awareness, password awareness, data handling awareness, remote work awareness y social engineering awareness.
- **Contenidos enseñados (`p028`):** suspicious messages, strong passwords, information, devices, networks, office y manipulation attempts.
- **Refuerzo y medición (`p028`):** awareness campaigns, secure behavior, training completion metrics, user participation, simulated phishing exercises, user response y phishing scenarios.
- **Entidades/instancias explícitas:** no hay nombres propios ni individuos identificados. “A candidate”, “employees” y “users” introducen participantes genéricos; tratarlos como clases o roles es **ENTRAÑADO/compatible**, pero convertirlos en individuos concretos sería **NO SOPORTADO**.
- **Definiciones:** hay dos relaciones literales con el verbo *defines*: el acuerdo define obligaciones y el proceso disciplinario define consecuencias. El texto no expresa definiciones de clase mediante “is a”. Las demás oraciones son descripciones funcionales genéricas, no axiomas taxonómicos.
- **Correferencias:** no aparecen pronombres ni expresiones anafóricas que exijan resolución. Las repeticiones de “Employees”, “users” y “employment” son recurrencias léxicas del mismo rol o concepto genérico, no cadenas pronominales explícitas.

### Proposiciones con evidencia

Todas las proposiciones literales del texto son:

1. **EXPLÍCITO (`p027`):** Human resource security addresses security responsibilities, con alcance “before, during, and after employment”. Cita: “**addresses security responsibilities before, during, and after employment**”.
2. **EXPLÍCITO (`p027`):** A background check evaluates a candidate, temporalmente before employment. Cita: “**evaluates a candidate before employment**”.
3. **EXPLÍCITO (`p027`):** A confidentiality agreement defines obligations. Cita: “**defines obligations related to sensitive information**”.
4. **EXPLÍCITO (`p027`):** Esas obligations están related to sensitive information. Cita: “**obligations related to sensitive information**”.
5. **EXPLÍCITO (`p027`):** Security awareness training educates users. Cita: “**educates users about policies, threats, and expected behavior**”.
6. **EXPLÍCITO (`p027`):** Los temas de esa educación son policies, threats y expected behavior. Cita: “**about policies, threats, and expected behavior**”.
7. **EXPLÍCITO (`p027`):** Role-based training provides specialized security knowledge. Cita: “**provides specialized security knowledge for specific responsibilities**”.
8. **EXPLÍCITO (`p027`):** Ese conocimiento es para specific responsibilities. Cita: “**for specific responsibilities**”. Una relación genérica `related_to` es **ENTRAÑADA** como debilitamiento; una finalidad más específica es solo **PLAUSIBLE**.
9. **EXPLÍCITO (`p027`):** Disciplinary process defines consequences. Cita: “**defines consequences for policy violations**”.
10. **EXPLÍCITO (`p027`):** Las consequences son for policy violations. Cita: “**consequences for policy violations**”. Una relación genérica `related_to` es **ENTRAÑADA**.
11. **EXPLÍCITO (`p027`):** Termination procedure removes access bajo la condición de que employment ends. Cita: “**removes access when employment ends**”.
12. **EXPLÍCITO (`p027`):** Employees tienen la obligación de proteger credentials. Cita: “**Employees must protect credentials**”.
13. **EXPLÍCITO (`p027`):** Employees tienen la obligación de reportar suspected incidents. Cita: “**Employees must report suspected incidents**”.
14. **EXPLÍCITO (`p027`):** Employees tienen la obligación de seguir acceptable use policies. Cita: “**Employees must follow acceptable use policies**”.
15. **EXPLÍCITO (`p028`):** Security awareness reduces human-related security risks. Cita: “**reduces human-related security risks**”.
16. **EXPLÍCITO (`p028`):** Phishing awareness teaches users to identify suspicious messages. Cita: “**teaches users to identify suspicious messages**”. La acción no contextualizada “users identify suspicious messages” es **NO SOPORTADO**; como contenido enseñado es **EXPLÍCITO**.
17. **EXPLÍCITO (`p028`):** Password awareness teaches users to create and protect strong passwords. Cita: “**teaches users to create and protect strong passwords**”. Afirmar que los usuarios ya lo hacen sería **NO SOPORTADO**.
18. **EXPLÍCITO (`p028`):** Data handling awareness teaches users to classify, store, transmit y dispose of information safely. Cita: “**classify, store, transmit, and dispose of information safely**”.
19. **EXPLÍCITO (`p028`):** Remote work awareness teaches users to protect devices and networks outside the office. Cita: “**protect devices and networks outside the office**”.
20. **EXPLÍCITO (`p028`):** Social engineering awareness teaches users to recognize manipulation attempts. Cita: “**recognize manipulation attempts**”.
21. **EXPLÍCITO (`p028`):** Awareness campaigns reinforce secure behavior. Cita: “**reinforce secure behavior**”.
22. **EXPLÍCITO (`p028`):** Training completion metrics measure user participation. Cita: “**measure user participation**”.
23. **EXPLÍCITO (`p028`):** Simulated phishing exercises measure user response. Cita: “**measure user response to phishing scenarios**”.
24. **EXPLÍCITO (`p028`):** La user response medida es respecto de phishing scenarios. Cita: “**response to phishing scenarios**”. `in_context_of` es una generalización **ENTRAÑADA**; una relación causal sería **NO SOPORTADO**.

Interpretaciones adicionales relevantes:

- Que phishing/password/data-handling/remote-work/social-engineering awareness sean subclases de SecurityAwareness es **PLAUSIBLE**, pero no está formulado como taxonomía.
- Que Employees sean idénticos a Users es **NO SOPORTADO**.
- Que SecurityAwarenessTraining “expects” behavior es **NO SOPORTADO**: “expected” modifica “behavior” dentro del tema educativo.
- Que las prácticas de `p027` sean partes formales de HumanResourceSecurity es **PLAUSIBLE** por proximidad temática, no una relación literal.
- No hay ninguna interpretación **CONTRADICHA** por una negación textual; los errores detectados son principalmente no soportados, pérdidas o desanclajes de identidad.

### Taxonomías explícitas

No hay relaciones explícitas `is-a`, `subclass-of`, generalizaciones ni membresías de instancia. Los compuestos “Phishing awareness”, “Password awareness”, “Role-based training”, etc. denominan conceptos, pero por sí solos no autorizan una jerarquía formal. La ausencia de taxonomías y de type assertions es, por tanto, una decisión conservadora correcta.

### Modalidad

- **Deóntica explícita (`p027`):** tres usos de “must” sobre protect, report y follow. La modalidad no debe reducirse a una acción factual ordinaria.
- **Temporal (`p027`):** before/during/after employment; before employment; y la condición “when employment ends”.
- **Contenido enseñado (`p028`):** los infinitivos posteriores a “teaches users to” tienen alcance instruccional; no son hechos de ejecución actual.
- **Calificadores:** “suspected” conserva incertidumbre sobre incidents; “expected” califica behavior sin identificar quién lo espera; “strong” califica passwords; “safely” expresa manera; “outside the office” expresa ubicación del evento de protección.
- **Asertividad:** el resto son afirmaciones genéricas en presente, sin negación ni posibilidad explícita.

### Ambigüedades

- **`p027`, alcance temporal:** “before, during, and after employment” se interpreta como alcance de `addresses`; es la lectura gramatical más fuerte.
- **`p027`, preposición “for”:** “knowledge for responsibilities” y “consequences for violations” soportan relación, pero no una semántica más específica sin añadir conocimiento.
- **`p028`, alcance de “safely”:** puede modificar toda la coordinación o, en una lectura sintáctica estrecha, solo `dispose`. Aplicarlo a las cuatro acciones es **PLAUSIBLE/lectura coordinada**, no debe presentarse como certeza superior a la frase.
- **`p028`, “outside the office”:** la lectura principal ubica la protección; no afirma que los dispositivos y redes sean intrínsecamente “de fuera”.
- **Singularización:** normalizar plurales genéricos a `Employee`, `User`, `Policy`, etc. es compatible; no autoriza crear individuos.

## 2. Resultado por etapa

Escala: 0 = ausente/incorrecto, 1 = grave, 2 = parcial, 3 = adecuado con defectos, 4 = completo y fiel.

| Paso | Etapa | Fidelidad | Cobertura | Precisión | Trazabilidad | Coherencia | Estado |
|---:|---|---:|---:|---:|---:|---:|---|
| 01 | input_intake | 4 | 4 | 4 | 4 | 4 | OK |
| 02 | preprocessing | 4 | 4 | 4 | 4 | 4 | OK |
| 03 | sentence_segmentation | 4 | 4 | 4 | 4 | 4 | OK |
| 04 | tokenization | 4 | 4 | 4 | 4 | 4 | OK |
| 05 | linguistic_annotation | 3 | 4 | 3 | 4 | 3 | WARN |
| 06 | entity_extraction | 4 | 4 | 4 | 4 | 4 | OK |
| 07 | concept_extraction | 3 | 4 | 3 | 4 | 3 | WARN |
| 08 | coreference_resolution | 4 | 4 | 4 | 4 | 4 | OK |
| 09 | relation_extraction | 2 | 2 | 2 | 3 | 2 | FAIL |
| 10 | canonical_claims / semantic_claims | 4 | 4 | 4 | 4 | 4 | OK |
| 11 | semantic_debug_ir | 3 | 3 | 4 | 4 | 2 | WARN |
| 12 | triple_extraction | 4 | 4 | 4 | 3 | 3 | WARN |
| 13 | taxonomy_induction | 4 | 4 | 4 | 4 | 4 | OK |
| 14 | type_assertion | 4 | 4 | 4 | 4 | 4 | OK |
| 15 | semantic_quality | 2 | 2 | 2 | 4 | 2 | FAIL |
| 16 | output_generation | 4 | 4 | 4 | 3 | 3 | WARN |

## 3. Hallazgos

### Q-infosec_p027_p028-05-1

- **Severidad:** MEDIA
- **Tipo:** ANOTACIÓN LINGÜÍSTICA / PRECISIÓN
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** `p027`: “Security awareness training educates users about policies, threats, and **expected behavior**.”
- **Archivo y JSON Pointer:** `observed_p027_p028_05_linguistic_annotation.json`, `/tokens/44` y `/tokens/45`.
- **Evaluación razonada:** `expected` aparece como `VERB`, dependencia `conj` de `educates`, y `behavior` como su objeto. En la frase fuente, “expected behavior” es un sintagma nominal temático; no afirma que training sea el sujeto de `expect`. La lectura `training expects behavior` es **NO SOPORTADA**.
- **Impacto downstream:** origina la relación espuria de paso 09. El paso 10 la elimina y conserva `ExpectedBehavior` solo como topic, por lo que el error no llega al RDF final.

### Q-infosec_p027_p028-05-2

- **Severidad:** MEDIA
- **Tipo:** ANOTACIÓN LINGÜÍSTICA / ESTRUCTURA SINTÁCTICA
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** `p028`: “**Data handling awareness** teaches users to classify, store, transmit, and dispose of information safely.”
- **Archivo y JSON Pointer:** `observed_p027_p028_05_linguistic_annotation.json`, `/tokens/122`, `/tokens/123` y `/tokens/124`.
- **Evaluación razonada:** el análisis marca `Data` como sujeto de `teaches` y `awareness` como objeto de `handling`, fragmentando el sujeto compuesto literal. La unidad semántica explícita es “Data handling awareness”.
- **Impacto downstream:** produce un candidato conceptual solapado y una relación de paso 09 con sujeto `data`. El paso 10 reconstruye correctamente `DataHandlingAwareness`, de modo que la degradación queda corregida antes de triples.

### Q-infosec_p027_p028-07-1

- **Severidad:** BAJA
- **Tipo:** PRECISIÓN DE CONCEPTO
- **Atribución:** ERROR_PROPAGADO
- **Cita literal:** `p028`: “**Data handling awareness** teaches users…”
- **Archivo y JSON Pointer:** `observed_p027_p028_07_concept_extraction.json`, `/concepts/36` y `/concepts/37`.
- **Evaluación razonada:** se emiten simultáneamente `Data` y `Data handling awareness` sobre spans solapados. `Data` no funciona aquí como participante independiente de `teaches`; procede del análisis sintáctico defectuoso del paso 05. El candidato completo sí es fiel.
- **Impacto downstream:** el concepto aislado alimenta la identidad equivocada de la relación del paso 09. No se vuelve a contar como error nuevo allí y no sobrevive a canonical claims.

### Q-infosec_p027_p028-09-1

- **Severidad:** ALTA
- **Tipo:** RELACIÓN NO SOPORTADA
- **Atribución:** ERROR_PROPAGADO
- **Cita literal:** `p027`: “Security awareness training educates users about policies, threats, and **expected behavior**.”
- **Archivo y JSON Pointer:** `observed_p027_p028_09_relation_extraction.json`, `/relations/14`.
- **Evaluación razonada:** la relación `training —expect→ behavior` convierte un modificador nominal en una proposición. Es **NO SOPORTADA**, no una paráfrasis de la fuente. Su origen está en Q-infosec_p027_p028-05-1; por ello no se contabiliza como un segundo origen.
- **Impacto downstream:** sería una invención grave si se materializara. El paso 10 la descarta y el output final no contiene `expects`.

### Q-infosec_p027_p028-09-2

- **Severidad:** ALTA
- **Tipo:** IDENTIDAD SEMÁNTICA Y COBERTURA
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** `p027`: “**Role-based training** provides specialized security knowledge…”; `p028`: “**Password awareness** teaches users…” y “**Data handling awareness** teaches users…”.
- **Archivo y JSON Pointer:** `observed_p027_p028_09_relation_extraction.json`, `/relations/16/subject_ref`, `/relations/0/subject_ref`, `/relations/12/subject_ref` y `/relations`.
- **Evaluación razonada:** Role-based training se referencia como el concepto de Security awareness training; Password awareness se referencia como Security awareness; y Data handling awareness se reduce a Data. Además, no hay relaciones para las proposiciones raíz de phishing awareness, remote work awareness ni social engineering awareness. Los spans de evidencia son correctos, pero no compensan la identidad errónea ni las omisiones.
- **Impacto downstream:** el paso 09 no es utilizable como modelo semántico autónomo. El paso 10 corrige las identidades y recupera las tres familias omitidas, evitando propagación a triples/RDF.

### Q-infosec_p027_p028-09-3

- **Severidad:** ALTA
- **Tipo:** PÉRDIDA DE MODALIDAD
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** `p027`: “Employees **must protect** credentials. Employees **must report** suspected incidents. Employees **must follow** acceptable use policies.”
- **Archivo y JSON Pointer:** `observed_p027_p028_09_relation_extraction.json`, `/relations/2`, `/relations/3` y `/relations/15` (miembro `modality` ausente).
- **Evaluación razonada:** las relaciones se reducen a `protect`, `report` y `follow`; así no distinguen obligación de hecho ordinario. La pérdida cambia el tipo de afirmación.
- **Impacto downstream:** el paso 10 lo corrige con `modality: must` y predicados `mustProtect`, `mustReport`, `mustFollow`; la pérdida no llega al output final.

### Q-infosec_p027_p028-10-1

- **Severidad:** INFO
- **Tipo:** RECUPERACIÓN SEMÁNTICA
- **Atribución:** ERROR_CORREGIDO
- **Cita literal:** `p027`: “Employees must protect credentials”; `p028`: “Phishing awareness teaches users to identify suspicious messages.”
- **Archivo y JSON Pointer:** `observed_p027_p028_10_canonical_claims.json`, `/canonical_claims/claims/8`, `/canonical_claims/claims/12`, `/canonical_claims/claims/13` y, de forma análoga, `/canonical_claims/claims/14` a `/canonical_claims/claims/26`.
- **Evaluación razonada:** canonical claims restaura sujetos específicos, modalidad deóntica y alcance `taught_action`; también recupera las acciones coordinadas, condición, temporalidad, manera y ubicación. Las 19 oraciones quedan cubiertas por 33 claims trazados a evidencia y `sentence_id`. Los cuatro candidatos temporales defectuosos están explícitamente rechazados, no proyectados.
- **Impacto downstream:** corrige las degradaciones de 05/07/09 y se convierte en la base semántica fiel de triples y output.

### Q-infosec_p027_p028-11-1

- **Severidad:** MEDIA
- **Tipo:** COHERENCIA ESTRUCTURAL DEL DEBUG IR
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** `p027`: “about **policies, threats, and expected behavior**” y “when **employment** ends”; `p028`: “outside the **office**”.
- **Archivo y JSON Pointer:** `observed_p027_p028_11_semantic_debug_ir.json`, `/artifacts/semantic_debug_ir/relations/2/topics`, `/artifacts/semantic_debug_ir/relations/7/condition_subject`, `/artifacts/semantic_debug_ir/relations/23/location` y `/artifacts/semantic_debug_ir/entities`.
- **Evaluación razonada:** las relaciones referencian `Policy`, `Threat`, `ExpectedBehavior`, `Employment` y `Office`, pero esos términos no aparecen en `entities` del sidecar. El contenido de las relaciones es fiel, pero el IR de depuración no es referencialmente autocontenido.
- **Impacto downstream:** dificulta inspección y validación automática del sidecar. Output generation vuelve a crear esas clases, por lo que el defecto estructural no causa pérdida final.

### Q-infosec_p027_p028-12-1

- **Severidad:** BAJA
- **Tipo:** TRAZABILIDAD DE REFERENCIAS
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** `p028`: “Password awareness teaches users to create and protect strong passwords.”
- **Archivo y JSON Pointer:** `observed_p027_p028_12_triple_extraction.json`, `/triples/0/subject_ref`, `/triples/0/predicate_ref` y `/triples/0/object_ref` (patrón repetido en los triples).
- **Evaluación razonada:** los tres campos `*_ref` apuntan al mismo claim, no a referencias diferenciadas de sujeto, predicado y objeto. `relation_id` ya aporta el vínculo al claim, así que los nombres de esos campos prometen una granularidad que el contenido no ofrece.
- **Impacto downstream:** no altera el SPO ni su evidencia, pero limita auditorías de identidad término-a-término. El modelo final reconstruye IRIs separados y mantiene el `claim_id` en scoped relations o en projection.

### Q-infosec_p027_p028-15-1

- **Severidad:** ALTA
- **Tipo:** PUNTO CIEGO DE CALIDAD
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** `p027`: “expected behavior” y “Employees must…”; `p028`: “Data handling awareness…”
- **Archivo y JSON Pointer:** `observed_p027_p028_15_semantic_quality.json`, `/semantic_quality_report/quality_score`, `/semantic_quality_report/relation_gaps`, `/semantic_quality_report/semantic_integrity_issues` y `/semantic_quality_report/warnings`.
- **Evaluación razonada:** el informe declara `quality_score: 1.0`, cero gaps y cero warnings pese a que el payload previo contiene una relación no soportada, sujetos desanclados, modalidad ausente en relation extraction, referencias de triple poco granulares y un debug IR no autocontenido. Que canonical claims haya corregido el camino de proyección no vuelve perfectas todas las estructuras que esta etapa declara evaluar.
- **Impacto downstream:** no introduce contenido semántico, pero genera confianza excesiva y no protege a consumidores que inspeccionen relaciones/conceptos en lugar de canonical claims.

### Q-infosec_p027_p028-16-1

- **Severidad:** BAJA
- **Tipo:** DUPLICACIÓN ESTRUCTURAL
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** `p027`: “Human resource security…”; `p028`: “Security awareness…” (el defecto afecta a las clases derivadas de ambos párrafos).
- **Archivo y JSON Pointer:** `observed_p027_p028_16_output_generation.json`, `/output/graph/classes` y `/output/graph/schema/classes`; también `/output/graph/object_property_schema` y `/output/graph/schema/object_properties`.
- **Evaluación razonada:** `classes` y `schema/classes` contienen exactamente el mismo array de 46 clases. Las propiedades se exponen igualmente en dos vistas semánticamente redundantes. No duplica los 33 claims —20 facts más 13 scoped relations—, pero incumple en sentido estricto el requisito de un modelo final sin duplicación estructural.
- **Impacto downstream:** consumidores que recorran ambas vistas sin conocer el contrato pueden contar o materializar dos veces el esquema. No hay invención de hechos fuente.

## 4. Diagnóstico

- **Primera degradación:** paso 05. El análisis de “expected behavior” y “Data handling awareness” introduce lecturas sintácticas incorrectas.
- **Principal pérdida:** paso 09 pierde modalidad deóntica, acciones instruccionales, varias relaciones raíz y especificidad de sujetos. Es el punto semánticamente más débil del pipeline aislado.
- **Principal contenido no soportado:** `SecurityAwarenessTraining expects ExpectedBehavior` en el paso 09. Se origina en paso 05 y queda **ERROR_CORREGIDO** en paso 10.
- **Errores que llegan a RDF/OWL:** no llega ninguna relación semántica no soportada detectada. El output conserva los 33 claims exactamente una vez entre `facts` y `scoped_relations`, mantiene must, taught_action, temporalidad, condición, topics, manera y ubicación, y no inventa taxonomías ni instancias. Sí llegan debilidades de trazabilidad y duplicación de vistas del esquema.
- **Aciertos:** intake, normalización, segmentación y tokenización son íntegros; entity extraction y coreference son prudentemente vacíos; canonical claims corrige las degradaciones previas; triple extraction conserva los 33 claims; taxonomy/type assertion evita inferencias no autorizadas; el modelo final incluye las clases auxiliares necesarias para topics y scopes.
- **Incertidumbres:** el alcance de `safely`, la semántica precisa de `for`, la ubicación “outside the office” y el modelado de sustantivos genéricos como clases admiten alternativas. El pipeline usa representaciones razonables y suficientemente marcadas; no se penaliza el conservadurismo taxonómico.

## 5. Veredicto

- **Calidad global:** **87/100**.
- **Output final:** **parcialmente fiel**. Semánticamente conserva el contenido literal y sus alcances sin invenciones materiales detectadas; no alcanza “fiel” en sentido estricto por duplicación estructural y trazabilidad desigual entre facts, scoped relations y términos.
- **Tres correcciones prioritarias:**
  1. Corregir o blindar relation extraction frente a sujetos compuestos, adjetivos participiales y modalidad, eliminando `training expects behavior` y preservando las identidades específicas desde el paso 09.
  2. Hacer que semantic quality audite también relaciones candidatas, referencias y consistencia del debug IR, evitando `quality_score: 1.0` cuando existen defectos observables aunque canonical claims los corrija.
  3. Emitir una sola vista canónica del esquema final y conservar referencias explícitas a claim, sentence y source en todos los facts materializados.

Siguiente caso pendiente: infosec_p029_p030.
