# Revisión semántica: infosec_p003_p004

## 1. Lectura independiente

### Resumen

Los dos párrafos describen, sin aportar conocimiento externo, (i) medios organizativos para proteger información, (ii) cinco clases de documentos o conjuntos de seguridad y sus funciones, y (iii) responsabilidades genéricas de nueve roles organizativos. `p003` es principalmente definicional; `p004` asigna acciones y obligaciones a roles.

No hay nombres propios ni individuos concretos. “An organization”, “the board of directors”, “senior management” y los restantes roles se leen como menciones genéricas de clases o roles, no como instancias identificadas. Tratar cualquiera de ellos como individuo nombrado sería **NO SOPORTADO**.

### Conceptos

- **p003 — protección y medios:** organization, information, governance, policies, procedures, controls, monitoring mechanisms, incident response processes.
- **p003 — documentos y contenido:** security policy, formal document, rules, expectations, security standard, control document, mandatory requirements, security procedure, operational document, step-by-step activities, security guideline, advisory document, good practices, security baseline, minimum set of controls, system, application, infrastructure component.
- **p004 — roles:** board of directors, senior management, information security manager, asset owner, asset custodian, system administrator, security analyst, auditor, end user.
- **p004 — objetos de responsabilidad:** strategic oversight, information security, security policies, resources, security initiatives, information security program, information assets, protection requirements, technical environment, servers, networks, operating systems, technical services, security events, suspicious activity, compliance with security requirements, systems.
- **Entidades/instancias explícitas:** ninguna instancia individual identificable; todas las menciones anteriores son genéricas.

### Proposiciones con evidencia

#### p003

1. **EXPLÍCITO:** una organización protege información: “**An organization protects information**”.
2. **EXPLÍCITO, con función instrumental:** la organización implementa governance como medio de esa protección: “**by implementing governance**”.
3. **EXPLÍCITO, con función instrumental:** implementa policies: “**governance, policies**”.
4. **EXPLÍCITO, con función instrumental:** implementa procedures: “**policies, procedures**”.
5. **EXPLÍCITO, con función instrumental:** implementa controls: “**procedures, controls**”.
6. **EXPLÍCITO, con función instrumental:** implementa monitoring mechanisms: “**monitoring mechanisms**”.
7. **EXPLÍCITO, con función instrumental:** implementa incident response processes: “**incident response processes**”.
8. **EXPLÍCITO — definición:** security policy es formal document: “**A security policy is a formal document**”.
9. **EXPLÍCITO:** el formal document correferido define rules y expectations: “**document that defines rules and expectations**”.
10. **ENTRAÑADO por la identidad de la definición:** security policy define rules y expectations. No requiere conocimiento de dominio, pero deriva de 8–9.
11. **EXPLÍCITO como modificador de finalidad, con alcance ambiguo:** “**rules and expectations for protecting information**”. Que la finalidad se distribuya a ambos coordinados o solo al más próximo es **PLAUSIBLE**, no inequívocamente entrañado para cada miembro por separado.
12. **EXPLÍCITO — definición/taxonomía:** security standard es un tipo de control document: “**is a type of control document**”.
13. **EXPLÍCITO:** ese control document define mandatory requirements: “**control document that defines mandatory requirements**”; que security standard las define es **ENTRAÑADO** por 12.
14. **EXPLÍCITO — definición/taxonomía:** security procedure es un tipo de operational document: “**is a type of operational document**”.
15. **EXPLÍCITO:** ese operational document define step-by-step activities: “**operational document that defines step-by-step activities**”; atribuirlo a security procedure es **ENTRAÑADO**.
16. **EXPLÍCITO — definición/taxonomía:** security guideline es un tipo de advisory document: “**is a type of advisory document**”.
17. **EXPLÍCITO:** ese advisory document recomienda good practices: “**advisory document that recommends good practices**”; atribuirlo a security guideline es **ENTRAÑADO**.
18. **EXPLÍCITO — definición:** security baseline es un minimum set of controls: “**is a minimum set of controls**”.
19. **EXPLÍCITO como relación con objeto disyuntivo:** los controls del conjunto son “**required for a system, application, or infrastructure component**”. Cada rama aislada no debe presentarse como hecho categórico independiente sin conservar `or`.

#### p004

20. **EXPLÍCITO:** board of directors provides strategic oversight for information security: “**provides strategic oversight for information security**”.
21. **EXPLÍCITO:** senior management approves security policies: “**approves security policies**”.
22. **EXPLÍCITO:** senior management allocates resources for security initiatives: “**allocates resources for security initiatives**”.
23. **EXPLÍCITO:** information security manager coordinates information security program: “**coordinates the information security program**”.
24. **EXPLÍCITO:** asset owner classifies information assets: “**classifies information assets**”.
25. **EXPLÍCITO:** asset owner defines protection requirements: “**defines protection requirements**”.
26. **EXPLÍCITO:** asset custodian operates technical environment: “**operates ... the technical environment**”.
27. **EXPLÍCITO:** asset custodian maintains technical environment: “**maintains the technical environment**”.
28. **EXPLÍCITO como disyunción:** technical environment “**stores or processes information**”. `stores` y `processes` comparten antecedente y objeto, pero las ramas aisladas no están afirmadas conjuntamente.
29. **EXPLÍCITO:** system administrator manages servers: “**manages servers**”.
30. **EXPLÍCITO:** manages networks: “**servers, networks**”.
31. **EXPLÍCITO:** manages operating systems: “**operating systems**”.
32. **EXPLÍCITO:** manages technical services: “**technical services**”.
33. **EXPLÍCITO:** security analyst monitors security events: “**monitors security events**”.
34. **EXPLÍCITO:** security analyst investigates suspicious activity: “**investigates suspicious activity**”.
35. **EXPLÍCITO:** auditor evaluates compliance with security requirements: “**evaluates compliance with security requirements**”.
36. **EXPLÍCITO:** end user accesses systems: “**accesses systems**”.
37. **EXPLÍCITO, deóntico:** end user must follow security policies: “**must follow security policies**”. Afirmar que de hecho ya las sigue, omitiendo `must`, sería **NO SOPORTADO**.

### Taxonomías explícitas

- `SecurityPolicy → FormalDocument`: “**is a formal document**” (p003).
- `SecurityStandard → ControlDocument`: “**is a type of control document**” (p003).
- `SecurityProcedure → OperationalDocument`: “**is a type of operational document**” (p003).
- `SecurityGuideline → AdvisoryDocument`: “**is a type of advisory document**” (p003).
- `SecurityBaseline → MinimumSetOfControls`: “**is a minimum set of controls**” (p003).

No son taxonomías explícitas los verbos `protects`, `implements`, `defines`, `recommends`, `provides`, `approves`, `allocates`, `coordinates`, `classifies`, `operates`, `maintains`, `manages`, `monitors`, `investigates`, `evaluates`, `accesses` o `must follow`.

### Modalidad

- **Medio/finalidad:** “**protects information by implementing**” (p003) vincula la implementación como medio, no como una acción de `information`.
- **Finalidad con alcance ambiguo:** “**rules and expectations for protecting information**” (p003).
- **Obligatoriedad/calificación:** `mandatory requirements`, controls `required for ...`, y “**must follow**” (p003–p004).
- **Carácter advisory:** “**recommends good practices**” (p003) no equivale a obligación.
- **Disyunción:** “**system, application, or infrastructure component**” (p003) y “**stores or processes**” (p004). La lectura disyuntiva agrupada es **EXPLÍCITA**; afirmar todas las ramas a la vez es **NO SOPORTADO**.
- **Sin negación ni incertidumbre epistémica:** el texto usa declarativas genéricas.

### Ambigüedades

- **Alcance de `for protecting information` (p003):** alcance sobre `rules and expectations` y alcance solo sobre `expectations` son **PLAUSIBLES**. Dos hechos categóricos separados no están inequívocamente entrañados.
- **Semántica de `or` (p003/p004):** el texto no decide exclusividad frente a inclusividad; debe conservarse la disyunción. Convertir las ramas en hechos simultáneos sería **NO SOPORTADO**.
- **Cuantificación genérica (p003/p004):** una lectura de clases/roles es **PLAUSIBLE** por el estilo definicional; una lectura como individuos nombrados es **NO SOPORTADO**.
- **Correferencias explícitas:** los cinco `that` remiten respectivamente a `formal document`, `control document`, `operational document`, `advisory document` y `technical environment`. Esas resoluciones son **EXPLÍCITAS/ENTRAÑADAS** por la estructura relativa.
- **No correferencias:** `policies`/`procedures` del primer enunciado y `security policy`/`security procedure` posteriores guardan afinidad léxica, pero una identidad de clase adicional no se declara. Forzarla sería **PLAUSIBLE** como máximo.
- Negar la obligación de “**must follow security policies**” (p004) sería **CONTRADICHO** por el texto.

## 2. Resultado por etapa

| Paso | Etapa | Fidelidad | Cobertura | Precisión | Trazabilidad | Coherencia | Estado |
|---:|---|---:|---:|---:|---:|---:|---|
| 01 | input_intake | 4 | 4 | 4 | 4 | 4 | OK |
| 02 | preprocessing | 4 | 4 | 4 | 4 | 4 | OK |
| 03 | sentence_segmentation | 4 | 4 | 4 | 4 | 4 | OK |
| 04 | tokenization | 4 | 4 | 4 | 4 | 4 | OK |
| 05 | linguistic_annotation | 3 | 4 | 3 | 4 | 3 | WARN |
| 06 | entity_extraction | 4 | 4 | 4 | 4 | 4 | OK |
| 07 | concept_extraction | 3 | 2 | 3 | 4 | 3 | WARN |
| 08 | coreference_resolution | 4 | 4 | 4 | 4 | 4 | OK |
| 09 | relation_extraction | 1 | 2 | 1 | 3 | 1 | FAIL |
| 10 | canonical_claims / semantic_claims | 3 | 4 | 3 | 4 | 4 | WARN |
| 11 | semantic_debug_ir | N/A | N/A | N/A | N/A | N/A | N/A |
| 12 | triple_extraction | 4 | 4 | 4 | 4 | 4 | OK |
| 13 | taxonomy_induction | 4 | 4 | 4 | 4 | 4 | OK |
| 14 | type_assertion | 4 | 4 | 4 | 4 | 4 | OK |
| 15 | semantic_quality | 4 | 4 | 4 | 4 | 4 | OK |
| 16 | output_generation | 4 | 4 | 4 | 4 | 3 | WARN |

## 3. Hallazgos

### Q-infosec_p003_p004-05-1

- **Severidad:** MEDIA
- **Tipo:** anotación morfosintáctica incorrecta
- **Atribución:** ERROR_ORIGEN en 05; ERROR_AMPLIFICADO en 07/09; ERROR_CORREGIDO en 10/15
- **Cita literal:** “**the technical environment that stores or processes information**” (p004).
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p003_p004/artifacts/pipeline_outputs/observed_p003_p004_05_linguistic_annotation.json` — `/tokens/158/pos`, `/tokens/158/tag`, `/tokens/158/dependency`.
- **Evaluación razonada:** `stores` es el primer predicado verbal coordinado con `processes`, pero se anota `NOUN/NNS`. La dependencia `relcl` hacia `environment` revela la función verbal esperada. La lectura nominal es **CONTRADICHA** por “stores or processes information”.
- **Impacto downstream:** 07 crea el concepto espurio `stores` (`/concepts/51`) y 09 produce `store process information` (`/relations/17`). 10 recupera correctamente `TechnicalEnvironment stores Information`; 15 excluye `stores` como `coordinated_predicate_misclassified_as_concept`, por lo que el error espurio no llega al modelo final.

### Q-infosec_p003_p004-07-1

- **Severidad:** MEDIA
- **Tipo:** pérdida y granularidad conceptual
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** “**control document that defines mandatory requirements**”, “**operational document that defines step-by-step activities**” y “**advisory document that recommends good practices**” (p003).
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p003_p004/artifacts/pipeline_outputs/observed_p003_p004_07_concept_extraction.json` — `/concepts`.
- **Evaluación razonada:** faltan candidatos autónomos para `control document`, `operational document`, `advisory document` y `step-by-step activities`, aunque son argumentos centrales y evidencias de las definiciones. Además, `rules and expectations` se fusiona en un solo candidato cuyo lema es `expectations`, lo que dificulta representar ambos coordinados. La lista sigue siendo usable, pero su cobertura de conceptos definitorios es baja.
- **Impacto downstream:** contribuye a relaciones 09 incompletas (`be type`) y objetos reducidos (`activity`, `requirement`). 10 corrige estas pérdidas al producir claims con `ControlDocument`, `OperationalDocument`, `AdvisoryDocument`, `StepByStepActivity`, `Rule` y `Expectation`.

### Q-infosec_p003_p004-09-1

- **Severidad:** ALTA
- **Tipo:** asignación incorrecta de roles semánticos y dirección SPO
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** “**An organization protects information by implementing governance**” (p003); “**Senior management ... allocates resources**”, “**The asset owner ... defines protection requirements**” y “**The end user ... must follow security policies**” (p004).
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p003_p004/artifacts/pipeline_outputs/observed_p003_p004_09_relation_extraction.json` — `/relations/37`, `/relations/4`, `/relations/12`, `/relations/21`.
- **Evaluación razonada:** se generan, respectivamente, `information implement governance`, `policy allocate resource`, `asset define protection` y `system follow security`. Son lecturas **NO SOPORTADAS**: los sujetos literales son organization, senior management, asset owner y end user. La proximidad o coordinación de constituyentes se ha usado como si determinara semántica.
- **Impacto downstream:** distorsiona severamente el IR relacional y lo hace inadecuado como fuente directa de triples. 10 corrige las cuatro familias de errores; ninguna de estas relaciones erróneas llega a RDF/OWL.

### Q-infosec_p003_p004-09-2

- **Severidad:** ALTA
- **Tipo:** omisión sistemática de coordinados, definiciones y modificadores
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** “**implementing governance, policies, procedures, controls, monitoring mechanisms, and incident response processes**” (p003) y “**manages servers, networks, operating systems, and technical services**” (p004).
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p003_p004/artifacts/pipeline_outputs/observed_p003_p004_09_relation_extraction.json` — `/relations`.
- **Evaluación razonada:** de la primera lista solo aparece un `implement` y con sujeto incorrecto; de la segunda solo `administrator manage server`. Las definiciones `type of control/operational/advisory document` se reducen a objetos vacíos o genéricos `type` (`/relations/10`, `/relations/28`, `/relations/35`). También se pierden `strategic`, `information security`, `mandatory`, `step-by-step`, `good`, `protection` y varios complementos. La cobertura es insuficiente aunque existan algunas relaciones correctas.
- **Impacto downstream:** es la principal pérdida del pipeline intermedio. 10 la corrige mediante 42 claims completos, incluyendo todas las listas, las cinco definiciones y los modificadores relevantes.

### Q-infosec_p003_p004-09-3

- **Severidad:** ALTA
- **Tipo:** pérdida de modalidad y alcance
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** “**controls required for a system, application, or infrastructure component**” (p003), “**stores or processes information**” y “**must follow security policies**” (p004).
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p003_p004/artifacts/pipeline_outputs/observed_p003_p004_09_relation_extraction.json` — `/relations/25`, `/relations/18`, `/relations/22`.
- **Evaluación razonada:** `control require system` invierte `required for` y omite dos ramas y `or`; `technical environment process information` elimina la alternativa `stores`; `user follow policy` elimina `must` y convertiría una obligación en hecho actual. Tales lecturas sin modalidad son **NO SOPORTADAS**.
- **Impacto downstream:** si se proyectaran directamente, producirían RDF semánticamente más fuerte o dirigido al revés. 10 corrige dirección, `must` y ambos grupos disyuntivos; 12 conserva esas marcas.

### Q-infosec_p003_p004-10-1

- **Severidad:** MEDIA
- **Tipo:** sobrecompromiso ante ambigüedad de alcance
- **Atribución:** ERROR_ORIGEN; ERROR_PROPAGADO en 12; ERROR_AMPLIFICADO en 16
- **Cita literal:** “**defines rules and expectations for protecting information**” (p003).
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p003_p004/artifacts/pipeline_outputs/observed_p003_p004_10_canonical_claims.json` — `/canonical_claims/claims/10`, `/canonical_claims/claims/11` y sus duplicados semánticos `/semantic_claims/claims/10`, `/semantic_claims/claims/11`.
- **Evaluación razonada:** se afirman categóricamente `Rule has_purpose_to_protect Information` y `Expectation has_purpose_to_protect Information`. El alcance compartido es **PLAUSIBLE**, pero también lo es la adjunción solo al coordinado más próximo; el texto no autoriza resolver la ambigüedad sin marca. El resto de los 42 claims es notablemente atómico, completo, modal y trazable, y corrige los errores de 09.
- **Impacto downstream:** 12 proyecta fielmente ambos claims. 16 los materializa como facts (`/output/graph/facts/9`, `/output/graph/facts/10`) y como restricciones (`/output/graph/restrictions/12`, `/output/graph/restrictions/13`), convirtiendo una lectura plausible en cuatro estructuras categóricas. Es el único sobrecompromiso semántico relevante que llega al output final.

### Q-infosec_p003_p004-16-1

- **Severidad:** BAJA
- **Tipo:** duplicación estructural del modelo de salida
- **Atribución:** ERROR_ORIGEN
- **Cita literal de ejemplo:** “**The system administrator manages servers, networks, operating systems, and technical services**” (p004).
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p003_p004/artifacts/pipeline_outputs/observed_p003_p004_16_output_generation.json` — `/output/graph/classes`, `/output/graph/schema/classes`, `/output/graph/object_property_schema`, `/output/graph/schema/object_properties`.
- **Evaluación razonada:** los 49 registros de `classes` se repiten exactamente en `schema/classes`; el esquema de 19 propiedades también se repite en dos formas equivalentes. Además, las 32 relaciones materializadas aparecen en capas de facts, uso observado y restricciones. Estas capas pueden tener funciones distintas, pero los contenedores de clases y propiedades son redundantes y reducen coherencia estructural sin añadir evidencia.
- **Impacto downstream:** aumenta tamaño y riesgo de divergencia entre vistas. No introduce por sí mismo una proposición falsa ni pierde claims; la proyección conserva disposiciones para los 42 claims, con 37 materializados y 5 representados en dos grupos lógicos.

## 4. Diagnóstico

- **Primera degradación:** 05, al etiquetar `stores` como nombre pese a su función verbal coordinada (p004). Es localizada y luego corregida.
- **Primera degradación semántica amplia:** 07 pierde varios conceptos definitorios; la degradación decisiva ocurre en 09, donde coordinación, compuestos y adjuntos generan sujetos incorrectos, listas truncadas y modalidad eliminada.
- **Principal pérdida:** la cobertura relacional de 09: casi toda la lista de medios de protección (p003), tres objetos administrados (p004), objetos taxonómicos y calificadores.
- **Principal contenido no soportado:** `policy allocate resource` en 09 frente a “**Senior management ... allocates resources**” (p004). Compite con otros errores de sujeto (`information implements governance`, `system follows security`), pero ninguno sobrevive a 10.
- **Errores que llegan a RDF/OWL:** no llegan los SPO erróneos de 09 ni el concepto nominal `stores`. Sí llega el alcance no resuelto de “**rules and expectations for protecting information**” (p003), materializado para `Rule` y `Expectation`. También llega redundancia estructural, no una falsedad adicional.
- **Errores corregidos:** 10 reconstruye 42 claims fieles en casi todos los aspectos: seis medios de implementación, cinco definiciones, listas coordinadas, finalidad, obligación y dos grupos disyuntivos. 15 detecta y excluye `stores` como ruido. 13 induce solo las cinco jerarquías justificadas y 14 evita inventar instancias.
- **Aciertos:** intake, normalización, 15 frases, 208 tokens y offsets preservan el texto; las cinco correferencias relativas son correctas; las evidencias de claims remiten al párrafo y frase; 12 conserva modalidad, dirección y trazas; 16 representa las cinco ramas disyuntivas como `evidence_only` dentro de grupos lógicos, en vez de afirmarlas como facts independientes.
- **Incertidumbres legítimas:** alcance de `for protecting information`, inclusividad de `or` y cuantificación genérica de roles. No se penaliza la ausencia de instancias ni el conservadurismo de 06/14. La representación de relaciones genéricas como restricciones de clase es plausible, pero la cuantificación no está formalizada por el texto.

## 5. Veredicto

- **Calidad global:** **84/100**.
- **Output final:** **parcialmente fiel**. Es completo y mayoritariamente preciso; la grave degradación de 09 se corrige antes de la proyección. La reserva principal es un sobrecompromiso de alcance que llega a RDF/OWL, más redundancia estructural.
- **Tres correcciones prioritarias:**
  1. Corregir en 09 la herencia de sujeto en coordinaciones, la expansión completa de listas y la dirección de pasivas/adjuntos; nunca inferir roles por proximidad.
  2. Preservar en 07–09 frases nominales completas y modalidad (`must`, `required_for`, `or`, finalidad), evitando promover predicados como `stores` a conceptos.
  3. Representar el alcance ambiguo de `for protecting information` como grupo o claim compuesto/no resuelto y evitar duplicar vistas equivalentes de clases y propiedades en 16.

Siguiente caso pendiente: infosec_p005_p006.
