# Revisión semántica: infosec_p041_p042

## 1. Lectura independiente

### Resumen

Los dos párrafos combinan dos planos distintos:

1. **p041** presenta un escenario ilustrativo de brecha de datos: un usuario no autorizado accede a un repositorio restringido, se registran y detectan hechos, distintos actores organizativos intervienen y se adoptan acciones correctivas.
2. **p042** formula una capacidad deseada de ORION y declara un pequeño vocabulario de clases con cuatro taxonomías explícitas.

La lectura separa cuidadosamente las menciones de escenario de **p041** —potencialmente instancias u ocurrencias— de las clases declaradas en **p042**. No se presupone conocimiento de seguridad externo al texto.

### Conceptos

- **Tema principal de p041:** escenario de brecha de datos, control de acceso, protección de datos, detección, respuesta, evaluación de notificación, obligaciones regulatorias y acciones correctivas.
- **Conceptos explícitos del escenario:** `data breach scenario`, `access control`, `data protection`, `unauthorized user`, `restricted document repository`, `confidential information`, `personal data`, `unauthorized access`, `access control policy`, `audit logs`, `access event`, `detection rule`, `security alert`, `security analyst`, `incident response team`, `data breach`, `privacy officer`, `data subjects`, `legal team`, `regulatory obligations`, `organization`, `corrective actions` y `recurrence`.
- **Entidad nombrada explícita:** `ORION` en p042. El texto no declara si es organización, producto, sistema, individuo ontológico o clase.
- **Participantes/instancias discursivas de p041:** un usuario no autorizado, un repositorio restringido, el acceso narrado, unos registros de auditoría, una regla de detección, una alerta, un analista, un equipo de respuesta, una brecha confirmada, un responsable de privacidad, sujetos de datos, un equipo legal, una organización y sus acciones correctivas.
- **Clases explícitamente calificadas como importantes en p042:** `information asset`, `security control`, `security incident`, `authentication factor`, `threat actor`, `compliance requirement`, `cloud workload`, `endpoint` y `supplier`.
- **Superclases explícitas adicionales:** `credential` aparece como superclase de una taxonomía; por tanto, que funciona como clase está **ENTRAÑADO**, aunque no se la declara “important class”.
- **Definiciones/clasificaciones:** las únicas definiciones taxonómicas literales son las cuatro construcciones “are subclasses of”. No hay sinonimias, equivalencias, disyunciones ni definiciones necesarias y suficientes.
- **Distinciones que deben conservarse:** `confidential document` no es lo mismo que `restricted document repository`; `corrective actions` del escenario no se identifican literalmente con la clase `corrective control`; `unauthorized user` no se declara `threat actor`.

### Proposiciones con evidencia

Todas las proposiciones siguientes son **EXPLÍCITAS**; la distribución atómica de los miembros de una coordinación mantiene el contenido literal de la lista.

**p041 — escenario**

1. El escenario de brecha ilustra la importancia del control de acceso — “illustrates the importance of access control” (p041).
2. El mismo escenario ilustra la importancia de la protección de datos — “and data protection” (p041).
3. Un usuario no autorizado accede a un repositorio documental restringido — “An unauthorized user accesses a restricted document repository” (p041).
4. El repositorio restringido almacena información confidencial — “stores confidential information” (p041).
5. El repositorio restringido almacena datos personales — “and personal data” (p041).
6. El acceso no autorizado viola la política de control de acceso — “violates the access control policy” (p041).
7. Los registros de auditoría registran el evento de acceso — “Audit logs record the access event” (p041).
8. Una regla de detección genera una alerta de seguridad — “A detection rule generates a security alert” (p041).
9. El analista de seguridad investiga la alerta — “The security analyst investigates the alert” (p041).
10. El equipo de respuesta a incidentes confirma una brecha de datos — “confirms a data breach” (p041).
11. El responsable de privacidad evalúa la cuestión de si los sujetos de datos deben ser notificados — “assesses whether data subjects must be notified” (p041). No afirma el resultado de esa evaluación.
12. El equipo legal evalúa obligaciones regulatorias — “evaluates regulatory obligations” (p041).
13. La organización implementa acciones correctivas — “implements corrective actions” (p041).
14. La prevención de la recurrencia es la finalidad de esas acciones — “to prevent recurrence” (p041). No afirma que la prevención ya haya tenido éxito.

**p042 — capacidad deseada y clases**

15. ORION debería poder identificar conceptos de seguridad — “should be able to identify security concepts” (p042).
16. ORION debería poder clasificar relaciones jerárquicas — “classify hierarchical relationships” (p042).
17. ORION debería poder extraer relaciones significativas de “this text” — “extract meaningful relationships from this text” (p042).
18. `information asset` es una clase importante — “Information asset ... are important classes” (p042).
19. `security control` es una clase importante — misma cita coordinada (p042).
20. `security incident` es una clase importante — misma cita coordinada (p042).
21. `authentication factor` es una clase importante — misma cita coordinada (p042).
22. `threat actor` es una clase importante — misma cita coordinada (p042).
23. `compliance requirement` es una clase importante — misma cita coordinada (p042).
24. `cloud workload` es una clase importante — misma cita coordinada (p042).
25. `endpoint` es una clase importante — misma cita coordinada (p042).
26. `supplier` es una clase importante — misma cita coordinada (p042).
27. `confidential document` es subclase de `information asset` — “are subclasses of information asset” (p042).
28. `corporate database` es subclase de `information asset` — misma cita coordinada (p042).
29. `customer record` es subclase de `information asset` — misma cita coordinada (p042).
30. `source code repository` es subclase de `information asset` — misma cita coordinada (p042).
31. `preventive control` es subclase de `security control` — “are subclasses of security control” (p042).
32. `detective control` es subclase de `security control` — misma cita coordinada (p042).
33. `corrective control` es subclase de `security control` — misma cita coordinada (p042).
34. `compensating control` es subclase de `security control` — misma cita coordinada (p042).
35. `password` es subclase de `credential` — “are subclasses of credential” (p042).
36. `certificate` es subclase de `credential` — misma cita coordinada (p042).
37. `access token` es subclase de `credential` — misma cita coordinada (p042).
38. `API key` es subclase de `credential` — misma cita coordinada (p042).
39. `private key` es subclase de `credential` — misma cita coordinada (p042).
40. `malware infection` es subclase de `security incident` — “are subclasses of security incident” (p042).
41. `phishing attack` es subclase de `security incident` — misma cita coordinada (p042).
42. `ransomware attack` es subclase de `security incident` — misma cita coordinada (p042).
43. `data breach` es subclase de `security incident` — misma cita coordinada (p042).
44. `denial-of-service attack` es subclase de `security incident` — misma cita coordinada (p042).
45. `unauthorized access` es subclase de `security incident` — misma cita coordinada (p042).
46. `insider misuse` es subclase de `security incident` — misma cita coordinada (p042).
47. `lost device incident` es subclase de `security incident` — misma cita coordinada (p042).

### Taxonomías explícitas

| Subclases explícitas | Superclase explícita | Cantidad |
|---|---|---:|
| Confidential document; corporate database; customer record; source code repository | Information asset | 4 |
| Preventive control; detective control; corrective control; compensating control | Security control | 4 |
| Password; certificate; access token; API key; private key | Credential | 5 |
| Malware infection; phishing attack; ransomware attack; data breach; denial-of-service attack; unauthorized access; insider misuse; lost device incident | Security incident | 8 |

Total: **21 relaciones directas de subclase**. La lista de nueve “important classes” es una clasificación metamodelo explícita, pero no expresa subordinación entre esas nueve clases.

### Modalidad

- Las oraciones narrativas de p041 son aseveraciones en presente dentro de un **escenario ilustrativo**.
- “whether ... must be notified” (p041) contiene una obligación posible dentro del contenido evaluado. Es **NO SOPORTADO** proyectar fuera de ese ámbito que la notificación es obligatoria o que ocurrió.
- “to prevent recurrence” (p041) expresa **finalidad**. Es **NO SOPORTADO** convertirla en prevención consumada.
- “ORION should be able to ...” (p042) expresa capacidad deseada/normativa. Es **NO SOPORTADO** afirmar que ORION ya posee esas capacidades.
- “important” (p042) es una calificación evaluativa explícita, no una relación taxonómica adicional.

### Ambigüedades

- **ENTRAÑADO:** “the restricted document repository” retoma el repositorio introducido inmediatamente antes; la repetición léxica y el artículo definido sostienen la correferencia.
- **ENTRAÑADO:** “the alert” retoma la “security alert” generada en la oración anterior.
- **ENTRAÑADO:** la acción “accesses” introduce una ocurrencia de acceso, pero el nombre técnico `UnauthorizedAccessOccurrence` no es literal.
- **PLAUSIBLE:** “the unauthorized access” y “the access event” podrían referirse a la misma ocurrencia; el texto no declara su identidad formal.
- **PLAUSIBLE:** la brecha confirmada puede ser la del escenario inicial; no hay un enlace anafórico inequívoco entre “data breach scenario” y “a data breach”.
- **AMBIGUO/PLAUSIBLE:** “recurrence” puede ser recurrencia del acceso, de la brecha o del incidente global.
- **AMBIGUO:** “this text” puede abarcar p042, ambos párrafos o el material suministrado como conjunto.
- **NO SOPORTADO:** identificar la organización de p041 con ORION, el usuario no autorizado con `threat actor`, las acciones correctivas con `corrective control`, o el repositorio restringido con `confidential document`.
- **NO SOPORTADO:** declarar ORION como clase a partir de su uso como sujeto de una capacidad deseada.
- **CONTRADICHO:** interpretar que el acceso no autorizado cumple la política contradice “violates the access control policy” (p041).

## 2. Resultado por etapa

Escala: 0 = inexistente/incorrecto; 1 = muy deficiente; 2 = deficiente; 3 = adecuado con reservas; 4 = sólido.

| Paso | Etapa | Fidelidad | Cobertura | Precisión | Trazabilidad | Coherencia | Estado |
|---:|---|---:|---:|---:|---:|---:|---|
| 01 | input_intake | 4 | 4 | 4 | 4 | 4 | OK |
| 02 | preprocessing | 4 | 4 | 4 | 3 | 4 | OK |
| 03 | sentence_segmentation | 4 | 4 | 4 | 4 | 4 | OK |
| 04 | tokenization | 4 | 4 | 4 | 4 | 4 | OK |
| 05 | linguistic_annotation | 2 | 4 | 2 | 4 | 2 | FAIL |
| 06 | entity_extraction | 4 | 3 | 4 | 4 | 4 | WARN |
| 07 | concept_extraction | 2 | 3 | 2 | 4 | 2 | FAIL |
| 08 | coreference_resolution | 4 | 1 | 4 | 1 | 4 | FAIL |
| 09 | relation_extraction | 2 | 1 | 2 | 4 | 2 | FAIL |
| 10 | canonical_claims / semantic_claims | 4 | 4 | 4 | 4 | 4 | OK |
| 11 | semantic_debug_ir | 4 | 4 | 4 | 4 | 4 | OK |
| 12 | triple_extraction | 4 | 4 | 4 | 4 | 4 | OK |
| 13 | taxonomy_induction | 4 | 4 | 4 | 4 | 4 | OK |
| 14 | type_assertion | 4 | 4 | 4 | 4 | 4 | OK |
| 15 | semantic_quality | 2 | 3 | 2 | 4 | 2 | FAIL |
| 16 | output_generation | 3 | 4 | 3 | 4 | 3 | WARN |

La etapa 06 no se penaliza por no efectuar extracción de conceptos de dominio: su contrato es NER genérico y el texto apenas contiene una entidad nombrada inequívoca, ORION. La salida vacía es conservadora, aunque pierde esa observación potencial.

## 3. Hallazgos

### Q-infosec_p041_p042-05-1

- **Severidad:** ALTA
- **Tipo:** ANOTACIÓN_LINGÜÍSTICA
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** “The restricted document repository stores confidential information and personal data.” (p041)
- **Archivo:** `tests/smoke/cases/infosec_p041_p042/artifacts/pipeline_outputs/observed_p041_p042_05_linguistic_annotation.json`
- **JSON Pointer:** `/tokens/27` (con efectos visibles también en `/tokens/23`–`/tokens/32`)
- **Evaluación razonada:** `stores` se anota como `NOUN`, dependencia `nmod`, mientras `information` queda como `ROOT`. Esto contradice la estructura predicativa literal: el repositorio es sujeto, `stores` es verbo y los dos objetos coordinados son `confidential information` y `personal data`.
- **Impacto downstream:** origina el concepto proposicional espurio del paso 07 y la omisión completa de ambas relaciones `stores` en el paso 09. El paso 10 corrige el error mediante dos claims fieles, por lo que no llega al RDF final.

### Q-infosec_p041_p042-05-2

- **Severidad:** ALTA
- **Tipo:** ANOTACIÓN_LINGÜÍSTICA
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** “Audit logs record the access event.” (p041)
- **Archivo:** `tests/smoke/cases/infosec_p041_p042/artifacts/pipeline_outputs/observed_p041_p042_05_linguistic_annotation.json`
- **JSON Pointer:** `/tokens/44` y `/tokens/45`
- **Evaluación razonada:** `logs` se trata como verbo raíz y `record` como sustantivo, invirtiendo la lectura literal `Audit logs` (sujeto nominal) + `record` (verbo) + `the access event` (objeto).
- **Impacto downstream:** el paso 07 propone `Audit`, `record` y `record the access event` como conceptos; el paso 09 genera `audit —log→ record` y `audit —log→ access event`, relaciones no fieles. El claim `AuditLogs record AccessEvent` del paso 10 corrige la cadena antes de triples y RDF.

### Q-infosec_p041_p042-07-1

- **Severidad:** ALTA
- **Tipo:** EXTRACCIÓN_DE_CONCEPTOS
- **Atribución:** ERROR_AMPLIFICADO
- **Cita literal:** “The restricted document repository stores confidential information and personal data.” (p041)
- **Archivo:** `tests/smoke/cases/infosec_p041_p042/artifacts/pipeline_outputs/observed_p041_p042_07_concept_extraction.json`
- **JSON Pointer:** `/concepts/4`
- **Evaluación razonada:** una proposición completa, incluido el predicado `stores`, se eleva a candidato de concepto con confianza `0.95`. No es un concepto atómico fiel y, además, desplaza los conceptos explícitos `confidential information` y `personal data`. Casos análogos aparecen en `/concepts/9` para “record the access event” (p041) y `/concepts/48` para la oración taxonómica de `credential` (p042).
- **Impacto downstream:** aumenta ruido, dificulta relaciones y obliga al paso 15 a excluir chunks proposicionales. La semántica atómica se recupera en los claims del paso 10.

### Q-infosec_p041_p042-08-1

- **Severidad:** ALTA
- **Tipo:** CORREFERENCIA
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** “A detection rule generates a security alert. The security analyst investigates the alert.” (p041)
- **Archivo:** `tests/smoke/cases/infosec_p041_p042/artifacts/pipeline_outputs/observed_p041_p042_08_coreference_resolution.json`
- **JSON Pointer:** `/coreferences`
- **Evaluación razonada:** la lista vacía omite al menos la correferencia fuertemente entrañada `the alert` → `security alert`, además de la repetición definida del repositorio. Se respeta el conservadurismo ante identidades ambiguas como `access event`, pero no hay ambigüedad material en el caso de la alerta inmediata.
- **Impacto downstream:** el paso 09 investiga un concepto genérico `alert` en vez de enlazar la alerta de seguridad generada. El paso 10 lo corrige explícitamente con `discourse_resolution: definite_antecedent`.

### Q-infosec_p041_p042-09-1

- **Severidad:** ALTA
- **Tipo:** EXTRACCIÓN_DE_RELACIONES / IDENTIDAD
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** “The legal team evaluates regulatory obligations.” (p041)
- **Archivo:** `tests/smoke/cases/infosec_p041_p042/artifacts/pipeline_outputs/observed_p041_p042_09_relation_extraction.json`
- **JSON Pointer:** `/relations/9/subject_ref`
- **Evaluación razonada:** la relación textual dice `team —evaluate→ regulatory obligation`, pero `subject_ref` apunta a `con-cde247ad0f9e6bf5`, el concepto `incident response team`, no a `legal team`. Compartir el lema `team` no autoriza a identificar ambos participantes.
- **Impacto downstream:** si se proyectara directamente, atribuiría la evaluación regulatoria al actor equivocado. El paso 10 lo corrige a `LegalTeam evaluates RegulatoryObligation`, y ese error no llega al RDF.

### Q-infosec_p041_p042-09-2

- **Severidad:** CRÍTICA
- **Tipo:** COBERTURA_RELACIONAL_Y_TAXONÓMICA
- **Atribución:** ERROR_PROPAGADO
- **Cita literal:** “Confidential document, corporate database, customer record, and source code repository are subclasses of information asset.” (p042)
- **Archivo:** `tests/smoke/cases/infosec_p041_p042/artifacts/pipeline_outputs/observed_p041_p042_09_relation_extraction.json`
- **JSON Pointer:** `/relations/2` y, globalmente, `/relations`
- **Evaluación razonada:** la etapa no distribuye las coordinaciones taxonómicas. Solo representa el primer miembro de dos listas y lo hace como `be → subclass`, no como relación directa con la superclase. Omite por completo las listas de `security control` y `credential`. También faltan relaciones narrativas explícitas de p041, entre ellas `stores`, la evaluación modal del responsable de privacidad y la finalidad de prevenir recurrencia.
- **Impacto downstream:** es la principal pérdida del flujo lingüístico ordinario. El paso 10 corrige la cobertura y produce las 21 relaciones taxonómicas y las relaciones narrativas ausentes; por ello el defecto no se repite como error nuevo en los pasos 12–14.

### Q-infosec_p041_p042-10-1

- **Severidad:** INFORMATIVA (acierto decisivo)
- **Tipo:** RECUPERACIÓN_CANÓNICA
- **Atribución:** ERROR_CORREGIDO
- **Cita literal:** “Password, certificate, access token, API key, and private key are subclasses of credential.” (p042)
- **Archivo:** `tests/smoke/cases/infosec_p041_p042/artifacts/pipeline_outputs/observed_p041_p042_10_canonical_claims.json`
- **JSON Pointer:** `/canonical_claims/claims/38`–`/canonical_claims/claims/42`
- **Evaluación razonada:** la etapa reconstruye fielmente los cinco miembros de la taxonomía y, en conjunto, las 51 claims: relaciones narrativas, modalidades, nueve declaraciones de clase, 21 subordinaciones y dos ocurrencias tipadas con sus enlaces. Cada claim conserva evidencia, párrafo y oración.
- **Impacto downstream:** corrige los errores propagados de los pasos 05–09 y proporciona una base sólida a triples, taxonomía, tipos y salida RDF. Las reificaciones `UnauthorizedAccessOccurrence` y `DataBreachOccurrence` son interpretaciones entrañadas, no expresiones literales, pero se mantienen separadas de sus clases y con evidencia.

### Q-infosec_p041_p042-15-1

- **Severidad:** MEDIA
- **Tipo:** EXCLUSIÓN_SEMÁNTICA_INCORRECTA
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** “denial-of-service attack ... [is a] subclass of security incident.” (p042)
- **Archivo:** `tests/smoke/cases/infosec_p041_p042/artifacts/pipeline_outputs/observed_p041_p042_15_semantic_quality.json`
- **JSON Pointer:** `/excluded_concepts/7` y `/semantic_quality_report/concept_noise/8`
- **Evaluación razonada:** `denial-of-service attack` es un miembro atómico y explícito de la taxonomía, no un chunk que haya absorbido un predicado. Su exclusión como `predicate_absorbed_into_concept` es un falso positivo. Además, el mismo reporte declara `rdf_readiness: false` y `quality_score: 0.5` pese a no registrar claims inválidas ni problemas de integridad, lo que reduce su coherencia diagnóstica.
- **Impacto downstream:** podría eliminar una clase válida si la proyección dependiera de `excluded_concepts`. En este caso el paso 16 conserva `DenialOfServiceAttack` y su `rdfs:subClassOf`, por lo que el error queda corregido/contendido en la salida final.

### Q-infosec_p041_p042-16-1

- **Severidad:** MEDIA
- **Tipo:** PROYECCIÓN_RDF / CLASE_NO_SOPORTADA
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** “ORION should be able to identify security concepts, classify hierarchical relationships, and extract meaningful relationships from this text.” (p042)
- **Archivo:** `tests/smoke/cases/infosec_p041_p042/artifacts/pipeline_outputs/observed_p041_p042_16_output_generation.json`
- **JSON Pointer:** `/output/graph/classes/23`
- **Evaluación razonada:** el modelo declara `orion:Orion` dentro de `classes`. El texto usa ORION como sujeto de una capacidad deseada, pero no afirma que ORION sea una clase. La modalidad sí se conserva correctamente en `/output/graph/scoped_relations/2`–`/output/graph/scoped_relations/4`; el problema es exclusivamente el tipado adicional como clase.
- **Impacto downstream:** introduce en OWL/RDF una categoría ontológica no soportada y confunde actor/recurso con clase. Es el principal contenido no soportado que alcanza el modelo final.

### Q-infosec_p041_p042-16-2

- **Severidad:** BAJA
- **Tipo:** DUPLICACIÓN_ESTRUCTURAL
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** “Information asset ... and supplier are important classes.” (p042)
- **Archivo:** `tests/smoke/cases/infosec_p041_p042/artifacts/pipeline_outputs/observed_p041_p042_16_output_generation.json`
- **JSON Pointer:** `/output/graph/classes` y `/output/graph/schema/classes`
- **Evaluación razonada:** el mismo catálogo de clases se serializa dos veces dentro del grafo; las taxonomías también aparecen como `subclass_facts`, disposiciones de proyección y `taxonomy_relations` de nivel superior. Algunas vistas sirven a trazabilidad, pero la repetición exacta de `classes` es duplicación estructural, aunque no crea por sí sola una contradicción semántica.
- **Impacto downstream:** aumenta el volumen y obliga a consumidores a decidir qué vista es autoritativa. No se observan duplicados contradictorios ni multiplicación de las 21 relaciones taxonómicas.

## 4. Diagnóstico

- **Primera degradación:** paso 05, `linguistic_annotation`. Las ambigüedades léxicas `stores` y `record/logs` se resuelven incorrectamente y rompen estructuras sujeto–predicado–objeto literales de p041.
- **Principal pérdida:** paso 09, `relation_extraction`. La etapa ofrece solo 13 relaciones, no distribuye coordinaciones y no representa adecuadamente las taxonomías ni varias relaciones narrativas/modales. Es una pérdida propagada desde anotación y conceptos, no un error nuevo repetido en cada etapa.
- **Principal contenido no soportado:** la declaración de `orion:Orion` como clase en el paso 16. La fuente solo presenta ORION como sujeto de una capacidad deseada.
- **Errores que llegan a RDF/OWL:** llega el tipado no soportado de ORION como clase y llega duplicación estructural de vistas. No llegan las relaciones espurias `audit —log→ ...`, la confusión `legal team`/`incident response team` ni las omisiones taxonómicas del paso 09, porque el paso 10 las corrige. La exclusión errónea de `denial-of-service attack` tampoco llega: la clase y su subordinación aparecen en la salida.
- **Aciertos:** intake, normalización, 17 oraciones y tokenización son fieles; el paso 10 cubre las 47 proposiciones atómicas literales y añade solo reificaciones entrañadas con alcance; los pasos 12–14 conservan las 51 claims, las 21 taxonomías y las dos aserciones de instancia; el paso 16 preserva `whether`/`must`, propósito y `should` como relaciones scoped, evitando materializarlas como hechos categóricos.
- **Incertidumbres legítimas:** identidad entre `unauthorized access` y `access event`; identidad de la brecha confirmada con el escenario inicial; referente de `recurrence`; alcance de `this text`; estatus ontológico de los sustantivos de capacidad. El conservadurismo ante estas cuestiones no debe penalizarse. Las reificaciones de acceso y brecha son **ENTRAÑADAS**, pero conviene mantener explícito que no son nombres literales de la fuente.

## 5. Veredicto

- **Calidad global:** **82/100**.
- **Output final:** **parcialmente fiel**. Conserva prácticamente todo el contenido proposicional, las 21 taxonomías y la modalidad; no obstante, introduce el tipado no soportado de ORION como clase y presenta duplicación estructural.
- **Tres correcciones prioritarias:**
  1. Corregir la desambiguación verbo/sustantivo y la distribución de coordinaciones en los pasos 05–09, especialmente `stores`, `Audit logs record` y las cuatro listas taxonómicas.
  2. Resolver correferencias de alta certeza en el paso 08 y mantener identidades de conceptos completas en el paso 09, evitando colisiones por lemas genéricos como `team`.
  3. Ajustar calidad y proyección: no excluir `denial-of-service attack`, no declarar ORION como clase sin evidencia y eliminar vistas duplicadas o marcar una representación canónica autoritativa.

Siguiente caso pendiente: infosec_p043.
