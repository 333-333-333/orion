# Revisión semántica: infosec_p021_p022

## 1. Lectura independiente

### Resumen

Los dos párrafos son descripciones genéricas, no relatos sobre individuos concretos.

- **p021** describe funciones y artefactos de monitorización de seguridad: un sistema de gestión de información y eventos de seguridad, recolección, normalización y correlación de logs, reglas de detección, casos de uso, dashboards, analistas y políticas de retención.
- **p022** define la respuesta a incidentes como un proceso compuesto por actividades, describe el resultado de varias de esas actividades y define un plan de respuesta a incidentes como documento.
- No hay nombres propios, organizaciones, productos identificados, incidentes concretos ni otras instancias individualizadas. Los sintagmas indefinidos y plurales expresan clases o conceptos genéricos.

### Conceptos

**p021:** security information and event management system; security logs; log collection; records; systems; applications; log normalization; log formats; common structure; log correlation; relationships; events; detection rule; conditions; alert; use case; scenario; monitoring; dashboard; security metrics; operational status; security analyst; monitoring system; log retention policy; storage duration no especificada; logs.

**p022:** incident response; process; preparation/preparing; detection/detecting; analysis/analyzing; containment/containing; eradication/eradicating; recovery/recovering; security incidents; plans; tools; roles; communication channels; potential incidents; scope; cause; impact; spread; damage; root cause; systems; services; normal operation; post-incident review; lessons learned; improvement actions; incident response plan; document; handling incidents.

**Entidades o instancias explícitas:** ninguna instancia individual. “A security analyst”, “a dashboard”, “an incident” y expresiones semejantes son menciones genéricas. “Incident” al comienzo de una oración tampoco constituye un nombre propio.

**Definiciones y descripciones funcionales:** son definiciones explícitas las de incident response y incident response plan. Las restantes oraciones formulan funciones genéricas: qué recolecta, convierte, identifica, define, presenta, investiga, establece, limita, elimina o restaura cada concepto.

### Proposiciones con evidencia

Salvo indicación contraria, la clasificación es **EXPLÍCITO**.

**p021**

1. El sistema de gestión de información y eventos de seguridad **collects** security logs — «system collects ... security logs».
2. El mismo sistema **normalizes** security logs — «collects, normalizes ... security logs».
3. El mismo sistema **correlates** security logs — «normalizes, correlates ... security logs».
4. El mismo sistema **analyzes** security logs — «and analyzes security logs».
5. Log collection gathers records — «Log collection gathers records».
6. Los records se recogen **from systems** — «records from systems».
7. Los records se recogen **from applications** — «and applications».
8. Log normalization converts different log formats — «converts different log formats».
9. La conversión tiene como resultado una common structure — «into a common structure».
10. Log correlation identifies relationships between events — «identifies relationships between events».
11. Una detection rule defines conditions — «defines conditions».
12. Esas conditions generate an alert — «conditions that generate an alert»; “that” refiere a “conditions”.
13. Un use case describes a scenario — «describes a scenario».
14. Monitoring **should** detect ese scenario — «a scenario that monitoring should detect»; no se afirma detección efectiva.
15. Un dashboard presents security metrics — «presents security metrics».
16. El dashboard presents operational status — «and operational status».
17. Un security analyst investigates alerts — «investigates alerts».
18. Esos alerts son produced by the monitoring system — «alerts produced by the monitoring system».
19. Una log retention policy defines la duración de almacenamiento de logs — «defines how long logs ... be stored»; **ENTRAÑADO** como nominalización de “how long”, sin valor temporal concreto.
20. Los logs **must be stored** — «logs must be stored»; la duración queda sin especificar.

**p022**

21. Incident response is a process — «Incident response is the process».
22. El proceso incluye preparing for — «the process of preparing for»; el complemento de “for” queda elidido o desplazado.
23. El proceso incluye detecting — «detecting».
24. El proceso incluye analyzing — «analyzing».
25. El proceso incluye containing — «containing».
26. El proceso incluye eradicating — «eradicating».
27. El proceso incluye recovering from security incidents — «recovering from security incidents».
28. La correspondencia de esas formas verbales con Preparation, Detection, Analysis, Containment, Eradication y Recovery queda **ENTRAÑADA** por las oraciones siguientes, que usan esas nominalizaciones como sujetos; no se explicita un orden temporal estricto.
29. Preparation establishes plans — «Preparation establishes plans».
30. Preparation establishes tools — «plans, tools».
31. Preparation establishes roles — «tools, roles».
32. Preparation establishes communication channels — «and communication channels».
33. Detection identifies potential incidents — «Detection identifies potential incidents»; “potential” no autoriza a tratarlos como incidentes confirmados.
34. Analysis determines the scope of an incident — «the scope, cause, and impact of an incident».
35. Analysis determines the cause of an incident — misma cita; el alcance compartido de “of an incident” es la lectura coordinada natural.
36. Analysis determines the impact of an incident — «impact of an incident».
37. Containment limits una alternativa entre spread y damage of an incident — «limits the spread or damage of an incident»; no son dos afirmaciones conjuntivas independientes.
38. Eradication removes the root cause of an incident — «removes the root cause of an incident».
39. Recovery restores systems to normal operation — «restores systems ... to normal operation».
40. Recovery restores services to normal operation — «and services to normal operation».
41. Post-incident review identifies lessons learned — «identifies lessons learned».
42. Post-incident review identifies improvement actions — «and improvement actions».
43. An incident response plan is a document — «is a document».
44. Ese document defines a process — «a document that defines the process»; “that” refiere a “document”.
45. El process definido tiene como finalidad handling incidents — «the process for handling incidents».

### Taxonomías explícitas

- **IncidentResponse ⊆ Process** — p022: «Incident response is the process ...» (**EXPLÍCITO** como definición genérica; su proyección como subclase es **ENTRAÑADA** por la lectura de clases).
- **IncidentResponsePlan ⊆ Document** — p022: «An incident response plan is a document ...» (**EXPLÍCITO**; la proyección como subclase es **ENTRAÑADA**).
- No hay una taxonomía explícita para las seis actividades ni aserciones de tipo sobre individuos.

### Modalidad

- **Deóntica/esperada:** p021, «monitoring **should** detect»; debe conservarse el `should`, sin convertirlo en detección efectiva.
- **Obligatoria:** p021, «logs **must** be stored»; debe conservarse el `must` y no inventarse una duración.
- **Potencialidad:** p022, «potential incidents»; no equivale a incidentes confirmados.
- **Disyunción:** p022, «spread **or** damage»; exige alcance alternativo, no conjunción plana.
- **Finalidad:** p022, «process **for handling incidents**».
- El resto usa presente genérico descriptivo.

### Ambigüedades

- **EXPLÍCITO:** los tres relativos “that” tienen como antecedentes locales “conditions”, “scenario” y “document”, respectivamente.
- **PLAUSIBLE, no explícito:** p021, «the monitoring system» podría referirse al security information and event management system introducido al comienzo, pero el texto no declara esa identidad.
- **PLAUSIBLE, no explícito:** p022, «the process» de la última oración podría ser el proceso de incident response definido al inicio, pero también puede designar el proceso que el plan documenta. No debe fusionarse sin marcar la incertidumbre.
- **PLAUSIBLE:** p022 presenta las seis actividades en un orden textual, pero no afirma formalmente que ese orden sea obligatorio o total.
- **AMBIGUO:** en «preparing for, detecting, analyzing, containing, eradicating, and recovering from security incidents», “from security incidents” se adjunta literalmente a “recovering”; extender “security incidents” como objeto de todas las actividades es plausible, no explícito.
- **AMBIGUO:** en «spread or damage of an incident», “of an incident” puede tener alcance solo sobre “damage” o sobre la coordinación completa.
- **NO SOPORTADO:** identificar los “systems” de «records from systems and applications» específicamente con el security information and event management system.
- **NO SOPORTADO:** asignar una duración concreta a la retención o afirmar que monitoring efectivamente detecta el scenario.
- **CONTRADICHO:** negar la obligación de almacenamiento sería incompatible con «logs must be stored»; ningún artifact debería proyectar tal negación.

## 2. Resultado por etapa

Escala: 0 = ausente/inservible; 4 = completo y fiel dentro de la responsabilidad del paso.

| Paso | Etapa | Fidelidad | Cobertura | Precisión | Trazabilidad | Coherencia | Estado |
|---:|---|---:|---:|---:|---:|---:|---|
| 01 | input_intake | 4 | 4 | 4 | 4 | 4 | OK |
| 02 | preprocessing | 4 | 4 | 4 | 4 | 4 | OK |
| 03 | sentence_segmentation | 4 | 4 | 4 | 4 | 4 | OK |
| 04 | tokenization | 4 | 4 | 4 | 4 | 4 | OK |
| 05 | linguistic_annotation | 2 | 4 | 2 | 4 | 2 | WARN |
| 06 | entity_extraction | 4 | 4 | 4 | 4 | 4 | OK |
| 07 | concept_extraction | 3 | 3 | 2 | 4 | 3 | WARN |
| 08 | coreference_resolution | 4 | 4 | 4 | 4 | 4 | OK |
| 09 | relation_extraction | 2 | 2 | 2 | 2 | 2 | FAIL |
| 10 | canonical_claims / semantic_claims | 3 | 4 | 3 | 4 | 4 | WARN |
| 11 | semantic_debug_ir | 3 | 4 | 3 | 4 | 4 | WARN |
| 12 | triple_extraction | 3 | 4 | 3 | 4 | 4 | WARN |
| 13 | taxonomy_induction | 4 | 4 | 4 | 4 | 4 | OK |
| 14 | type_assertion | 4 | 4 | 4 | 4 | 4 | OK |
| 15 | semantic_quality | 2 | 2 | 2 | 4 | 3 | FAIL |
| 16 | output_generation | 3 | 4 | 3 | 3 | 4 | WARN |

El paso 11 no es N/A: está configurado y contiene un IR de depuración no vacío. El vacío de entidades del paso 06 y el de type assertions del paso 14 son conservadores y correctos, porque los párrafos no individualizan instancias.

## 3. Hallazgos

### Q-infosec_p021_p022-05-1

- **Severidad:** ALTA
- **Tipo:** anotación sintáctica infiel
- **Atribución:** ERROR_ORIGEN; sus efectos en relaciones quedan ERROR_CORREGIDO en el paso 10.
- **Cita literal:** p021: «A security information and event management system collects, normalizes, correlates, and analyzes security logs.»
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p021_p022/artifacts/pipeline_outputs/observed_p021_p022_05_linguistic_annotation.json`, `/tokens/0`, `/tokens/2`, `/tokens/7`.
- **Evaluación razonada:** “normalizes” aparece como raíz; “information” como su sujeto; “A” depende de “normalizes”; y “collects” figura como conjunción de “information”. La estructura literal exige como sujeto el sintagma completo encabezado por “system” y cuatro verbos coordinados con el mismo objeto “security logs”.
- **Impacto downstream:** el paso 09 omite las cuatro relaciones de esta oración. El paso 10 las reconstruye fielmente, por lo que la pérdida no llega al RDF final.

### Q-infosec_p021_p022-05-2

- **Severidad:** MEDIA
- **Tipo:** POS, lema y coordinación
- **Atribución:** ERROR_ORIGEN; ERROR_PROPAGADO a conceptos/relaciones y ERROR_CORREGIDO en canonical claims.
- **Cita literal:** p022: «Incident response is the process of preparing for, detecting, analyzing, containing, eradicating, and recovering from security incidents.»
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p021_p022/artifacts/pipeline_outputs/observed_p021_p022_05_linguistic_annotation.json`, `/tokens/107`, `/tokens/109`, `/tokens/113`.
- **Evaluación razonada:** “detecting”, “analyzing” y “eradicating” se etiquetan como `NOUN`, y dos conservan la forma flexionada como lema, aunque son elementos coordinados de la serie verbal introducida por «process of preparing ...». La lectura como actividades está explícita y reforzada por las nominalizaciones posteriores.
- **Impacto downstream:** dificulta extraer la composición del proceso en los pasos 07 y 09. El paso 10 recupera las seis actividades con `has_activity`.

### Q-infosec_p021_p022-05-3

- **Severidad:** MEDIA
- **Tipo:** coordinación mal analizada
- **Atribución:** ERROR_ORIGEN; ERROR_PROPAGADO al paso 09 y ERROR_CORREGIDO en el paso 10.
- **Cita literal:** p022: «Post-incident review identifies lessons learned and improvement actions.»
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p021_p022/artifacts/pipeline_outputs/observed_p021_p022_05_linguistic_annotation.json`, `/tokens/185`, `/tokens/188`.
- **Evaluación razonada:** “actions” se anota como `appos` de “lessons” y “learned” como modificador de “actions”. La coordinación literal es entre “lessons learned” e “improvement actions”.
- **Impacto downstream:** relation extraction conserva solo la relación con “lesson”; canonical claims restaura también `PostIncidentReview identifies ImprovementAction`.

### Q-infosec_p021_p022-07-1

- **Severidad:** MEDIA
- **Tipo:** candidato conceptual ruidoso
- **Atribución:** ERROR_ORIGEN; ERROR_CORREGIDO en el paso 10.
- **Cita literal:** p021: «A log retention policy defines how long logs must be stored.»
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p021_p022/artifacts/pipeline_outputs/observed_p021_p022_07_concept_extraction.json`, `/concepts/23`, `/concepts/54`.
- **Evaluación razonada:** “how long logs” y “long logs” se proponen como conceptos con confianza 0.95 y 0.8. No son conceptos nominales fieles: “how long” expresa una duración interrogada/indirecta y modifica el almacenamiento, no una clase de logs “largos”.
- **Impacto downstream:** el paso 09 no produce la semántica de retención. El paso 10 corrige la representación mediante `StorageDuration`, `Log` y modalidad `must`; los candidatos ruidosos no llegan al modelo final.

### Q-infosec_p021_p022-07-2

- **Severidad:** MEDIA
- **Tipo:** cobertura y trazabilidad conceptual
- **Atribución:** ERROR_ORIGEN; ERROR_PROPAGADO al paso 09 y ERROR_CORREGIDO en el paso 10.
- **Cita literal:** p022: «Incident response is the process of preparing for ...» y «An incident response plan ... defines the process for handling incidents.»
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p021_p022/artifacts/pipeline_outputs/observed_p021_p022_07_concept_extraction.json`, `/concepts` y `/concepts/52`.
- **Evaluación razonada:** no existe un candidato “process” trazado al primer enunciado; el único `process` está en `/concepts/52`, con el span de la última oración. Pese a ello, la relación `incident response be process` del paso 09 reutiliza ese identificador de otra oración.
- **Impacto downstream:** crea trazabilidad cruzada impropia en relation extraction. Canonical claims vuelve a anclar la definición de IncidentResponse en su propia oración.

### Q-infosec_p021_p022-09-1

- **Severidad:** ALTA
- **Tipo:** pérdida de cobertura relacional
- **Atribución:** ERROR_ORIGEN en el paso 09; ERROR_CORREGIDO casi por completo en el paso 10.
- **Cita literal:** p021: «system collects, normalizes, correlates, and analyzes security logs», «alerts produced by the monitoring system» y «logs must be stored»; p022: «Preparation establishes plans, tools, roles, and communication channels», «Analysis determines the scope, cause, and impact» y «lessons learned and improvement actions».
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p021_p022/artifacts/pipeline_outputs/observed_p021_p022_09_relation_extraction.json`, `/relations`.
- **Evaluación razonada:** las 25 relaciones candidatas omiten familias completas de relaciones explícitas: las cuatro operaciones del sistema inicial; el destino `common structure`; el complemento `between events`; `produced_by`; la política y su modalidad; la composición de incident response; roles y communication channels; impact; improvement actions; y la finalidad handling incidents. No se penaliza por no inventar identidades ambiguas, sino por perder predicaciones literales.
- **Impacto downstream:** canonical claims eleva la cobertura a 45 claims y repara estas ausencias. Por tanto, esta es la principal pérdida intermedia, no la principal pérdida del output final.

### Q-infosec_p021_p022-09-2

- **Severidad:** ALTA
- **Tipo:** referencia cruzada no soportada
- **Atribución:** ERROR_ORIGEN; parcialmente ERROR_CORREGIDO para Recovery y ERROR_AMPLIFICADO en el paso 10 para la procedencia de Record.
- **Cita literal:** p021: «Log collection gathers records from systems and applications» y «alerts produced by the monitoring system»; p022: «Recovery restores systems and services to normal operation.»
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p021_p022/artifacts/pipeline_outputs/observed_p021_p022_09_relation_extraction.json`, `/relations/20/object_ref`, `/relations/8/object_ref`, `/relations/9`.
- **Evaluación razonada:** tanto el “system” de la fuente de records como el “system” restaurado por Recovery apuntan a `con-9218...`, cuyo span corresponde a «the monitoring system» de otra oración. El texto solo ofrece “systems” genéricos en esas dos oraciones; la identidad con MonitoringSystem no es explícita.
- **Impacto downstream:** canonical claims corrige Recovery a `System`, pero transforma la fuente genérica de records en el todavía más específico `SecurityInformationAndEventManagementSystem`; ese segundo ramal sí alcanza triples y RDF.

### Q-infosec_p021_p022-10-1

- **Severidad:** ALTA
- **Tipo:** contenido no soportado y cambio de referente
- **Atribución:** ERROR_AMPLIFICADO respecto del enlace erróneo del paso 09; después ERROR_PROPAGADO por 11, 12, 15 y 16.
- **Cita literal:** p021: «Log collection gathers records from systems and applications.»
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p021_p022/artifacts/pipeline_outputs/observed_p021_p022_10_canonical_claims.json`, `/canonical_claims/claims/5`.
- **Evaluación razonada:** el claim `Record originates_from SecurityInformationAndEventManagementSystem` sustituye “systems” por un tipo específico introducido en otra oración. Esa identidad es **NO SOPORTADA**. Además, `originates_from` es una normalización algo más fuerte que el literal “gathers ... from”; puede aceptarse como relación de fuente solo si se conserva el referente genérico `System`.
- **Impacto downstream:** aparece en debug IR como fuente del SIEM, en `observed_p021_p022_12_triple_extraction.json#/triples/34`, y en `observed_p021_p022_16_output_generation.json#/output/graph/facts/5`; además induce el par de dominio/rango en `/output/graph/object_property_facts/31` y `/output/graph/object_property_schema/17`. Es el principal contenido inventado del modelo final.

### Q-infosec_p021_p022-15-1

- **Severidad:** ALTA
- **Tipo:** control semántico ineficaz
- **Atribución:** ERROR_AMPLIFICADO: el paso no origina el claim, pero lo certifica sin reservas.
- **Cita literal:** p021: «records from systems and applications», no «from the security information and event management system».
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p021_p022/artifacts/pipeline_outputs/observed_p021_p022_15_semantic_quality.json`, `/semantic_quality_report/quality_score`, `/semantic_quality_report/rdf_readiness`, `/semantic_quality_report/semantic_integrity_issues`, `/semantic_quality_report/warnings`.
- **Evaluación razonada:** el informe asigna `quality_score: 1.0`, `rdf_readiness: true` y listas vacías de issues/warnings pese al claim no soportado del paso 10. En particular, `source_connectors_grounded: true` no concuerda con la sustitución de `System` por `SecurityInformationAndEventManagementSystem`.
- **Impacto downstream:** permite materializar como hecho y como uso de propiedad un enlace que debió rechazarse, degradarse a genérico o marcarse ambiguo antes de RDF.

### Q-infosec_p021_p022-16-1

- **Severidad:** BAJA
- **Tipo:** trazabilidad final indirecta
- **Atribución:** ERROR_ORIGEN del paso 16; no altera la semántica taxonómica.
- **Cita literal:** p022: «Incident response is the process ...» y «An incident response plan is a document ...».
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p021_p022/artifacts/pipeline_outputs/observed_p021_p022_16_output_generation.json`, `/output/graph/subclass_facts/0`, `/output/graph/subclass_facts/1`, `/taxonomy_relations/0`, `/taxonomy_relations/1`.
- **Evaluación razonada:** las dos subclases son fieles, pero esas vistas finales no llevan `claim_id` ni evidencia directa, aunque el paso 13 sí los tenía. La trazabilidad puede reconstruirse indirectamente mediante `projection.claim_dispositions`, por lo que no es una pérdida total.
- **Impacto downstream:** un consumidor que lea solo `subclass_facts` o `taxonomy_relations` no puede localizar directamente la oración justificativa.

## 4. Diagnóstico

- **Primera degradación:** paso 05. El análisis sintáctico de la primera oración de p021 rompe el sujeto y la coordinación verbal; también falla en parte la serie de actividades y la coordinación de “lessons learned and improvement actions” en p022.
- **Principal pérdida:** paso 09. Relation extraction conserva 25 candidatos, pero pierde numerosas predicaciones explícitas. Esta pérdida es mayormente **corregida** por los 45 canonical/semantic claims del paso 10.
- **Principal contenido no soportado:** `Record originates_from SecurityInformationAndEventManagementSystem`. El texto solo dice «records from systems and applications»; escoger específicamente el SIEM no está entrañado.
- **Errores que llegan a RDF/OWL:** el caso genera RDF, no aserciones de instancia OWL. El enlace no soportado llega como `orion:Record orion:originatesFrom orion:SecurityInformationAndEventManagementSystem` y se amplifica en los pares observados y el schema de `orion:originatesFrom`. No llegan los conceptos ruidosos “how long logs/long logs” ni las omisiones del paso 09.
- **Aciertos:** intake, preprocessing, segmentación y tokenización son completos; las tres correferencias relativas son correctas; entity extraction y type assertion son prudentemente vacíos; canonical claims recupera coordinaciones, modalidad `should`/`must`, finalidad, destino de Recovery, seis actividades y dos definiciones; taxonomy induction deriva solo las dos jerarquías soportadas; output generation conserva los 45 claim dispositions, representa la disyunción por separado y mantiene las relaciones modales como scoped relations.
- **Incertidumbres:** no debe forzarse la identidad entre MonitoringSystem y el SIEM, ni entre los dos usos de “the process”; tampoco un orden obligatorio de fases, una duración concreta de retención o un alcance único de «of an incident» cuando la coordinación admite más de una lectura.

## 5. Veredicto

- **Calidad global:** **87/100**.
- **Output final:** **parcialmente fiel**. Tiene cobertura muy alta y conserva modalidad, coordinación, finalidad y taxonomías, pero contiene un enlace de procedencia específico no soportado y el control de calidad no lo detecta.
- **Tres correcciones prioritarias:**
  1. Sustituir o rechazar `Record originates_from SecurityInformationAndEventManagementSystem`; conservar el referente literal genérico `System` y la coordinación con `Application`, sin afirmar una identidad específica.
  2. Corregir el tratamiento lingüístico y relacional de sujetos largos, coordinaciones, gerundios, pasivas y complementos preposicionales para que relation extraction cubra las proposiciones literales sin depender de la reparación posterior del paso 10.
  3. Hacer que semantic quality contraste cada claim con sus referentes léxicos y marque sustituciones no entrañadas antes de RDF; mantener también evidencia o `claim_id` directo en las taxonomías finales.

Siguiente caso pendiente: infosec_p023_p024.
