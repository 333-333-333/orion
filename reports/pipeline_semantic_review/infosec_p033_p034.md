# Revisión semántica: infosec_p033_p034

## 1. Lectura independiente

### Resumen

Los dos párrafos presentan descripciones genéricas, no casos concretos. **p033** trata la gestión de vulnerabilidades: detección, valoración, priorización, remediación, mitigación, excepciones y dos subtipos explícitos de remediación. **p034** trata la inteligencia de amenazas: contenido informativo, definición y subtipos de actor de amenaza, indicador de compromiso, táctica, técnica y actividades soportadas. No hay nombres propios ni instancias individualizadas; los sintagmas se usan como clases, procesos, cualidades o roles genéricos.

Escala interpretativa usada:

- **EXPLÍCITO**: afirmado literalmente.
- **ENTRAÑADO**: se sigue necesariamente de la formulación literal.
- **PLAUSIBLE**: lectura posible, pero no necesaria.
- **NO SOPORTADO**: no se desprende del texto.
- **CONTRADICHO**: incompatible con una restricción literal del texto.

### Conceptos

- **p033, conceptos explícitos:** vulnerability management, weakness, vulnerability scan, known vulnerability, system, application, vulnerability finding, detected weakness, severity rating, technical seriousness, vulnerability, risk rating, severity, exposure, likelihood, business impact, remediation, mitigation, risk, patch deployment, configuration change y vulnerability exception.
- **p034, conceptos explícitos:** threat intelligence, information, threat, threat actor, tactic, technique, indicator, entity, harm, cybercriminal group, insider, nation-state actor, hacktivist, indicator of compromise, evidence, system, objective, detection, prevention y response activity.
- **Entidades/instancias explícitas:** ninguna instancia concreta. “A threat actor is an entity…” [p034] usa *entity* como categoría genérica, no como individuo. Por ello, una extracción vacía de instancias es conservadora y semánticamente admisible.
- **Definiciones o caracterizaciones funcionales explícitas:**
  - vulnerability management por sus cuatro acciones sobre weaknesses [p033];
  - vulnerability scan por lo que detecta y dónde [p033];
  - vulnerability finding por lo que describe [p033];
  - severity rating por lo que estima [p033];
  - risk rating por los cuatro elementos que combina [p033];
  - remediation y mitigation por sus efectos y, para mitigation, su condición [p033];
  - threat intelligence por la información que proporciona y las actividades que soporta [p034];
  - threat actor por su categoría y capacidad modal [p034];
  - indicator of compromise por su carácter evidencial y alcance modal [p034];
  - tactic y technique por lo que describen [p034].
- **Distinciones que deben conservarse:** weakness no se declara equivalente a vulnerability; severity no equivale a severity rating; risk no equivale a risk rating; indicator no equivale a indicator of compromise; ThreatActorObjective y el Objective genérico de la oración sobre técnicas no se declaran idénticos.

### Proposiciones con evidencia

1. **EXPLÍCITO:** Vulnerability management identifica weaknesses: “identifies … weaknesses” [p033].
2. **EXPLÍCITO:** Vulnerability management evalúa weaknesses: “evaluates … weaknesses” [p033].
3. **EXPLÍCITO:** Vulnerability management prioriza weaknesses: “prioritizes … weaknesses” [p033].
4. **EXPLÍCITO:** Vulnerability management remedia weaknesses: “remediates weaknesses” [p033].
5. **EXPLÍCITO:** Un vulnerability scan detecta known vulnerabilities: “detects known vulnerabilities” [p033].
6. **EXPLÍCITO:** Esa detección se sitúa en systems: “in systems” [p033].
7. **EXPLÍCITO:** Esa detección también se sitúa en applications: “and applications” [p033].
8. **EXPLÍCITO:** Un vulnerability finding describe una detected weakness: “describes a detected weakness” [p033].
9. **EXPLÍCITO:** Un severity rating estima technical seriousness: “estimates the technical seriousness” [p033].
10. **EXPLÍCITO:** Esa technical seriousness tiene como objeto una vulnerability: “of a vulnerability” [p033].
11. **EXPLÍCITO:** Un risk rating combina severity: “combines severity” [p033].
12. **EXPLÍCITO:** También combina exposure: “exposure” [p033].
13. **EXPLÍCITO:** También combina likelihood: “likelihood” [p033].
14. **EXPLÍCITO:** También combina business impact: “business impact” [p033].
15. **EXPLÍCITO como disyunción:** Remediation “removes or fixes a vulnerability” [p033]. Cada alternativa está mencionada, pero afirmar categóricamente solo una de ellas sin conservar el `or` sería **NO SOPORTADO**.
16. **EXPLÍCITO y condicionado:** Mitigation reduce risk cuando “remediation is not immediately possible” [p033].
17. **EXPLÍCITO:** Patch deployment es un tipo de remediation: “is a type of remediation” [p033].
18. **EXPLÍCITO:** Configuration change es un tipo de remediation: “is a type of remediation” [p033].
19. **EXPLÍCITO, deóntico:** Vulnerability exceptions deben ser documented: “must be documented” [p033].
20. **EXPLÍCITO, deóntico:** También deben ser approved: “approved” bajo el mismo `must` coordinado [p033].
21. **EXPLÍCITO, deóntico:** También deben ser reviewed: “reviewed” bajo el mismo `must` coordinado [p033].
22. **EXPLÍCITO:** Threat intelligence proporciona information about threats: “information about threats” [p034].
23. **EXPLÍCITO:** También sobre threat actors: “threat actors” [p034].
24. **EXPLÍCITO:** También sobre tactics: “tactics” [p034].
25. **EXPLÍCITO:** También sobre techniques: “techniques” [p034].
26. **EXPLÍCITO:** También sobre indicators: “indicators” [p034].
27. **EXPLÍCITO:** Un threat actor es una entity: “is an entity” [p034].
28. **EXPLÍCITO con modalidad y manera:** Un threat actor puede causar daño intencionalmente: “can intentionally cause harm” [p034].
29. **EXPLÍCITO:** Cybercriminal group es un tipo de threat actor [p034].
30. **EXPLÍCITO:** Insider es un tipo de threat actor [p034].
31. **EXPLÍCITO:** Nation-state actor es un tipo de threat actor [p034].
32. **EXPLÍCITO:** Hacktivist es un tipo de threat actor [p034].
33. **EXPLÍCITO:** Indicator of compromise es evidence: “is evidence” [p034].
34. **EXPLÍCITO con modalidad:** La evidencia indica que un system puede estar compromised: “may be compromised” [p034]. La afirmación categórica de compromiso efectivo es **NO SOPORTADO**.
35. **EXPLÍCITO:** Una tactic describe un threat actor objective [p034].
36. **EXPLÍCITO:** Una technique describe cómo un threat actor achieves an objective [p034].
37. **EXPLÍCITO:** Threat intelligence soporta detection [p034].
38. **EXPLÍCITO:** Threat intelligence soporta prevention [p034].
39. **EXPLÍCITO:** Threat intelligence soporta response activities [p034].

Interpretaciones de control:

- “Threat actors are always harmful” es **NO SOPORTADO**: el texto expresa capacidad, no actuación universal [p034].
- “The system is compromised” es **NO SOPORTADO** por la modalidad `may` [p034].
- “Mitigation applies when remediation is immediately possible” es **CONTRADICHO** por “not immediately possible” [p033].
- “A threat actor cannot intentionally cause harm” es **CONTRADICHO** por “can intentionally cause harm” [p034].
- Identificar el Objective de technique con ThreatActorObjective es **PLAUSIBLE**, pero no necesario [p034].

### Taxonomías explícitas

- **EXPLÍCITO mediante “type of”:** PatchDeployment ⊑ Remediation y ConfigurationChange ⊑ Remediation [p033].
- **EXPLÍCITO mediante “type of”:** CybercriminalGroup ⊑ ThreatActor, Insider ⊑ ThreatActor, NationStateActor ⊑ ThreatActor y Hacktivist ⊑ ThreatActor [p034].
- **ENTRAÑADO por definiciones genéricas copulares:** ThreatActor ⊑ Entity e IndicatorOfCompromise ⊑ Evidence [p034]. Son clasificaciones fieles, aunque el texto no usa literalmente “type of” en estas dos oraciones.
- No hay taxonomías explícitas entre weakness y vulnerability, indicator e indicator of compromise, tactic y technique, ni severity y risk.

### Modalidad

- **Obligación:** `must` tiene alcance sobre documented, approved y reviewed [p033].
- **Capacidad:** `can` modifica cause harm; `intentionally` expresa manera [p034]. No debe proyectarse como hecho incondicionado de daño efectivo.
- **Posibilidad epistémica:** `may` modifica be compromised [p034].
- **Condición negativa y temporal:** mitigation reduce risk solo bajo “when remediation is not immediately possible” [p033].
- **Alternativa:** `or` une removes y fixes [p033]; el texto no determina si la disyunción es inclusiva o exclusiva.
- **Coordinación conjuntiva:** las listas con `and` exigen conservar todos sus miembros [p033, p034].

### Ambigüedades

- En “removes or fixes” no se especifica `or` inclusivo o exclusivo [p033].
- “systems and applications” enumera dos ámbitos; reducirlos a uno pierde información literal [p033].
- “detection, prevention, and response activities” permite discutir si *activities* modifica solo *response* o toda la lista. La lectura mínima segura conserva Detection, Prevention y ResponseActivity por separado [p034].
- El `that` de “an entity that can…” es pronombre relativo con antecedente sintáctico *entity*; por la cópula, la restricción caracteriza al threat actor [p034].
- El `that` de “evidence that a system…” es complementizador, no mención correferencial [p034].
- “evidence that a system may be compromised” no introduce literalmente una clase llamada *CompromiseState* [p034].
- No hay enlace semántico explícito entre los temas de p033 y p034 más allá de su yuxtaposición; no debe inventarse uno.

## 2. Resultado por etapa

Escala por dimensión: 0 = ausente o gravemente incorrecto; 1 = deficiente; 2 = parcial; 3 = sólido con defectos; 4 = completo y fiel. Las puntuaciones juzgan la responsabilidad propia de cada etapa, no errores ajenos ya existentes.

| Paso | Etapa | Fidelidad | Cobertura | Precisión | Trazabilidad | Coherencia | Estado |
|---:|---|---:|---:|---:|---:|---:|---|
| 01 | input_intake | 4 | 4 | 4 | 4 | 4 | OK |
| 02 | preprocessing | 4 | 4 | 4 | 4 | 4 | OK |
| 03 | sentence_segmentation | 4 | 4 | 4 | 4 | 4 | OK |
| 04 | tokenization | 4 | 4 | 4 | 4 | 4 | OK |
| 05 | linguistic_annotation | 3 | 4 | 3 | 4 | 3 | WARN |
| 06 | entity_extraction | 4 | 4 | 4 | 4 | 4 | OK |
| 07 | concept_extraction | 3 | 3 | 2 | 4 | 3 | WARN |
| 08 | coreference_resolution | 2 | 4 | 2 | 4 | 4 | WARN |
| 09 | relation_extraction | 2 | 1 | 2 | 4 | 2 | FAIL |
| 10 | canonical_claims / semantic_claims | 3 | 3 | 3 | 4 | 4 | WARN |
| 11 | semantic_debug_ir | 3 | 3 | 3 | 4 | 4 | WARN |
| 12 | triple_extraction | 4 | 4 | 4 | 4 | 4 | OK |
| 13 | taxonomy_induction | 4 | 4 | 4 | 4 | 4 | OK |
| 14 | type_assertion | 4 | 4 | 4 | 4 | 4 | OK |
| 15 | semantic_quality | 2 | 1 | 1 | 2 | 2 | FAIL |
| 16 | output_generation | 3 | 3 | 3 | 3 | 3 | WARN |

## 3. Hallazgos

### Q-infosec_p033_p034-05-1

- **Severidad:** MEDIA
- **Tipo:** análisis morfosintáctico incorrecto
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** “Vulnerability management identifies, evaluates, prioritizes, and remediates weaknesses.” [p033]
- **Archivo y JSON Pointer:** `observed_p033_p034_05_linguistic_annotation.json`, `/tokens/9`
- **Evaluación razonada:** `remediates` se etiqueta como `NOUN`/`NNS`, con dependencia `compound` de `weaknesses`, aunque en la coordinación funciona como verbo junto con `identifies`, `evaluates` y `prioritizes`. La lectura del token contradice la estructura literal de p033.
- **Impacto downstream:** origina el concepto espurio “remediates weaknesses” en 07 y contribuye a que 09 no extraiga las cuatro relaciones. Las cuatro proposiciones quedan **ERROR_CORREGIDO** en 10 y llegan correctamente al output final.

### Q-infosec_p033_p034-07-1

- **Severidad:** MEDIA
- **Tipo:** candidato conceptual espurio
- **Atribución:** ERROR_AMPLIFICADO
- **Cita literal:** “…and remediates weaknesses.” [p033]
- **Archivo y JSON Pointer:** `observed_p033_p034_07_concept_extraction.json`, `/concepts/1`
- **Evaluación razonada:** se propone “remediates weaknesses” como `noun_chunk` con confianza `0.95`. Es una frase verbal, no un concepto nominal explícito. La alta confianza amplifica el error de 05.
- **Impacto downstream:** contamina el inventario conceptual, aunque no se materializa en claims ni en RDF/OWL.

### Q-infosec_p033_p034-07-2

- **Severidad:** BAJA
- **Tipo:** sobreextracción de modificador
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** “remediation is not immediately possible.” [p033]
- **Archivo y JSON Pointer:** `observed_p033_p034_07_concept_extraction.json`, `/concepts/50`
- **Evaluación razonada:** `possible` se eleva a concepto independiente. En p033 es un predicado adjetival dentro de una condición negativa, no una entidad o clase autónoma.
- **Impacto downstream:** no alcanza el modelo final, pero debería haber sido detectado como `concept_noise` en 15.

### Q-infosec_p033_p034-08-1

- **Severidad:** MEDIA
- **Tipo:** falsa correferencia
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** “An indicator of compromise is evidence that a system may be compromised.” [p034]
- **Archivo y JSON Pointer:** `observed_p033_p034_08_coreference_resolution.json`, `/coreferences/1`
- **Evaluación razonada:** el segundo `that` es complementizador de la cláusula que especifica el contenido de la evidencia; no es una mención que refiera a `evidence`. Resolverlo como correferencia es **NO SOPORTADO**.
- **Impacto downstream:** no se observa propagación directa a claims; 10 interpreta la cláusula como contexto modal. El error permanece como ruido local de 08.

### Q-infosec_p033_p034-09-1

- **Severidad:** ALTA
- **Tipo:** referencia de sujeto semánticamente incorrecta
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** “A risk rating combines severity, exposure, likelihood, and business impact.” [p033]
- **Archivo y JSON Pointer:** `observed_p033_p034_09_relation_extraction.json`, `/relations/2/subject_ref`
- **Evaluación razonada:** la relación de `combines` apunta a `con-26aba0a54aae9665`, que en 07 es **severity rating**, no **risk rating**. Además, `subject_text` se reduce a “rating”. Esto asigna la acción al concepto equivocado.
- **Impacto downstream:** 10 lo **ERROR_CORREGIDO** al generar cuatro claims con sujeto `RiskRating`; no alcanza RDF/OWL.

### Q-infosec_p033_p034-09-2

- **Severidad:** ALTA
- **Tipo:** pérdida masiva de relaciones explícitas
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** “Vulnerability management identifies, evaluates, prioritizes, and remediates weaknesses.” [p033]; “Vulnerability exceptions must be documented, approved, and reviewed.” [p033]; “Threat intelligence supports detection, prevention, and response activities.” [p034]
- **Archivo y JSON Pointer:** `observed_p033_p034_09_relation_extraction.json`, `/relations`
- **Evaluación razonada:** no aparecen las cuatro acciones de vulnerability management ni las tres obligaciones; también falta `supports ResponseActivity`. Se pierden además `removes`, `combines Likelihood`, `combines BusinessImpact` y la relación principal que hace de Technique el sujeto de `describes how`. La etapa cubre fragmentos, no el conjunto de patrones explícitos.
- **Impacto downstream:** 10 corrige la mayor parte mediante claims completos. La mala calidad de 09 queda enmascarada por esa recuperación y no debe contabilizarse de nuevo como error de 10.

### Q-infosec_p033_p034-09-3

- **Severidad:** ALTA
- **Tipo:** pérdida de alcance coordinado
- **Atribución:** ERROR_PROPAGADO
- **Cita literal:** “A vulnerability scan detects known vulnerabilities in systems and applications.” [p033]
- **Archivo y JSON Pointer:** origen visible en `observed_p033_p034_09_relation_extraction.json`, `/relations/19`; propagación en `observed_p033_p034_10_canonical_claims.json`, `/canonical_claims/claims/4/location`; salida en `observed_p033_p034_16_output_generation.json`, `/output/graph/facts/4/location`
- **Evaluación razonada:** 09 no representa ninguno de los ámbitos. 10 recupera solo `System`, y 16 proyecta únicamente `orion:System`. `Application` desaparece incluso como clase. La conjunción literal exige conservar ambos miembros.
- **Impacto downstream:** es la principal pérdida que llega al RDF/OWL final.

### Q-infosec_p033_p034-09-4

- **Severidad:** MEDIA
- **Tipo:** relación taxonómica candidata incompleta
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** “Patch deployment is a type of remediation.” [p033]
- **Archivo y JSON Pointer:** `observed_p033_p034_09_relation_extraction.json`, `/relations/0/object_text`
- **Evaluación razonada:** la relación queda como `patch deployment —be→ type`, sin referencia ni enlace a `remediation`. El patrón “type of” no está representado semánticamente por esta etapa.
- **Impacto downstream:** 10 lo **ERROR_CORREGIDO** como `PatchDeployment is_a Remediation`; 13 y 16 inducen la subclase correcta. El mismo defecto afecta inicialmente a las demás oraciones “type of”.

### Q-infosec_p033_p034-10-1

- **Severidad:** ALTA
- **Tipo:** contenido semántico sintético no marcado
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** “An indicator of compromise is evidence that a system may be compromised.” [p034]
- **Archivo y JSON Pointer:** `observed_p033_p034_10_canonical_claims.json`, `/canonical_claims/claims/27/object`
- **Evaluación razonada:** el objeto `CompromiseState` no aparece en p034 ni está entrañado como clase nombrada. Puede ser una técnica de reificación **PLAUSIBLE**, pero el claim `System compromised CompromiseState` lo presenta como contenido del texto sin marcarlo como nodo sintético. La fuente solo afirma modalmente que un sistema “may be compromised”.
- **Impacto downstream:** se propaga a 12, al esquema de propiedad de 16 y a la clase RDF `orion:CompromiseState`; es el principal contenido no soportado del modelo final.

### Q-infosec_p033_p034-11-1

- **Severidad:** BAJA
- **Tipo:** pérdida en sidecar de depuración
- **Atribución:** ERROR_CORREGIDO
- **Cita literal:** “A technique describes how a threat actor achieves an objective.” [p034]
- **Archivo y JSON Pointer:** `observed_p033_p034_11_semantic_debug_ir.json`, `/artifacts/semantic_debug_ir/relations/29`
- **Evaluación razonada:** la relación proyectada conserva Technique, `describes_how_achieves` y Objective, pero omite el campo `actor: ThreatActor` presente en el claim de 10. Para un IR de depuración, esa omisión impide inspeccionar un rol semántico explícito.
- **Impacto downstream:** no se propaga: 12 vuelve a incluir `actor` desde los claims. El problema queda limitado al sidecar configurado.

### Q-infosec_p033_p034-15-1

- **Severidad:** ALTA
- **Tipo:** falso negativo del control de calidad
- **Atribución:** ERROR_AMPLIFICADO
- **Cita literal:** “…remediates weaknesses.” [p033]; “…systems and applications.” [p033]; “…a system may be compromised.” [p034]
- **Archivo y JSON Pointer:** `observed_p033_p034_15_semantic_quality.json`, `/semantic_quality_report`
- **Evaluación razonada:** el reporte declara `quality_score: 1.0`, `concept_noise: []`, `relation_gaps: []` y `warnings: []` pese al concepto verbal “remediates weaknesses”, al concepto adjetival `possible`, a la pérdida de Application y al nodo sintético CompromiseState. El control no solo omite alertas, sino que certifica perfección.
- **Impacto downstream:** permite que la pérdida y la invención pasen sin advertencia a 16 y vuelve poco fiable la señal `rdf_readiness: true` como indicador de fidelidad semántica.

### Q-infosec_p033_p034-16-1

- **Severidad:** MEDIA
- **Tipo:** incoherencia de proyección RDF
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** “A technique describes how a threat actor achieves an objective.” [p034]
- **Archivo y JSON Pointer:** `observed_p033_p034_16_output_generation.json`, `/output/graph/facts/13/actor`
- **Evaluación razonada:** `subject` y `object` se proyectan como IRI (`orion:Technique`, `orion:Objective`), pero `actor` queda como literal no cualificado `ThreatActor`, aunque existe la clase `orion:ThreatActor`. El rol se conserva lexicalmente, pero no queda conectado de forma estructural al recurso del grafo.
- **Impacto downstream:** consumidores RDF no pueden resolver uniformemente el actor; es una degradación originada en la proyección final.

## 4. Diagnóstico

- **Primera degradación:** paso 05. La lectura de `remediates` como sustantivo rompe la coordinación verbal de p033. Esta degradación se amplifica en 07 y explica parte de la baja cobertura de 09, aunque 10 la corrige para el modelo final.
- **Principal pérdida:** `Application` y el segundo ámbito de detección de vulnerabilidades. El concepto combinado existe en 07, pero 09 no lo representa, 10 solo recupera `System` y 16 omite `Application` por completo.
- **Principal contenido no soportado:** `CompromiseState`, introducido en 10 como objeto/clase sin marca de reificación sintética y proyectado en 16.
- **Errores que llegan a RDF/OWL:** (1) ausencia de Application en la localización del scan; (2) clase y rango `CompromiseState`; (3) `actor: ThreatActor` sin IRI en el hecho de Technique. La falsa correferencia de 08, las referencias erróneas de RiskRating y las relaciones “type” truncadas de 09 no llegan al modelo final porque 10 las corrige.
- **Aciertos:** intake, normalización, segmentación y tokenización son exactos; la ausencia de entidades/instancias y de type assertions es conservadora y correcta; 10 recupera 33 claims con buena evidencia, preserva `must`, `can`, `may`, la condición negativa y la disyunción; 12 convierte los 33 claims sin pérdida adicional; 13 induce las ocho clasificaciones justificables; 16 mantiene las alternativas y relaciones modalizadas en estructuras separadas en vez de afirmarlas como hechos incondicionados.
- **Incertidumbres legítimas:** inclusividad de `or`; alcance de *activities* en la lista final; identidad entre Objective y ThreatActorObjective; conveniencia ontológica de tratar “is evidence” como subclase. No se penaliza el tratamiento conservador de estas ambigüedades.

## 5. Veredicto

- **Calidad global:** **82/100**.
- **Output final:** **parcialmente fiel**. Preserva la gran mayoría de las proposiciones, taxonomías, coordinaciones y modalidades, pero no cumple fidelidad total por una pérdida literal relevante, una clase sintética no marcada y una incoherencia de enlace RDF.
- **Tres correcciones prioritarias:**
  1. Conservar todos los miembros y alcances de coordinaciones durante claims y proyección, en particular `System` **y** `Application` para el vulnerability scan.
  2. Representar “may be compromised” como estado/modalidad unaria o marcar explícitamente cualquier reificación; no presentar `CompromiseState` como clase extraída del texto.
  3. Hacer que semantic_quality detecte ruido, gaps e invenciones antes de RDF y valide que roles auxiliares como `actor` se proyecten a IRIs coherentes.

Siguiente caso pendiente: infosec_p035_p036.
