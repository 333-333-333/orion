# Revisión semántica: infosec_p039_p040

## 1. Lectura independiente

### Resumen

Los párrafos presentan dos ejemplos ilustrativos, no reglas universales:

- **p039** narra una secuencia de phishing —envío, enlace, clic, entrega y compromiso de una contraseña, y uso de la credencial— seguida de posibles medidas de prevención, reducción, detección, bloqueo, monitorización y contención.
- **p040** narra cifrado de archivos y pérdida de disponibilidad, seguida de posibles medidas de detección, limitación, recuperación, aislamiento, revisión y corrección.

No hay definiciones formales ni jerarquías taxonómicas explícitas. Las expresiones con **“may”** son posibilidades, no hechos consumados ni reglas necesarias. Ambos textos mantienen algunas identidades discursivas deliberadamente ambiguas.

### Conceptos

- **p039:** phishing scenario, threats, vulnerabilities, controls, incidents, threat actor, phishing email, employee, malicious link, password/submitted password, compromised credential, attacker, cloud account, multi-factor authentication, unauthorized access, security awareness training, likelihood of clicking, email filtering, log monitoring, suspicious login activity, incident response y compromised account.
- **p040:** ransomware scenario, backups, monitoring, response, malware, files/encrypted files, file server, business users, event, availability, integrity, endpoint detection and response, malware activity, network segmentation, ransomware spread, backup restoration, incident response team, affected systems, post-incident review, missing patches, weak access controls, insufficient monitoring, corrective actions, patch deployment, privilege reduction e improved detection rules.
- **Entidades o instancias discursivas explícitas:** p039 introduce un actor de amenaza, un correo, un empleado, un enlace, una contraseña/credencial, un atacante y una cuenta; p040 introduce malware, archivos, un servidor, usuarios, un evento, un equipo y sistemas afectados. Son participantes genéricos del ejemplo, no individuos nombrados. El texto no permite decidir de manera general si cada término debe proyectarse como clase, instancia o recurso conceptual.
- **Definiciones:** ninguna. “The submitted password becomes a compromised credential” describe un cambio de estado o rol, no una definición léxica universal.
- **Relaciones:** envío y destinatario, contención, clic, entrega, cambio de estado, uso y propósito de acceso; cifrado y localización, indisponibilidad para usuarios, afectación, detección, limitación, recuperación, aislamiento, identificación e inclusión.

### Proposiciones con evidencia

| ID | Párrafo | Clasificación | Proposición literal o entrañada | Evidencia breve |
|---|---|---|---|---|
| P39-01 | p039 | EXPLÍCITO | El escenario de phishing ilustra cómo amenazas, vulnerabilidades, controles e incidentes se relacionan entre sí. | “threats, vulnerabilities, controls, and incidents relate to each other” |
| P39-02 | p039 | EXPLÍCITO | Un actor de amenaza envía un correo de phishing a un empleado. | “A threat actor sends a phishing email to an employee” |
| P39-03 | p039 | EXPLÍCITO | El correo de phishing contiene un enlace malicioso. | “contains a malicious link” |
| P39-04 | p039 | EXPLÍCITO | El empleado pulsa el enlace malicioso. | “The employee clicks the malicious link” |
| P39-05 | p039 | EXPLÍCITO | El empleado entrega una contraseña. | “submits a password” |
| P39-06 | p039 | EXPLÍCITO | La contraseña entregada pasa a ser una credencial comprometida. | “becomes a compromised credential” |
| P39-07 | p039 | EXPLÍCITO | El atacante usa la credencial comprometida. | “uses the compromised credential” |
| P39-08 | p039 | ENTRAÑADO | El acceso a la cuenta cloud es el contenido finalista del uso de la credencial; el texto no separa intento de éxito. | “to access a cloud account” |
| P39-09 | p039 | EXPLÍCITO | La autenticación multifactor **puede** impedir acceso no autorizado. | “may prevent unauthorized access” |
| P39-10 | p039 | EXPLÍCITO | La formación de concienciación **puede** reducir la probabilidad de pulsar el enlace. | “may reduce the likelihood” |
| P39-11 | p039 | EXPLÍCITO | El filtrado de correo **puede** detectar el correo de phishing. | “may detect” |
| P39-12 | p039 | EXPLÍCITO | El filtrado de correo **puede** bloquear el correo de phishing. | “and block the phishing email” |
| P39-13 | p039 | EXPLÍCITO | La monitorización de logs **puede** identificar actividad sospechosa de inicio de sesión. | “may identify suspicious login activity” |
| P39-14 | p039 | EXPLÍCITO | La respuesta a incidentes **puede** contener la cuenta comprometida. | “may contain the compromised account” |
| P40-01 | p040 | EXPLÍCITO | El escenario de ransomware ilustra la importancia de backups, monitorización y respuesta. | “illustrates the importance of backups, monitoring, and response” |
| P40-02 | p040 | EXPLÍCITO | Malware cifra archivos. | “Malware encrypts files” |
| P40-03 | p040 | EXPLÍCITO | Los archivos cifrados están en un servidor de archivos. | “files on a file server” |
| P40-04 | p040 | EXPLÍCITO | El servidor pasa a estar no disponible para usuarios de negocio. | “becomes unavailable to business users” |
| P40-05 | p040 | EXPLÍCITO | El evento afecta a la disponibilidad. | “The event affects availability” |
| P40-06 | p040 | EXPLÍCITO | El evento **puede** afectar a la integridad. | “may affect integrity” |
| P40-07 | p040 | EXPLÍCITO | Endpoint detection and response **puede** detectar la actividad del malware. | “may detect the malware activity” |
| P40-08 | p040 | EXPLÍCITO | La segmentación de red **puede** limitar la propagación del ransomware. | “may limit the spread of the ransomware” |
| P40-09 | p040 | EXPLÍCITO | La restauración de backup **puede** recuperar archivos cifrados. | “may recover encrypted files” |
| P40-10 | p040 | EXPLÍCITO | El equipo de respuesta **puede** aislar sistemas afectados. | “may isolate affected systems” |
| P40-11 | p040 | EXPLÍCITO | La revisión posterior **puede** identificar alguna de tres alternativas: parches ausentes, controles débiles o monitorización insuficiente. | “may identify missing patches, weak access controls, or insufficient monitoring” |
| P40-12 | p040 | EXPLÍCITO | Las acciones correctivas **pueden** incluir despliegue de parches. | “may include patch deployment” |
| P40-13 | p040 | EXPLÍCITO | Las acciones correctivas **pueden** incluir reducción de privilegios. | “privilege reduction” |
| P40-14 | p040 | EXPLÍCITO | Las acciones correctivas **pueden** incluir reglas de detección mejoradas. | “improved detection rules” |

### Taxonomías explícitas

No hay relaciones explícitas de subclase ni aserciones inequívocas de pertenencia a clase. En particular:

- **NO SOPORTADO:** convertir “submitted password becomes a compromised credential” (p039) en una taxonomía `Password ⊑ Credential`; el texto habla de ese participante y de un cambio.
- **NO SOPORTADO:** convertir “Corrective actions may include…” (p040) en subclases necesarias; la pertenencia es modal y ejemplificativa.
- **NO SOPORTADO:** clasificar automáticamente malware como ransomware; el contexto lo hace plausible, no literal.

### Modalidad

- **Asertadas sin modal:** la secuencia principal de p039 hasta el acceso; en p040, el cifrado, la ubicación de los archivos, la indisponibilidad y la afectación de disponibilidad.
- **Posibilidad (`may`):** p039 P39-09 a P39-14; p040 P40-06 a P40-14. Quitar `may` produciría una interpretación más fuerte y **NO SOPORTADA**.
- **Propósito:** “uses … to access” (p039) vincula uso, instrumento y acceso; no garantiza de forma separada que todo intento de acceso tenga éxito.
- **Coordinación:** “detect and block” (p039) comparte el mismo `may`; la lista de acciones correctivas (p040) está bajo un único `may include`.
- **Alternativa:** “missing patches, weak access controls, **or** insufficient monitoring” (p040) debe conservar el grupo disyuntivo; no afirma que las tres carencias existan.
- **Alcance ilustrativo:** ambos párrafos son escenarios. Generalizar sus relaciones como leyes universales sería **NO SOPORTADO**.

### Ambigüedades

- **ENTRAÑADO por continuidad definida:** “the phishing email”, “the employee”, “the malicious link”, “the submitted password”, “the compromised credential” (p039) y “the file server” (p040) retoman menciones anteriores.
- **PLAUSIBLE, no entrañado:** `Attacker = ThreatActor` (p039). Mantenerlos separados con candidato de correferencia es correcto; fusionarlos sin marca no está soportado.
- **PLAUSIBLE, no entrañado:** `CompromisedAccount = CloudAccount`, `UnauthorizedAccess = acceso del atacante` y `SuspiciousLoginActivity = ese acceso` (p039).
- **Ambigüedad real:** “The event” (p040) puede retomar el cifrado, la indisponibilidad o el episodio compuesto. Elegir un único antecedente es **NO SOPORTADO**.
- **PLAUSIBLE, no entrañado:** `Malware = ransomware`, `malware activity = encrypting files`, `affected systems` incluye el servidor y `encrypted files` retoma los archivos anteriores (p040).
- No se observan contradicciones internas. Una atribución del escenario de ransomware al “phishing scenario” sí sería **CONTRADICHA** por los sujetos literales de p039 y p040.

## 2. Resultado por etapa

Escala: 0 = ausente/incorrecto; 4 = completo y fiel. No hay etapa N/A: el sidecar del paso 11 está configurado.

| Paso | Etapa | Fidelidad | Cobertura | Precisión | Trazabilidad | Coherencia | Estado |
|---:|---|---:|---:|---:|---:|---:|---|
| 01 | input_intake | 4 | 4 | 4 | 4 | 4 | OK |
| 02 | preprocessing | 4 | 4 | 4 | 4 | 4 | OK |
| 03 | sentence_segmentation | 4 | 4 | 4 | 4 | 4 | OK |
| 04 | tokenization | 4 | 4 | 4 | 4 | 4 | OK |
| 05 | linguistic_annotation | 3 | 4 | 3 | 4 | 4 | WARN |
| 06 | entity_extraction | 4 | 4 | 4 | 4 | 4 | OK |
| 07 | concept_extraction | 3 | 3 | 3 | 4 | 3 | WARN |
| 08 | coreference_resolution | 1 | 0 | 4 | 0 | 4 | FAIL |
| 09 | relation_extraction | 2 | 2 | 2 | 4 | 3 | FAIL |
| 10 | canonical_claims / semantic_claims | 4 | 4 | 4 | 4 | 4 | OK |
| 11 | semantic_debug_ir | 4 | 4 | 4 | 4 | 4 | OK |
| 12 | triple_extraction | 4 | 4 | 4 | 4 | 4 | OK |
| 13 | taxonomy_induction | 4 | 4 | 4 | 4 | 4 | OK |
| 14 | type_assertion | 4 | 4 | 4 | 4 | 4 | OK |
| 15 | semantic_quality | 3 | 3 | 4 | 4 | 3 | WARN |
| 16 | output_generation | 3 | 4 | 3 | 3 | 2 | WARN |

La precisión 4 del paso 08 significa únicamente que el array vacío no introduce fusiones falsas; no compensa su cobertura nula.

## 3. Hallazgos

### Q-infosec_p039_p040-05-1

- **Severidad:** baja
- **Tipo:** anotación lingüística
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** p039, “Email filtering may detect and block the phishing email.”
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p039_p040/artifacts/pipeline_outputs/observed_p039_p040_05_linguistic_annotation.json`, `/tokens/97/pos` y `/tokens/97/lemma`.
- **Evaluación razonada:** “phishing” aparece como `VERB`, tag `VBG` y lema `phishe`, aunque funciona como modificador de “email”. La dependencia `amod` conserva parte de la estructura, por lo que el daño es acotado.
- **Impacto downstream:** puede degradar la normalización de conceptos. En este caso el sintagma “phishing email” se recupera después; no se vuelve a contabilizar como error nuevo.

### Q-infosec_p039_p040-07-1

- **Severidad:** media
- **Tipo:** ruido y solapamiento conceptual
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** p039, “may reduce the likelihood of clicking the malicious link.”
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p039_p040/artifacts/pipeline_outputs/observed_p039_p040_07_concept_extraction.json`, `/concepts/21` y `/concepts/22`.
- **Evaluación razonada:** se propone el fragmento incompleto “likelihood of” como concepto y, además, el sintagma completo. La primera propuesta absorbe una preposición sin su complemento y no es un concepto autónomo fiel. También aparece “unavailable” como `noun_chunk` en `/concepts/37`, pese a ser el estado predicativo de p040.
- **Impacto downstream:** el paso 09 selecciona el concepto incompleto y reduce el objeto a “likelihood”; el paso 10 lo corrige como `MaliciousLinkClickingLikelihood`.

### Q-infosec_p039_p040-07-2

- **Severidad:** media
- **Tipo:** identidad de menciones
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** p039, “an employee” / “The employee”; p040, “a file server” / “The file server”.
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p039_p040/artifacts/pipeline_outputs/observed_p039_p040_07_concept_extraction.json`, `/concepts/7/concept_id`, `/concepts/10/concept_id`, `/concepts/35/concept_id` y `/concepts/36/concept_id`.
- **Evaluación razonada:** las menciones normalizadas idénticamente como `employee` y `file server` reciben IDs distintos, mientras otras repeticiones sí comparten ID. La diferencia del determinante no justifica fragmentar el participante discursivo.
- **Impacto downstream:** exige reparación en correferencia; como el paso 08 queda vacío, la fragmentación persiste en la ruta de relaciones observadas, aunque las claims canónicas la corrigen.

### Q-infosec_p039_p040-08-1

- **Severidad:** alta
- **Tipo:** cobertura de correferencia
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** p039, “A threat actor sends a phishing email…” / “The phishing email contains…”; p040, “a file server” / “The file server becomes unavailable…”.
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p039_p040/artifacts/pipeline_outputs/observed_p039_p040_08_coreference_resolution.json`, `/coreferences`.
- **Evaluación razonada:** el array vacío evita fusiones arriesgadas —por ejemplo, atacante/actor de amenaza o cuenta comprometida/cuenta cloud—, pero también omite retomadas definidas de alta confianza: correo, empleado, enlace, contraseña/credencial y servidor. El conservadurismo es correcto para antecedentes ambiguos, no para todas las repeticiones literales.
- **Impacto downstream:** no existe una capa explícita y trazable de identidad discursiva para el paso 09. El paso 10 repara varias identidades, por lo que este error no llega como falsedad al output final.

### Q-infosec_p039_p040-09-1

- **Severidad:** alta
- **Tipo:** pérdida de modalidad, coordinación y complementos
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** p040, “The event affects availability and **may affect** integrity”; p039, “Email filtering **may detect and block** the phishing email.”
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p039_p040/artifacts/pipeline_outputs/observed_p039_p040_09_relation_extraction.json`, `/relations/1`, `/relations/3`, `/relations/5`, `/relations/11` y `/relations/16`.
- **Evaluación razonada:** las relaciones usan predicados no modales (`affect`, `prevent`, `identify`, `block`, `reduce`) con confianza 0.9 y sin campo `modality`; esto vuelve categóricas posibilidades del texto. Además, se pierde `detect` en la coordinación del filtrado, “insufficient monitoring” en la alternativa, “improved detection rules” en la inclusión y el complemento “of the ransomware” al reducir el objeto a `spread`.
- **Impacto downstream:** sería una degradación grave si se proyectara directamente. El paso 10 repone `may`, grupos coordinados/disyuntivos y complementos; por ello se clasifica después como ERROR_CORREGIDO, no como propagado a RDF.

### Q-infosec_p039_p040-09-2

- **Severidad:** alta
- **Tipo:** precisión semántica y alcance de escenario
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** p040, “A **ransomware scenario** illustrates the importance…”; p039 habla de “A **phishing scenario**…”.
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p039_p040/artifacts/pipeline_outputs/observed_p039_p040_09_relation_extraction.json`, `/relations/17/subject_ref` y `/relations/17/sentence_id`.
- **Evaluación razonada:** la relación respaldada por la oración de p040 usa `con-15249cc0617055ef`, ID del concepto `phishing scenario`, en vez del `ransomware scenario` de esa oración. La interpretación “el escenario de phishing ilustra la importancia de backups” está **CONTRADICHA** por el sujeto literal de p040.
- **Impacto downstream:** mezcla los dos párrafos y sería el principal contenido no soportado. El paso 10 lo reemplaza por tres claims cuyo sujeto es `RansomwareScenario`; no llega al modelo final.

### Q-infosec_p039_p040-10-1

- **Severidad:** informativa/positiva
- **Tipo:** reparación semántica
- **Atribución:** ERROR_CORREGIDO
- **Cita literal:** p039, “Multi-factor authentication may prevent…”; p040, “A ransomware scenario illustrates…” y “may identify … or …”.
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p039_p040/artifacts/pipeline_outputs/observed_p039_p040_10_canonical_claims.json`, `/canonical_claims/claims/14`, `/canonical_claims/claims/20`, `/canonical_claims/claims/33` y `/canonical_claims/claims/36`.
- **Evaluación razonada:** las claims reponen modalidad, propósito, ubicación, estado, coordinación, disyunción y alcance ilustrativo. También mantienen como `unresolved` las correferencias realmente ambiguas y corrigen el sujeto erróneo del escenario de p040.
- **Impacto downstream:** permite que los 39 claims tengan triple y disposición final sin heredar las falsedades de los pasos 08–09.

### Q-infosec_p039_p040-15-1

- **Severidad:** media
- **Tipo:** cobertura del diagnóstico de calidad
- **Atribución:** ERROR_PROPAGADO
- **Cita literal:** p039, “the likelihood of clicking the malicious link”; p040, “becomes unavailable”.
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p039_p040/artifacts/pipeline_outputs/observed_p039_p040_15_semantic_quality.json`, `/semantic_quality_report/concept_noise` y `/semantic_quality_report/warnings`.
- **Evaluación razonada:** se detecta correctamente `importance of backups` como concepto que absorbió parte del predicado, pero no se reportan el fragmento `likelihood of`, el solapamiento con el sintagma completo ni el estado `unavailable` etiquetado como concepto nominal. No es un error semántico nuevo: es cobertura incompleta sobre el ruido originado en el paso 07.
- **Impacto downstream:** el informe subestima el ruido conceptual. Aun así, las claims y triples ya están corregidos, por lo que el defecto afecta más a auditabilidad que al contenido final.

### Q-infosec_p039_p040-16-1

- **Severidad:** media
- **Tipo:** duplicación estructural del modelo final
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** p039, “Multi-factor authentication may prevent unauthorized access.”
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p039_p040/artifacts/pipeline_outputs/observed_p039_p040_16_output_generation.json`, `/output/graph/scoped_relations/7`, `/output/graph/object_property_schema/16/scoped_pairs/0` y `/output/graph/schema/object_properties/16/scoped_pairs/0`.
- **Evaluación razonada:** el mismo par modal aparece como relación scoped y vuelve a resumirse en dos vistas paralelas de schema. Las dos colecciones de propiedades contienen 25 entradas semánticamente redundantes. No duplica hechos dentro de `facts`, pero sí multiplica representaciones del mismo contenido en el modelo entregado.
- **Impacto downstream:** consumidores que no distingan relación observada, resumen de pares y vista de schema pueden contar varias veces la misma evidencia o interpretar un ejemplo como restricción de esquema. El marcado `illustrative_example` limita la generalización, pero no elimina la redundancia.

## 4. Diagnóstico

- **Primera degradación:** paso 05, con errores menores de POS/lema. La primera degradación semántica estructural aparece en el paso 07 y la primera pérdida grave en el paso 08.
- **Principal pérdida:** el paso 09 elimina modalidad, coordinación y complementos de varias proposiciones. Es la pérdida intermedia más importante, aunque el paso 10 la corrige.
- **Principal contenido no soportado:** en `/relations/17`, el `phishing scenario` queda como sujeto de la importancia de backups, monitorización y respuesta de p040. Está contradicho por “A ransomware scenario…”.
- **Errores que llegan a RDF/OWL:** no llega ninguna falsedad proposicional identificada en el paso 09. Sí llega una duplicación estructural de relaciones scoped en dos vistas de schema, con riesgo de lectura como generalización. Los hechos materializados carecen de `claim_id` propio, aunque conservan evidencia literal y pueden rastrearse mediante `projection.claim_dispositions`.
- **Aciertos:** texto y offsets intactos; 21 oraciones correctamente segmentadas; tokenización completa; ausencia prudente de taxonomías y tipos; 39 claims fieles y trazados; modalidad, propósito, ubicación, estado, coordinación, disyunción y ambigüedad preservados desde el paso 10; los 39 claims tienen representación final exactamente en una disposición principal —12 hechos, 24 relaciones scoped y 3 alternativas—; no se fusionan atacante/actor, cuenta comprometida/cuenta cloud ni los candidatos de “event”.
- **Incertidumbres:** siguen abiertas, correctamente, las identidades `Attacker/ThreatActor`, `CompromisedAccount/CloudAccount`, el antecedente de `Event`, `Malware/Ransomware`, `MalwareActivity/MalwareEncryptingFiles` y `AffectedSystem/FileServer`. Resolverlas categóricamente añadiría conocimiento no presente.

## 5. Veredicto

- **Calidad global:** **88/100**.
- **Output final:** **parcialmente fiel**. La cobertura proposicional y el tratamiento de modalidad/ambigüedad son altos y no se observa invención factual final; no alcanza “fiel” por la duplicación estructural de la proyección RDF y la pérdida de trazabilidad directa en los hechos materializados.
- **Tres correcciones prioritarias:**
  1. Resolver en el paso 08 las retomadas definidas de alta confianza, manteniendo explícitamente `unresolved` las ambiguas.
  2. Hacer que el paso 09 conserve `may`, coordinación, disyunción, complementos y el concepto sujeto de la propia oración, sin depender de la reparación del paso 10.
  3. Emitir en el paso 16 una sola representación autoritativa de cada relación scoped; evitar duplicar `object_property_schema` y `schema.object_properties`, y conservar `claim_id`/origen directamente en cada hecho.

Siguiente caso pendiente: infosec_p041_p042.
