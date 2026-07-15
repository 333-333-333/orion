# Revisión semántica: infosec_p013_p014

## 1. Lectura independiente

### Resumen

Los dos párrafos presentan, en modo genérico y asertivo, controles, tecnologías, activos y efectos de seguridad de red (`p013`) y de endpoints (`p014`). El texto combina cuatro estructuras semánticas: relaciones funcionales (`protects`, `reduces`, `separates`, `hosts`, `exposes`), taxonomías explícitas mediante “is a type of”, propiedades definitorias mediante relativas o participios, y mecanismos/finalidades introducidos por “by”, “into”, “to” y “used for”.

No aparecen nombres propios ni individuos nombrados. Los sintagmas indefinidos (“a firewall”, “an endpoint”, “a server”) se usan genéricamente como clases o categorías, no como instancias. “The organizational network” introduce un referente definido, pero el texto no permite decidir si designa una red concreta o una clase contextual.

### Conceptos

- **`p013`:** network security; communication channel; network device; network service; firewall; network access control system; network security control; intrusion detection system; detective network control; intrusion prevention system; preventive network control; virtual private network; remote access; encrypted communication tunnel; network segmentation; system; different zone; demilitarized zone; network segment; controlled service; external network; production network; business system; management network; administrative access.
- **`p014`:** endpoint security; laptop; desktop; mobile device; server; endpoint; device; organizational network; antivirus software; endpoint protection control; endpoint detection and response; endpoint security technology; device encryption; data; patch management; vulnerability; software update; configuration hardening; attack surface; unnecessary service; secure setting; workstation; mobile phone.
- **Entidades/instancias explícitas:** ninguna instancia nombrada. Todos los anteriores son términos genéricos. No está soportado convertir los artículos indefinidos en individuos RDF.
- **Definiciones explícitas o definitorias:** “An endpoint is a device connected to the organizational network” (`p014`); las catorce expresiones “is a type of”; y las caracterizaciones restrictivas o de finalidad de demilitarized zone, production network y management network (`p013`).

### Proposiciones con evidencia

| ID | Proposición mínima | Evidencia breve | Clasificación |
|---|---|---|---|
| P013-01 | Network security protege communication channels. | `p013`: “protects communication channels” | EXPLÍCITO |
| P013-02 | Network security protege network devices. | `p013`: “network devices” | EXPLÍCITO |
| P013-03 | Network security protege network services. | `p013`: “and network services” | EXPLÍCITO |
| P013-04 | Firewall es subtipo de network security control. | `p013`: “A firewall is a type of…” | EXPLÍCITO |
| P013-05 | Network access control system es subtipo de network security control. | `p013`: “A network access control system is a type of…” | EXPLÍCITO |
| P013-06 | Intrusion detection system es subtipo de detective network control. | `p013`: “is a type of detective network control” | EXPLÍCITO |
| P013-07 | Intrusion prevention system es subtipo de preventive network control. | `p013`: “is a type of preventive network control” | EXPLÍCITO |
| P013-08 | Virtual private network protege remote access. | `p013`: “protects remote access” | EXPLÍCITO |
| P013-09 | Virtual private network crea un encrypted communication tunnel como medio de P013-08. | `p013`: “by creating an encrypted communication tunnel” | ENTRAÑADO |
| P013-10 | Network segmentation separa systems. | `p013`: “separates systems” | EXPLÍCITO |
| P013-11 | El destino de la separación son different zones. | `p013`: “into different zones” | EXPLÍCITO |
| P013-12 | Demilitarized zone es subtipo de network segment. | `p013`: “is a type of network segment” | EXPLÍCITO |
| P013-13 | La clase descrita por la relativa expone controlled services. | `p013`: “that exposes controlled services” | EXPLÍCITO |
| P013-14 | La exposición de P013-13 tiene como destino external networks. | `p013`: “to external networks” | EXPLÍCITO |
| P013-15 | Production network es subtipo de network segment. | `p013`: “A production network is a type of network segment” | EXPLÍCITO |
| P013-16 | La clase descrita por la relativa aloja business systems. | `p013`: “that hosts business systems” | EXPLÍCITO |
| P013-17 | Management network es subtipo de network segment. | `p013`: “A management network is a type of network segment” | EXPLÍCITO |
| P013-18 | La clase descrita se usa para administrative access. | `p013`: “used for administrative access” | EXPLÍCITO |
| P014-01 | Endpoint security protege laptops. | `p014`: “protects laptops” | EXPLÍCITO |
| P014-02 | Endpoint security protege desktops. | `p014`: “desktops” | EXPLÍCITO |
| P014-03 | Endpoint security protege mobile devices. | `p014`: “mobile devices” | EXPLÍCITO |
| P014-04 | Endpoint security protege servers. | `p014`: “and servers” | EXPLÍCITO |
| P014-05 | Endpoint es una clase de device. | `p014`: “An endpoint is a device” | EXPLÍCITO |
| P014-06 | Endpoint tiene como propiedad definitoria estar connected to the organizational network. | `p014`: “device connected to the organizational network” | ENTRAÑADO |
| P014-07 | Antivirus software es subtipo de endpoint protection control. | `p014`: “is a type of endpoint protection control” | EXPLÍCITO |
| P014-08 | Endpoint detection and response es subtipo de endpoint security technology. | `p014`: “is a type of endpoint security technology” | EXPLÍCITO |
| P014-09 | Device encryption protege data. | `p014`: “protects data” | EXPLÍCITO |
| P014-10 | La data protegida está stored on an endpoint. | `p014`: “data stored on an endpoint” | EXPLÍCITO |
| P014-11 | Patch management reduce vulnerabilities. | `p014`: “reduces vulnerabilities” | EXPLÍCITO |
| P014-12 | Patch management aplica software updates como medio de P014-11. | `p014`: “by applying software updates” | ENTRAÑADO |
| P014-13 | Configuration hardening reduce attack surface. | `p014`: “reduces attack surface” | EXPLÍCITO |
| P014-14 | Configuration hardening deshabilita unnecessary services como medio de P014-13. | `p014`: “by disabling unnecessary services” | ENTRAÑADO |
| P014-15 | Configuration hardening aplica secure settings como medio coordinado de P014-13. | `p014`: “and applying secure settings” | ENTRAÑADO |
| P014-16 | Laptop es subtipo de endpoint. | `p014`: “A laptop is a type of endpoint” | EXPLÍCITO |
| P014-17 | Workstation es subtipo de endpoint. | `p014`: “A workstation is a type of endpoint” | EXPLÍCITO |
| P014-18 | Mobile phone es subtipo de endpoint. | `p014`: “A mobile phone is a type of endpoint” | EXPLÍCITO |
| P014-19 | Server es subtipo de endpoint. | `p014`: “A server is a type of endpoint” | EXPLÍCITO |

### Taxonomías explícitas

No se añade transitividad ni conocimiento de dominio. Las únicas taxonomías soportadas son:

1. `p013`: Firewall ⊑ NetworkSecurityControl.
2. `p013`: NetworkAccessControlSystem ⊑ NetworkSecurityControl.
3. `p013`: IntrusionDetectionSystem ⊑ DetectiveNetworkControl.
4. `p013`: IntrusionPreventionSystem ⊑ PreventiveNetworkControl.
5. `p013`: DemilitarizedZone ⊑ NetworkSegment.
6. `p013`: ProductionNetwork ⊑ NetworkSegment.
7. `p013`: ManagementNetwork ⊑ NetworkSegment.
8. `p014`: Endpoint ⊑ Device.
9. `p014`: AntivirusSoftware ⊑ EndpointProtectionControl.
10. `p014`: EndpointDetectionAndResponse ⊑ EndpointSecurityTechnology.
11. `p014`: Laptop ⊑ Endpoint.
12. `p014`: Workstation ⊑ Endpoint.
13. `p014`: MobilePhone ⊑ Endpoint.
14. `p014`: Server ⊑ Endpoint.

En particular, DetectiveNetworkControl ⊑ NetworkSecurityControl, PreventiveNetworkControl ⊑ NetworkSecurityControl, Desktop ⊑ Endpoint y MobileDevice ⊑ Endpoint son **NO SOPORTADO** por estos párrafos, aunque pudieran resultar plausibles con conocimiento externo.

### Modalidad

- Todas las oraciones son genéricas, declarativas y asertivas en presente; no hay posibilidad, probabilidad, obligación, negación ni condicionalidad explícitas.
- `p013` “by creating…” y `p014` “by applying…”, “by disabling… and applying…” expresan **medio/mecanismo**, no taxonomía ni causalidad universal independiente.
- `p013` “used for…” expresa **finalidad**.
- `p013` “into different zones” y “to external networks”, y `p014` “on an endpoint”, expresan argumentos locativos/destino que forman parte de la proposición y no deben descartarse al reducirla a SPO.
- Las relativas y participiales son restrictivas/definitorias; no introducen nuevos individuos.

### Ambigüedades

- **Correferencia de “that” (`p013`):** en “a type of network segment that exposes…” y “a type of network segment that hosts…”, el antecedente sintáctico inmediato es “network segment”. Proyectar la propiedad sobre DemilitarizedZone o ProductionNetwork es **ENTRAÑADO** bajo la lectura de subtipo definido por esa propiedad y, como mínimo, **PLAUSIBLE**; afirmar que todo NetworkSegment expone o aloja esos objetos es **NO SOPORTADO**.
- **Participio “used” (`p013`):** puede adjuntarse formalmente a “network segment”, aunque la lectura informativa natural caracteriza ManagementNetwork. No debe generalizarse a todo NetworkSegment.
- **“Endpoint” y “device” (`p014`):** la definición soporta Endpoint ⊑ Device y la conexión definitoria; no soporta Device ⊑ Endpoint.
- **Plural frente a clase:** “laptops”, “servers”, etc. son menciones genéricas. Singularizarlas para nombrar clases es **ENTRAÑADO**; convertirlas en individuos es **NO SOPORTADO**.
- **Separación entre ámbitos:** que NetworkSecurity proteja laptops/desktops es **NO SOPORTADO**; `p014` asigna esa relación a EndpointSecurity. La interpretación contraria “un endpoint está desconectado de la red organizativa” queda **CONTRADICHO** por `p014`: “connected to the organizational network”.

## 2. Resultado por etapa

Escala: 0 = ausente/incorrecto; 4 = completo y fiel. Las puntuaciones se limitan a la responsabilidad contractual de cada etapa.

| Paso | Etapa | Fidelidad | Cobertura | Precisión | Trazabilidad | Coherencia | Estado |
|---:|---|---:|---:|---:|---:|---:|---|
| 01 | input_intake | 4 | 4 | 4 | 4 | 4 | OK |
| 02 | preprocessing | 4 | 4 | 4 | 4 | 4 | OK |
| 03 | sentence_segmentation | 4 | 4 | 4 | 4 | 4 | OK |
| 04 | tokenization | 4 | 4 | 4 | 4 | 4 | OK |
| 05 | linguistic_annotation | 3 | 4 | 3 | 4 | 3 | WARN |
| 06 | entity_extraction | 4 | 4 | 4 | 4 | 4 | OK |
| 07 | concept_extraction | 3 | 2 | 3 | 4 | 2 | WARN |
| 08 | coreference_resolution | 4 | 4 | 4 | 4 | 4 | OK |
| 09 | relation_extraction | 1 | 1 | 1 | 2 | 1 | FAIL |
| 10 | canonical_claims / semantic_claims | 4 | 4 | 4 | 4 | 4 | OK |
| 11 | semantic_debug_ir | 4 | 4 | 4 | 4 | 4 | OK |
| 12 | triple_extraction | 4 | 4 | 4 | 4 | 4 | OK |
| 13 | taxonomy_induction | 4 | 4 | 4 | 4 | 4 | OK |
| 14 | type_assertion | 4 | 4 | 4 | 4 | 4 | OK |
| 15 | semantic_quality | 2 | 1 | 1 | 3 | 2 | FAIL |
| 16 | output_generation | 3 | 3 | 4 | 4 | 2 | WARN |

La etapa 11 está configurada y produce un sidecar; por ello no es N/A. La ausencia de entidades en 06 y de type assertions en 14 es correcta: el texto no contiene individuos nombrados.

## 3. Hallazgos

### Q-infosec_p013_p014-05-1

- **Severidad:** BAJA
- **Tipo:** ANOTACIÓN_LINGÜÍSTICA_INCONSISTENTE
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** `p014`: “Endpoint security protects laptops, desktops, mobile devices, and servers.”
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p013_p014/artifacts/pipeline_outputs/observed_p013_p014_05_linguistic_annotation.json` — `/tokens/127/lemma`, `/tokens/127/pos` (también `/tokens/151/lemma` y `/tokens/182/lemma`).
- **Evaluación razonada:** “Endpoint” queda como lema `Endpoint` y POS `PROPN` por estar al inicio, mientras otras apariciones del mismo término se anotan como nombre común y lema `endpoint`. El mismo efecto de capitalización aparece en “Antivirus” y “Patch”. Es evidencia lingüística válida pero inconsistente para identidad conceptual genérica.
- **Impacto downstream:** puede fragmentar conceptos por capitalización/POS. En este caso, 07 y especialmente 10 normalizan los conceptos, por lo que el defecto no llega al modelo final.

### Q-infosec_p013_p014-07-1

- **Severidad:** ALTA
- **Tipo:** OMISIÓN_DE_CONCEPTOS_RELACIONALES
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** `p013`: “A firewall is a type of network security control.”; `p014`: “Antivirus software is a type of endpoint protection control.”
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p013_p014/artifacts/pipeline_outputs/observed_p013_p014_07_concept_extraction.json` — `/concepts`.
- **Evaluación razonada:** se proponen `firewall` y `antivirus software`, pero se omiten como candidatos los objetos taxonómicos de las construcciones “type of”: NetworkSecurityControl, DetectiveNetworkControl, PreventiveNetworkControl, NetworkSegment, EndpointProtectionControl y EndpointSecurityTechnology. También faltan varias apariciones de Endpoint como objeto de las cuatro taxonomías finales. La omisión no inventa contenido, pero reduce sustancialmente la cobertura propia de la etapa.
- **Impacto downstream:** el error se propaga a 09, donde las relaciones taxonómicas quedan como `be(type)` sin objeto conceptual. La etapa 10 lo corrige reconstruyendo las definiciones explícitas.

### Q-infosec_p013_p014-07-2

- **Severidad:** MEDIA
- **Tipo:** CONTAMINACIÓN_DE_CONCEPTO
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** `p014`: “Configuration hardening reduces attack surface by disabling unnecessary services and applying secure settings.”
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p013_p014/artifacts/pipeline_outputs/observed_p013_p014_07_concept_extraction.json` — `/concepts/39`.
- **Evaluación razonada:** el candidato `unnecessary services and applying secure settings` incorpora el verbo “applying” y fusiona dos objetos coordinados. Los conceptos fieles son UnnecessaryService y SecureSetting, unidos por dos mecanismos coordinados, no un único concepto nominal.
- **Impacto downstream:** 09 no recupera los dos mecanismos desde este candidato. 10 corrige el error creando dos claims separados y conservando la coordinación y el objetivo común.

### Q-infosec_p013_p014-09-1

- **Severidad:** CRÍTICA
- **Tipo:** COLISIÓN_DE_IDENTIDAD_Y_REFERENCIA
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** `p014`: “Endpoint security protects laptops, desktops, mobile devices, and servers.”; `p013`: “A production network is a type of network segment that hosts business systems.”
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p013_p014/artifacts/pipeline_outputs/observed_p013_p014_09_relation_extraction.json` — `/relations/6/subject_ref`, `/relations/6/subject_text`, `/relations/7/subject_ref`, `/relations/11/subject_ref`.
- **Evaluación razonada:** las relaciones de EndpointSecurity usan como sujeto `security` y enlazan al concepto de NetworkSecurity (`con-92338985246a0069`). Además, las relaciones cuyo `subject_text` es `network segment` enlazan al concepto de VirtualPrivateNetwork (`con-409234144aed85ef`). El texto no soporta que NetworkSecurity proteja laptops/desktops ni que VirtualPrivateNetwork sea el sujeto que aloja BusinessSystem.
- **Impacto downstream:** corrompe identidad, precisión y trazabilidad en 09. No llega a RDF porque 10 reemplaza esos sujetos por EndpointSecurity, ProductionNetwork y DemilitarizedZone con evidencia de párrafo correcta.

### Q-infosec_p013_p014-09-2

- **Severidad:** ALTA
- **Tipo:** PÉRDIDA_RELACIONAL_Y_TAXONÓMICA
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** `p013`: “A firewall is a type of network security control.”; `p014`: “An endpoint is a device connected to the organizational network.”
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p013_p014/artifacts/pipeline_outputs/observed_p013_p014_09_relation_extraction.json` — `/relations/18`, `/relations/8`, `/relations`.
- **Evaluación razonada:** las construcciones “is a type of X” se reducen a `subject —be→ type`, sin X. La etapa omite además NetworkService en la lista de `p013`, MobileDevice y Server en la de `p014`, la conexión definitoria de Endpoint, los destinos `into/to`, la finalidad `used for` y casi todos los mecanismos introducidos por “by”. Esto excede el conservadurismo ante ambigüedad: son argumentos literales.
- **Impacto downstream:** 09 no puede sostener por sí sola la semántica del caso. 10 corrige esta degradación; por independencia de responsabilidades, 12–14 no se penalizan por el defecto ya corregido.

### Q-infosec_p013_p014-10-1

- **Severidad:** INFORMATIVA
- **Tipo:** RECUPERACIÓN_SEMÁNTICA_COMPLETA
- **Atribución:** ERROR_CORREGIDO
- **Cita literal:** `p013`: “Network security protects communication channels, network devices, and network services.”; `p014`: “Configuration hardening reduces attack surface by disabling unnecessary services and applying secure settings.”
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p013_p014/artifacts/pipeline_outputs/observed_p013_p014_10_canonical_claims.json` — `/canonical_claims/claims`, en especial `/canonical_claims/claims/0`, `/canonical_claims/claims/21`, `/canonical_claims/claims/23` y `/canonical_claims/claims/32`–`/canonical_claims/claims/34`.
- **Evaluación razonada:** los 35 claims cubren las proposiciones principales, taxonomías y descomposiciones de mecanismos/argumentos; restauran NetworkService, los cuatro objetos de EndpointSecurity, los sujetos completos, las catorce taxonomías, los destinos y las propiedades definitorias. Cada claim incluye evidencia, párrafo, oración y `source_text_id`.
- **Impacto downstream:** impide que las colisiones y pérdidas de 09 alcancen triples, taxonomía y RDF. Es el principal acierto del pipeline.

### Q-infosec_p013_p014-15-1

- **Severidad:** ALTA
- **Tipo:** CONTROL_DE_CALIDAD_CIEGO_A_DEFECTOS_OBSERVABLES
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** `p014`: “Configuration hardening reduces attack surface by disabling unnecessary services and applying secure settings.”; `p013`: “A firewall is a type of network security control.”
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p013_p014/artifacts/pipeline_outputs/observed_p013_p014_15_semantic_quality.json` — `/semantic_quality_report/quality_score`, `/semantic_quality_report/concept_noise`, `/semantic_quality_report/relation_gaps`, `/semantic_quality_report/warnings`.
- **Evaluación razonada:** declara `quality_score: 1.0`, listas de ruido/gaps vacías y ausencia de warnings pese al concepto contaminado de 07 y a las relaciones sin objeto taxonómico y con referencias cruzadas incorrectas de 09. Que 10 haya corregido el flujo canónico no hace perfectos todos los componentes que el contrato de 15 dice evaluar: conceptos, entidades, relaciones y triples.
- **Impacto downstream:** no introduce hechos falsos, pero produce una señal de confianza excesiva y no permite localizar la degradación intermedia. El output se genera sin advertencia semántica.

### Q-infosec_p013_p014-16-1

- **Severidad:** MEDIA
- **Tipo:** DUPLICACIÓN_ESTRUCTURAL
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** `p013`: “A firewall is a type of network security control.”
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p013_p014/artifacts/pipeline_outputs/observed_p013_p014_16_output_generation.json` — `/output/graph/classes` y `/output/graph/schema/classes`; `/output/graph/facts` y `/output/graph/object_property_facts`; `/output/graph/subclass_facts` y `/taxonomy_relations`.
- **Evaluación razonada:** el mismo inventario de clases y los mismos hechos reaparecen en vistas paralelas dentro del output. Aunque algunas vistas añaden metadatos de uso, la representación final no es canónica y única. No hay invención semántica, pero sí duplicación estructural contraria al requisito de un modelo final sin duplicación.
- **Impacto downstream:** consumidores que no distingan vistas de materialización, esquema observado y resumen pueden contabilizar o serializar dos veces clases y aristas.

### Q-infosec_p013_p014-16-2

- **Severidad:** ALTA
- **Tipo:** PÉRDIDA_DE_ARGUMENTO_EN_PROYECCIÓN_RDF
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** `p013`: “Network segmentation separates systems into different zones.”; “A demilitarized zone … exposes controlled services to external networks.”
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p013_p014/artifacts/pipeline_outputs/observed_p013_p014_16_output_generation.json` — `/output/graph/facts/12/target`, `/output/graph/facts/13/target`, `/output/graph/projection/claim_dispositions/23/output_spo`, `/output/graph/projection/claim_dispositions/25/output_spo`, `/output/graph/restrictions`, `/output/graph/scoped_relations`.
- **Evaluación razonada:** `DifferentZone` y `ExternalNetwork` sobreviven como campos auxiliares `target`, pero no forman parte de los SPO marcados como materializados; `restrictions` y `scoped_relations` están vacíos. Por tanto, el JSON permite rastrear el argumento, pero la proyección RDF declarada no expresa semánticamente “into different zones” ni “to external networks”.
- **Impacto downstream:** un consumidor RDF ve `NetworkSegmentation separates System` y `DemilitarizedZone exposes ControlledService`, pero pierde los destinos que delimitan ambas proposiciones. Es la principal pérdida que sí alcanza el modelo final.

## 4. Diagnóstico

- **Primera degradación:** 05 introduce una inconsistencia menor de lema/POS por capitalización. La primera degradación semántica material aparece en 07 al omitir objetos taxonómicos y fusionar los dos mecanismos de configuration hardening.
- **Principal pérdida:** 09 pierde sujetos completos, miembros de coordinaciones, objetos taxonómicos y argumentos oblicuos. La mayor parte queda corregida en 10; en 16 persiste la no materialización RDF de `DifferentZone` y `ExternalNetwork` como argumentos semánticos.
- **Principal contenido no soportado:** en 09, las referencias hacen que las relaciones de `p014` puedan leerse como NetworkSecurity protegiendo laptops/desktops y que VirtualPrivateNetwork aloje BusinessSystem. Ambas lecturas son **NO SOPORTADO**. No llegan al output final.
- **Errores que llegan a RDF/OWL:** no llegan taxonomías inventadas ni type assertions de individuos; las catorce subclases son fieles. Sí llegan (a) pérdida de los destinos en los SPO materializados y (b) duplicación de vistas del mismo contenido. El resto de los errores de 07/09 queda corregido antes de RDF.
- **Aciertos:** intake, normalización, 21 oraciones, 238 tokens y offsets son fieles; 06 y 14 conservan correctamente la ausencia de instancias; 08 resuelve las dos relativas con trazabilidad y sin sobreafirmar; 10 recupera 35 claims respaldados; 12 conserva metadatos de medio, finalidad, ubicación y grupos proposicionales; 13 reproduce exactamente las catorce taxonomías explícitas.
- **Incertidumbres:** la adjunción de “that” y “used” en `p013` admite una lectura sintáctica sobre NetworkSegment y una lectura definitoria sobre sus subtipos. La elección final de DemilitarizedZone/ProductionNetwork/ManagementNetwork es razonable y no se penaliza, pero no autoriza propiedades universales para todo NetworkSegment. “The organizational network” permanece ambiguo entre referente contextual y clase.

## 5. Veredicto

- **Calidad global:** **86/100**.
- **Output final:** **parcialmente fiel**. El contenido canónico y las catorce taxonomías son precisos y no inventan conocimiento de dominio; sin embargo, la proyección RDF no materializa dos argumentos de destino y el modelo presenta duplicación estructural.
- **Tres correcciones prioritarias:**
  1. Corregir 09 para extraer relaciones con el concepto completo y su referencia correcta, cubrir coordinaciones y reconocer `is a type of X` con X como objeto.
  2. Hacer que 15 contraste conceptos y relaciones observados con claims/triples, detecte ruido, referencias cruzadas y gaps, y no otorgue calidad perfecta cuando existen.
  3. En 16, materializar los argumentos `into/to` mediante una representación RDF inequívoca y emitir una sola vista canónica de clases, hechos y taxonomías.

Siguiente caso pendiente: infosec_p015_p016.
