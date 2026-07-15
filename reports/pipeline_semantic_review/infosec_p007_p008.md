# Revisión semántica: infosec_p007_p008

## 1. Lectura independiente

### Resumen

Los dos párrafos exponen dos temas relacionados, pero distintos:

- **p007:** clasificación de información, niveles de protección, clases de información/datos y propiedades que justifican o caracterizan esas clases.
- **p008:** control de acceso, identidad, procesos de identificación/autenticación/autorización, accountability y clases de cuentas.

El texto no presenta personas, organizaciones, sistemas o cuentas concretos. Todos los referentes son **conceptos genéricos o clases**; «the organization» tampoco identifica una organización particular. No hay instancias nombradas.

### Conceptos

- **p007:** Information classification, organization, protection level, kind of information, Information, Public information, Internal information, Confidential information, Restricted information, highly sensitive information, sensitive information, Personal data, Financial data, Authentication data, unauthorized disclosure, harm, access/storage/transmission controls, natural person, payments, accounts, budgets, financial transactions, access y systems.
- **p008:** Access control, resource, condition, Identification, Authentication, Authorization, Accountability, identity, authenticated identity, action, User account, Digital identity, Service account, Non-human account, Application, Script, Integration, Automated process, Privileged account, Account, Permission, Shared account, Individual y Accountability risk.
- **Definiciones explícitas:** las construcciones «is a type of», «is the process of» e «is the ability to» definen o clasifican sus sujetos. «A user account represents a digital identity» es una relación de representación, no una taxonomía.
- **Entidades/instancias explícitas:** ninguna. «organizations», «customers», «employees», «partners», «a natural person», «systems» e «individuals» son categorías o participantes genéricos.

### Proposiciones con evidencia

Todas las proposiciones siguientes son **EXPLÍCITAS**, salvo la descomposición elíptica de los controles, marcada como **ENTRAÑADA**:

1. **[p007]** Information classification ayuda a organizaciones a aplicar niveles apropiados de protección a distintas clases de información: «Information classification helps organizations apply appropriate protection levels to different kinds of information.»
2. **[p007]** Public information es un tipo de Information: «Public information is a type of information».
3. **[p007]** Public information puede divulgarse sin causar daño: «can be disclosed without causing harm».
4. **[p007]** Internal information es un tipo de Information: «Internal information is a type of information».
5. **[p007]** Internal information está destinada a uso dentro de la organización: «intended for use inside the organization».
6. **[p007]** Confidential information es un tipo de Information: «Confidential information is a type of information».
7. **[p007]** La divulgación no autorizada de Confidential information puede dañar, como alternativas coordinadas, a organización, clientes, empleados o socios: «whose unauthorized disclosure may harm the organization, customers, employees, or partners».
8. **[p007]** Restricted information es un tipo de Highly sensitive information: «Restricted information is a type of highly sensitive information».
9. **[p007]** Se requieren controles estrictos de acceso, almacenamiento y transmisión: «requires strict access, storage, and transmission controls». La expansión a **Access control**, **Storage control** y **Transmission control** es **ENTRAÑADA** por coordinación elíptica, no tres sintagmas completos independientes.
10. **[p007]** Personal data es un tipo de Sensitive information: «Personal data is a type of sensitive information».
11. **[p007]** Personal data identifica o puede identificar a una persona natural: «identifies or can identify a natural person».
12. **[p007]** Financial data es un tipo de Sensitive information: «Financial data is a type of sensitive information».
13. **[p007]** Financial data se relaciona, como alternativas coordinadas, con pagos, cuentas, presupuestos o transacciones financieras: «related to payments, accounts, budgets, or financial transactions».
14. **[p007]** Authentication data es un tipo de Restricted information: «Authentication data is a type of restricted information».
15. **[p007]** La razón expresada es que Authentication data puede conceder acceso a sistemas: «because it can grant access to systems».
16. **[p008]** Access control regula quién puede acceder a qué recurso y bajo qué condiciones: «regulates who can access which resource and under which conditions».
17. **[p008]** Identification es el proceso de reclamar una identidad: «Identification is the process of claiming an identity.»
18. **[p008]** Authentication es el proceso de verificar una identidad: «Authentication is the process of verifying an identity.»
19. **[p008]** Authorization es el proceso de determinar qué acciones puede realizar una identidad autenticada: «determining what actions an authenticated identity may perform».
20. **[p008]** Accountability es la capacidad de rastrear acciones hasta una identidad específica: «the ability to trace actions to a specific identity».
21. **[p008]** User account representa una Digital identity: «A user account represents a digital identity.»
22. **[p008]** Service account es un tipo de Non-human account: «A service account is a type of non-human account».
23. **[p008]** Service account es usado, como alternativas coordinadas, por aplicaciones, scripts, integraciones o procesos automatizados: «used by applications, scripts, integrations, or automated processes».
24. **[p008]** Privileged account es un tipo de Account y tiene permisos elevados: «is a type of account with elevated permissions».
25. **[p008]** Shared account es un tipo de Account, es usado por múltiples individuos y crea riesgo de accountability: «is a type of account used by multiple individuals and creates accountability risk».

### Taxonomías explícitas

- **[p007]** PublicInformation → Information; InternalInformation → Information; ConfidentialInformation → Information; RestrictedInformation → HighlySensitiveInformation; PersonalData → SensitiveInformation; FinancialData → SensitiveInformation; AuthenticationData → RestrictedInformation.
- **[p008]** ServiceAccount → NonHumanAccount; PrivilegedAccount → Account; SharedAccount → Account.
- Como clasificaciones definicionales también son explícitas: **[p008]** Identification → Process; Authentication → Process; Authorization → Process; Accountability → Ability.
- No está expresado que HighlySensitiveInformation sea subclase de SensitiveInformation, ni que UserAccount sea subclase de Account.

### Modalidad

- **Posibilidad/capacidad:** «can be disclosed» y «can identify» **[p007]**; «can grant access» **[p007]**; «who can access» **[p008]**.
- **Posibilidad epistémica:** «may harm» **[p007]** y «may perform» **[p008]**. No deben proyectarse como hechos incondicionales.
- **Negación circunstancial:** «without causing harm» **[p007]** niega el daño bajo la condición de divulgación.
- **Necesidad:** «requires strict ... controls» **[p007]**.
- **Finalidad:** «intended for use» **[p007]**.
- **Capacidad definicional:** «ability to trace» **[p008]**.
- **Coordinación:** los «or» preservan alternativas; no autorizan a convertir cada alternativa modal en un hecho incondicional.
- **Ayuda/habilitación:** «helps» **[p007]** no equivale por sí solo a causalidad fuerte.

### Ambigüedades

- **[p007]** En «a type of information that can be disclosed», «that» tiene como antecedente sintáctico inmediato *information*, aunque la lectura definicional pretende caracterizar *Public information*. Extender la propiedad a toda Information es **NO SOPORTADO**.
- **[p007]** En «highly sensitive information that requires...» y «sensitive information that identifies...», la relativa puede adjuntarse al supertipo inmediato; atribuirla a RestrictedInformation/PersonalData es **PLAUSIBLE** y coherente con la función definicional, pero universalizarla a todo el supertipo no es seguro.
- **[p007]** «whose» vincula la divulgación no autorizada con Confidential information; «it» en «because it can grant...» remite a Authentication data. Ambas correferencias son **ENTRAÑADAS** con alta seguridad.
- **[p008]** «who», «which resource» y «which conditions» son variables interrogativas embebidas, no menciones anafóricas. Resolver «who» como Access control es **CONTRADICHO** por los roles de la oración.
- **[p008]** «an identity» en Identification y Authentication no significa *Authenticated identity*. Esa especialización es **NO SOPORTADA**. Solo Authorization menciona explícitamente «an authenticated identity».
- **[p007]** Convertir «accounts» en *Financial account* es **PLAUSIBLE** por el contexto, pero no **EXPLÍCITO**; la forma léxica disponible es *accounts*.
- **[p008]** «Access control accesses a resource» es **CONTRADICHO**: el texto dice que Access control regula el acceso de un actor variable.

## 2. Resultado por etapa

Escala: 0 = ausente/incorrecto; 1 = deficiente; 2 = parcial; 3 = bueno con defectos; 4 = completo y fiel. N/A se usa cuando no existen elementos aplicables.

| Paso | Etapa | Fidelidad | Cobertura | Precisión | Trazabilidad | Coherencia | Estado |
|---:|---|---:|---:|---:|---:|---:|---|
| 01 | input_intake | 4 | 4 | 4 | 4 | 4 | OK |
| 02 | preprocessing | 4 | 4 | 4 | 4 | 4 | OK |
| 03 | sentence_segmentation | 4 | 4 | 4 | 4 | 4 | OK |
| 04 | tokenization | 4 | 4 | 4 | 4 | 4 | OK |
| 05 | linguistic_annotation | 3 | 3 | 3 | 4 | 3 | WARN |
| 06 | entity_extraction | 4 | 4 | 4 | N/A | 4 | OK |
| 07 | concept_extraction | 3 | 3 | 2 | 4 | 3 | WARN |
| 08 | coreference_resolution | 1 | 1 | 1 | 4 | 2 | FAIL |
| 09 | relation_extraction | 1 | 2 | 1 | 3 | 2 | FAIL |
| 10 | canonical_claims / semantic_claims | 3 | 4 | 3 | 4 | 4 | WARN |
| 11 | semantic_debug_ir | 2 | 3 | 2 | 4 | 3 | WARN |
| 12 | triple_extraction | 4 | 4 | 4 | 4 | 4 | OK |
| 13 | taxonomy_induction | 4 | 4 | 4 | 4 | 4 | OK |
| 14 | type_assertion | 4 | 4 | 4 | N/A | 4 | OK |
| 15 | semantic_quality | 1 | 1 | 1 | 3 | 2 | FAIL |
| 16 | output_generation | 3 | 4 | 2 | 4 | 4 | FAIL |

## 3. Hallazgos

### Q-infosec_p007_p008-05-1

- **Severidad:** media
- **Tipo:** alcance de cláusula relativa en anotación lingüística
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** **[p007]** «Public information is a type of information that can be disclosed without causing harm»; **[p007]** «whose unauthorized disclosure may harm...».
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p007_p008/artifacts/pipeline_outputs/observed_p007_p008_05_linguistic_annotation.json`, `/tokens/24/head_text` y `/tokens/54/head_text`.
- **Evaluación razonada:** las relativas quedan encabezadas por `type`, lo que debilita la identificación del referente semántico. La anotación sigue siendo trazable y conserva todos los tokens, pero su estructura no representa de forma segura el alcance de las propiedades definitorias.
- **Impacto downstream:** facilita sujetos sintéticos o demasiado generales en 08–09. La etapa 10 corrige gran parte de esa degradación.

### Q-infosec_p007_p008-07-1

- **Severidad:** media
- **Tipo:** concepto mal formado y ruido pronominal
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** **[p008]** «what actions an authenticated identity may perform»; **[p007]** «because it can grant access to systems».
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p007_p008/artifacts/pipeline_outputs/observed_p007_p008_07_concept_extraction.json`, `/concepts/35/text` y `/concepts/27/text`.
- **Evaluación razonada:** `actions an authenticated identity` fusiona dos participantes distintos; `it` se propone como concepto ontológico en vez de quedar solo como mención por resolver. Existen candidatos correctos separados para Action y AuthenticatedIdentity, por lo que el defecto es de precisión, no una pérdida total.
- **Impacto downstream:** el pronombre pasa como sujeto a una relación en 09; el concepto fusionado vuelve menos fiable la selección de referencias. Ambos defectos son reparados en buena medida por 10.

### Q-infosec_p007_p008-08-1

- **Severidad:** alta
- **Tipo:** correferencia falsa de variables
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** **[p008]** «Access control regulates who can access which resource and under which conditions.»
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p007_p008/artifacts/pipeline_outputs/observed_p007_p008_08_coreference_resolution.json`, `/coreferences/3`, `/coreferences/4` y `/coreferences/5`.
- **Evaluación razonada:** `who` y ambos `which` introducen variables, no remiten a Access control ni a resource. En particular, `who → Access control` invierte el rol regulador y el rol del actor que accede; la interpretación queda **CONTRADICHA** por la oración.
- **Impacto downstream:** 09 amplifica el error como `access control access resource`; 10 lo corrige mediante variables explícitas de actor, recurso y condición.

### Q-infosec_p007_p008-08-2

- **Severidad:** alta
- **Tipo:** omisión y sobreafirmación de correferencias
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** **[p007]** «whose unauthorized disclosure may harm...» y «Authentication data ... because it can grant access to systems.»
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p007_p008/artifacts/pipeline_outputs/observed_p007_p008_08_coreference_resolution.json`, `/coreferences` y `/coreferences/1/antecedent`.
- **Evaluación razonada:** no se registran las dos referencias más seguras, `whose` y `it`. A la vez, se fabrica el antecedente no literal `Restricted sensitive information`. Las relativas ambiguas se resuelven con confianza 0.95 sin conservar la alternativa de alcance.
- **Impacto downstream:** 09 conserva `it` como sujeto y genera sujetos sintéticos; 10 corrige ambos mediante AuthenticationData y RestrictedInformation.

### Q-infosec_p007_p008-09-1

- **Severidad:** alta
- **Tipo:** pérdida de modalidad, calificadores y coordinación
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** **[p007]** «whose unauthorized disclosure may harm the organization, customers, employees, or partners.»
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p007_p008/artifacts/pipeline_outputs/observed_p007_p008_09_relation_extraction.json`, `/relations/12` y `/relations/13`.
- **Evaluación razonada:** las relaciones omiten `may`, reducen `unauthorized disclosure` a `disclosure` y solo cubren Organization y Customer, perdiendo Employee y Partner. El patrón extrae hechos más fuertes y menos completos que la proposición literal.
- **Impacto downstream:** sería una degradación crítica si se proyectara directamente. La etapa 10 la marca como **ERROR_CORREGIDO** al restaurar modalidad, contexto, calificadores y las cuatro alternativas.

### Q-infosec_p007_p008-09-2

- **Severidad:** alta
- **Tipo:** colapso de roles semánticos
- **Atribución:** ERROR_AMPLIFICADO
- **Cita literal:** **[p008]** «Access control regulates who can access which resource and under which conditions»; **[p008]** «A user account represents a digital identity»; **[p008]** «A shared account ... creates accountability risk.»
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p007_p008/artifacts/pipeline_outputs/observed_p007_p008_09_relation_extraction.json`, `/relations/24`, `/relations/15` y `/relations/22`.
- **Evaluación razonada:** se produce `access control access resource`, que está **CONTRADICHO**, y se generalizan UserAccount y SharedAccount al sujeto `account`. La primera relación amplifica Q-08-1; las otras pierden modificadores que delimitan clases distintas.
- **Impacto downstream:** las tres relaciones serían peligrosas como RDF por ampliar dominios. 10 las corrige como AccessControl-regulates-Access, UserAccount-represents-DigitalIdentity y SharedAccount-creates-AccountabilityRisk.

### Q-infosec_p007_p008-10-1

- **Severidad:** alta
- **Tipo:** especialización no soportada
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** **[p008]** «Identification is the process of claiming an identity» y «Authentication is the process of verifying an identity.»
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p007_p008/artifacts/pipeline_outputs/observed_p007_p008_10_canonical_claims.json`, `/artifacts/canonical_claims/claims/27/object` y `/artifacts/canonical_claims/claims/29/object` (duplicado en `/artifacts/semantic_claims/claims/27/object` y `/artifacts/semantic_claims/claims/29/object`).
- **Evaluación razonada:** `Identity` se sustituye por `AuthenticatedIdentity` en dos oraciones que no contienen ese modificador. La mención de AuthenticatedIdentity en la oración posterior sobre Authorization no licencia retroactivamente la especialización. Las dos claims son **NO SOPORTADAS**.
- **Impacto downstream:** el error se propaga fielmente a triples y se materializa y amplifica como hechos y rangos de propiedades en 16.

### Q-infosec_p007_p008-10-2

- **Severidad:** media
- **Tipo:** normalización semántica no literal
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** **[p007]** «related to payments, accounts, budgets, or financial transactions.»
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p007_p008/artifacts/pipeline_outputs/observed_p007_p008_10_canonical_claims.json`, `/artifacts/canonical_claims/claims/20/object` y `/artifacts/canonical_claims/claims/20/source_term`.
- **Evaluación razonada:** la claim usa `FinancialAccount` aunque la fuente solo dice `accounts`; `source_term: Account` deja visible la divergencia. La especialización es **PLAUSIBLE**, pero no **EXPLÍCITA** y debería conservarse como Account o quedar marcada como interpretación.
- **Impacto downstream:** se propaga a una alternativa lógica y al rango de `relatedTo` en 16; no se materializa como hecho simple.

### Q-infosec_p007_p008-11-1

- **Severidad:** media
- **Tipo:** pérdida de metadatos semánticos en IR de depuración
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** **[p007]** «without causing harm» y «requires strict access, storage, and transmission controls»; **[p008]** «with elevated permissions» y «used by multiple individuals».
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p007_p008/artifacts/pipeline_outputs/observed_p007_p008_11_semantic_debug_ir.json`, `/artifacts/semantic_debug_ir/relations/3`, `/artifacts/semantic_debug_ir/relations/12`, `/artifacts/semantic_debug_ir/relations/42` y `/artifacts/semantic_debug_ir/relations/44`.
- **Evaluación razonada:** la proyección de depuración elimina, respectivamente, `polarity: negative`, `strictness: strict`, `qualifier: elevated` y `quantifier: multiple`. Los SPO siguen presentes, pero el IR ya no permite depurar fielmente su alcance.
- **Impacto downstream:** no contamina el output final, que se genera desde semantic claims y recupera esos campos; sí puede inducir un diagnóstico humano equivocado del pipeline.

### Q-infosec_p007_p008-15-1

- **Severidad:** alta
- **Tipo:** certificación de calidad semántica incorrecta
- **Atribución:** ERROR_AMPLIFICADO
- **Cita literal:** **[p008]** «claiming an identity» y «verifying an identity»; **[p007]** «accounts».
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p007_p008/artifacts/pipeline_outputs/observed_p007_p008_15_semantic_quality.json`, `/semantic_quality_report/quality_score`, `/semantic_quality_report/semantic_integrity_issues`, `/semantic_quality_report/warnings` y `/semantic_quality_report/concept_noise`.
- **Evaluación razonada:** se asigna `quality_score: 1.0`, sin advertencias ni ruido, pese a Q-10-1, Q-10-2 y al concepto mal formado de Q-07-1. La etapa no origina esas claims, pero amplifica el riesgo al declararlas íntegramente aptas para RDF.
- **Impacto downstream:** ninguna claim queda excluida; los dos objetos AuthenticatedIdentity alcanzan materialización y esquema en 16.

### Q-infosec_p007_p008-16-1

- **Severidad:** crítica
- **Tipo:** contenido no soportado materializado en RDF/esquema
- **Atribución:** ERROR_AMPLIFICADO (manifestación downstream de Q-10-1; no se cuenta como un error semántico nuevo)
- **Cita literal:** **[p008]** «Identification is the process of claiming an identity» y «Authentication is the process of verifying an identity.»
- **Archivo y JSON Pointer:** `tests/smoke/cases/infosec_p007_p008/artifacts/pipeline_outputs/observed_p007_p008_16_output_generation.json`, `/output/graph/facts/5`, `/output/graph/facts/6`, `/output/graph/object_property_facts/0`, `/output/graph/object_property_facts/11` y `/output/graph/object_property_schema/1`.
- **Evaluación razonada:** el modelo final materializa Identification-claims-AuthenticatedIdentity y Authentication-verifies-AuthenticatedIdentity, y reutiliza AuthenticatedIdentity como rango observado. La trazabilidad cita oraciones que solo dicen `identity`, por lo que la evidencia no sustenta los objetos proyectados.
- **Impacto downstream:** consumidores RDF/OWL reciben dos hechos y restricciones descriptivas más específicos que la fuente. El resto de las 46 claims queda representado sin pérdida relevante mediante hechos, taxonomía, relaciones acotadas o alternativas lógicas; la modalidad y la negación de p007 sí se preservan.

## 4. Diagnóstico

- **Primera degradación:** 05 introduce adjunciones débiles de relativas; la primera degradación semántica inequívoca aparece en 07 con conceptos ruidosos. La primera falla grave es 08, al tratar variables como correferencias y omitir `it`/`whose`.
- **Principal pérdida:** 09 pierde modalidad, coordinación, calificadores y sujetos específicos. No obstante, 10 corrige de forma explícita la mayor parte: restaura listas, variables, clases de cuenta, controles, negación y modalidad.
- **Principal contenido no soportado:** la sustitución de `Identity` por `AuthenticatedIdentity` en las definiciones de Identification y Authentication, originada en 10.
- **Errores que llegan a RDF/OWL:** Q-10-1 llega como dos hechos materializados y como rangos observados; Q-10-2 llega como `FinancialAccount` dentro de una alternativa lógica y del rango acotado de `relatedTo`. Los errores de roles de 08–09 no llegan porque 10 los corrige.
- **Aciertos:** intake, normalización, 17 oraciones, 255 tokens y offsets son fieles; la ausencia de entidades y type assertions es conservadora y correcta; 10 cubre las 17 oraciones y conserva disyunciones/modalidad; 12 proyecta fielmente las 46 claims; 13 recupera exactamente las 14 clasificaciones explícitas sin añadir jerarquías de dominio; 16 conserva negación, modalidad, cuantificadores, strictness, variables y evidencia, y representa las 46 disposiciones sin exclusiones silenciosas.
- **Incertidumbres:** el alcance de las relativas con `that` en p007 es genuinamente ambiguo; no se penaliza una lectura conservadora. `FinancialAccount` es plausible, no contradictorio, pero debe distinguirse de lo explícito. La expansión de «access, storage, and transmission controls» a tres controles es entrañada por elipsis coordinada.

## 5. Veredicto

- **Calidad global:** **81/100**.
- **Output final:** **parcialmente fiel**. Tiene cobertura alta, trazabilidad fuerte y buena conservación de estructura lógica, pero incumple el requisito estricto de ausencia de invención al materializar dos relaciones con AuthenticatedIdentity no sustentadas y al especializar `accounts` sin marcar la interpretación.
- **Tres correcciones prioritarias:**
  1. Conservar `Identity` en las claims de Identification y Authentication; usar `AuthenticatedIdentity` únicamente en Authorization, donde aparece literalmente.
  2. Separar referencias anafóricas de variables (`who`/`which`), resolver `it` y `whose`, y mantener explícita la ambigüedad de las relativas de p007.
  3. Hacer que semantic_quality contraste cada término normalizado con su evidencia antes de RDF, rechace o advierta especializaciones no soportadas y no emita `quality_score: 1.0` mientras existan.

Siguiente caso pendiente: infosec_p009_p010.
