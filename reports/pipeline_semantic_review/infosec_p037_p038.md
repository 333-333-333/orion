# Revisión semántica: infosec_p037_p038

## 1. Lectura independiente

- **Resumen.** Los dos párrafos presentan ejemplos ilustrativos, no reglas universales. `p037` describe una base de datos de clientes, los datos que almacena, su alojamiento y protección, la gestión de claves, la recolección de logs, la revisión de alertas y su clasificación. `p038` describe acceso remoto mediante portátil, aplicación corporativa, autenticación, autorización, cifrado y monitorización; termina con una obligación de política. Esta lectura se construyó antes de abrir los outputs.

- **Conceptos.** Todas las expresiones son descripciones nominales comunes; el texto no proporciona nombres propios ni identificadores externos.

  | Párrafo | Expresiones explícitas | Lectura semántica independiente |
  |---|---|---|
  | `p037` | customer database; personal data; financial data; database server; production network; firewall; network access rules; cryptographic key; key management service; security information and event management system; audit logs; security analyst; alerts; asset owner; restricted information | Participantes, objetos y categorías mencionados explícitamente en el ejemplo. Las menciones con artículo definido retoman normalmente la mención indefinida precedente. El texto no decide por sí solo una ontología completa de clases e individuos. |
  | `p038` | remote access; remote employee / remote employees; laptop; corporate application; endpoint; web application; multi-factor authentication; identity provider; employee identity; authorization service; access; role assignments; virtual private network; communication channel; endpoint detection and response tool; security policy; lost devices | Participantes, objetos, mecanismos y una política explícitos. El portátil y la aplicación reciben clasificaciones copulares locales; la política introduce modalidad de obligación. |

  **Definiciones/clasificaciones explícitas:** “The laptop is an endpoint” y “The corporate application is a web application”. “Classifies ... as restricted information” expresa un acto y su resultado de clasificación; no autoriza por sí solo a convertir `restricted information` en una superclase ontológica universal.

- **Proposiciones con evidencia.** `EXPLÍCITO` significa literalmente expresado; no se incorpora conocimiento de dominio.

  | ID | Párrafo | Proposición | Evidencia breve | Clasificación |
  |---|---|---|---|---|
  | P01 | `p037` | Lo descrito es un ejemplo ilustrativo. | “For example” | EXPLÍCITO |
  | P02 | `p037` | Una base de datos de clientes almacena datos personales. | “database stores personal data” | EXPLÍCITO |
  | P03 | `p037` | La misma base de datos almacena datos financieros. | “and financial data” | EXPLÍCITO |
  | P04 | `p037` | La base de datos está alojada en un servidor de base de datos. | “is hosted on a database server” | EXPLÍCITO |
  | P05 | `p037` | El servidor se ejecuta dentro de una red de producción. | “runs inside a production network” | EXPLÍCITO |
  | P06 | `p037` | La red de producción está protegida por un firewall. | “is protected by a firewall” | EXPLÍCITO |
  | P07 | `p037` | El firewall aplica reglas de acceso de red. | “enforces network access rules” | EXPLÍCITO |
  | P08 | `p037` | La base de datos está cifrada usando una clave criptográfica. | “encrypted using a cryptographic key” | EXPLÍCITO |
  | P09 | `p037` | La clave está almacenada en un servicio de gestión de claves. | “key is stored in a key management service” | EXPLÍCITO |
  | P10 | `p037` | El sistema de gestión de información y eventos de seguridad recopila logs de auditoría. | “system collects audit logs” | EXPLÍCITO |
  | P11 | `p037` | Los logs recopilados proceden del servidor de base de datos. | “logs from the database server” | EXPLÍCITO |
  | P12 | `p037` | Un analista de seguridad revisa alertas. | “analyst reviews alerts” | EXPLÍCITO |
  | P13 | `p037` | Esas alertas están relacionadas con la base de datos de clientes. | “alerts related to the customer database” | EXPLÍCITO |
  | P14 | `p037` | El propietario del activo clasifica la base de datos como información restringida. | “classifies ... as restricted information” | EXPLÍCITO |
  | P15 | `p038` | El segundo ejemplo trata de acceso remoto. | “Another example involves remote access” | EXPLÍCITO |
  | P16 | `p038` | Un empleado remoto usa un portátil. | “employee uses a laptop” | EXPLÍCITO |
  | P17 | `p038` | El empleado accede a una aplicación corporativa usando ese portátil. | “uses a laptop to access a corporate application” | EXPLÍCITO |
  | P18 | `p038` | El portátil es un endpoint. | “laptop is an endpoint” | EXPLÍCITO |
  | P19 | `p038` | La aplicación corporativa es una aplicación web. | “application is a web application” | EXPLÍCITO |
  | P20 | `p038` | El empleado remoto se autentica mediante autenticación multifactor. | “authenticates through multi-factor authentication” | EXPLÍCITO |
  | P21 | `p038` | El proveedor de identidad verifica la identidad del empleado. | “verifies the employee identity” | EXPLÍCITO |
  | P22 | `p038` | El servicio de autorización concede acceso. | “grants access” | EXPLÍCITO |
  | P23 | `p038` | La concesión se basa en asignaciones de roles. | “based on role assignments” | EXPLÍCITO |
  | P24 | `p038` | La red privada virtual cifra el canal de comunicación. | “encrypts the communication channel” | EXPLÍCITO |
  | P25 | `p038` | La herramienta de detección y respuesta de endpoint monitoriza el portátil. | “tool monitors the laptop” | EXPLÍCITO |
  | P26 | `p038` | La política obliga a los empleados remotos a informar inmediatamente de dispositivos perdidos. | “requires ... to report lost devices immediately” | EXPLÍCITO |

- **Taxonomías explícitas.** Solo hay dos aserciones locales de pertenencia/tipado: `laptop instance_of endpoint` y `corporate application instance_of web application`. No hay ninguna relación explícita `subclass_of`, jerarquía de clases, disyunción ni equivalencia. Que `personal data` y `financial data` compartan el núcleo léxico “data” no constituye por sí solo una taxonomía formal. La clasificación como `restricted information` es resultado explícito de una acción, no una licencia para inducir una jerarquía universal.

- **Modalidad.** Ambos bloques están bajo alcance ilustrativo por “For example” y “Another example”. P01–P25 son descripciones afirmativas en presente, algunas en voz pasiva; no expresan necesidad universal. P26 es deóntica: “requires” entraña una obligación, por lo que parafrasearla como `must report` es `ENTRAÑADO`; “immediately” es un modificador temporal/de manera que debe conservarse. “using”, “through”, “from”, “related to” y “based on” aportan, respectivamente, instrumento/método, procedencia, relación y base; no son relaciones decorativas.

- **Ambigüedades.** Las continuidades `a customer database` → `The customer database`, `a database server` → `The database server`, `a laptop` → `The laptop`, `a corporate application` → `The corporate application` y `a remote employee` → `The remote employee` son `ENTRAÑADO` por la progresión definida del discurso. Vincular “the employee identity” específicamente con la única persona remota del ejemplo es `PLAUSIBLE`, pero el texto no usa una forma posesiva inequívoca. Identificar el plural genérico “remote employees” de la política con un único individuo es `PLAUSIBLE`, no una correferencia literal. Igualar `production network` con `virtual private network`, interpretar “endpoint” dentro del nombre de la herramienta como correferencia al portátil, declarar disjuntos los datos personales y financieros o universalizar los dominios/rangos es `NO SOPORTADO`. “The laptop is not an endpoint”, “the database stores neither kind of data” o que la política permita retrasar el reporte son interpretaciones `CONTRADICHO` por las citas afirmativas y por “immediately”.

## 2. Resultado por etapa

Escala: 0 = ausente/incorrecto; 1 = muy deficiente; 2 = deficiente; 3 = adecuado con reservas; 4 = sólido. Las puntuaciones juzgan solo la responsabilidad contractual de cada etapa.

| Paso | Etapa | Fidelidad | Cobertura | Precisión | Trazabilidad | Coherencia | Estado |
|---:|---|---:|---:|---:|---:|---:|---|
| 01 | input_intake | 4 | 4 | 4 | 4 | 4 | OK |
| 02 | preprocessing | 4 | 4 | 4 | 4 | 4 | OK |
| 03 | sentence_segmentation | 4 | 4 | 4 | 4 | 4 | OK |
| 04 | tokenization | 4 | 4 | 4 | 4 | 4 | OK |
| 05 | linguistic_annotation | 2 | 4 | 2 | 4 | 2 | FAIL |
| 06 | entity_extraction | 4 | 4 | 4 | 4 | 4 | OK |
| 07 | concept_extraction | 2 | 3 | 2 | 4 | 2 | FAIL |
| 08 | coreference_resolution | 4 | 4 | 4 | 4 | 4 | OK |
| 09 | relation_extraction | 2 | 1 | 2 | 4 | 2 | FAIL |
| 10 | canonical_claims / semantic_claims | 3 | 3 | 4 | 4 | 3 | WARN |
| 11 | semantic_debug_ir | 4 | 4 | 4 | 4 | 4 | OK |
| 12 | triple_extraction | 4 | 4 | 4 | 3 | 3 | WARN |
| 13 | taxonomy_induction | 4 | 4 | 4 | 4 | 4 | OK |
| 14 | type_assertion | 4 | 4 | 4 | 4 | 4 | OK |
| 15 | semantic_quality | 4 | 4 | 4 | 4 | 4 | OK |
| 16 | output_generation | 3 | 3 | 4 | 4 | 2 | FAIL |

La ausencia de entidades NER en 06 no se penaliza: los párrafos no contienen nombres propios inequívocos y los sintagmas comunes corresponden a 07. La salida vacía de 08 tampoco se penaliza: no hay pronombres y la continuidad por repetición nominal puede conservarse sin inventar cadenas. La taxonomía vacía de 13 es el resultado conservador correcto: los dos “is a” son aserciones de tipo, atendidas en 14, no `subclass_of`.

## 3. Hallazgos

### Q-infosec_p037_p038-05-1

- **Severidad:** alta
- **Tipo:** fidelidad y precisión lingüística
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** `p037`: “a customer database stores personal data and financial data”; `p037`: “A security analyst reviews alerts”; `p038`: “The authorization service grants access”.
- **Archivo y JSON Pointer:** `observed_p037_p038_05_linguistic_annotation.json`, `/tokens/6`, `/tokens/87`, `/tokens/159`.
- **Evaluación razonada:** `stores` se anota como `NOUN/NNS/nmod`, `reviews` como `NOUN/NNS/compound` y `grants` como `NOUN/NNS/ROOT`, aunque en las tres citas funcionan como predicados verbales. También se fragmentan los sujetos: `analyst` queda como `compound` de `reviews`, y `service` como `compound` de `grants`. No es una diferencia estilística: altera la estructura sujeto–predicado explícita.
- **Impacto downstream:** origina los sintagmas proposicionales espurios de 07 y contribuye a omisiones de 09. El error queda corregido en 10 por claims explícitos y no llega como hecho falso al output final.

### Q-infosec_p037_p038-07-1

- **Severidad:** alta
- **Tipo:** precisión conceptual
- **Atribución:** ERROR_AMPLIFICADO
- **Cita literal:** `p037`: “a customer database stores personal data and financial data”; `p037`: “A security analyst reviews alerts related to the customer database”; `p038`: “The authorization service grants access based on role assignments”.
- **Archivo y JSON Pointer:** `observed_p037_p038_07_concept_extraction.json`, `/concepts/1`, `/concepts/17`, `/concepts/33`.
- **Evaluación razonada:** 07 eleva a conceptos con confianza `0.95` tres proposiciones parciales: `customer database stores personal data and financial data`, `security analyst reviews alerts` y `authorization service grants access based`. Absorber el verbo dentro del concepto confunde participantes con afirmaciones. Es amplificación del error lingüístico de 05, no un error independiente repetido.
- **Impacto downstream:** degrada la disponibilidad de conceptos limpios para 09. La etapa 15 identifica y excluye exactamente estos tres ruidos, por lo que no llegan como recursos proposicionales al RDF.

### Q-infosec_p037_p038-07-2

- **Severidad:** media
- **Tipo:** coherencia de identidad conceptual
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** `p037`: “a database server”; “The database server runs”; “from the database server”.
- **Archivo y JSON Pointer:** `observed_p037_p038_07_concept_extraction.json`, `/concepts/3/concept_id`, `/concepts/4/concept_id`, `/concepts/16/concept_id`.
- **Evaluación razonada:** las tres menciones de `database server` reciben tres IDs distintos pese a compartir texto normalizado y continuidad discursiva. También ocurre con `firewall` (`/concepts/7` y `/concepts/8`) y con algunas menciones de `customer database`. En contraste, otras repeticiones sí reutilizan ID, por lo que el criterio es internamente inconsistente.
- **Impacto downstream:** debilita la correferencia implícita y facilita selecciones de referencia erróneas en 09. La canonicalización de 10 vuelve a consolidar las identidades.

### Q-infosec_p037_p038-09-1

- **Severidad:** crítica
- **Tipo:** cobertura relacional
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** `p037`: “database stores personal data and financial data”, “is hosted on a database server”, “runs inside a production network”, “is encrypted using a cryptographic key”, “key is stored”; `p038`: “to access a corporate application”, “authenticates through multi-factor authentication”, “grants access based on role assignments”.
- **Archivo y JSON Pointer:** `observed_p037_p038_09_relation_extraction.json`, `/relations`.
- **Evaluación razonada:** no aparecen relaciones candidatas para varias proposiciones centrales, incluso cuando 05 sí ofrece una estructura verbal utilizable (`hosted`, `runs`, `encrypted`, `stored`, `authenticates`). La lista contiene 13 relaciones, una de ellas meramente discursiva (`example involve remote access`), mientras omite varios núcleos explícitos y parte de las estructuras de propósito y base. Las tres omisiones asociadas a `stores`, `reviews` y `grants` comparten el linaje del error de 05; las restantes nacen en 09.
- **Impacto downstream:** 09 por sí sola no sustenta un modelo fiel. La etapa 10 corrige esta pérdida al generar 21 claims sustantivos con evidencia; por ello las omisiones no se propagan al conjunto principal de triples.

### Q-infosec_p037_p038-09-2

- **Severidad:** alta
- **Tipo:** precisión de sujeto y referencia
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** `p038`: “The virtual private network encrypts the communication channel.”
- **Archivo y JSON Pointer:** `observed_p037_p038_09_relation_extraction.json`, `/relations/3/subject_ref` y `/relations/3/subject_text`.
- **Evaluación razonada:** la relación `encrypt` usa como sujeto `network` y referencia el concepto de `production network` (`con-b33e...`), no el concepto explícito `virtual private network` (`con-f04e...`). Atribuir el cifrado a la red de producción es `NO SOPORTADO` por la oración citada y mezcla los dos ejemplos.
- **Impacto downstream:** sería una contaminación entre escenarios si se proyectara. 10 la corrige a `VirtualPrivateNetwork encrypts CommunicationChannel`; el error no llega al RDF final.

### Q-infosec_p037_p038-09-3

- **Severidad:** alta
- **Tipo:** fidelidad de relaciones complejas y modalidad
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** `p037`: “classifies the customer database as restricted information”; `p038`: “requires remote employees to report lost devices immediately”.
- **Archivo y JSON Pointer:** `observed_p037_p038_09_relation_extraction.json`, `/relations/8` y `/relations/9`.
- **Evaluación razonada:** la primera relación conserva solo `owner classify customer database` y pierde el resultado `restricted information`. La segunda conserva `policy require remote employee`, pero pierde la acción exigida, su objeto y `immediately`. Reducir estas construcciones a SPO incompletos cambia materialmente su contenido.
- **Impacto downstream:** 10 actúa como ERROR_CORREGIDO al incorporar `target: RestrictedInformation` y el claim modal `RemoteEmployee reports LostDevice` con `context`, `must` e `immediately`.

### Q-infosec_p037_p038-10-1

- **Severidad:** media
- **Tipo:** coherencia estructural de cualificadores
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** `p037`: “A security analyst reviews alerts related to the customer database.”
- **Archivo y JSON Pointer:** `observed_p037_p038_10_canonical_claims.json`, `/canonical_claims/claims/9/target` y `/semantic_claims/claims/9/target`.
- **Evaluación razonada:** el claim principal `SecurityAnalyst reviews Alert` es fiel, pero `target: CustomerDatabase` no explicita que la relación es `Alert related_to CustomerDatabase`. Unido al claim de revisión, `target` también puede leerse como objetivo de la revisión. La evidencia humana desambigua, pero la estructura de máquina pierde el predicado literal `related to`.
- **Impacto downstream:** la ambigüedad se conserva en 11, 12 y `/output/graph/facts/9/target`; es la principal pérdida semántica que sí alcanza el modelo final.

### Q-infosec_p037_p038-10-2

- **Severidad:** baja
- **Tipo:** cobertura discursiva
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** `p038`: “Another example involves remote access.”
- **Archivo y JSON Pointer:** `observed_p037_p038_10_canonical_claims.json`, `/canonical_claims/claims` y `/semantic_claims/claims`.
- **Evaluación razonada:** 09 había observado la relación discursiva `example involve remote access`, pero 10 no conserva un claim equivalente. `observation_scope: illustrative_example` preserva que se trata de un ejemplo, no que su tema declarado sea `remote access`.
- **Impacto downstream:** se pierde ese encuadre temático en triples y output. No afecta a los 21 hechos operativos principales, por lo que la severidad es baja.

### Q-infosec_p037_p038-12-1

- **Severidad:** baja
- **Tipo:** trazabilidad estructural
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** `p038`: “The corporate application is a web application.”
- **Archivo y JSON Pointer:** `observed_p037_p038_12_triple_extraction.json`, `/triples/0/subject_ref`, `/triples/0/predicate_ref` y `/triples/0/object_ref`.
- **Evaluación razonada:** los tres campos apuntan al mismo ID de claim. El claim ofrece procedencia válida, pero los campos no distinguen referencias del sujeto, predicado y objeto; el mismo patrón se repite en los 21 triples. No altera el SPO textual, pero reduce la capacidad de resolver cada término de manera independiente.
- **Impacto downstream:** el output final conserva trazabilidad por `claim_dispositions` y evidencia literal, de modo que el problema no inventa hechos; sí limita auditoría y enlace fino entre recursos.

### Q-infosec_p037_p038-15-1

- **Severidad:** informativa
- **Tipo:** saneamiento semántico
- **Atribución:** ERROR_CORREGIDO
- **Cita literal:** `p037`: “database stores personal data and financial data”; `p037`: “analyst reviews alerts”; `p038`: “authorization service grants access”.
- **Archivo y JSON Pointer:** `observed_p037_p038_15_semantic_quality.json`, `/excluded_concepts` y `/semantic_quality_report/concept_noise`.
- **Evaluación razonada:** 15 detecta como `predicate_absorbed_into_concept` y excluye los tres sintagmas proposicionales espurios originados en 05 y amplificados en 07. No excluye los claims canónicos correctos correspondientes.
- **Impacto downstream:** evita que esos fragmentos se materialicen como recursos semánticos; es una corrección efectiva antes de 16.

### Q-infosec_p037_p038-16-1

- **Severidad:** alta
- **Tipo:** coherencia y duplicación del modelo final
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** `p038`: “The laptop is an endpoint.” y “The corporate application is a web application.”
- **Archivo y JSON Pointer:** `observed_p037_p038_16_output_generation.json`, `/output/graph/instance_facts`, `/output/graph/type_assertions`, `/output/graph/classes`, `/output/graph/schema/classes` y `/type_assertions`.
- **Evaluación razonada:** las dos aserciones de tipo aparecen duplicadas en `instance_facts` y `type_assertions`; las clases aparecen tanto en `classes` como en `schema/classes`. Además, el campo superior `/type_assertions` está vacío mientras `/output/graph/type_assertions` contiene dos elementos. Aunque pueden ser vistas de una misma proyección, el output no declara esa equivalencia y viola la exigencia estricta de no duplicación ni incoherencia estructural.
- **Impacto downstream:** un consumidor puede contar dos veces las aserciones o interpretar el campo superior vacío como ausencia de tipado. No añade una proposición distinta, pero impide considerar el modelo final plenamente limpio y unívoco.

## 4. Diagnóstico

- **Primera degradación:** 05, al etiquetar como nombres los verbos `stores`, `reviews` y `grants`. 01–04 preservan íntegramente texto, oraciones, tokens, offsets e identidad de fuente.
- **Principal pérdida:** 09 tiene la mayor pérdida intermedia de cobertura. En el resultado final, la principal pérdida restante es no representar explícitamente `Alert related_to CustomerDatabase`; se conserva solo un `target` ambiguo. El encuadre “example involves remote access” también desaparece, con impacto menor.
- **Principal contenido no soportado:** no llega al final ningún hecho sustantivo claramente inventado. El caso más grave durante el pipeline es la atribución de `encrypt` a `production network` en 09, `NO SOPORTADO` por `p038`; 10 lo corrige antes de triples/RDF. En el output final queda el riesgo de leer `/facts/9/target` como “la base de datos es objetivo de la revisión”, interpretación no respaldada por la cita.
- **Errores que llegan a RDF/OWL:** (1) cualificador `target` sin predicado `related_to`; (2) pérdida del enunciado temático de acceso remoto; (3) duplicación de las dos aserciones de tipo y de las clases, junto con el desacuerdo del campo superior vacío. Los errores de parsing, los conceptos proposicionales y la confusión `production network`/`virtual private network` son corregidos y no llegan como hechos falsos.
- **Aciertos:** 10 reconstruye con evidencia los 21 claims operativos sustantivos; conserva coordinación, voz, alcance ilustrativo, procedencia de logs, propósito/instrumento, resultado de clasificación, base de autorización y modalidad con `immediately`. 12 proyecta los 21 núcleos SPO sin hechos extra. 13 no inventa taxonomías. 14 tipa correctamente portátil y aplicación. 15 excluye el ruido conceptual. 16 materializa 18 hechos ordinarios, dos tipos y una relación modal, con evidencia literal y disposición por claim.
- **Incertidumbres:** el texto no fija una distinción ontológica global entre clase e individuo para todos los sintagmas; tampoco garantiza que el plural normativo `remote employees` sea idéntico a un único individuo del ejemplo. Los campos auxiliares `context`, `target` y `relation_role` preservan información, pero su semántica formal no es uniforme ni siempre inequívoca. Se mantiene una lectura conservadora y no se penaliza la ausencia de jerarquías no expresadas.

## 5. Veredicto

- **Calidad global:** **86/100**.
- **Output final:** **parcialmente fiel**. Conserva casi todo el contenido operativo y no proyecta invenciones sustantivas, pero falla el requisito estricto de ausencia de pérdida y duplicación por la relación `alerts related to`, el encuadre temático omitido y las vistas de tipado duplicadas/incoherentes.
- **Tres correcciones prioritarias:**
  1. Representar cualificadores n-arios con predicados inequívocos, en especial `Alert related_to CustomerDatabase`, manteniendo también procedencia, resultado de clasificación, instrumento, base y modalidad.
  2. Emitir una sola representación autoritativa de clases y aserciones de tipo, o declarar explícitamente las vistas derivadas; alinear además `/type_assertions` con `/output/graph/type_assertions`.
  3. Corregir el análisis de verbos y exigir extracción relacional completa con identidad conceptual estable, para que 09 produzca los hechos explícitos sin sintagmas proposicionales ni confusión entre `production network` y `virtual private network`.

Siguiente caso pendiente: infosec_p039_p040.
