# Revisión semántica: infosec_p015_p016

## 1. Lectura independiente

### Resumen

Los dos párrafos presentan conocimiento genérico, no instancias nominales. `p015` caracteriza la seguridad de aplicaciones, define o describe vulnerabilidades, controles y actividades de verificación. `p016` aporta cuatro taxonomías explícitas y describe funciones de componentes tecnológicos. La lectura se limita a lo expresado por los párrafos: no se incorporan definiciones externas de API, inyección, cross-site scripting, servidores ni controles de seguridad.

### Conceptos

- **Tema de `p015`:** seguridad de aplicaciones durante el ciclo de vida del software.
- **Conceptos de protección:** application security, input validation, output encoding, secure authentication, secure session management y secure error handling.
- **Objetos protegidos o afectados:** software systems, lifecycle, malicious or malformed data, application, risk of injection, risk of cross-site scripting, user login processes, session tokens, user state, sensitive information y error messages.
- **Conceptos de especificación y aseguramiento:** security requirement, protection need, security test, security requirement implementation, code review, source code, defects, weaknesses y policy violations.
- **Conceptos de arquitectura en `p016`:** application, web application, mobile application, API, application interface, database, data storage system, web server, application server, database server, load balancer, server, API gateway, backend service, content delivery network, availability, performance, distributed user, technology component y specific security control.
- **Entidades/instancias explícitas:** no hay personas, organizaciones, productos ni sistemas individualizados. Los sintagmas indefinidos (“a web application”, “a database”) tienen lectura genérica/de clase. Interpretarlos como individuos concretos sería **NO SOPORTADO**.
- **Definiciones o caracterizaciones funcionales explícitas:**
  - “A software vulnerability is a weakness…” (`p015`).
  - “A security requirement defines a protection need…” (`p015`).
  - “A security test verifies whether…” (`p015`).
  - “A code review examines source code…” (`p015`).
  - Las cuatro construcciones “is a type of” de `p016` son definiciones taxonómicas explícitas.

### Proposiciones con evidencia

| ID | Proposición independiente | Evidencia breve | Evaluación |
|---|---|---|---|
| P01 | Application security protege software systems. | “Application security protects software systems” (`p015`) | **EXPLÍCITO** |
| P02 | La protección de P01 se mantiene durante el lifecycle de esos software systems. | “throughout their lifecycle” (`p015`) | **ENTRAÑADO**; la posesión de “their” se resuelve a “software systems”. |
| P03 | Una software vulnerability es una weakness. | “A software vulnerability is a weakness” (`p015`) | **EXPLÍCITO** |
| P04 | La weakness de P03 puede estar en application code, configuration o design, como alternativas coordinadas. | “in application code, configuration, or design” (`p015`) | **EXPLÍCITO** como coordinación disyuntiva; proyectar las tres alternativas como simultáneamente ciertas sería **NO SOPORTADO**. |
| P05 | Input validation impide un evento de entrada de datos a una aplicación. | “prevents … data from entering an application” (`p015`) | **EXPLÍCITO**; la reificación del evento es **ENTRAÑADA**. |
| P06 | Los datos afectados por P05 son malicious data o malformed data. | “malicious or malformed data” (`p015`) | **EXPLÍCITO** como disyunción no necesariamente exclusiva. |
| P07 | El destino del evento de P05 es una application. | “entering an application” (`p015`) | **EXPLÍCITO** |
| P08 | Output encoding reduce el riesgo coordinado de injection y cross-site scripting. | “reduces the risk of injection and cross-site scripting” (`p015`) | **EXPLÍCITO**; separarlo en dos objetos `RiskOf…` es una descomposición **ENTRAÑADA**, no dos afirmaciones independientes de origen. |
| P09 | Secure authentication protege user login processes. | “Secure authentication protects user login processes” (`p015`) | **EXPLÍCITO** |
| P10 | Secure session management protege session tokens. | “protects session tokens” (`p015`) | **EXPLÍCITO** |
| P11 | Secure session management protege user state. | “and user state” (`p015`) | **EXPLÍCITO** por distribución de la coordinación. |
| P12 | Secure error handling impide un evento de exposición. | “prevents … from being exposed” (`p015`) | **EXPLÍCITO**; `ExposureEvent` es una reificación **ENTRAÑADA**. |
| P13 | El paciente de P12 es sensitive information. | “sensitive information” (`p015`) | **EXPLÍCITO** |
| P14 | El canal de P12 son error messages. | “through error messages” (`p015`) | **EXPLÍCITO** |
| P15 | Security requirement define protection need. | “defines a protection need” (`p015`) | **EXPLÍCITO** |
| P16 | La protection need de P15 es para una application. | “for an application” (`p015`) | **EXPLÍCITO**; denominar la relación `has_beneficiary` es una normalización **PLAUSIBLE** y compatible, no vocabulario literal. |
| P17 | Security test verifica si una security requirement está implementada correctamente. | “verifies whether … is implemented correctly” (`p015`) | **EXPLÍCITO** con modalidad interrogativa/evaluativa `whether`; afirmar que ya está correctamente implementada es **NO SOPORTADO**. |
| P18 | Code review examina source code. | “examines source code” (`p015`) | **EXPLÍCITO** |
| P19 | El propósito del examen es detectar defects, weaknesses y policy violations. | “to detect defects, weaknesses, and policy violations” (`p015`) | **EXPLÍCITO** como propósito; afirmar detección efectiva sin conservar ese alcance es **NO SOPORTADO**. |
| P20 | Web application es un tipo de application. | “A web application is a type of application” (`p016`) | **EXPLÍCITO** |
| P21 | Mobile application es un tipo de application. | “A mobile application is a type of application” (`p016`) | **EXPLÍCITO** |
| P22 | API es un tipo de application interface. | “An API is a type of application interface” (`p016`) | **EXPLÍCITO**; expandir la sigla API no está soportado por el texto. |
| P23 | Database es un tipo de data storage system. | “A database is a type of data storage system” (`p016`) | **EXPLÍCITO** |
| P24 | Web server aloja web applications. | “A web server hosts web applications” (`p016`) | **EXPLÍCITO** |
| P25 | Application server ejecuta business logic. | “An application server executes business logic” (`p016`) | **EXPLÍCITO** |
| P26 | Database server almacena structured data. | “A database server stores structured data” (`p016`) | **EXPLÍCITO** |
| P27 | Load balancer distribuye traffic a través de multiple servers. | “distributes traffic across multiple servers” (`p016`) | **EXPLÍCITO**; `multiple` cuantifica los servidores. |
| P28 | API gateway controla access cuyo destino son backend services. | “controls access to backend services” (`p016`) | **EXPLÍCITO**; la descomposición `controls Access` + `Access has_target BackendService` es **ENTRAÑADA**. |
| P29 | Content delivery network mejora availability. | “improves availability” (`p016`) | **EXPLÍCITO** |
| P30 | Content delivery network mejora performance. | “and performance” (`p016`) | **EXPLÍCITO** por distribución de la coordinación. |
| P31 | Las mejoras P29–P30 son para distributed users. | “for distributed users” (`p016`) | **ENTRAÑADO** para ambos objetos coordinados. |
| P32 | Cada technology component puede requerir specific security controls. | “Each technology component may require specific security controls” (`p016`) | **EXPLÍCITO** con cuantificador universal y modalidad de posibilidad. Una relación categórica `requires` sin `may` sería **NO SOPORTADO**. |

### Taxonomías explícitas

1. `SoftwareVulnerability` **subclass_of** `Weakness` — “is a weakness” (`p015`).
2. `WebApplication` **subclass_of** `Application` — “is a type of application” (`p016`).
3. `MobileApplication` **subclass_of** `Application` — “is a type of application” (`p016`).
4. `Api` **subclass_of** `ApplicationInterface` — “is a type of application interface” (`p016`).
5. `Database` **subclass_of** `DataStorageSystem` — “is a type of data storage system” (`p016`).

No son taxonomías explícitas las posibles clasificaciones `WebServer/ApplicationServer/DatabaseServer subclass_of Server`, ni la pertenencia de todos los elementos enumerados a `TechnologyComponent`: resultan **PLAUSIBLES** por la forma léxica o el contexto, pero el texto no las declara.

### Modalidad

- El presente simple se usa con alcance genérico en ambos párrafos.
- `or` introduce alternativas en “application code, configuration, or design” y “malicious or malformed data” (`p015`). No se debe convertir cada alternativa en un hecho conjuntivo.
- `and` distribuye el predicado en “injection and cross-site scripting”, “session tokens and user state”, “defects, weaknesses, and policy violations” y “availability and performance” (`p015`, `p016`).
- `whether` mantiene abierta la corrección de la implementación (`p015`).
- `to detect` expresa propósito y no garantiza resultado (`p015`).
- `may` expresa posibilidad; `each` conserva alcance universal sobre technology components (`p016`).

### Ambigüedades

- **Correferencia:** “their” en “throughout their lifecycle” (`p015`) refiere a “software systems”: **ENTRAÑADO** por concordancia plural y proximidad. Referirlo a “Application security” es **CONTRADICHO** por la concordancia singular/plural.
- **Riesgo coordinado:** “the risk of injection and cross-site scripting” (`p015`) admite representación como un riesgo coordinado o como dos objetos de riesgo vinculados por `and`. Ambas son **PLAUSIBLES**; perder la coordinación no lo es.
- **Disyunciones:** el texto no indica exclusividad entre malicious y malformed, ni entre las ubicaciones de una weakness. La exclusividad sería **NO SOPORTADA**.
- **Technology component:** que la frase “Each technology component” (`p016`) retome exactamente todos los componentes anteriores es **PLAUSIBLE**, pero no explícito; no autoriza taxonomías adicionales.
- **Genérico frente a instancia:** la lectura de clase es **ENTRAÑADA** por el estilo definicional; generar individuos concretos es **NO SOPORTADO**.
- **Compuestos nominales:** inferir jerarquías solo por los nombres “web server”, “application server” y “database server” (`p016`) es **PLAUSIBLE**, no una taxonomía explícita.

## 2. Resultado por etapa

Escala: 0 = ausente/incorrecto, 1 = muy deficiente, 2 = parcial, 3 = bueno con defectos, 4 = completo y fiel. El paso 11 está configurado, por lo que no corresponde N/A en este caso.

| Paso | Etapa | Fidelidad | Cobertura | Precisión | Trazabilidad | Coherencia | Estado |
|---:|---|---:|---:|---:|---:|---:|---|
| 01 | input_intake | 4 | 4 | 4 | 4 | 4 | OK |
| 02 | preprocessing | 4 | 4 | 4 | 4 | 4 | OK |
| 03 | sentence_segmentation | 4 | 4 | 4 | 4 | 4 | OK |
| 04 | tokenization | 4 | 4 | 4 | 4 | 4 | OK |
| 05 | linguistic_annotation | 3 | 3 | 3 | 4 | 2 | WARN |
| 06 | entity_extraction | 4 | 4 | 4 | 4 | 4 | OK |
| 07 | concept_extraction | 3 | 2 | 2 | 4 | 2 | WARN |
| 08 | coreference_resolution | 2 | 1 | 4 | 1 | 4 | WARN |
| 09 | relation_extraction | 2 | 1 | 2 | 4 | 2 | FAIL |
| 10 | canonical_claims / semantic_claims | 4 | 4 | 4 | 4 | 3 | OK |
| 11 | semantic_debug_ir | 4 | 4 | 4 | 4 | 4 | OK |
| 12 | triple_extraction | 4 | 4 | 4 | 4 | 4 | OK |
| 13 | taxonomy_induction | 4 | 4 | 4 | 4 | 4 | OK |
| 14 | type_assertion | 4 | 4 | 4 | 4 | 4 | OK |
| 15 | semantic_quality | 3 | 3 | 3 | 4 | 2 | WARN |
| 16 | output_generation | 4 | 4 | 4 | 4 | 3 | OK |

## 3. Hallazgos

### Q-infosec_p015_p016-05-1

- **Severidad:** MEDIA
- **Tipo:** anotación morfosintáctica incorrecta
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** “A web server hosts web applications.” y “A database server stores structured data.” (`p016`)
- **Archivo y JSON Pointer:**
  - `tests/smoke/cases/infosec_p015_p016/artifacts/pipeline_outputs/observed_p015_p016_05_linguistic_annotation.json` — `/tokens/157`, `/tokens/158`, `/tokens/160`, `/tokens/171`, `/tokens/172`, `/tokens/174`.
- **Evaluación razonada:** en la primera oración, `hosts` se etiqueta como `NOUN/compound` y `applications` como `ROOT`; en la segunda, `stores` se etiqueta como `NOUN/nmod` y `data` como `ROOT`. Esto contradice la estructura literal sujeto–verbo–objeto de ambas oraciones. Los tokens y offsets siguen siendo fieles, pero la evidencia lingüística no lo es.
- **Impacto downstream:** el error se propaga en el paso 07 como los conceptos espurios “web server hosts web applications” y “database server stores structured data”, y causa ausencia de ambas relaciones en el paso 09. El paso 10 lo corrige y el paso 15 excluye los chunks ruidosos; por tanto, no llega como error semántico al RDF final.

### Q-infosec_p015_p016-07-1

- **Severidad:** BAJA
- **Tipo:** solapamiento y ruido conceptual
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** “Input validation prevents malicious or malformed data from entering an application.” (`p015`)
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p015_p016/artifacts/pipeline_outputs/observed_p015_p016_07_concept_extraction.json` — `/concepts/9`, `/concepts/10`, `/concepts/51`.
- **Evaluación razonada:** se proponen simultáneamente “malicious or malformed data”, “malformed data” y el modificador aislado “malicious”. El primer chunk conserva la coordinación; el segundo se solapa y el tercero no constituye por sí solo la entidad conceptual expresada en el párrafo. Además, la misma etapa no propone por separado varios superconceptos taxonómicos de `p016`, como “application interface” y “data storage system”.
- **Impacto downstream:** reduce precisión y cobertura de candidatos y obliga a la etapa canónica a reconstruir `MaliciousData`, `MalformedData`, `ApplicationInterface` y `DataStorageSystem` desde la evidencia textual. Los candidatos ruidosos de este hallazgo no se proyectan al modelo final.

### Q-infosec_p015_p016-08-1

- **Severidad:** MEDIA
- **Tipo:** omisión de correferencia
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** “Application security protects software systems throughout their lifecycle.” (`p015`)
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p015_p016/artifacts/pipeline_outputs/observed_p015_p016_08_coreference_resolution.json` — `/coreferences`.
- **Evaluación razonada:** la lista vacía no registra la correferencia gramaticalmente resoluble `their` → `software systems`. El conservadurismo no justifica aquí la omisión: la concordancia plural descarta “Application security” como antecedente.
- **Impacto downstream:** el paso 09 pierde el alcance temporal y la posesión del lifecycle. El paso 10 corrige el error mediante `scope_owner: SoftwareSystem` y la claim `Lifecycle lifecycle_of SoftwareSystem`; el paso 16 conserva esa estructura en `scoped_relations` y `lifecycleOf`.

### Q-infosec_p015_p016-09-1

- **Severidad:** ALTA
- **Tipo:** pérdida sistemática de alcance, argumentos y modalidad
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** “A security test verifies whether a security requirement is implemented correctly.” (`p015`); “A code review examines source code to detect defects, weaknesses, and policy violations.” (`p015`); “Each technology component may require specific security controls.” (`p016`)
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p015_p016/artifacts/pipeline_outputs/observed_p015_p016_09_relation_extraction.json` — `/relations`, `/relations/0`, `/relations/11`, `/relations/18`, `/relations/19`.
- **Evaluación razonada:** solo se producen 20 relaciones de cabeza y quedan fuera proposiciones completas o roles esenciales: no hay relación para el security test; el propósito de code review no se representa; input validation pierde la alternativa malformed y el evento de entrada; output encoding se reduce a un objeto genérico `risk`; y `component require control` omite `may` y `each`. También se pierden complementos como lifecycle, backend services y multiple servers. La relación modal convertida en categórica es **NO SOPORTADA** por `p016`.
- **Impacto downstream:** si estas relaciones se proyectaran directamente, el modelo sería incompleto y sobregeneralizaría la obligación de controles. No se contabilizan de nuevo las pérdidas de `hosts` y `stores`, ya atribuidas al paso 05. El paso 10 reemplaza esta representación por 40 claims con roles, coordinación y modalidad, por lo que el defecto queda corregido antes de triples y RDF.

### Q-infosec_p015_p016-10-1

- **Severidad:** INFORMATIVA
- **Tipo:** recuperación semántica
- **Atribución:** ERROR_CORREGIDO
- **Cita literal:** “A security test verifies whether a security requirement is implemented correctly.” (`p015`); “A web server hosts web applications.” y “A database server stores structured data.” (`p016`)
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p015_p016/artifacts/pipeline_outputs/observed_p015_p016_10_canonical_claims.json` — `/canonical_claims/claims/20`, `/canonical_claims/claims/29`, `/canonical_claims/claims/31`, `/canonical_claims/claims/39`.
- **Evaluación razonada:** la etapa canónica recupera las relaciones ausentes, restaura los compuestos completos, representa `whether`, `purpose`, `may`, `each`, las disyunciones y los roles de eventos. Las 40 claims están respaldadas por evidencia literal, paragraph ID, sentence ID y source text ID.
- **Impacto downstream:** los pasos 12–16 reciben una representación semántica sustancialmente más fiel que la salida del paso 09. No se observa amplificación del error original.

### Q-infosec_p015_p016-15-1

- **Severidad:** BAJA
- **Tipo:** incoherencia del diagnóstico de calidad
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** “A web server hosts web applications.” y “A database server stores structured data.” (`p016`)
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p015_p016/artifacts/pipeline_outputs/observed_p015_p016_15_semantic_quality.json` — `/semantic_quality_report/concept_noise/0`, `/semantic_quality_report/concept_noise/2`, `/semantic_quality_report/rdf_readiness`, `/semantic_quality_report/semantic_integrity_checks`.
- **Evaluación razonada:** la etapa identifica correctamente los dos chunks que absorbieron el predicado, pero duplica cada caso bajo dos razones y declara `rdf_readiness: false` mientras no hay claims rechazadas, no hay claims sin triple, no hay issues de integridad y todos los checks internos son `true`. El diagnóstico de ruido es preciso; su agregación y conclusión de readiness no son estructuralmente coherentes.
- **Impacto downstream:** no hay pérdida semántica porque el paso 16 excluye el ruido y proyecta las claims corregidas. Sí disminuye la confiabilidad del indicador de calidad para decidir automáticamente si proyectar.

## 4. Diagnóstico

- **Primera degradación:** paso 05, al analizar incorrectamente las dos oraciones simples con `hosts` y `stores` de `p016`. Los pasos 01–04 preservan texto, límites, tokens y trazabilidad.
- **Principal pérdida:** paso 09. Su representación no conserva de forma suficiente eventos, complementos, coordinaciones, propósito, `whether`, `may` ni `each`. Esta pérdida es más amplia que los dos errores propagados desde el análisis lingüístico.
- **Principal contenido no soportado:** en el paso 09, `component require specific security control` sin la modalidad “may” de `p016`. También sería no soportado leer `CodeReview detects …` como resultado efectivo; el paso 10 lo etiqueta correctamente como `purpose`.
- **Errores que llegan a RDF/OWL:** no se detectan errores semánticos sustantivos heredados. Los chunks con predicado absorbido se excluyen; las cinco taxonomías proyectadas son explícitas; las disyunciones se guardan en `logical_alternatives`; y `may`, `whether`, propósito y alcance de lifecycle se conservan como `scoped_relations`, no como hechos categóricos. La redundancia de vistas (`classes`/`schema.classes`, `subclass_facts`/`taxonomy_relations`) reduce ligeramente la coherencia estructural, pero no duplica hechos dentro de la lista principal `facts`.
- **Aciertos:** texto íntegro; 21 oraciones y 215 tokens con offsets; ausencia conservadora de entidades nominales y type assertions; recuperación de 40 claims y 40 triples; cinco taxonomías explícitas exactas; trazabilidad por claim y evidencia literal; modelo final sin taxonomías inferidas solo por nombres compuestos.
- **Incertidumbres:** la separación de “risk of injection and cross-site scripting” en dos recursos de riesgo es una descomposición razonable, pero el texto también admite un único riesgo coordinado. La relación `has_beneficiary` para “for an application” es una normalización plausible. Identificar todos los componentes previos como instancias o subclases de `TechnologyComponent` no está autorizado por el párrafo y correctamente no se materializa.

## 5. Veredicto

- **Calidad global:** **89/100**.
- **Output final:** **fiel**. El modelo final conserva las proposiciones, taxonomías, coordinaciones, roles y modalidades relevantes sin invención de conocimiento de dominio. Las degradaciones intermedias son graves en el paso 09, pero quedan corregidas antes de la proyección final.
- **Tres correcciones prioritarias:**
  1. Corregir la anotación lingüística de construcciones sujeto–verbo–objeto con compuestos nominales, en especial “web server hosts…” y “database server stores…” (`p016`).
  2. Hacer que relation extraction preserve desde origen complementos, eventos, coordinación, propósito y modalidad (`whether`, `may`, `each`) en lugar de depender de la reconstrucción del paso 10.
  3. Mejorar concept extraction y coreference resolution para separar conceptos coordinados sin solapamiento y resolver `their` → `software systems`, manteniendo siempre sus spans y evidencia.

Siguiente caso pendiente: infosec_p017_p018.
