# Consolidated semantic corrections

## Audit baseline

- 22/22 cases independently audited.
- Initial/latest baseline: 2 cases at or above 80; 20 below target.
- Full ranking: [`scoreboard.md`](scoreboard.md).
- First remediation target: `infosec_p027_p028` (42/100 baseline).

## Cross-case root causes

The reports repeatedly identify four systemic failure families:

1. **Nominal components promoted to predicates**: words such as `awareness`, `process`, `campaigns`, `metrics`, and `exercises` replaced the explicit finite verb.
2. **Scope flattened into SPO**: modality, disjunction, condition, temporal scope, location, and instructional content were either lost or materialized as unconditional facts.
3. **Propositions promoted to classes**: clauses such as `TeachUser`, `MeasureUserResponse`, and `Occurrence` appeared as ontology resources.
4. **Observed text strengthened into OWL axioms**: relations were duplicated as facts, global property signatures, and existential restrictions even when the text did not license those commitments.

## Consolidated implementation changes

### Canonical claims

- Added source-faithful handling for instructional constructions (`educates/teaches ... about/to ...`).
- Preserved compound subjects such as `SecurityAwarenessTraining`, `DataHandlingAwareness`, `AwarenessCampaign`, `TrainingCompletionMetric`, and `SimulatedPhishingExercise`.
- Decomposed taught actions into scoped claims linked to their teaching context.
- Preserved coordinated actions and objects, including classify/store/transmit/dispose, create/protect, and device/network alternatives.
- Added structured topics, manner, location, conditions, and context relations.
- Corrected temporal scope so it qualifies the original event instead of creating false `Candidate applies_before Employment`-style relations.
- Replaced the invented `Occurrence` resource with `Likelihood has_probability_of RiskScenario`, retaining `occurs` as event metadata.

### Linguistic and concept processing

- Added repairs for coordinated gerunds and unmatched `cannot` modal tokens.
- Corrected recurring nominal compounds and `expected behavior` adjective attachment.
- Prevented coordinated predicates from becoming concepts.
- Improved relation extraction precision by removing proximity-based segmented SVO guesses and tightening coordinated-object handling.

### Semantic quality

- Added checks for noncanonical predicates, propositional resources, unstructured disjunction/scope, and missing control mechanisms.
- Added `invalid_projection_claim_ids` so output generation can exclude claims rejected by semantic quality.
- Kept readiness false when integrity issues remain.

### RDF/output projection

- Removed automatic existential restrictions derived only from observed usages.
- Stopped emitting global `rdfs:domain/range` from textual observations.
- Added explicit scoped relation views for modality, conditions, temporal scope, and instructional content.
- Declared properties used only by scoped claims without treating their endpoints as global signatures.
- Added resolvable IRIs for scoped targets, conditions, locations, and temporal resources.

## `infosec_p027_p028` remediation result

The corrected artifacts now preserve:

- explicit predicates (`educates`, `teaches`, `defines`, `reinforces`, `measures`, `reduces`);
- all employee obligations with `must`;
- training topics and taught actions;
- temporal qualification of background checks and employment responsibilities;
- termination condition, safe handling manner, and outside-office location;
- no `awareness/process/campaigns/metrics/exercises/networks/applies_before` pseudo-predicates;
- no automatic OWL restrictions.

Semantic quality reports `1.0`, `rdf_readiness: true`, and no integrity issues. The first independent rescore improved the case from 42 to 78. Residual fixes then replaced the overstrong `intended_for` relation with neutral `related_to`, structured education topics as an IRI list, removed verbal noun-chunk concepts, and propagated scope qualifiers into semantic debug IR. The final independent rescore reached **87/100**, so the case meets the target.

## Final cross-case remediation

The remaining cases were remediated in isolated parallel copies, merged manually, regression-tested, and independently rescored. Reusable corrections now cover:

- deontic, modal, conditional, temporal, purpose, capability, and disjunctive scope without categorical strengthening;
- coordinated subjects, predicates, objects, mechanisms, alternatives, and exact scoped endpoint pairs;
- explicit agents, patients, recipients, beneficiaries, instruments, destinations, locations, channels, lifecycle ownership, and event targets;
- source ambiguities and unresolved discourse references as qualified metadata rather than invented identities or facts;
- separate class, individual, occurrence, anonymous-referent, and unresolved-type-expression representations;
- `instance_of` projection without accidental subclass induction or class/instance IRI conflation;
- evidence-only lexical claims and qualified `rdf:Statement` output for obligations and unresolved interpretations;
- conservative observed/scoped property signatures without global domain/range or existential strengthening;
- claim-to-triple qualifier preservation, semantic role checks, source-connector checks, concept-noise gates, and projection disposition traceability.

Dedicated remediation rule modules were added incrementally for the parallel batches and residual rounds. Focused smoke regressions were added for every remediated case.

## Final validation and scores

- Independent audits completed: **22/22**.
- Cases at or above 80: **22/22**.
- Score range: **80–89**; mean **84.6**; median **85**.
- Final smoke suite: **206 passed, 0 failed**.
- Graphify synchronized after the final implementation.
- Final ranking: [`scoreboard.md`](scoreboard.md).

Notable remediation trajectories include:

- `infosec_p027_p028`: **42 → 87**.
- `infosec_p007_p008`: **43 → 72 → 76 → 81**.
- `infosec_p029_p030`: **43 → 74 → 76 → 81**.
- `infosec_p019_p020`: **44 → 74 → 88**.
- `infosec_p037_p038`: **44 → 74 → 86**.
- `infosec_p011_p012`: **46 → 70 → 84**.
- `infosec_p015_p016`: **58 → 76 → 79 → 89**.
- `infosec_p039_p040`: **54 → 73 → 72 → 88**.
- `infosec_p023_p024`: **61 → 76 → 73 → 78 → 86**.
