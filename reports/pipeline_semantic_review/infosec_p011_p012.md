# Revisión semántica: infosec_p011_p012

## 1. Lectura independiente

### Resumen

Los párrafos describen, en presente genérico, dos bloques relacionados:

- **p011:** principio de mínimo privilegio, permisos, roles, grupos, asignaciones, revisiones, segregación de funciones y tres clases explícitas de riesgo de acceso.
- **p012:** gestión del ciclo de vida de identidades y acceso, incluidos aprovisionamiento, desaprovisionamiento, modificación, certificación, procesos joiner/mover/leaver y dos sistemas de gestión.

No aparecen personas, cuentas, organizaciones o sistemas con nombre propio. Las menciones como “an identity”, “a user”, “a new employee”, “a person” y “the organization” son genéricas; el texto no permite identificarlas como individuos determinados.

**Escala interpretativa empleada:** EXPLÍCITO = dicho literalmente; ENTRAÑADO = consecuencia lingüística necesaria; PLAUSIBLE = lectura posible pero no obligada; NO SOPORTADO = no se deriva del texto; CONTRADICHO = incompatible con él.

### Conceptos

- **p011:** principle of least privilege, identity, permission, action, resource, duty, role, collection of permissions, user group, collection of identities, common permissions, role assignment, permission review, assigned permissions, segregation of duties, person, incompatible activities, excessive permission, dormant account access, orphaned account access y access risk.
- **p012:** identity and access management, lifecycle, identities, accounts, roles, permissions, credentials, user provisioning, user account, user deprovisioning, access, user, access modification, access certification, joiner process, employee, mover process, person, role, leaver process, organization, identity management system, identity records, access management system, authentication decisions y authorization decisions.
- **Definiciones/composiciones literales:** “A role is a collection of permissions” (p011); “A user group is a collection of identities” (p011); una permission “grants an action over a resource” (p011). Convertir las dos colecciones en relaciones `has_member` es ENTRAÑADO, no una taxonomía explícita.
- **Entidades/instancias explícitas:** hay menciones genéricas de identity, person, user, employee, organization y systems, pero ninguna instancia nombrada. Equiparar `User`, `Employee`, `Person` e `Identity` sería NO SOPORTADO.

### Proposiciones con evidencia

1. **EXPLÍCITO:** el principio exige que una identidad reciba solo los permisos necesarios para sus funciones: “an identity must receive only the permissions required to perform its duties” (p011).
2. **EXPLÍCITO:** “A permission grants an action over a resource” (p011).
3. **EXPLÍCITO:** “A role is a collection of permissions” (p011).
4. **EXPLÍCITO:** “A user group is a collection of identities” (p011).
5. **EXPLÍCITO:** las identidades del grupo “share common permissions” (p011).
6. **EXPLÍCITO:** “A role assignment links a role to an identity” (p011).
7. **EXPLÍCITO:** “A permission review verifies whether assigned permissions remain necessary” (p011). No afirma por sí sola que sigan siendo necesarias.
8. **EXPLÍCITO:** “Segregation of duties prevents one person from controlling incompatible activities” (p011).
9. **EXPLÍCITO:** “Excessive permission is a type of access risk” (p011).
10. **EXPLÍCITO:** “Dormant account access is a type of access risk” (p011).
11. **EXPLÍCITO:** “Orphaned account access is a type of access risk” (p011).
12. **EXPLÍCITO:** “Identity and access management controls the lifecycle of identities, accounts, roles, permissions, and credentials” (p012).
13. **EXPLÍCITO:** “User provisioning creates a new user account” (p012).
14. **EXPLÍCITO, con disyunción:** “User deprovisioning disables or removes access” (p012); no deben materializarse ambas alternativas como una conjunción incondicional.
15. **EXPLÍCITO:** el usuario afectado “no longer requires it”, donde `it` refiere a access (p012).
16. **EXPLÍCITO:** “Access modification changes the permissions assigned to an identity” (p012).
17. **EXPLÍCITO:** “Access certification confirms that access remains appropriate” (p012).
18. **ENTRAÑADO por el verbo confirm:** dentro de esa confirmación, “access remains appropriate” (p012), pero debe conservarse el contexto de certificación.
19. **EXPLÍCITO:** “A joiner process creates access for a new employee” (p012).
20. **EXPLÍCITO:** “A mover process changes access” (p012).
21. **EXPLÍCITO como condición temporal:** “when a person changes role” (p012).
22. **EXPLÍCITO:** “A leaver process removes access” (p012).
23. **EXPLÍCITO como condición temporal:** “when a person leaves the organization” (p012).
24. **EXPLÍCITO:** “The identity management system stores identity records” (p012).
25. **EXPLÍCITO:** “The access management system enforces authentication … decisions” (p012).
26. **EXPLÍCITO:** “The access management system enforces … authorization decisions” (p012).

Lecturas de control:

- **ENTRAÑADO:** `its duties` son las funciones de la identity de la misma oración (p011); `it` es access y `who` es the user (p012); `that` refiere a identities solo en “identities that share…” (p011).
- **PLAUSIBLE:** que `role` en el mover process sea el mismo concepto técnico de role usado en p011; el texto también permite una función laboral (p012).
- **NO SOPORTADO:** que una cuenta pertenezca necesariamente a una identity, que employee sea identity, que ambos sistemas sean subclases de IdentityAndAccessManagement o que existan reglas de remediación “A/A2”.
- **CONTRADICHO:** afirmar sin negación que el usuario todavía requiere access, frente a “no longer requires it” (p012). También es CONTRADICHO por la sintaxis tratar los `that` de “states that” (p011) y “confirms that” (p012) como menciones referenciales.

### Taxonomías explícitas

Solo hay tres relaciones taxonómicas literales, todas en p011:

- ExcessivePermission `subclass_of` AccessRisk: “is a type of access risk”.
- DormantAccountAccess `subclass_of` AccessRisk: “is a type of access risk”.
- OrphanedAccountAccess `subclass_of` AccessRisk: “is a type of access risk”.

No hay taxonomías explícitas para roles, identidades, usuarios, empleados, procesos o sistemas. Las colecciones expresan composición/pertenencia, no `subclass_of`.

### Modalidad

- **Normativa/restrictiva:** `must`, `only` y `required to perform its duties` en p011.
- **Contenido evaluado, no aseverado:** `whether … remain necessary` en p011.
- **Negación temporal:** `no longer requires` en p012.
- **Disyunción:** `disables or removes` en p012.
- **Condición temporal:** las dos cláusulas con `when` en p012.
- **Confirmación:** `confirms that` presenta “access remains appropriate” bajo el contexto de AccessCertification (p012).
- El resto usa presente genérico sin marcas de posibilidad o incertidumbre.

### Ambigüedades

- `role` en “a person changes role” puede ser función laboral o role de acceso; escoger una sola lectura técnica es PLAUSIBLE, no EXPLÍCITO (p012).
- `authentication and authorization decisions` admite una lectura como dos tipos coordinados de decisión o como una categoría coordinada; separarlos en dos proposiciones es razonable, pero debe conservarse `and` (p012).
- `disables or removes access` no especifica exclusividad ni criterio para escoger alternativa (p012).
- `Dormant account access` y `Orphaned account access` son compuestos nominales completos; descomponerlos en relaciones internas entre account y access sería NO SOPORTADO (p011).
- `Identity and access management` funciona gramaticalmente como un sujeto combinado singular; no se afirma que identity management y access management sean dos sujetos independientes (p012).
- `the organization` no identifica una organización concreta (p012).
- Las repeticiones de identity, access, role y permission no garantizan identidad de instancia entre oraciones; tratarlas como conceptos canónicos es PLAUSIBLE, no correferencia de individuos.

## 2. Resultado por etapa

| Paso | Etapa | Fidelidad | Cobertura | Precisión | Trazabilidad | Coherencia | Estado |
|---:|---|---:|---:|---:|---:|---:|---|
| 01 | input_intake | 4 | 4 | 4 | 4 | 4 | OK |
| 02 | preprocessing | 4 | 4 | 4 | 4 | 4 | OK |
| 03 | sentence_segmentation | 4 | 4 | 4 | 4 | 4 | OK |
| 04 | tokenization | 4 | 4 | 4 | 4 | 4 | OK |
| 05 | linguistic_annotation | 3 | 4 | 3 | 4 | 2 | WARN |
| 06 | entity_extraction | 4 | 4 | 4 | 4 | 4 | OK |
| 07 | concept_extraction | 2 | 2 | 2 | 3 | 2 | FAIL |
| 08 | coreference_resolution | 1 | 1 | 2 | 4 | 2 | FAIL |
| 09 | relation_extraction | 1 | 2 | 1 | 2 | 1 | FAIL |
| 10 | canonical_claims / semantic_claims | 4 | 4 | 3 | 4 | 4 | WARN |
| 11 | semantic_debug_ir | 3 | 3 | 4 | 4 | 4 | WARN |
| 12 | triple_extraction | 4 | 4 | 4 | 4 | 4 | OK |
| 13 | taxonomy_induction | 4 | 4 | 4 | 4 | 4 | OK |
| 14 | type_assertion | 4 | 4 | 4 | 4 | 4 | OK |
| 15 | semantic_quality | 2 | 2 | 2 | 4 | 2 | FAIL |
| 16 | output_generation | 3 | 4 | 3 | 3 | 2 | WARN |

## 3. Hallazgos

### Q-infosec_p011_p012-05-1

- **Severidad:** ALTA
- **Tipo:** anotación morfosintáctica incorrecta
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** “The principle of least privilege states that…” (p011) y “The identity management system stores identity records” (p012).
- **Archivo y JSON Pointer:** `observed_p011_p012_05_linguistic_annotation.json`, `/tokens/4`, `/tokens/5`, `/tokens/206`, `/tokens/207`, `/tokens/209`.
- **Evaluación razonada:** `privilege` se etiqueta como VERB/ROOT y `states` como NOUN/dobj, aunque `states` es el predicado. En p012, `stores` queda como NOUN/compound y `records` como ROOT. Las formas y offsets son fieles, pero la estructura sintáctica contradice las proposiciones literales.
- **Impacto downstream:** origina el falso concepto `states`, una relación espuria en 09 y el concepto fusionado “identity management system stores identity records”.

### Q-infosec_p011_p012-07-1

- **Severidad:** ALTA
- **Tipo:** conceptos espurios y fusión proposicional
- **Atribución:** ERROR_AMPLIFICADO
- **Cita literal:** “The principle of least privilege states that…” (p011) y “The identity management system stores identity records” (p012).
- **Archivo y JSON Pointer:** `observed_p011_p012_07_concept_extraction.json`, `/concepts/1` y `/concepts/52`.
- **Evaluación razonada:** se promueve `states` a concepto nominal y se absorbe una proposición completa como un único concepto. La etapa amplifica los errores sintácticos de 05 en vez de mantener candidatos nominales separados.
- **Impacto downstream:** `states` participa en la relación no soportada de 09; la fusión oculta IdentityManagementSystem e IdentityRecord hasta que 10 los reconstruye.

### Q-infosec_p011_p012-07-2

- **Severidad:** ALTA
- **Tipo:** omisión y colisión de identificadores
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** “Excessive permission is a type of access risk” (p011), repetido para dormant y orphaned account access; “A role assignment links a role…” (p011).
- **Archivo y JSON Pointer:** `observed_p011_p012_07_concept_extraction.json`, `/concepts` (ausencia de `access risk`) y `/concepts/8`, `/concepts/14`, `/concepts/47`.
- **Evaluación razonada:** no se emite `access risk` en ninguna de las tres definiciones taxonómicas. Además, el mismo `concept_id` de role se reutiliza para menciones con spans distintos. La canonicalización léxica es admisible, pero usar el mismo identificador como si fuera también identificador de observación rompe la referencia inequívoca al span.
- **Impacto downstream:** 09 produce objetos `type` sin referencia para las taxonomías y referencias cruzadas a ocurrencias equivocadas; 10 corrige ambas pérdidas.

### Q-infosec_p011_p012-08-1

- **Severidad:** ALTA
- **Tipo:** resolución de correferencia falsa y omisión de anáforas reales
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** “states that an identity…” (p011), “perform its duties” (p011), “a user who no longer requires it” (p012) y “confirms that access…” (p012).
- **Archivo y JSON Pointer:** `observed_p011_p012_08_coreference_resolution.json`, `/coreferences/0`, `/coreferences/3` y `/coreferences` (ausencias de `its` e `it`).
- **Evaluación razonada:** los `that` complementantes se resuelven falsamente a `states` y AccessCertification. En cambio, no se resuelven `its → identity` ni `it → access`. Las resoluciones relativas `that → identities` y `who → user` sí son fieles.
- **Impacto downstream:** deja sin normalizar el objeto de `requires` y añade dos enlaces referenciales sin base; los errores falsos no llegan a claims y la anáfora `it` se recupera en 10.

### Q-infosec_p011_p012-09-1

- **Severidad:** CRÍTICA
- **Tipo:** producto cartesiano semántico y referencias de sujeto erróneas
- **Atribución:** ERROR_AMPLIFICADO
- **Cita literal:** “A mover process changes access when a person changes role” y “A leaver process removes access…” (p012).
- **Archivo y JSON Pointer:** `observed_p011_p012_09_relation_extraction.json`, `/relations/1`, `/relations/14`, `/relations/16` y `/relations/17`.
- **Evaluación razonada:** la etapa genera correctamente MoverProcess→changes→Access y Person→changes→Role, pero añade las combinaciones no soportadas MoverProcess→changes→Role y Person→changes→Access. Además, las relaciones de mover/leaver usan como `subject_ref` el concepto de JoinerProcess (`con-ff6…`). Esto amplifica la reutilización incoherente de IDs de 07.
- **Impacto downstream:** una proyección directa de 09 atribuiría conductas a actores equivocados. 10 descarta las combinaciones espurias y restaura Joiner/Mover/Leaver como sujetos distintos.

### Q-infosec_p011_p012-09-2

- **Severidad:** CRÍTICA
- **Tipo:** pérdida de negación, disyunción, argumentos y cobertura relacional
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** “disables or removes access for a user who no longer requires it” (p012); “links a role to an identity” (p011); “grants an action over a resource” (p011).
- **Archivo y JSON Pointer:** `observed_p011_p012_09_relation_extraction.json`, `/relations/22`, `/relations/3`, `/relations/18` y `/relations`.
- **Evaluación razonada:** `user require it` elimina `no longer` y queda CONTRADICHO por p012. Solo se extrae `removes`, no la alternativa `disables`; `links` pierde identity y `grants` deja resource fuera del SPO. También faltan las relaciones de PermissionReview, AccessCertification e IdentityManagementSystem. No se penaliza a 08 por esta responsabilidad relacional.
- **Impacto downstream:** 09 por sí sola no conserva alcance lógico ni argumentos ternarios. 10 corrige negación, disyunción, targets y relaciones omitidas.

### Q-infosec_p011_p012-09-3

- **Severidad:** ALTA
- **Tipo:** relación no soportada propagada
- **Atribución:** ERROR_PROPAGADO
- **Cita literal:** “The principle of least privilege states that an identity…” (p011).
- **Archivo y JSON Pointer:** `observed_p011_p012_09_relation_extraction.json`, `/relations/6`.
- **Evaluación razonada:** `principle —privilege→ state` no expresa ninguna proposición del párrafo. Procede del análisis de `privilege` como verbo y `states` como nombre en 05, por lo que no se cuenta como un origen nuevo.
- **Impacto downstream:** no llega a 10, triples ni RDF/OWL; queda corregido por descarte.

### Q-infosec_p011_p012-10-1

- **Severidad:** MEDIA
- **Tipo:** metadato inventado
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** por ejemplo, “A role is a collection of permissions” (p011) y “User provisioning creates a new user account” (p012); ninguno menciona remediación.
- **Archivo y JSON Pointer:** `observed_p011_p012_10_canonical_claims.json`, `/canonical_claims/claims/0/remediation_rule` y `/canonical_claims/claims`.
- **Evaluación razonada:** los 24 claims incorporan `remediation_rule: A` o `A2`, categorías NO SOPORTADAS por p011/p012. El resto de cada claim puede ser fiel, pero la cita completa no justifica ese metadato.
- **Impacto downstream:** es el principal contenido inventado de los claims. Se elimina en 11, 12 y 16, por lo que no contamina el RDF final.

### Q-infosec_p011_p012-10-2

- **Severidad:** INFO
- **Tipo:** recuperación semántica
- **Atribución:** ERROR_CORREGIDO
- **Cita literal:** “must receive only… required to perform its duties” (p011), “disables or removes… no longer requires it” y las cláusulas `when` (p012).
- **Archivo y JSON Pointer:** `observed_p011_p012_10_canonical_claims.json`, `/canonical_claims/claims` y `/semantic_claims/claims`.
- **Evaluación razonada:** los 24 claims recuperan las 20 oraciones, separan coordinaciones útiles y preservan modalidad, negación, disyunción, condiciones, targets, estados y los tres `is_a`. También eliminan la relación espuria y el producto cartesiano de 09.
- **Impacto downstream:** triples, taxonomía y output final se apoyan en esta representación corregida, no en las relaciones defectuosas de 09.

### Q-infosec_p011_p012-11-1

- **Severidad:** BAJA
- **Tipo:** pérdida parcial en IR de depuración
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** “creates a new user account”, “permissions assigned to an identity” y “for a new employee” (p012).
- **Archivo y JSON Pointer:** `observed_p011_p012_11_semantic_debug_ir.json`, `/artifacts/semantic_debug_ir/relations/12`, `/artifacts/semantic_debug_ir/relations/15` y `/artifacts/semantic_debug_ir/relations/18`.
- **Evaluación razonada:** el IR omite los qualifiers `new`, `assigned` y `new → Employee` que sí existen en 10. La evidencia literal permanece, y 12 recupera los campos; la pérdida afecta principalmente la utilidad diagnóstica del sidecar configurado.
- **Impacto downstream:** no se propaga a triples ni al output final.

### Q-infosec_p011_p012-15-1

- **Severidad:** ALTA
- **Tipo:** exclusión falsa y detección incompleta de ruido
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** “Segregation of duties prevents one person…” (p011) y “states that an identity…” (p011).
- **Archivo y JSON Pointer:** `observed_p011_p012_15_semantic_quality.json`, `/excluded_concepts/1`, `/semantic_quality_report/concept_noise` y `/semantic_quality_report/relation_gaps`.
- **Evaluación razonada:** `Segregation of duties` es el sujeto nominal explícito, no un predicado absorbido, por lo que excluirlo como ruido es incorrecto. A la vez, el informe no detecta `states`, las falsas correferencias, las referencias de proceso erróneas ni el producto cartesiano de 09. La detección correcta del concepto proposicional fusionado no compensa esas omisiones.
- **Impacto downstream:** la exclusión no elimina SegregationOfDuties de los claims ni de RDF, pero el informe de calidad ofrece una imagen demasiado favorable e incompleta del payload intermedio.

### Q-infosec_p011_p012-15-2

- **Severidad:** MEDIA
- **Tipo:** incoherencia del diagnóstico de calidad
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** “Access certification confirms that access remains appropriate” (p012), cuya proyección requiere conservar contexto y estado.
- **Archivo y JSON Pointer:** `observed_p011_p012_15_semantic_quality.json`, `/semantic_quality_report/rdf_readiness`, `/semantic_quality_report/quality_score` y `/semantic_quality_report/semantic_integrity_checks`.
- **Evaluación razonada:** declara `rdf_readiness: false`, pero simultáneamente asigna 0.85 y marca todos los checks de integridad como `true`, sin issues ni ambigüedades. Dada la ambigüedad real de role y el ruido de 07–09, esas conclusiones no son internamente consistentes.
- **Impacto downstream:** 16 proyecta RDF pese a la señal de no preparación, sin que el informe delimite qué debe tratarse como incierto.

### Q-infosec_p011_p012-16-1

- **Severidad:** MEDIA
- **Tipo:** tipado ontológico no soportado
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** “access remains appropriate” (p012).
- **Archivo y JSON Pointer:** `observed_p011_p012_16_output_generation.json`, `/output/graph/classes/7` y `/output/graph/facts/9`.
- **Evaluación razonada:** el texto usa `appropriate` como estado/adjetivo, pero el modelo crea `orion:Appropriate` como clase y la usa como objeto de `orion:remains`. La proposición subyacente está conservada y contextualizada, pero su categorización como clase OWL es NO SOPORTADA por el párrafo.
- **Impacto downstream:** es el principal contenido no soportado que sí alcanza el modelo RDF/OWL; puede inducir una ontología de estados como clases sin evidencia textual.

### Q-infosec_p011_p012-16-2

- **Severidad:** MEDIA
- **Tipo:** duplicación estructural y trazabilidad incompleta
- **Atribución:** ERROR_ORIGEN
- **Cita literal:** “Excessive permission is a type of access risk” (p011) y “The identity management system stores identity records” (p012).
- **Archivo y JSON Pointer:** `observed_p011_p012_16_output_generation.json`, `/output/graph/classes`, `/output/graph/schema/classes`, `/output/graph/subclass_facts/0` y `/output/graph/object_property_schema`.
- **Evaluación razonada:** la lista de clases se repite íntegramente bajo `schema.classes`, y la información de propiedades se replica entre facts, `object_property_facts` y schema. Los `subclass_facts` y resúmenes de schema no llevan evidencia ni claim ID directos, aunque la tabla de disposiciones permite una trazabilidad indirecta.
- **Impacto downstream:** no inventa nuevas proposiciones de negocio, pero incumple el requisito de modelo final sin duplicación y debilita la auditoría directa de cada aserción RDF.

### Q-infosec_p011_p012-16-3

- **Severidad:** INFO
- **Tipo:** contención de errores
- **Atribución:** ERROR_CORREGIDO
- **Cita literal:** “A mover process changes access when a person changes role” y “a user who no longer requires it” (p012).
- **Archivo y JSON Pointer:** `observed_p011_p012_16_output_generation.json`, `/output/graph/scoped_relations`, `/output/graph/logical_alternatives` y `/output/graph/projection/claim_dispositions`.
- **Evaluación razonada:** ninguna falsa correferencia, relación `principle—privilege→state`, combinación Person→changes→Access ni afirmación positiva `User requires Access` llega al graph. La disyunción y las condiciones se mantienen como estructuras scoped/evidence-only.
- **Impacto downstream:** evita que los fallos críticos de 08–09 se conviertan en hechos RDF incondicionales.

## 4. Diagnóstico

- **Primera degradación:** paso 05. Los textos, offsets, oraciones y tokens son exactos hasta 04; la primera pérdida semántica aparece al analizar `privilege/states` y `stores/records` con categorías y dependencias incorrectas.
- **Principal pérdida:** paso 09. La extracción relacional pierde negación, disyunción, argumentos y relaciones completas, y además crea combinaciones no soportadas. Es una pérdida grave de esa etapa, aunque 10 la corrige casi por completo.
- **Principal contenido no soportado:** `remediation_rule: A/A2` en los 24 claims de 10. No llega al output final. En RDF/OWL, el principal residuo no soportado es tratar `Appropriate` como clase.
- **Errores que llegan a RDF/OWL:** no llegan las falsas correferencias ni relaciones de 08–09, ni las reglas A/A2. Sí llegan el tipado ontológico discutible de `Appropriate`, la duplicación de vistas de clases/schema y una trazabilidad directa incompleta en subclass/schema summaries. Además, 16 proyecta aunque 15 declaró `rdf_readiness: false`.
- **Aciertos:** intake y normalización sin pérdida; 20 oraciones y 221 tokens trazables; conservadurismo correcto al no inventar entidades nombradas ni instancias; 24 claims y 24 triples con alcance lógico; tres taxonomías exactas; condiciones mover/leaver y disyunción de deprovisioning preservadas; todas las claims quedan contabilizadas en la proyección.
- **Incertidumbres:** sentido de `role` en mover, alcance exacto de la coordinación de authentication/authorization decisions y elección de categorías OWL para estados, procesos y conceptos abstractos. El conservadurismo ante estas ambigüedades no debe penalizarse.

## 5. Veredicto

- **Calidad global:** **84/100**.
- **Output final:** **parcialmente fiel**. Conserva las proposiciones y su alcance mucho mejor que las etapas 07–09 y no propaga sus errores críticos, pero no satisface plenamente “sin pérdida, duplicación o invención” por el tipado de `Appropriate`, la duplicación estructural y la trazabilidad desigual del schema.
- **Tres correcciones prioritarias:**
  1. Corregir la cadena 05–09 para preservar predicados, negación, coordinación, argumentos y condiciones sin productos cartesianos ni referencias cruzadas entre Joiner/Mover/Leaver.
  2. Separar identificador canónico de concepto e identificador de mención; extraer `AccessRisk`, resolver solo referencias reales (`its`, `it`, relativos) y rechazar complementantes como correferencias.
  3. Hacer que 15 y 16 respeten la preparación RDF: eliminar metadatos no sustentados, no excluir `SegregationOfDuties`, evitar clases inferidas para estados ambiguos, deduplicar las vistas del graph y adjuntar claim ID/evidencia a toda aserción de schema/taxonomía.

Siguiente caso pendiente: infosec_p013_p014.
