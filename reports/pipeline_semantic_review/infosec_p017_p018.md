# Revisión semántica: infosec_p017_p018

## 1. Lectura independiente

### Resumen

Los dos párrafos son textos definitorios y declarativos sobre dos dominios separados:

- **p017:** seguridad en la nube, recursos, identidades y herramientas de control.
- **p018:** criptografía, mecanismos, procesos, claves y propiedades verificadas o protegidas.

No aparecen nombres propios de organizaciones, personas o productos ni instancias individualizadas. Los sintagmas indefinidos (“a cloud account”, “a virtual machine”, “a cryptographic key”) tienen lectura genérica de clase o concepto. La lectura independiente identifica 19 oraciones y no requiere conocimiento externo.

### Conceptos

- **p017:** Cloud security, cloud service, cloud infrastructure, cloud workload, cloud data, cloud account, administrative boundary, cloud resource, computing resource, cloud environment, virtual machine, container, serverless function, object storage bucket, cloud storage resource, cloud identity, identity, cloud security posture management tool, misconfiguration, cloud access security broker y cloud service usage.
- **p018:** Cryptography, information, mathematical technique, encryption, cryptographic mechanism, confidentiality, decryption, process, encrypted data, readable data, cryptographic key, value, cryptographic algorithm, symmetric encryption, key, asymmetric encryption, public key, private key, digital signature, authenticity, integrity, hash function, fixed-length digest, input data, message authentication code y message integrity.
- **Entidades/instancias explícitas:** ninguna instancia singular identificada; todos los referentes son genéricos. Interpretar “a container” o “a digital signature” como individuo concreto sería **NO SOPORTADO**.
- **Definiciones explícitas:** cloud account como administrative boundary; cloud workload como tipo de computing resource; cloud identity como identity; encryption y digital signature como cryptographic mechanism; decryption como process; cryptographic key como value.

### Proposiciones con evidencia

Todas las proposiciones siguientes son **EXPLÍCITAS** salvo indicación distinta:

1. **p017:** Cloud security protege cloud services. Evidencia: “protects cloud services”.
2. **p017:** Cloud security protege cloud infrastructure. Evidencia: “cloud infrastructure”.
3. **p017:** Cloud security protege cloud workloads. Evidencia: “cloud workloads”.
4. **p017:** Cloud security protege cloud data. Evidencia: “and cloud data”.
5. **p017:** Un cloud account es un administrative boundary cuyo ámbito se expresa con “for cloud resources”. Evidencia: “is an administrative boundary for cloud resources”. Separar la definición de la relación con cloud resources está **ENTRAÑADO** por la estructura, pero el predicado exacto de esa segunda relación no está lexicalizado.
6. **p017:** Cloud workload es un tipo de computing resource. Evidencia: “a type of computing resource”.
7. **p017:** La clase definida queda restringida a recursos “hosted in a cloud environment”. Evidencia: “hosted in a cloud environment”. Atribuir `hosted_in` al cloud workload es **ENTRAÑADO** por la definición relativa.
8. **p017:** Virtual machine es un tipo de cloud workload. Evidencia: “A virtual machine is a type of cloud workload”.
9. **p017:** Container es un tipo de cloud workload. Evidencia: “A container is a type of cloud workload”.
10. **p017:** Serverless function es un tipo de cloud workload. Evidencia: “A serverless function is a type of cloud workload”.
11. **p017:** Object storage bucket es un tipo de cloud storage resource. Evidencia: “is a type of cloud storage resource”.
12. **p017:** Cloud identity es una identity. Evidencia: “is an identity”.
13. **p017:** Cloud identity se usa para acceder a cloud services. Evidencia: “used to access cloud services”; la finalidad debe conservarse.
14. **p017:** Cloud security posture management tool detecta misconfigurations. Evidencia: “detects misconfigurations”.
15. **p017:** La detección/misconfiguración está localizada “in cloud environments”. Evidencia: “misconfigurations in cloud environments”; el punto exacto de adjunción es ambiguo, pero no la presencia de la localización.
16. **p017:** Cloud access security broker monitoriza cloud service usage. Evidencia: “monitors … cloud service usage”.
17. **p017:** Cloud access security broker controla cloud service usage. Evidencia: “and controls cloud service usage”.
18. **p018:** Cryptography protege information. Evidencia: “protects information”.
19. **p018:** Mathematical techniques expresan el medio de esa protección. Evidencia: “through mathematical techniques”. Parafrasearlo como `uses MathematicalTechnique` es **ENTRAÑADO**, siempre que se conserve el rol de medio.
20. **p018:** Encryption es un cryptographic mechanism. Evidencia: “is a cryptographic mechanism”.
21. **p018:** Encryption protege confidentiality. Evidencia: “that protects confidentiality”; atribuir la propiedad al término definido es **ENTRAÑADO** por la construcción definitoria.
22. **p018:** Decryption es un process. Evidencia: “is the process”.
23. **p018:** Decryption convierte encrypted data en readable data. Evidencia: “converts encrypted data back into readable data”. El origen y el destino forman una sola proposición de transformación.
24. **p018:** Cryptographic key es un value. Evidencia: “is a value”.
25. **p018:** Cryptographic key es usado por un cryptographic algorithm. Evidencia: “used by a cryptographic algorithm”.
26. **p018:** Symmetric encryption es un tipo de encryption. Evidencia: “is a type of encryption”.
27. **p018:** Symmetric encryption usa una key para encryption. Evidencia: “uses the same key for encryption”.
28. **p018:** Symmetric encryption usa esa misma key para decryption. Evidencia: “and decryption”. La identidad de la clave entre ambos usos es **EXPLÍCITA** por “the same key”.
29. **p018:** Asymmetric encryption es un tipo de encryption. Evidencia: “is a type of encryption”.
30. **p018:** Asymmetric encryption usa una public key. Evidencia: “uses a public key”.
31. **p018:** Asymmetric encryption usa una private key. Evidencia: “and a private key”.
32. **p018:** Digital signature es un cryptographic mechanism. Evidencia: “is a cryptographic mechanism”.
33. **p018:** Digital signature verifica authenticity. Evidencia: “verifies authenticity”.
34. **p018:** Digital signature verifica integrity. Evidencia: “and integrity”.
35. **p018:** Hash function genera un fixed-length digest a partir de input data. Evidencia: “generates a fixed-length digest from input data”. Parafrasear la procedencia como `uses InputData` es **ENTRAÑADO** solo si se conserva el rol de fuente.
36. **p018:** Message authentication code verifica message integrity. Evidencia: “verifies message integrity”.
37. **p018:** Message authentication code verifica authenticity. Evidencia: “and authenticity”.

Interpretaciones adicionales:

- PublicKey o PrivateKey como subclases de CryptographicKey: **PLAUSIBLE**, pero no afirmado por estos párrafos.
- CloudStorageResource como subclase de CloudResource: **PLAUSIBLE**, no explícito.
- Todo Encryption usa la misma clave o usa necesariamente public/private keys: **NO SOPORTADO**; las cláusulas están restringidas a SymmetricEncryption o AsymmetricEncryption.
- Encryption y Decryption son procesos inversos: **NO SOPORTADO**.
- SymmetricEncryption usa claves diferentes para cifrar y descifrar: **CONTRADICHO** por “the same key”.
- Decryption convierte readable data en encrypted data: **CONTRADICHO** por la dirección “encrypted data … into readable data”.

### Taxonomías explícitas

- **p017:** VirtualMachine ⊑ CloudWorkload; Container ⊑ CloudWorkload; ServerlessFunction ⊑ CloudWorkload; ObjectStorageBucket ⊑ CloudStorageResource; CloudWorkload ⊑ ComputingResource.
- **p017, definiciones copulares con lectura de clase:** CloudAccount ⊑ AdministrativeBoundary; CloudIdentity ⊑ Identity.
- **p018:** SymmetricEncryption ⊑ Encryption; AsymmetricEncryption ⊑ Encryption.
- **p018, definiciones copulares con lectura de clase:** Encryption ⊑ CryptographicMechanism; DigitalSignature ⊑ CryptographicMechanism; Decryption ⊑ Process; CryptographicKey ⊑ Value.
- No se soportan otras aristas taxonómicas por mera semejanza léxica.

### Modalidad

- Predomina el presente declarativo genérico; no hay negación, posibilidad, obligación, recomendación ni marcadores epistémicos.
- **p017:** “used to access” expresa finalidad; “hosted in” y “used” están en voz pasiva; “in cloud environments” expresa localización con adjunción potencialmente ambigua.
- **p018:** “through” expresa medio; “from input data” expresa fuente; “back into” aporta aspecto restitutivo y dirección; “same” impone identidad entre los dos usos de la clave; las coordinaciones con “and” deben distribuirse sin fusionar sus objetos.

### Ambigüedades

- **Correferencias relativas:** en p018 hay cinco “that”. Sus antecedentes sintácticos locales son “cryptographic mechanism”, “process”, “encryption”, “encryption” y “cryptographic mechanism”. En construcciones definitorias, proyectar la propiedad al término definido (Encryption, Decryption, SymmetricEncryption, AsymmetricEncryption, DigitalSignature) es **ENTRAÑADO**; proyectarla a toda la clase genérica del antecedente local sería **NO SOPORTADO**.
- **“same key”:** refiere a una única clave compartida por los usos de encryption y decryption. Dos relaciones independientes con una clase `Key`, sin vínculo de identidad, son semánticamente más débiles.
- **“for cloud resources”:** es un complemento de AdministrativeBoundary. Puede modelarse como ámbito, destino o relación definitoria, pero elegir un predicado más específico sin evidencia sería **PLAUSIBLE**, no explícito.
- **“in cloud environments”:** puede modificar las misconfigurations o el evento de detección. Conservar la localización sin fijar más alcance es correcto y conservador.
- **Genérico frente a instancia:** los artículos indefinidos introducen clases en este texto definitorio; crear individuos concretos sería **NO SOPORTADO**.

## 2. Resultado por etapa

Escala: 0 = ausente/incorrecto; 1 = deficiente; 2 = parcial; 3 = bueno con defectos; 4 = completo y fiel.

| Paso | Etapa | Fidelidad | Cobertura | Precisión | Trazabilidad | Coherencia | Estado |
|---:|---|---:|---:|---:|---:|---:|---|
| 01 | input_intake | 4 | 4 | 4 | 4 | 4 | OK |
| 02 | preprocessing | 4 | 4 | 4 | 4 | 4 | OK |
| 03 | sentence_segmentation | 4 | 4 | 4 | 4 | 4 | OK |
| 04 | tokenization | 4 | 4 | 4 | 4 | 4 | OK |
| 05 | linguistic_annotation | 3 | 4 | 3 | 4 | 3 | WARN |
| 06 | entity_extraction | 4 | 4 | 4 | 4 | 4 | OK |
| 07 | concept_extraction | 3 | 3 | 3 | 4 | 3 | WARN |
| 08 | coreference_resolution | 3 | 4 | 3 | 4 | 4 | WARN |
| 09 | relation_extraction | 2 | 2 | 2 | 4 | 2 | FAIL |
| 10 | canonical_claims / semantic_claims | 4 | 4 | 4 | 4 | 4 | OK |
| 11 | semantic_debug_ir | 4 | 4 | 4 | 4 | 4 | OK |
| 12 | triple_extraction | 4 | 4 | 4 | 4 | 4 | OK |
| 13 | taxonomy_induction | 4 | 4 | 4 | 4 | 4 | OK |
| 14 | type_assertion | 4 | 4 | 4 | 4 | 4 | OK |
| 15 | semantic_quality | 3 | 3 | 3 | 4 | 3 | WARN |
| 16 | output_generation | 3 | 3 | 4 | 3 | 3 | FAIL |

## 3. Hallazgos

### Q-infosec_p017_p018-05-1

- **Severidad:** Media.
- **Tipo:** anotación morfosintáctica incorrecta.
- **Atribución:** **ERROR_ORIGEN** en 05; propagado a 07 y 09, sin contarlo como errores nuevos.
- **Cita literal:** p017, “A cloud access security broker monitors and controls cloud service usage.”
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p017_p018/artifacts/pipeline_outputs/observed_p017_p018_05_linguistic_annotation.json`, `/tokens/112/pos` y `/tokens/112/dependency`; propagación observable en `observed_p017_p018_07_concept_extraction.json`, `/concepts/20`, y en `observed_p017_p018_09_relation_extraction.json`, `/relations`.
- **Evaluación razonada:** `monitors` queda anotado como `NOUN/ROOT`, mientras `broker` se integra como `compound` del supuesto nombre. Esto convierte “cloud access security broker monitors” en un sintagma nominal y elimina el sujeto verbal correcto. La interpretación resultante no es fiel a p017.
- **Impacto downstream:** 07 propone el concepto espurio “cloud access security broker monitors” y 09 omite las relaciones explícitas `monitors` y `controls`. La etapa 10 las reconstruye correctamente, por lo que el error no llega al modelo final.

### Q-infosec_p017_p018-07-1

- **Severidad:** Media.
- **Tipo:** cobertura conceptual incompleta y coordinación fusionada.
- **Atribución:** **ERROR_ORIGEN** en 07, posteriormente **ERROR_CORREGIDO** en 10.
- **Cita literal:** p017, “A cloud workload is a type of computing resource hosted in a cloud environment” y “An object storage bucket is a type of cloud storage resource”; p018, “verifies authenticity and integrity”.
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p017_p018/artifacts/pipeline_outputs/observed_p017_p018_07_concept_extraction.json`, `/concepts` (ausencia de candidatos independientes para `computing resource` y `cloud storage resource`) y `/concepts/43` (fusión “authenticity and integrity”).
- **Evaluación razonada:** la etapa propone numerosos conceptos fieles, pero omite dos objetos taxonómicos explícitos y representa algunas coordinaciones como un único candidato, pese a que las proposiciones distribuyen propiedades sobre elementos separados.
- **Impacto downstream:** 09 produce objetos `type` sin referencia y referencias coordinadas poco precisas. 10 recupera `ComputingResource`, `CloudStorageResource`, `Authenticity` e `Integrity` con evidencia correcta.

### Q-infosec_p017_p018-09-1

- **Severidad:** Alta.
- **Tipo:** pérdida de alcance en cláusulas relativas.
- **Atribución:** **ERROR_AMPLIFICADO** en 09 a partir de una resolución sintáctica local admisible en 08; **ERROR_CORREGIDO** en 10.
- **Cita literal:** p018, “Symmetric encryption is a type of encryption that uses the same key…” y “Asymmetric encryption is a type of encryption that uses a public key and a private key.”
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p017_p018/artifacts/pipeline_outputs/observed_p017_p018_09_relation_extraction.json`, `/relations/0/subject_text`, `/relations/1/subject_text` y `/relations/18/subject_text`.
- **Evaluación razonada:** las tres relaciones usan el sujeto genérico `encryption`. El texto restringe el uso de la misma clave a SymmetricEncryption y el uso de public/private keys a AsymmetricEncryption. Generalizar esas propiedades a todo Encryption es **NO SOPORTADO**.
- **Impacto downstream:** habría producido afirmaciones excesivas en RDF/OWL. 10 sustituye los sujetos por `SymmetricEncryption` y `AsymmetricEncryption`, por lo que la generalización no llega a 12–16.

### Q-infosec_p017_p018-09-2

- **Severidad:** Alta.
- **Tipo:** referencia cruzada semánticamente errónea.
- **Atribución:** **ERROR_ORIGEN** en 09; **ERROR_CORREGIDO** en 10.
- **Cita literal:** p018, “A hash function generates a fixed-length digest from input data.”
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p017_p018/artifacts/pipeline_outputs/observed_p017_p018_09_relation_extraction.json`, `/relations/3/subject_text` y `/relations/3/subject_ref`.
- **Evaluación razonada:** la relación usa `subject_text: "function"` y la referencia `con-e9d7bd17432f605d`, que en 07 identifica `serverless function`, no `hash function`. También degrada “fixed-length digest” a “length digest”.
- **Impacto downstream:** sin corrección, mezclaría los dominios cloud y cryptography. 10 genera `HashFunction generates FixedLengthDigest`, y esa versión fiel es la que llega al triple y al output.

### Q-infosec_p017_p018-10-1

- **Severidad:** Positiva.
- **Tipo:** recuperación semántica trazable.
- **Atribución:** **ERROR_CORREGIDO**.
- **Cita literal:** p017, “A cloud access security broker monitors and controls cloud service usage”; p018, “A hash function generates a fixed-length digest from input data.”
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p017_p018/artifacts/pipeline_outputs/observed_p017_p018_10_canonical_claims.json`, `/canonical_claims/claims/21`, `/canonical_claims/claims/22`, `/canonical_claims/claims/35` y sus equivalentes en `/semantic_claims/claims`.
- **Evaluación razonada:** la etapa 10 no propaga ciegamente los defectos de 05–09: restaura sujetos completos, coordinaciones, objetos taxonómicos, roles de fuente/medio, finalidad, localización y grupos proposicionales. Sus 37 claims corresponden a la lectura independiente y cada uno conserva oración, párrafo y `source_text_id`.
- **Impacto downstream:** 12 y 13 reciben una base semántica sustancialmente corregida; evita que los errores intermedios contaminen la taxonomía y la mayoría del output final.

### Q-infosec_p017_p018-15-1

- **Severidad:** Media.
- **Tipo:** evaluación de calidad sobreconfiada.
- **Atribución:** **ERROR_ORIGEN** en 15.
- **Cita literal:** p017, “A cloud account is an administrative boundary for cloud resources”; p018, “uses the same key for encryption and decryption.”
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p017_p018/artifacts/pipeline_outputs/observed_p017_p018_15_semantic_quality.json`, `/semantic_quality_report/quality_score`, `/semantic_quality_report/rdf_readiness`, `/semantic_quality_report/warnings` y `/semantic_quality_report/semantic_integrity_checks/logical_scope_structured`.
- **Evaluación razonada:** el informe declara `quality_score: 1.0`, `rdf_readiness: true`, alcance lógico completo y cero advertencias. Sin embargo, existen claims con `target`, `location`, `quantifier`, `proposition_group` y roles de medio/fuente cuya materialización RDF necesita una comprobación explícita. La etapa no detecta el riesgo de reducirlos a un SPO simple.
- **Impacto downstream:** 16 materializa todos los claims como si fueran íntegramente proyectables y no alerta de las pérdidas descritas en Q-16-1 y Q-16-2.

### Q-infosec_p017_p018-16-1

- **Severidad:** Alta.
- **Tipo:** pérdida de contenido explícito en el modelo final.
- **Atribución:** **ERROR_ORIGEN** en 16; el riesgo no fue detectado en 15.
- **Cita literal:** p017, “A cloud account is an administrative boundary for cloud resources.”
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p017_p018/artifacts/pipeline_outputs/observed_p017_p018_16_output_generation.json`, `/output/graph/projection/claim_dispositions/15/output_spo`, `/output/graph/subclass_facts/1` y `/output/graph/classes`.
- **Evaluación razonada:** el claim de 10 y el triple de 12 conservaban `target: CloudResource`. El output solo materializa `CloudAccount rdfs:subClassOf AdministrativeBoundary`; `CloudResource` ni siquiera aparece entre las clases. El comentario textual preserva la oración, pero no sustituye una representación semántica de “for cloud resources”.
- **Impacto downstream:** RDF/OWL pierde el ámbito definitorio del cloud account y no permite consultar CloudResource ni su vínculo con AdministrativeBoundary/CloudAccount.

### Q-infosec_p017_p018-16-2

- **Severidad:** Alta.
- **Tipo:** debilitamiento de alcance y relaciones n-arias en la proyección RDF.
- **Atribución:** **ERROR_ORIGEN** en 16, con advertencia omitida en 15.
- **Cita literal:** p018, “converts encrypted data back into readable data” y “uses the same key for encryption and decryption”; p017, “detects misconfigurations in cloud environments.”
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p017_p018/artifacts/pipeline_outputs/observed_p017_p018_16_output_generation.json`, `/output/graph/facts/16`, `/output/graph/facts/18`, `/output/graph/facts/19`, `/output/graph/projection/claim_dispositions/26/output_spo`, `/output/graph/restrictions` y `/output/graph/scoped_relations`.
- **Evaluación razonada:** `target`, `location`, `quantifier` y `proposition_group` sobreviven como metadatos JSON en `facts`, lo cual es un acierto de trazabilidad, pero los `output_spo` materializados no expresan la transformación hacia ReadableData, la localización ni la identidad de la misma Key. `restrictions` y `scoped_relations` están vacíos. Dos hechos sobre la clase `Key` no codifican por sí solos que sea la misma clave.
- **Impacto downstream:** un consumidor RDF/OWL que use los SPO materializados obtiene afirmaciones verdaderas pero más débiles que las proposiciones fuente; se pierde capacidad de inferencia y consulta sobre destino, alcance e identidad.

### Q-infosec_p017_p018-16-3

- **Severidad:** Baja.
- **Tipo:** duplicación estructural de vistas semánticas.
- **Atribución:** **ERROR_ORIGEN** en 16.
- **Cita literal:** p017, “Cloud security protects cloud services…”
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p017_p018/artifacts/pipeline_outputs/observed_p017_p018_16_output_generation.json`, `/output/graph/facts/0`, `/output/graph/object_property_facts/8` y `/output/graph/projection/claim_dispositions/0/output_spo`.
- **Evaluación razonada:** el mismo SPO aparece como hecho, observación de propiedad y disposición de proyección. Parte de la repetición puede funcionar como vista de trazabilidad o esquema observado, pero el modelo no delimita con claridad cuál sección constituye el grafo autoritativo. No introduce contradicción ni contenido nuevo.
- **Impacto downstream:** consumidores ingenuos pueden contar o serializar varias veces el mismo hecho; la coherencia estructural es menor aunque la precisión semántica del SPO sea correcta.

## 4. Diagnóstico

- **Primera degradación:** paso 05. El análisis de “broker monitors” confunde el verbo con un nombre y altera la estructura de sujeto y coordinación.
- **Principal pérdida:** paso 16. `CloudResource` y la relación expresada por “administrative boundary for cloud resources” desaparecen de la estructura semántica materializada; otros alcances n-arios quedan solo como metadatos.
- **Principal contenido no soportado:** en 09 se atribuye al concepto genérico `encryption` el uso de same/public/private keys. Es una generalización **NO SOPORTADA**, pero queda corregida en 10 y no llega al output final. No se observa una invención categórica equivalente en los 37 claims finales.
- **Errores que llegan a RDF/OWL:** pérdida de CloudResource y su vínculo; debilitamiento de `converts … into ReadableData`; localización no materializada; identidad de “same key” no expresada por restricciones; redundancia de representaciones SPO.
- **Aciertos:** intake, normalización, 19 segmentos y 230 tokens son fieles y trazables; 06 no inventa entidades nombradas; 10 recupera las 37 proposiciones con buena evidencia; 12 conserva un triple por claim y sus calificadores; 13 induce exactamente las 13 taxonomías soportadas; 14 evita crear instancias ficticias; 16 materializa todos los claims y no conserva las generalizaciones erróneas de 09.
- **Incertidumbres:** `through` y `from` admiten la paráfrasis `uses` solo con los roles `means_for` y `source_for`; la adjunción de “in cloud environments” no debe sobreespecificarse; el antecedente sintáctico local de “that” no debe confundirse con el sujeto semántico restringido de la definición.

## 5. Veredicto

- **Calidad global:** **86/100**.
- **Output final:** **parcialmente fiel**. Conserva la totalidad de las afirmaciones nucleares y la taxonomía, sin invenciones claras, pero no satisface el criterio estricto de ausencia de pérdida: varios calificadores sobreviven como metadatos y no como semántica RDF/OWL materializada, y CloudResource se pierde por completo.
- **Tres correcciones prioritarias:**
  1. Materializar los calificadores `target`, `location`, `quantifier`, `proposition_group` y roles de fuente/medio mediante relaciones o estructuras RDF consultables; incluir explícitamente CloudResource y el alcance “for cloud resources”.
  2. Corregir la cadena 05–09 para preservar sujeto, coordinación, alcance relativo y referencias conceptuales —en especial broker/monitors, HashFunction y Symmetric/AsymmetricEncryption— sin depender de remediación posterior.
  3. Hacer que 15 compare claim por claim, incluidos calificadores y nodos auxiliares, contra la proyección prevista; emitir warnings ante pérdida o duplicación y no declarar 1.0 cuando el SPO no conserva toda la semántica.

Siguiente caso pendiente: infosec_p019_p020.
