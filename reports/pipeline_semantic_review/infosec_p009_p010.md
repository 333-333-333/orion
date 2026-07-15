# Revisión semántica: infosec_p009_p010

## 1. Lectura independiente

### Resumen

Los dos párrafos describen, en forma genérica, dos núcleos temáticos relacionados:

- **p009:** qué es una credencial, varios tipos de credencial o secreto, el uso de una API key y cinco obligaciones de protección, almacenamiento, expiración, rotación y revocación.
- **p010:** el efecto de la autenticación multifactor, una taxonomía de factores de autenticación, ejemplos genéricos de esos factores y una reducción de riesgo asociada a contraseñas robadas.

No aparecen individuos nombrados. Los sintagmas indefinidos —“a password”, “a certificate”, “an access token”, etc.— se leen como afirmaciones genéricas sobre clases, no como instancias particulares. “Applications”, “requests” y “the user” son participantes genéricos.

### Conceptos

- **p009:** Credential, Evidence, Identity, Password, Certificate, Cryptographic Credential, Access Token, Temporary Credential, API Key, Application, Request, Private Key, Cryptographic Secret, Disclosure, Secure Location, Defined Period, Compromised Credential, Rotation y Revocation. Los dos últimos son nominalizaciones **ENTRAÑADAS** por “rotated” y “revoked”, no nombres literales del texto.
- **p010:** Multi-factor Authentication, Authentication Strength, Verification Factor, Authentication Factor, Knowledge Factor, Possession Factor, Inherence Factor, Hardware Token, Mobile Authenticator Application, Fingerprint, Risk of Unauthorized Access, Stolen Password, User y los rellenos indefinidos expresados como “something”.
- **Entidades/instancias explícitas:** ninguna instancia nombrada. “User”, “Application” y “Request” designan roles o clases genéricas; tratarlos como individuos concretos sería **NO SOPORTADO**.
- **Correferencia:** no hay pronombres anafóricos que exijan resolución entre oraciones. Las repeticiones de “password”, “API key”, “private key”, “access token” y “multi-factor authentication” son recurrencias léxicas del mismo concepto genérico. Los tres “something” no están explícitamente correferidos entre sí.

### Proposiciones con evidencia

| # | Clasificación | Proposición literal o descomposición conservadora | Evidencia breve |
|---:|---|---|---|
| 1 | EXPLÍCITO | Una credencial es evidencia. | p009: “A credential is evidence” |
| 2 | EXPLÍCITO | Esa evidencia se usa para probar una identidad; como propiedad definitoria, una credencial se usa para probar una identidad. | p009: “evidence used to prove an identity” |
| 3 | EXPLÍCITO | Password es un tipo de Credential. | p009: “A password is a type of credential” |
| 4 | EXPLÍCITO | Certificate es un tipo de Cryptographic Credential. | p009: “A certificate is a type of cryptographic credential” |
| 5 | EXPLÍCITO | Access Token es un tipo de Temporary Credential. | p009: “An access token is a type of temporary credential” |
| 6 | EXPLÍCITO | API Key es un tipo de Credential. | p009: “An API key is a type of credential” |
| 7 | EXPLÍCITO | Las aplicaciones usan API keys. | p009: “credential used by applications” |
| 8 | EXPLÍCITO | El propósito de ese uso es que las aplicaciones autentiquen solicitudes. | p009: “to authenticate requests” |
| 9 | EXPLÍCITO | Private Key es un tipo de Cryptographic Secret. | p009: “A private key is a type of cryptographic secret” |
| 10 | EXPLÍCITO | Password debe protegerse contra Disclosure. | p009: “must be protected against disclosure” |
| 11 | EXPLÍCITO | Private Key debe almacenarse en una Secure Location. | p009: “must be stored in a secure location” |
| 12 | EXPLÍCITO | Access Token debe expirar después de un Defined Period. | p009: “must expire after a defined period” |
| 13 | EXPLÍCITO | API Key debe rotarse periódicamente. | p009: “must be rotated periodically” |
| 14 | EXPLÍCITO | Compromised Credential debe revocarse inmediatamente. | p009: “must be revoked immediately” |
| 15 | EXPLÍCITO | Multi-factor Authentication mejora Authentication Strength. | p010: “improves authentication strength” |
| 16 | EXPLÍCITO | El mecanismo de esa mejora es requerir más de un Verification Factor. | p010: “by requiring more than one verification factor” |
| 17 | EXPLÍCITO | Knowledge Factor es un tipo de Authentication Factor. | p010: “a type of authentication factor” |
| 18 | EXPLÍCITO | Knowledge Factor se basa en algo que el usuario conoce. | p010: “something the user knows” |
| 19 | EXPLÍCITO | Possession Factor es un tipo de Authentication Factor. | p010: “a type of authentication factor” |
| 20 | EXPLÍCITO | Possession Factor se basa en algo que el usuario tiene. | p010: “something the user has” |
| 21 | EXPLÍCITO | Inherence Factor es un tipo de Authentication Factor. | p010: “a type of authentication factor” |
| 22 | EXPLÍCITO | Inherence Factor se basa en algo que el usuario es. | p010: “something the user is” |
| 23 | EXPLÍCITO | Password es Knowledge Factor. | p010: “A password is a knowledge factor” |
| 24 | EXPLÍCITO | Hardware Token es Possession Factor. | p010: “A hardware token is a possession factor” |
| 25 | EXPLÍCITO | Mobile Authenticator Application es Possession Factor. | p010: “A mobile authenticator application is a possession factor” |
| 26 | EXPLÍCITO | Fingerprint es Inherence Factor. | p010: “A fingerprint is an inherence factor” |
| 27 | EXPLÍCITO | Multi-factor Authentication reduce el riesgo de Unauthorized Access causado por Stolen Passwords. | p010: “reduces the risk of unauthorized access caused by stolen passwords” |
| 28 | EXPLÍCITO | Stolen Passwords causan Unauthorized Access dentro del riesgo descrito. | p010: “unauthorized access caused by stolen passwords” |
| 29 | ENTRAÑADO | Cryptographic Credential y Temporary Credential son clases de Credential por la cabeza nominal “credential”. | p009: “cryptographic credential”; “temporary credential” |
| 30 | ENTRAÑADO | Compromised Credential es Credential y Stolen Password es Password por composición del sintagma nominal. | p009: “compromised credential”; p010: “stolen passwords” |
| 31 | PLAUSIBLE | Los tres tipos de factor podrían ser categorías mutuamente excluyentes. El texto no lo afirma. | p010: “knowledge factor”, “possession factor”, “inherence factor” |
| 32 | NO SOPORTADO | Multi-factor Authentication exige exactamente dos factores. Solo se afirma “más de uno”. | p010: “more than one verification factor” |
| 33 | NO SOPORTADO | Multi-factor Authentication elimina el riesgo. Solo se afirma que lo reduce. | p010: “reduces the risk” |
| 34 | NO SOPORTADO | “The user is a type”. “Is” pertenece a la relativa “something the user is”, no a una clasificación del usuario. | p010: “something the user is” |
| 35 | CONTRADICHO | Las rotaciones, revocaciones, protecciones o almacenamientos ya ocurrieron como hechos consumados. El texto los mantiene bajo alcance de “must”. | p009: “must be protected/stored/rotated/revoked” |

### Taxonomías explícitas

- **p009:** Password ⊑ Credential; Certificate ⊑ Cryptographic Credential; Access Token ⊑ Temporary Credential; API Key ⊑ Credential; Private Key ⊑ Cryptographic Secret.
- **p010:** Knowledge Factor ⊑ Authentication Factor; Possession Factor ⊑ Authentication Factor; Inherence Factor ⊑ Authentication Factor; Password ⊑ Knowledge Factor; Hardware Token ⊑ Possession Factor; Mobile Authenticator Application ⊑ Possession Factor; Fingerprint ⊑ Inherence Factor.
- **Definición clasificatoria:** Credential ⊑ Evidence es una lectura conservadora de p009: “A credential is evidence”. No se justifica equivalencia de clases.
- **Taxonomías solo entrañadas por composición:** Cryptographic Credential ⊑ Credential, Temporary Credential ⊑ Credential, Compromised Credential ⊑ Credential y Stolen Password ⊑ Password. No se exige materializarlas si la política prefiere conservar solo taxonomías literalmente formuladas.

### Modalidad

- p009 contiene cinco obligaciones con **must**: proteger Password, almacenar Private Key, hacer expirar Access Token, rotar API Key y revocar Compromised Credential.
- “after a defined period”, “periodically” e “immediately” forman parte del alcance de sus respectivas obligaciones.
- p010 usa modalidad asertiva. “By requiring” expresa el medio de la mejora, y “caused by” expresa una relación causal dentro del riesgo descrito.
- No hay negación, posibilidad, permiso ni incertidumbre epistémica explícita.

### Ambigüedades

- **Clase frente a instancia:** los artículos indefinidos admiten una lectura superficial de instancia, pero el patrón definitorio y normativo favorece la lectura genérica de clase. No se penaliza que no haya type assertions de individuos.
- **“Something”:** cada aparición introduce un relleno indefinido bajo un predicado distinto —knows, has, is—. El texto no obliga ni impide que coincidan; fusionarlos como un mismo individuo sería **NO SOPORTADO**.
- **“Evidence used to prove”:** gramaticalmente “used to prove” modifica a Evidence. Atribuir la propiedad a Credential es **ENTRAÑADO** por la definición, pero no autoriza relaciones adicionales sobre un agente no mencionado.
- **API key:** “to authenticate requests” expresa el propósito del uso por aplicaciones. Una relación Application–authenticates–Request es fiel solo si conserva el contexto de uso de API Key.
- **Causalidad final:** “caused by stolen passwords” modifica Unauthorized Access dentro del sintagma Risk. Separar la causalidad es válido si se conserva ese contexto.

## 2. Resultado por etapa

| Paso | Etapa | Fidelidad | Cobertura | Precisión | Trazabilidad | Coherencia | Estado |
|---:|---|---:|---:|---:|---:|---:|---|
| 01 | input_intake | 4 | 4 | 4 | 4 | 4 | OK |
| 02 | preprocessing | 4 | 4 | 4 | 4 | 4 | OK |
| 03 | sentence_segmentation | 4 | 4 | 4 | 4 | 4 | OK |
| 04 | tokenization | 4 | 4 | 4 | 4 | 4 | OK |
| 05 | linguistic_annotation | 4 | 4 | 4 | 4 | 4 | OK |
| 06 | entity_extraction | 4 | 4 | 4 | 4 | 4 | OK |
| 07 | concept_extraction | 3 | 2 | 3 | 4 | 3 | WARN |
| 08 | coreference_resolution | 4 | 4 | 4 | 4 | 4 | OK |
| 09 | relation_extraction | 1 | 1 | 1 | 3 | 1 | FAIL |
| 10 | canonical_claims / semantic_claims | 4 | 4 | 3 | 4 | 3 | WARN |
| 11 | semantic_debug_ir | 3 | 4 | 3 | 4 | 3 | WARN |
| 12 | triple_extraction | 3 | 4 | 3 | 4 | 2 | WARN |
| 13 | taxonomy_induction | 4 | 4 | 4 | 4 | 4 | OK |
| 14 | type_assertion | 4 | 4 | 4 | 4 | 4 | OK |
| 15 | semantic_quality | 2 | 2 | 1 | 3 | 2 | FAIL |
| 16 | output_generation | 3 | 3 | 4 | 4 | 3 | WARN |

## 3. Hallazgos

### Q-infosec_p009_p010-07-1

- **Severidad:** MEDIA
- **Tipo:** PÉRDIDA_DE_CONCEPTOS
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** p009: “a type of cryptographic credential”, “a type of temporary credential”, “a type of cryptographic secret”; p010: “a type of authentication factor”.
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p009_p010/artifacts/pipeline_outputs/observed_p009_p010_07_concept_extraction.json`, `/concepts`.
- **Evaluación razonada:** la etapa propone Certificate, Access Token, Private Key y los tres factores específicos, pero omite como candidatos los objetos clasificatorios explícitos Cryptographic Credential, Temporary Credential, Cryptographic Secret y Authentication Factor. No es un problema de NER ni de correferencia: son sintagmas nominales explícitos relevantes para ontología.
- **Impacto downstream:** contribuye a que relation_extraction no pueda referenciar los supertipos. Canonical claims los reconstruye en el paso 10, por lo que el error queda **corregido** antes de taxonomía y RDF.

### Q-infosec_p009_p010-07-2

- **Severidad:** BAJA
- **Tipo:** NORMALIZACIÓN_SEMÁNTICA
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** p010: “more than one verification factor”.
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p009_p010/artifacts/pipeline_outputs/observed_p009_p010_07_concept_extraction.json`, `/concepts/20/normalized_text`.
- **Evaluación razonada:** el texto del candidato conserva “more than one verification factor”, pero `normalized_text` queda como “than one verification factor”, perdiendo “more” y produciendo una forma no interpretable por sí sola. No se penaliza la decisión de proponer también “verification factor”; se penaliza únicamente la normalización defectuosa.
- **Impacto downstream:** podría destruir el cuantificador. El paso 10 lo recupera correctamente como `quantifier: more_than_one`, así que no llega al output final.

### Q-infosec_p009_p010-09-1

- **Severidad:** ALTA
- **Tipo:** RELACIÓN_MAL_FORMADA
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** p009: “A password is a type of credential”; p010: “A knowledge factor is a type of authentication factor”.
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p009_p010/artifacts/pipeline_outputs/observed_p009_p010_09_relation_extraction.json`, `/relations/0`, `/relations/1`, `/relations/3`, `/relations/4`, `/relations/6`, `/relations/7`, `/relations/10`, `/relations/14`.
- **Evaluación razonada:** los ocho patrones “is a type of X” se reducen a relaciones `be` cuyo objeto es literalmente `type` y cuyo `object_ref` está vacío. El objeto semántico debe ser Credential, Cryptographic Credential, Temporary Credential, Cryptographic Secret o Authentication Factor, según la oración. La evidencia termina antes de “of X”, por lo que tampoco traza la proposición completa.
- **Impacto downstream:** destruye la taxonomía si se consume esta etapa directamente. El paso 10 reemplaza estas relaciones lossy por claims `is_a` fieles; se trata de un **ERROR_CORREGIDO**, no de ocho errores nuevos en los pasos posteriores.

### Q-infosec_p009_p010-09-2

- **Severidad:** ALTA
- **Tipo:** PÉRDIDA_DE_RELACIONES
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** p009: “must be protected”, “must be stored”, “must expire”, “must be rotated”, “must be revoked”; p010: “by requiring more than one verification factor”.
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p009_p010/artifacts/pipeline_outputs/observed_p009_p010_09_relation_extraction.json`, `/relations`.
- **Evaluación razonada:** no aparece ninguna de las cinco obligaciones de p009. Tampoco se extraen el medio cuantificado de la mejora, las propiedades `based on` con knows/has/is, `used by applications`, el propósito de autenticar solicitudes ni la causalidad de Stolen Passwords. Son relaciones explícitas, no inferencias de dominio. La etapa sí conserva las relaciones simples improves/reduces y cuatro clasificaciones directas, pero su cobertura global es baja.
- **Impacto downstream:** es la principal pérdida semántica intermedia. Canonical claims reconstruye todos estos grupos con modalidad, temporalidad, contexto, cuantificador y evidencia; la pérdida no debe volver a contarse en 10–16.

### Q-infosec_p009_p010-09-3

- **Severidad:** ALTA
- **Tipo:** CONTENIDO_NO_SOPORTADO
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** p010: “An inherence factor is a type of authentication factor based on something the user is.”
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p009_p010/artifacts/pipeline_outputs/observed_p009_p010_09_relation_extraction.json`, `/relations/2`.
- **Evaluación razonada:** la relación `user —be→ type` mezcla el `is` de la relativa “something the user is” con el atributo `type` de la cláusula principal. La interpretación “User is a Type” es **NO SOPORTADA** y la evidencia seleccionada atraviesa indebidamente ambas cláusulas.
- **Impacto downstream:** sería una invención grave en una ontología. No aparece en canonical claims, triples, taxonomía ni output final; el paso 10 la corrige por exclusión y crea en su lugar el claim scoped `InherenceFactor based_on Something` con `actor: User` y `event_predicate: is`.

### Q-infosec_p009_p010-10-1

- **Severidad:** BAJA
- **Tipo:** DUPLICACIÓN_CONTROLADA
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** p009: “must expire after a defined period”, “must be rotated periodically”, “must be revoked immediately”.
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p009_p010/artifacts/pipeline_outputs/observed_p009_p010_10_canonical_claims.json`, `/semantic_claims/claims/17`, `/semantic_claims/claims/18`, `/semantic_claims/claims/19`, `/semantic_claims/claims/20`, `/semantic_claims/claims/21`, `/semantic_claims/claims/22`.
- **Evaluación razonada:** tres obligaciones tienen una forma scoped principal y otra forma `compatibility_only` interna. La marca `projection: internal` hace la duplicación explícita y evita considerarla una segunda proposición, pero `claim_count: 31` cuenta ambas representaciones y obliga a todas las etapas consumidoras a respetar visibilidad.
- **Impacto downstream:** triple_extraction amplifica temporalmente la duplicación. Output generation la corrige al excluir exactamente los tres claims internos.

### Q-infosec_p009_p010-12-1

- **Severidad:** MEDIA
- **Tipo:** PÉRDIDA_DE_VISIBILIDAD_Y_DUPLICACIÓN
- **Atribución:** ERROR_AMPLIFICADO
- **Cita literal:** p009: “An access token must expire after a defined period”, “An API key must be rotated periodically”, “A compromised credential must be revoked immediately”.
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p009_p010/artifacts/pipeline_outputs/observed_p009_p010_12_triple_extraction.json`, `/triples/0`, `/triples/1`, `/triples/22`, `/triples/23`, `/triples/25`, `/triples/26`.
- **Evaluación razonada:** la etapa convierte tanto el claim scoped principal como su variante `compatibility_only` en triples ordinarios y ya no conserva `projection: internal` ni `visibility: internal`. Así, cada una de las tres obligaciones queda duplicada en el conjunto de triples, aunque con predicados diferentes.
- **Impacto downstream:** semantic_quality no lo detecta. Output generation sí consulta las disposiciones de claims y excluye `claim-cc3a…`, `claim-49ab…` y `claim-b60a…`; por tanto es un **ERROR_CORREGIDO** en el RDF final.

### Q-infosec_p009_p010-15-1

- **Severidad:** ALTA
- **Tipo:** CONTROL_DE_CALIDAD_INEFICAZ
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** p009: “must expire after a defined period”; p010: “something the user knows/has/is”.
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p009_p010/artifacts/pipeline_outputs/observed_p009_p010_15_semantic_quality.json`, `/semantic_quality_report/quality_score`, `/semantic_quality_report/relation_gaps`, `/semantic_quality_report/semantic_ambiguities`, `/semantic_quality_report/warnings`.
- **Evaluación razonada:** el informe asigna `quality_score: 1.0`, no registra gaps, ambigüedades ni warnings, pese a que el payload previo contiene triples duplicados de compatibilidad, relations mal formadas y una normalización conceptual defectuosa. Aunque canonical claims corrigió el contenido utilizado para RDF, la responsabilidad declarada de esta etapa incluye conceptos, relaciones y triples; un resultado perfecto no está semánticamente justificado.
- **Impacto downstream:** no bloquea este caso porque output generation dispone de reglas propias de exclusión, pero ofrece una señal de confianza excesiva y no protegería una estrategia de salida que consumiera los triples sin esas disposiciones.

### Q-infosec_p009_p010-16-1

- **Severidad:** MEDIA
- **Tipo:** PÉRDIDA_DE_VÍNCULO_PROPOSICIONAL
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** p010: “improves authentication strength by requiring more than one verification factor”.
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p009_p010/artifacts/pipeline_outputs/observed_p009_p010_16_output_generation.json`, `/output/graph/facts/5`, `/output/graph/scoped_relations/5`.
- **Evaluación razonada:** el fact de mejora conserva `means_group`, pero la relación scoped que representa el requisito cuantificado pierde tanto `means_group` como `goal`, presentes en canonical claims y triples. `relation_role: means_for` indica que existe un medio, pero no identifica formalmente a qué proposición de mejora se vincula. La evidencia textual permite reconstruirlo, pero el modelo estructurado ya no lo hace sin heurística.
- **Impacto downstream:** consultas RDF/OWL sobre el mecanismo de la mejora no pueden unir de forma determinista ambas proposiciones. Es la principal pérdida residual del output final.

### Q-infosec_p009_p010-16-2

- **Severidad:** BAJA
- **Tipo:** DUPLICACIÓN_ESTRUCTURAL
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** p009: “A credential is evidence used to prove an identity”; p010: “Multi-factor authentication improves authentication strength”.
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p009_p010/artifacts/pipeline_outputs/observed_p009_p010_16_output_generation.json`, `/output/graph/classes`, `/output/graph/schema/classes`, `/output/graph/object_property_schema`, `/output/graph/schema/object_properties`, `/output/graph/subclass_facts`, `/taxonomy_relations`.
- **Evaluación razonada:** clases, esquema de propiedades y taxonomía se publican en representaciones paralelas prácticamente equivalentes. No inventan hechos ni generan contradicción, pero incumplen el criterio estricto de salida “sin duplicación” y aumentan el riesgo de divergencia entre vistas.
- **Impacto downstream:** consumidores pueden contar dos veces recursos o elegir vistas distintas. En este artifact las copias son consistentes, por lo que el impacto es estructural, no una falsedad semántica.

## 4. Diagnóstico

- **Primera degradación:** paso 07, al no proponer varios supertipos nominales explícitos y normalizar “more than one” como “than one”.
- **Principal pérdida:** paso 09. Relation extraction pierde las cinco obligaciones y la mayoría de los calificadores de propósito, medio, base y causalidad; además rompe todos los patrones “type of”. El paso 10 corrige casi completamente esta degradación mediante claims respaldados por evidencia.
- **Principal contenido no soportado:** `User —be→ type` en el paso 09, originado por mezclar la cláusula principal con “something the user is” de p010. No llega al modelo final.
- **Errores que llegan a RDF/OWL:** no sobreviven la taxonomía falsa sobre User ni los objetos `type`. Sí llegan (a) la pérdida del enlace estructural entre mejora y medio cuantificado, y (b) duplicación de vistas del mismo esquema. La nominalización scoped `must + requires + Rotation/Revocation` es **ENTRAÑADA** y conserva paciente, voz, temporalidad y evidencia, pero es menos directa que mantener los eventos rotate/revoke.
- **Aciertos:** intake, normalización, segmentación, tokens y offsets son fieles; la ausencia de NER y type assertions es correcta porque no hay individuos nombrados; coreference evita inventar resoluciones; canonical claims recupera modalidad, temporalidad, cuantificador, contexto de API Key, mecanismo causal y las doce taxonomías literales; taxonomy induction no convierte obligaciones en subclases; output generation excluye los tres claims internos duplicados y no materializa los scoped claims como hechos modales sin calificación.
- **Incertidumbres:** modelar genéricos como clases es razonable pero no la única formalización posible. Los tres “something” son existenciales deliberadamente vagos; no se penaliza conservar esa vaguedad. Tampoco se penaliza no materializar las taxonomías solo entrañadas por la cabeza nominal —por ejemplo Temporary Credential ⊑ Credential—, dado el criterio conservador solicitado.

## 5. Veredicto

- **Calidad global:** **82/100**.
- **Output final:** **parcialmente fiel**. Conserva casi todas las proposiciones literales, taxonomías, modalidad y trazabilidad, y no deja pasar la invención principal del paso 09. No alcanza “fiel” por la pérdida del enlace formal entre la mejora y su medio, y por la duplicación estructural del modelo publicado.
- **Tres correcciones prioritarias:**
  1. Corregir relation extraction para capturar íntegramente `is a type of X`, obligaciones modales y calificadores de propósito/medio/base/causa, sin depender de remediación posterior.
  2. Hacer que semantic_quality audite también concepts, relations y triples internos: detectar objetos `type`, gaps, pérdida de visibilidad y duplicados de compatibilidad antes de declarar RDF readiness perfecta.
  3. Preservar `means_group`/`goal` hasta `scoped_relations` y publicar una sola vista canónica de clases, propiedades y taxonomía.

Siguiente caso pendiente: infosec_p011_p012.
