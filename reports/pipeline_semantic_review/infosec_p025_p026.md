# Revisión semántica: infosec_p025_p026

## 1. Lectura independiente

### Resumen

Los dos párrafos describen, en presente genérico, dos ámbitos: **seguridad de proveedores** (`p025`) y **seguridad física** (`p026`). El texto define categorías, enumera subtipos, atribuye funciones a controles y documentos, y formula dos obligaciones mediante `must`. No aparecen nombres propios ni instancias inequívocas; los sintagmas indefinidos y plurales se leen como categorías genéricas. Esta lectura se construyó antes de consultar los outputs.

### Conceptos

- **p025 — categorías y participantes:** supplier security, risk, external party, supplier, external entity, goods, services, cloud provider, managed service provider, software vendor, supplier assessment, security posture, contract, obligation, organization, data processing agreement, responsibility, personal data, service-level agreement, service performance, availability y third-party access.
- **p026 — categorías y participantes:** physical security, facility, equipment, people, physical asset, data center, computing infrastructure, office, employee, business activity, badge reader, physical access control, security camera, monitoring control, visitor log, external person, locked cabinet, physical document, removable media, environmental control, fire, humidity, temperature, power failure, physical access y restricted area.
- **Definición explícita:** “A supplier is an external entity that provides goods or services” (`p025`). El núcleo taxonómico es `Supplier → ExternalEntity`; la relativa agrega la provisión disyuntiva de bienes o servicios.
- **Definiciones taxonómicas explícitas:** las ocho relaciones enumeradas en “Taxonomías explícitas”.
- **Descripciones funcionales explícitas:** supplier assessment/evaluates; contract y agreements/define; visitor log/records; security y controls/protect; data center/hosts; employees/perform.
- **Entidades o instancias explícitas:** no hay nombres propios ni individuos inequívocos. “the organization” y “the supplier” (`p025`) son roles discursivos en una relación entre participantes, no identificadores únicos. Crear individuos concretos para ellos sería **NO SOPORTADO**.

### Proposiciones con evidencia

| ID | Proposición de la lectura independiente | Evidencia breve | Clasificación |
|---|---|---|---|
| P25-01 | Supplier security manages risks. | “Supplier security manages risks” (`p025`) | EXPLÍCITO |
| P25-02 | Esos riesgos están asociados con external parties. | “risks associated with external parties” (`p025`) | EXPLÍCITO |
| P25-03 | Supplier es external entity. | “A supplier is an external entity” (`p025`) | EXPLÍCITO |
| P25-04 | La external entity de la definición provides goods or services. | “that provides goods or services” (`p025`) | EXPLÍCITO |
| P25-05 | Supplier provides goods or services, preservando la alternativa. | “supplier is an external entity that provides…” (`p025`) | ENTRAÑADO |
| P25-06 | Cloud provider es un tipo de supplier. | “cloud provider is a type of supplier” (`p025`) | EXPLÍCITO |
| P25-07 | Managed service provider es un tipo de supplier. | “managed service provider is a type of supplier” (`p025`) | EXPLÍCITO |
| P25-08 | Software vendor es un tipo de supplier. | “software vendor is a type of supplier” (`p025`) | EXPLÍCITO |
| P25-09 | Supplier assessment evaluates security posture. | “assessment evaluates the security posture” (`p025`) | EXPLÍCITO |
| P25-10 | La security posture evaluada es la de un supplier. | “security posture of a supplier” (`p025`) | EXPLÍCITO |
| P25-11 | Contract defines obligations. | “A contract defines obligations” (`p025`) | EXPLÍCITO |
| P25-12 | Las obligaciones son entre organization y supplier. | “between the organization and the supplier” (`p025`) | EXPLÍCITO |
| P25-13 | Data processing agreement defines responsibilities. | “defines responsibilities” (`p025`) | EXPLÍCITO |
| P25-14 | Esas responsibilities están relacionadas con personal data. | “responsibilities related to personal data” (`p025`) | EXPLÍCITO |
| P25-15 | Service-level agreement defines service performance. | “defines expected service performance” (`p025`) | EXPLÍCITO |
| P25-16 | Service performance está calificado como expected. | “expected service performance” (`p025`) | EXPLÍCITO |
| P25-17 | Service-level agreement defines availability. | “defines … availability” (`p025`) | EXPLÍCITO |
| P25-18 | Third-party access debe ser approved. | “must be approved” (`p025`) | EXPLÍCITO |
| P25-19 | Third-party access debe ser monitored. | “must be … monitored” (`p025`) | EXPLÍCITO |
| P25-20 | Third-party access debe ser revoked cuando deja de ser requerido. | “revoked when no longer required” (`p025`) | EXPLÍCITO |
| P25-21 | La condición “no longer required” tiene como sujeto tácito third-party access. | “Third-party access … when no longer required” (`p025`) | ENTRAÑADO |
| P26-01 | Physical security protects facilities. | “protects facilities” (`p026`) | EXPLÍCITO |
| P26-02 | Physical security protects equipment. | “facilities, equipment” (`p026`) | EXPLÍCITO |
| P26-03 | Physical security protects people. | “equipment, people” (`p026`) | EXPLÍCITO |
| P26-04 | Physical security protects physical assets. | “and physical assets” (`p026`) | EXPLÍCITO |
| P26-05 | Data center es un tipo de facility. | “data center is a type of facility” (`p026`) | EXPLÍCITO |
| P26-06 | La facility descrita hosts computing infrastructure. | “facility that hosts computing infrastructure” (`p026`) | EXPLÍCITO |
| P26-07 | Data center hosts computing infrastructure. | “data center is a type of facility that hosts…” (`p026`) | ENTRAÑADO |
| P26-08 | Office es un tipo de facility. | “office is a type of facility” (`p026`) | EXPLÍCITO |
| P26-09 | Employees perform business activities. | “employees perform business activities” (`p026`) | EXPLÍCITO |
| P26-10 | La realización de esas actividades se localiza en el office/facility introducido. | “facility where employees perform” (`p026`) | ENTRAÑADO |
| P26-11 | Badge reader es un tipo de physical access control. | “badge reader is a type of physical access control” (`p026`) | EXPLÍCITO |
| P26-12 | Security camera es un tipo de monitoring control. | “security camera is a type of monitoring control” (`p026`) | EXPLÍCITO |
| P26-13 | Visitor log records external persons. | “visitor log records external persons” (`p026`) | EXPLÍCITO |
| P26-14 | Las external persons registradas están entering a facility. | “external persons entering a facility” (`p026`) | EXPLÍCITO |
| P26-15 | Locked cabinet protects physical documents. | “protects physical documents” (`p026`) | EXPLÍCITO |
| P26-16 | Locked cabinet protects removable media. | “and removable media” (`p026`) | EXPLÍCITO |
| P26-17 | Environmental controls protect equipment. | “controls protect equipment” (`p026`) | EXPLÍCITO |
| P26-18 | La protección del equipment es frente a fire. | “equipment from fire” (`p026`) | EXPLÍCITO |
| P26-19 | La protección del equipment es frente a humidity. | “fire, humidity” (`p026`) | EXPLÍCITO |
| P26-20 | La protección del equipment es frente a temperature. | “humidity, temperature” (`p026`) | EXPLÍCITO |
| P26-21 | La protección del equipment es frente a power failures. | “and power failures” (`p026`) | EXPLÍCITO |
| P26-22 | Physical access tiene como objetivo restricted areas. | “Physical access to restricted areas” (`p026`) | EXPLÍCITO |
| P26-23 | Ese physical access debe ser authorized. | “must be authorized” (`p026`) | EXPLÍCITO |
| P26-24 | Ese physical access debe ser monitored. | “and monitored” (`p026`) | EXPLÍCITO |

Interpretaciones de control:

- “Expected” también modifica inequívocamente `availability`: **PLAUSIBLE**, pero no seguro por el alcance de la coordinación en “expected service performance and availability” (`p025`). No se exige esa expansión.
- Badge reader es monitoring control: **NO SOPORTADO**; `p026` solo explicita physical access control.
- Office hosts computing infrastructure: **NO SOPORTADO**; esa relativa aparece en la oración de data center (`p026`).
- Cloud provider no es supplier: **CONTRADICHO** por “is a type of supplier” (`p025`).
- Third-party access puede mantenerse cuando ya no es requerido: **CONTRADICHO** por “must be … revoked when no longer required” (`p025`).
- La organization es necesariamente quien aprueba third-party access: **NO SOPORTADO**; el agente de “approved” no se expresa (`p025`).

### Taxonomías explícitas

| Subclase | Superclase | Evidencia | Clasificación |
|---|---|---|---|
| Supplier | ExternalEntity | “supplier is an external entity” (`p025`) | EXPLÍCITO |
| CloudProvider | Supplier | “cloud provider is a type of supplier” (`p025`) | EXPLÍCITO |
| ManagedServiceProvider | Supplier | “managed service provider is a type of supplier” (`p025`) | EXPLÍCITO |
| SoftwareVendor | Supplier | “software vendor is a type of supplier” (`p025`) | EXPLÍCITO |
| DataCenter | Facility | “data center is a type of facility” (`p026`) | EXPLÍCITO |
| Office | Facility | “office is a type of facility” (`p026`) | EXPLÍCITO |
| BadgeReader | PhysicalAccessControl | “badge reader is a type of physical access control” (`p026`) | EXPLÍCITO |
| SecurityCamera | MonitoringControl | “security camera is a type of monitoring control” (`p026`) | EXPLÍCITO |

No hay taxonomías explícitas entre physical security y supplier security, entre physical access control y monitoring control, ni entre los cuatro peligros ambientales.

### Modalidad

- **Deóntica:** `must` aplica a approved, monitored y revoked en `p025`, y a authorized y monitored en `p026`.
- **Condicional/temporal con negación:** “when no longer required” restringe la revocación de third-party access (`p025`); no restringe approval ni monitoring.
- **Alternativa:** `or` en “goods or services” (`p025`) debe conservarse como disyunción, no como dos hechos conjuntivos independientes.
- **Coordinación:** `and` enumera objetos protegidos, resultados definidos, acciones obligatorias y peligros. Las coordinaciones permiten descomposición, pero deben conservar su agrupación.
- **Calificación:** `expected` modifica expresamente service performance (`p025`); su alcance sobre availability es ambiguo.
- **Aspecto genérico:** el presente simple formula descripciones de categoría, no eventos fechados ni instancias observadas.

### Ambigüedades

- **Correferencia de “that” en la definición de supplier:** el antecedente sintáctico inmediato es “external entity”; por la cópula, atribuir la provisión al supplier es **ENTRAÑADO**, no una nueva afirmación independiente (`p025`).
- **Correferencia de “that” en data center:** el antecedente inmediato es “facility”; atribuir `hosts` a DataCenter es **ENTRAÑADO** por la definición (`p026`).
- **“where” en office:** localiza el evento de employees en el office/facility descrito. `Office` como localización es **ENTRAÑADO**; una ubicación física más específica es **NO SOPORTADA** (`p026`).
- **“expected … and availability”:** el alcance compartido de expected es **PLAUSIBLE**, no inequívoco (`p025`).
- **“protect equipment from …”:** el paciente explícito es equipment; resumir que EnvironmentalControl `protects_against` cada peligro es **ENTRAÑADO** solo si se conserva `patient=Equipment` (`p026`).
- **Pasivas deónticas:** no se expresa quién aprueba, monitoriza, revoca o autoriza. Inventar agentes sería **NO SOPORTADO** (`p025`, `p026`).
- **Número gramatical:** singularizar plurales para etiquetas de categoría puede ser fiel; no autoriza a crear individuos concretos.

## 2. Resultado por etapa

Escala: 0 = ausente o contrario; 1 = muy deficiente; 2 = parcial con defectos importantes; 3 = adecuado con pérdidas menores; 4 = fiel y completo para la responsabilidad de la etapa.

| Paso | Etapa | Fidelidad | Cobertura | Precisión | Trazabilidad | Coherencia | Estado |
|---:|---|---:|---:|---:|---:|---:|---|
| 01 | input_intake | 4 | 4 | 4 | 4 | 4 | OK |
| 02 | preprocessing | 4 | 4 | 4 | 4 | 4 | OK |
| 03 | sentence_segmentation | 4 | 4 | 4 | 4 | 4 | OK |
| 04 | tokenization | 4 | 4 | 4 | 4 | 4 | OK |
| 05 | linguistic_annotation | 3 | 4 | 3 | 4 | 3 | WARN |
| 06 | entity_extraction | 4 | 4 | 4 | 4 | 4 | OK |
| 07 | concept_extraction | 3 | 3 | 2 | 4 | 2 | WARN |
| 08 | coreference_resolution | 4 | 3 | 4 | 4 | 4 | WARN |
| 09 | relation_extraction | 2 | 1 | 2 | 3 | 1 | FAIL |
| 10 | canonical_claims / semantic_claims | 4 | 4 | 4 | 4 | 4 | OK |
| 11 | semantic_debug_ir | 3 | 2 | 4 | 4 | 3 | WARN |
| 12 | triple_extraction | 3 | 3 | 4 | 4 | 3 | WARN |
| 13 | taxonomy_induction | 4 | 4 | 4 | 4 | 4 | OK |
| 14 | type_assertion | 4 | 4 | 4 | 4 | 4 | OK |
| 15 | semantic_quality | 2 | 2 | 1 | 4 | 2 | FAIL |
| 16 | output_generation | 3 | 3 | 3 | 4 | 3 | WARN |

`semantic_debug_ir` está configurado; por tanto no corresponde N/A. `entity_extraction` y `type_assertion` no se penalizan por devolver listas vacías: el texto no contiene nombres propios ni instancias inequívocas.

## 3. Hallazgos

### Q-infosec_p025_p026-05-1

- **Severidad:** Alta
- **Tipo:** Anotación morfosintáctica incorrecta
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** “A visitor log records external persons entering a facility.” (`p026`)
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p025_p026/artifacts/pipeline_outputs/observed_p025_p026_05_linguistic_annotation.json`, `/tokens/173` y `/tokens/174`
- **Evaluación razonada:** `log` queda como `nmod` de `records`, mientras `records` se etiqueta `NOUN/NNS` y `ROOT`. En la oración citada, `records` realiza la predicación y `visitor log` es su sujeto. La anotación conserva el texto y offsets, pero su estructura no representa la proposición literal.
- **Impacto downstream:** el error se propaga a los conceptos sobredimensionados de 07 y contribuye a que 09 no produzca `VisitorLog records ExternalPerson`. No alcanza el modelo final porque 10 reconstruye correctamente ambas proposiciones de la oración: **ERROR_CORREGIDO** desde 10.

### Q-infosec_p025_p026-07-1

- **Severidad:** Media
- **Tipo:** Frontera conceptual degradada
- **Atribución:** ERROR_PROPAGADO
- **Cita literal:** “A visitor log records external persons entering a facility.” (`p026`)
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p025_p026/artifacts/pipeline_outputs/observed_p025_p026_07_concept_extraction.json`, `/concepts/35` y `/concepts/36`
- **Evaluación razonada:** se proponen “visitor log records external persons” y toda la oración nominal como conceptos, en lugar de candidatos separados `visitor log` y `external persons`. Es la manifestación del error de 05, no un error nuevo contado de nuevo. Además, la lista no propone `physical access control` ni `monitoring control`, aunque ambos aparecen literalmente en `p026`; dado que esta etapa solo propone candidatos, la omisión se considera cobertura parcial y no invención.
- **Impacto downstream:** degrada los insumos de 09. Las cuatro categorías reaparecen correctamente en las claims de 10 y en la taxonomía/final, por lo que la pérdida queda **CORREGIDA** antes de RDF/OWL.

### Q-infosec_p025_p026-09-1

- **Severidad:** Alta
- **Tipo:** Conflación de referencias semánticas
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** “A service-level agreement defines expected service performance and availability.” (`p025`) y “Physical security protects facilities, equipment, people, and physical assets.” (`p026`)
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p025_p026/artifacts/pipeline_outputs/observed_p025_p026_09_relation_extraction.json`, `/relations/0/subject_ref` y `/relations/4/subject_ref`
- **Evaluación razonada:** la relación del service-level agreement referencia el concepto de data processing agreement (`con-accf...`), y la relación de physical security referencia el concepto de supplier security (`con-502...`). Los textos de sujeto se reducen además a `agreement` y `security`. Esto mezcla documentos y ámbitos que el texto mantiene separados.
- **Impacto downstream:** si se proyectara, produciría sujetos erróneos entre párrafos. 10 usa `ServiceLevelAgreement` y `PhysicalSecurity` correctamente, así que la conflación es **ERROR_CORREGIDO** y no llega a RDF/OWL.

### Q-infosec_p025_p026-09-2

- **Severidad:** Alta
- **Tipo:** Pérdida y mala representación de relaciones explícitas
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** “A cloud provider is a type of supplier.”, “Third-party access must be approved, monitored, and revoked when no longer required.” (`p025`), y “Physical access to restricted areas must be authorized and monitored.” (`p026`)
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p025_p026/artifacts/pipeline_outputs/observed_p025_p026_09_relation_extraction.json`, `/relations/13`, `/relations/8` y `/relations`
- **Evaluación razonada:** los patrones “is a type of” se reducen a relaciones como `CloudProvider be type`, sin el superclass `Supplier`; el mismo defecto afecta las siete oraciones con “type of”. No aparecen las cinco obligaciones deónticas ni su condición, y faltan varias relaciones y roles explícitos (personas y assets protegidos, data center/hosts, temas/participantes de documentos). Esto corresponde a la responsabilidad propia de extracción de relaciones, no a taxonomy induction.
- **Impacto downstream:** es la mayor degradación intermedia por cobertura. 10 reconstruye las ocho taxonomías, las obligaciones, la condición y las coordinaciones; por ello el conjunto queda **ERROR_CORREGIDO** antes de triples y RDF/OWL.

### Q-infosec_p025_p026-11-1

- **Severidad:** Media
- **Tipo:** Proyección incompleta en IR de depuración
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** “obligations between the organization and the supplier” y “responsibilities related to personal data” (`p025`)
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p025_p026/artifacts/pipeline_outputs/observed_p025_p026_11_semantic_debug_ir.json`, `/artifacts/semantic_debug_ir/relations/9`, `/artifacts/semantic_debug_ir/relations/10` y `/artifacts/semantic_debug_ir/entities`
- **Evaluación razonada:** las claims de entrada estructuran `participant_a`, `participant_b`, `relation_scope` y `topic`, pero el IR de depuración elimina esos campos y tampoco crea entidades trazables para `Organization` o `PersonalData`. El SPO básico y la evidencia se conservan, pero el sidecar ya no permite depurar toda la semántica proyectada.
- **Impacto downstream:** el sidecar no es la fuente declarada de la proyección final; por ello esta pérdida no causa por sí sola el output 16. Sí dificulta detectar la incoherencia posterior de esos mismos roles.

### Q-infosec_p025_p026-12-1

- **Severidad:** Media
- **Tipo:** Pérdida inconsistente de adjuntos semánticos al convertir claims a triples
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** “between the organization and the supplier”, “related to personal data” (`p025`) y “records external persons entering a facility” (`p026`)
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p025_p026/artifacts/pipeline_outputs/observed_p025_p026_12_triple_extraction.json`, `/triples/22`, `/triples/13` y `/triples/12`
- **Evaluación razonada:** están los 37 SPO con evidencia y claim IDs, pero desaparecen participantes del contrato, tema de personal data y `recorded_event=entering`, aunque otros adjuntos (`target`, `patient`, `location`, modalidad y condición) sí se preservan. Para un SPO básico la cobertura es completa; para una conversión semánticamente trazable es parcial e inconsistente.
- **Impacto downstream:** 16 vuelve a leer `semantic_claims` y recupera esos campos en `facts`; por tanto esta pérdida concreta es **ERROR_CORREGIDO**, aunque la normalización RDF de algunos valores sigue incompleta.

### Q-infosec_p025_p026-15-1

- **Severidad:** Alta
- **Tipo:** Falso positivo de ruido y evaluación sobreoptimista
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** “A data center is a type of facility that hosts computing infrastructure.” (`p026`)
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p025_p026/artifacts/pipeline_outputs/observed_p025_p026_15_semantic_quality.json`, `/semantic_quality_report/concept_noise/0`, `/excluded_concepts/0` y `/semantic_quality_report/quality_score`
- **Evaluación razonada:** `computing infrastructure` es un objeto nominal explícito de `hosts`, no “verbal_clause_boundary_noise”. Excluirlo contradice la claim y el triple válidos ya presentes. A la vez, `quality_score=0.95`, `rdf_readiness=true` y una lista vacía de issues no reflejan ni este falso positivo ni las pérdidas de roles observables en las proyecciones auxiliares.
- **Impacto downstream:** 16 incluye `ComputingInfrastructure` y `DataCenter hosts ComputingInfrastructure`, por lo que la exclusión queda **ERROR_CORREGIDO** en el output final. Sin esa corrección, se perdería una proposición explícita completa.

### Q-infosec_p025_p026-16-1

- **Severidad:** Alta
- **Tipo:** Recursos y roles no normalizados en el modelo final
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** “obligations between the organization and the supplier” y “responsibilities related to personal data” (`p025`)
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p025_p026/artifacts/pipeline_outputs/observed_p025_p026_16_output_generation.json`, `/output/graph/facts/3/participant_a`, `/output/graph/facts/3/participant_b`, `/output/graph/facts/4/topic` y `/output/graph/classes`
- **Evaluación razonada:** el modelo conserva los roles como cadenas desnudas (`Organization`, `Supplier`, `PersonalData`) en lugar de recursos `orion:` coherentes. `Supplier` sí existe como clase pero aquí no se referencia por IRI; `Organization` y `PersonalData` ni siquiera aparecen en `classes`. La evidencia textual evita una pérdida total, pero los roles no forman parte conectada del grafo RDF/OWL.
- **Impacto downstream:** es la principal pérdida del output final: consultas sobre participantes contractuales o el tema de la data processing agreement no pueden seguir aristas o recursos homogéneos. El defecto sí llega al modelo final.

### Q-infosec_p025_p026-16-2

- **Severidad:** Media
- **Tipo:** Promoción ontológica no soportada de nominalizaciones
- **Atribución:** ERROR_AMPLIFICADO
- **Cita literal:** “must be approved, monitored, and revoked” (`p025`) y “must be authorized and monitored” (`p026`)
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p025_p026/artifacts/pipeline_outputs/observed_p025_p026_16_output_generation.json`, `/output/graph/classes/0`, `/output/graph/classes/1`, `/output/graph/classes/21`, `/output/graph/classes/36` y `/output/graph/scoped_relations`
- **Evaluación razonada:** las nominalizaciones `Approval`, `Authorization`, `Monitoring` y `Revocation` son una forma plausible de completar SPO, y las `scoped_relations` preservan correctamente modalidad y condición. Sin embargo, declararlas como clases ontológicas es más fuerte que el texto: los párrafos expresan estados/acciones pasivas obligatorias, no una taxonomía de esas nominalizaciones. La nominalización nace como representación entrañada en 10 y se amplifica a classhood **NO SOPORTADA** en 16.
- **Impacto downstream:** no inventa agentes ni elimina la modalidad, pero introduce en RDF/OWL compromisos de clase que no están literalmente justificados. Es el principal contenido no soportado del output final.

## 4. Diagnóstico

- **Primera degradación:** paso 05. La lectura superficial permanece íntegra hasta tokenización; `records` en la oración de visitor log recibe categoría y dependencia erróneas. También hay una estructura dudosa en “hosts computing infrastructure” (`p026`), donde la anotación conecta `computing` con `type`; ambas anomalías son corregidas por las claims.
- **Principal pérdida:** en el pipeline intermedio, paso 09 pierde o deforma gran parte de las relaciones explícitas y mezcla referencias entre conceptos. En el output final, la pérdida principal es más acotada: `Organization` y `PersonalData` quedan como cadenas no declaradas/no conectadas, y `Supplier` se usa como cadena en un rol pese a existir como IRI.
- **Principal contenido no soportado:** la declaración como clases RDF/OWL de `Approval`, `Authorization`, `Monitoring` y `Revocation`. La nominalización es **PLAUSIBLE/ENTRAÑADA** como técnica representacional; su classhood es **NO SOPORTADA** por `p025` o `p026`.
- **Errores que llegan a RDF/OWL:** (1) participantes y tema sin normalización a recursos; (2) classhood de nominalizaciones deónticas. No llegan a RDF/OWL la conflación de agreements/security de 09, la pérdida de visitor log ni la falsa exclusión de computing infrastructure: todos quedan corregidos.
- **Aciertos:** intake, normalización, 19 oraciones, tokens y offsets son fieles; 10 reconstruye 37 claims con evidencia por párrafo/oración, conserva disyunción, coordinación, modalidad, condición y roles; 13 induce exactamente las ocho taxonomías explícitas; 14 evita inventar instancias; 16 conserva las cinco obligaciones como relaciones scoped, la alternativa goods/services como disyunción y la proposición sobre computing infrastructure pese al falso positivo de 15.
- **Incertidumbres legítimas:** el alcance de `expected` sobre availability (`p025`), el antecedente inmediato de las dos relativas con `that`, y la proyección de “protect equipment from hazards” a `protectsAgainst`. El output es razonable al no forzar expected sobre availability y es fiel en hazards porque conserva `patient=Equipment`. No se penaliza ese conservadurismo.

## 5. Veredicto

- **Calidad global:** **84/100**.
- **Output final:** **parcialmente fiel**. Cubre prácticamente todas las proposiciones, taxonomías, coordinaciones y modalidades, y corrige las degradaciones graves de las etapas 05–09. No alcanza “fiel” porque parte de la semántica de participantes/tema no queda conectada como RDF/OWL y porque convierte nominalizaciones de acciones obligatorias en clases no afirmadas por el texto.
- **Tres correcciones prioritarias:**
  1. Proyectar `Organization`, `Supplier` y `PersonalData` como recursos `orion:` declarados y conectados, conservando `between` y `related_to/topic` como estructura consultable.
  2. Representar approval/authorization/monitoring/revocation como estados o nodos scoped de la obligación sin promoverlos automáticamente a clases ontológicas.
  3. Corregir la cadena temprana de análisis (`records` verbal, relativas y “type of”) y hacer que semantic quality valide contra las claims antes de excluir un concepto explícito como `computing infrastructure`.

Siguiente caso pendiente: infosec_p027_p028.
