from __future__ import annotations

import importlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from observability import JsonlFileLogSink, LogEvent, LogSink, NullLogSink
from pipeline.step_013_output_generation.namespace import validate_and_resolve_prefixes, validate_base_iri
from pipeline.step_007_concept_extraction import extract_concepts_from_payload
from pipeline.step_006_entity_extraction import extract_entities_from_doc
from pipeline.step_001_input_intake import OrionError, process_input_intake
from pipeline.step_008_coreference_resolution import resolve_coreferences_from_payload
from pipeline.step_008_relation_extraction import extract_relations_from_payload
from pipeline.step_009_canonical_claims import extract_canonical_claims_from_payload
from pipeline.step_009_triple_extraction import extract_triples_from_payload
from pipeline.step_010_taxonomy_induction import extract_taxonomy_relations_from_payload
from pipeline.step_011_type_assertion import extract_type_assertions_from_payload
from pipeline.step_012_semantic_quality import assess_semantic_quality_from_payload
from pipeline.step_013_output_generation import generate_output_from_payload
from pipeline.step_005_linguistic_annotation import annotate_tokens
from pipeline.step_002_preprocessing import preprocess_input
from pipeline.step_003_sentence_segmentation import segment_sentences
from pipeline.step_004_tokenization import tokenize_sentences

_BR_DEFAULT_SPACY_MODEL = "en_core_web_lg"
_BR_DEFAULT_BASE_IRI = 'https://orion.local/resource/'
_BR_SEMANTIC_DEBUG_CONTEXT_PREPOSITIONS = frozenset({'across'})


def _semantic_debug_words(value: str) -> list[str]:
    split = re.sub(r'([a-z])([A-Z])', r'\1 \2', value or '')
    return [token for token in re.sub(r'[^A-Za-z0-9]+', ' ', split).split() if token]


def _semantic_debug_label(value: str) -> str:
    words = _semantic_debug_words(value)
    parts = []
    for word in words:
        parts.append(word if word.isupper() and len(word) <= 4 else word[:1].upper() + word[1:].lower())
    return ''.join(parts)


def _semantic_debug_relation_object(claim: dict[str, Any]) -> tuple[str, dict[str, Any] | None]:
    obj = str(claim.get('object') or '')
    source = claim.get('source') if isinstance(claim.get('source'), dict) else {}
    evidence = str(source.get('evidence') or '').strip()
    predicate = str(claim.get('predicate') or '').replace('_', ' ').strip()
    if not evidence or not predicate:
        return obj, None
    prepositions = '|'.join(sorted(_BR_SEMANTIC_DEBUG_CONTEXT_PREPOSITIONS))
    match = re.search(
        rf'\b{re.escape(predicate)}\b\s+(?P<object>.+?)\s+(?P<preposition>{prepositions})\b(?P<context>.*?)(?:[.;:]|$)',
        evidence,
        flags=re.IGNORECASE,
    )
    if not match:
        return obj, None
    direct_object = _semantic_debug_label(match.group('object'))
    if not direct_object or direct_object == obj:
        return obj, None
    context = {
        'claim_id': claim.get('claim_id'),
        'original_object': obj,
        'accepted_object': direct_object,
        'preposition': match.group('preposition').casefold(),
        'context': match.group('context').strip(' .;:'),
        'source_sentence': evidence,
    }
    return direct_object, context


def _build_semantic_debug_ir(payload: dict[str, Any]) -> dict[str, Any]:
    semantic = payload.get('semantic_claims') if isinstance(payload.get('semantic_claims'), dict) else payload.get('canonical_claims')
    claims = semantic.get('claims', []) if isinstance(semantic, dict) else []
    entities: dict[str, dict[str, Any]] = {}
    relations: list[dict[str, Any]] = []
    contexts: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    claim_items = claims if isinstance(claims, list) else []
    for claim in claim_items:
        if not isinstance(claim, dict) or not claim.get('subject') or not claim.get('predicate') or not claim.get('object'):
            continue
        source = claim.get('source') if isinstance(claim.get('source'), dict) else {}
        evidence = str(source.get('evidence') or '').strip()
        subject = str(claim.get('subject'))
        obj, context = _semantic_debug_relation_object(claim)
        relation = {
            'id': claim.get('claim_id'),
            'subject': subject,
            'predicate': claim.get('predicate'),
            'object': obj,
            'source_sentence': evidence,
            'source': source,
        }
        for key in ('extracted_by', 'behavior', 'derivation', 'source_claim_id'):
            if claim.get(key):
                relation[key] = claim.get(key)
        relations.append(relation)
        for label in (subject, obj):
            entities.setdefault(
                label,
                {
                    'id': label,
                    'label': label,
                    'source_sentence': evidence,
                },
            )
        rejected_compound = str(claim.get('rejected_compound') or '').strip()
        if rejected_compound:
            rejected.append({
                'type': str(claim.get('rejection_reason') or 'rejected_compound'),
                'claim_id': claim.get('claim_id'),
                'compound': rejected_compound,
                'source_sentence': evidence,
            })
        if context is not None:
            contexts.append(context)
            rejected.append({'type': 'prepositional_context_not_entity', **context})
    semantic_rejected = semantic.get('rejected_claims', []) if isinstance(semantic, dict) else []
    if isinstance(semantic_rejected, list):
        rejected.extend(item for item in semantic_rejected if isinstance(item, dict))
    ir: dict[str, Any] = {'entities': list(entities.values()), 'relations': relations}
    if contexts:
        ir['contexts'] = contexts
    if rejected:
        ir['rejected'] = rejected
    return ir



class ORIONResult(dict):
    def __init__(self, payload: dict[str, Any]) -> None:
        super().__init__(payload)
        output = payload.get('output') if isinstance(payload.get('output'), dict) else {}
        graph = output.get('ontology') or output.get('graph') or {}
        self.ontology = graph
        serialized = output.get('serialized')
        if not isinstance(serialized, dict):
            raw = json.dumps(graph, ensure_ascii=False, sort_keys=True)
            serialized = {'ttl': raw, 'rdfxml': raw, 'jsonld': raw, 'nt': raw}
        self.serialized = serialized
        self.deterministic_triples = payload.get('triples') if isinstance(payload.get('triples'), list) else []
        self.inferred_triples = payload.get('inferred_triples') if isinstance(payload.get('inferred_triples'), list) else []

    def __getattr__(self, name: str) -> Any:
        try:
            return self[name]
        except KeyError as exc:
            raise AttributeError(name) from exc

@dataclass(frozen=True)
class ORIONConfig:
    spacy_model: str = _BR_DEFAULT_SPACY_MODEL
    output_strategy: str = 'rdf'
    base_iri: str = _BR_DEFAULT_BASE_IRI
    prefixes: dict[str, str] | None = None
    canonical_claims: dict[str, Any] | None = None
    semantic_claims: dict[str, Any] | None = None
    semantic_debug_ir: dict[str, Any] | None = None

    def __init__(
        self,
        spacy_model: str | None = None,
        output_strategy: str | None = None,
        base_iri: str | None = None,
        prefixes: dict[str, str] | None = None,
        canonical_claims: dict[str, Any] | None = None,
        semantic_claims: dict[str, Any] | None = None,
        semantic_debug_ir: dict[str, Any] | None = None,
    ) -> None:
        resolved_model = _BR_DEFAULT_SPACY_MODEL if spacy_model is None else spacy_model
        if not isinstance(resolved_model, str) or resolved_model.strip() == "":
            raise OrionError("ORION config error: spacy_model must be a non-empty string")

        resolved_output_strategy = 'rdf' if output_strategy is None else output_strategy
        if resolved_output_strategy not in {'rdf', 'owl'}:
            raise OrionError('ORION config error: output_strategy must be one of: rdf, owl')

        try:
            resolved_base_iri = validate_base_iri(_BR_DEFAULT_BASE_IRI if base_iri is None else base_iri)
            resolved_prefixes = validate_and_resolve_prefixes(resolved_base_iri, prefixes)
        except ValueError as exc:
            raise OrionError(f'ORION config error: {exc}') from exc

        object.__setattr__(self, "spacy_model", resolved_model)
        object.__setattr__(self, 'output_strategy', resolved_output_strategy)
        object.__setattr__(self, 'base_iri', resolved_base_iri)
        object.__setattr__(self, 'prefixes', resolved_prefixes)
        object.__setattr__(self, 'canonical_claims', canonical_claims if isinstance(canonical_claims, dict) else {})
        object.__setattr__(self, 'semantic_claims', semantic_claims if isinstance(semantic_claims, dict) else {})
        object.__setattr__(self, 'semantic_debug_ir', semantic_debug_ir if isinstance(semantic_debug_ir, dict) else {})

    @classmethod
    def from_mapping(cls, config: dict[str, Any]) -> "ORIONConfig":
        if not isinstance(config, dict):
            raise OrionError("ORION config error: config must be a dict")
        return cls(
            spacy_model=config.get("spacy_model"),
            output_strategy=config.get("output_strategy"),
            base_iri=config.get('base_iri'),
            prefixes=config.get('prefixes'),
            canonical_claims=config.get('canonical_claims'),
            semantic_claims=config.get('semantic_claims'),
            semantic_debug_ir=config.get('semantic_debug_ir'),
        )


class ORION:
    def __init__(self, config: dict[str, Any] | None = None, log_sink: LogSink | None = None) -> None:
        active_sink = self._resolve_sink(config=config if isinstance(config, dict) else None, log_sink=log_sink)
        if not isinstance(active_sink, JsonlFileLogSink):
            active_sink.emit(
                LogEvent(
                    phase="orion_initialization",
                    event_type="started",
                    status="started",
                    metadata={"safe": True},
                )
            )
        try:
            if config is None or not isinstance(config, dict):
                raise ValueError("config must be a dict")
            self.config = config
            self._orion_config = ORIONConfig.from_mapping(config)
            self._log_sink = active_sink
            self._nlp_model: Any | None = None
            if not isinstance(active_sink, JsonlFileLogSink):
                active_sink.emit(
                    LogEvent(
                        phase="orion_initialization",
                        event_type="completed",
                        status="completed",
                        metadata={"safe": True},
                    )
                )
        except Exception as exc:
            if not isinstance(active_sink, JsonlFileLogSink):
                active_sink.emit(
                    LogEvent(
                        phase="orion_initialization",
                        event_type="failed",
                        status="failed",
                        exception_category=exc.__class__.__name__,
                        metadata={"safe": False},
                    )
                )
            raise

    @staticmethod
    def _resolve_sink(config: dict[str, Any] | None, log_sink: LogSink | None) -> LogSink:
        if log_sink is not None:
            return log_sink
        if isinstance(config, dict):
            candidate = config.get("logging", {}).get("sink")
            if candidate is not None and hasattr(candidate, "emit"):
                return candidate
        return NullLogSink()

    def _run_sentence_segmentation(self, payload: dict[str, Any]) -> dict[str, Any]:
        return segment_sentences(payload)

    def _run_tokenization(self, payload: dict[str, Any]) -> dict[str, Any]:
        return tokenize_sentences(payload)

    def _load_spacy_model(self) -> Any:
        if self._nlp_model is not None:
            return self._nlp_model
        try:
            spacy = importlib.import_module("spacy")
            self._nlp_model = spacy.load(self._orion_config.spacy_model)
            return self._nlp_model
        except Exception as exc:  # BR-LING-002: raise ORION-safe exception
            raise OrionError(
                f"ORION linguistic annotation model load failed for '{self._orion_config.spacy_model}'"
            ) from exc

    def _run_linguistic_annotation(self, payload: dict[str, Any]) -> dict[str, Any]:
        return annotate_tokens(payload, self._load_spacy_model())

    def _run_entity_extraction(self, payload: dict[str, Any]) -> dict[str, Any]:
        doc = getattr(self, "_active_doc", None)
        if doc is None:
            doc = self._load_spacy_model()(payload["preprocessed_text"])
        return extract_entities_from_doc(payload, doc)

    def _run_concept_extraction(self, payload: dict[str, Any]) -> dict[str, Any]:
        doc = getattr(self, "_active_doc", None)
        if doc is None:
            doc = self._load_spacy_model()(payload["preprocessed_text"])
        return extract_concepts_from_payload(payload, doc)

    def _run_coreference_resolution(self, payload: dict[str, Any]) -> dict[str, Any]:
        return resolve_coreferences_from_payload(payload)

    def _run_relation_extraction(self, payload: dict[str, Any]) -> dict[str, Any]:
        return extract_relations_from_payload(payload)

    def _run_canonical_claims(self, payload: dict[str, Any]) -> dict[str, Any]:
        if self._orion_config.semantic_claims:
            stage_config = {**self._orion_config.semantic_claims, 'emit_semantic_claims': True}
        else:
            stage_config = self._orion_config.canonical_claims
        return extract_canonical_claims_from_payload(payload, config=stage_config)

    def _run_semantic_debug_ir(self, payload: dict[str, Any]) -> dict[str, Any]:
        stage_config = self._orion_config.semantic_debug_ir
        raw_path = stage_config.get('artifact_path') or stage_config.get('output_path')
        if raw_path in (None, ''):
            return payload
        path = Path(raw_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        ir = _build_semantic_debug_ir(payload)
        path.write_text(json.dumps(ir, ensure_ascii=False, indent=2, sort_keys=True) + '\n', encoding='utf-8')
        artifacts = payload.get('artifacts') if isinstance(payload.get('artifacts'), dict) else {}
        result = {**payload, 'artifacts': {**artifacts, 'semantic_debug_ir_path': str(path), 'semantic_debug_ir': ir}}
        return result

    def _run_triple_extraction(self, payload: dict[str, Any]) -> dict[str, Any]:
        return extract_triples_from_payload(payload)

    def _run_taxonomy_induction(self, payload: dict[str, Any]) -> dict[str, Any]:
        return extract_taxonomy_relations_from_payload(payload)

    def _run_type_assertion(self, payload: dict[str, Any]) -> dict[str, Any]:
        return extract_type_assertions_from_payload(payload)

    def _run_semantic_quality(self, payload: dict[str, Any]) -> dict[str, Any]:
        return assess_semantic_quality_from_payload(payload)

    def _run_output_generation(self, payload: dict[str, Any]) -> dict[str, Any]:
        return generate_output_from_payload(
            payload,
            self._orion_config.output_strategy,
            base_iri=self._orion_config.base_iri,
            prefixes=self._orion_config.prefixes,
        )

    def process(self, input_data: Any) -> dict[str, Any]:
        self._log_sink.emit(
            LogEvent(
                phase="input_intake",
                event_type="started",
                status="started",
                metadata={"safe": True},
            )
        )

        try:
            intake_result = process_input_intake(input_data=input_data, config=self.config)
        except Exception as exc:
            self._log_sink.emit(
                LogEvent(
                    phase="input_intake",
                    event_type="failed",
                    status="failed",
                    exception_category=exc.__class__.__name__,
                    use_case_id="UC-002",
                    requirement_id="FUN-014",
                    metadata={"safe": False},
                )
            )
            raise

        self._log_sink.emit(
            LogEvent(
                phase="input_intake",
                event_type="completed",
                status="completed",
                source_context_id=intake_result.get("source_text_id"),
                use_case_id="UC-002",
                requirement_id="FUN-014",
                metadata={"safe": True},
            )
        )

        self._log_sink.emit(
            LogEvent(
                phase="preprocessing",
                event_type="started",
                status="started",
                source_context_id=intake_result.get("source_text_id"),
                metadata={"safe": True},
            )
        )

        try:
            preprocessed = preprocess_input(intake_result)
        except Exception as exc:
            self._log_sink.emit(
                LogEvent(
                    phase="preprocessing",
                    event_type="failed",
                    status="failed",
                    exception_category=exc.__class__.__name__,
                    metadata={"safe": False},
                )
            )
            raise

        self._log_sink.emit(
            LogEvent(
                phase="preprocessing",
                event_type="completed",
                status="completed",
                source_context_id=preprocessed.get("source_text_id"),
                metadata={"safe": True},
            )
        )

        self._log_sink.emit(
            LogEvent(
                phase="sentence_segmentation",
                event_type="started",
                status="started",
                source_context_id=preprocessed.get("source_text_id"),
                metadata={"safe": True},
            )
        )

        try:
            sentence_result = self._run_sentence_segmentation(preprocessed)
        except Exception as exc:
            self._log_sink.emit(
                LogEvent(
                    phase="sentence_segmentation",
                    event_type="failed",
                    status="failed",
                    source_context_id=preprocessed.get("source_text_id"),
                    exception_category=exc.__class__.__name__,
                    metadata={"safe": False},
                )
            )
            raise

        self._log_sink.emit(
            LogEvent(
                phase="sentence_segmentation",
                event_type="completed",
                status="completed",
                source_context_id=sentence_result.get("source_text_id"),
                metadata={"safe": True},
            )
        )

        self._log_sink.emit(
            LogEvent(
                phase="tokenization",
                event_type="started",
                status="started",
                source_context_id=sentence_result.get("source_text_id"),
                metadata={"safe": True},
            )
        )

        try:
            tokenized_result = self._run_tokenization(sentence_result)
        except Exception as exc:
            self._log_sink.emit(
                LogEvent(
                    phase="tokenization",
                    event_type="failed",
                    status="failed",
                    source_context_id=sentence_result.get("source_text_id"),
                    exception_category=exc.__class__.__name__,
                    metadata={"safe": False},
                )
            )
            raise

        self._log_sink.emit(
            LogEvent(
                phase="tokenization",
                event_type="completed",
                status="completed",
                source_context_id=tokenized_result.get("source_text_id"),
                metadata={"safe": True},
            )
        )

        self._log_sink.emit(
            LogEvent(
                phase="linguistic_annotation",
                event_type="started",
                status="started",
                source_context_id=tokenized_result.get("source_text_id"),
                metadata={"safe": True},
            )
        )

        try:
            annotated_result = self._run_linguistic_annotation(tokenized_result)
        except Exception as exc:
            self._log_sink.emit(
                LogEvent(
                    phase="linguistic_annotation",
                    event_type="failed",
                    status="failed",
                    source_context_id=tokenized_result.get("source_text_id"),
                    exception_category=exc.__class__.__name__,
                    metadata={"safe": False},
                )
            )
            raise

        self._log_sink.emit(
            LogEvent(
                phase="linguistic_annotation",
                event_type="completed",
                status="completed",
                source_context_id=annotated_result.get("source_text_id"),
                metadata={"safe": True},
            )
        )

        self._log_sink.emit(
            LogEvent(
                phase="entity_extraction",
                event_type="started",
                status="started",
                source_context_id=annotated_result.get("source_text_id"),
                metadata={"safe": True},
            )
        )

        self._active_doc = self._load_spacy_model()(annotated_result["preprocessed_text"])

        try:
            entity_result = self._run_entity_extraction(annotated_result)
        except Exception as exc:
            self._log_sink.emit(
                LogEvent(
                    phase="entity_extraction",
                    event_type="failed",
                    status="failed",
                    source_context_id=annotated_result.get("source_text_id"),
                    exception_category=exc.__class__.__name__,
                    metadata={"safe": False},
                )
            )
            raise

        self._log_sink.emit(
            LogEvent(
                phase="entity_extraction",
                event_type="completed",
                status="completed",
                source_context_id=entity_result.get("source_text_id"),
                metadata={"safe": True},
            )
        )

        self._log_sink.emit(
            LogEvent(
                phase="concept_extraction",
                event_type="started",
                status="started",
                source_context_id=entity_result.get("source_text_id"),
                metadata={"safe": True},
            )
        )

        try:
            concept_result = self._run_concept_extraction(entity_result)
        except Exception as exc:
            self._log_sink.emit(
                LogEvent(
                    phase="concept_extraction",
                    event_type="failed",
                    status="failed",
                    source_context_id=entity_result.get("source_text_id"),
                    exception_category=exc.__class__.__name__,
                    metadata={"safe": False},
                )
            )
            raise

        self._log_sink.emit(
            LogEvent(
                phase="concept_extraction",
                event_type="completed",
                status="completed",
                source_context_id=concept_result.get("source_text_id"),
                metadata={"safe": True},
            )
        )

        self._log_sink.emit(
            LogEvent(
                phase="coreference_resolution",
                event_type="started",
                status="started",
                source_context_id=concept_result.get("source_text_id"),
                metadata={"safe": True},
            )
        )

        try:
            coreference_result = self._run_coreference_resolution(concept_result)
        except Exception as exc:
            self._log_sink.emit(
                LogEvent(
                    phase="coreference_resolution",
                    event_type="failed",
                    status="failed",
                    source_context_id=concept_result.get("source_text_id"),
                    exception_category=exc.__class__.__name__,
                    metadata={"safe": False},
                )
            )
            self._active_doc = None
            raise

        self._log_sink.emit(
            LogEvent(
                phase="coreference_resolution",
                event_type="completed",
                status="completed",
                source_context_id=coreference_result.get("source_text_id"),
                metadata={"safe": True},
            )
        )

        self._log_sink.emit(
            LogEvent(
                phase="relation_extraction",
                event_type="started",
                status="started",
                source_context_id=coreference_result.get("source_text_id"),
                metadata={"safe": True},
            )
        )

        try:
            relation_result = self._run_relation_extraction(coreference_result)
        except Exception as exc:
            self._log_sink.emit(
                LogEvent(
                    phase="relation_extraction",
                    event_type="failed",
                    status="failed",
                    source_context_id=coreference_result.get("source_text_id"),
                    exception_category=exc.__class__.__name__,
                    metadata={"safe": False},
                )
            )
            self._active_doc = None
            raise

        self._log_sink.emit(
            LogEvent(
                phase="relation_extraction",
                event_type="completed",
                status="completed",
                source_context_id=relation_result.get("source_text_id"),
                metadata={"safe": True},
            )
        )

        self._log_sink.emit(
            LogEvent(
                phase="canonical_claims",
                event_type="started",
                status="started",
                source_context_id=relation_result.get("source_text_id"),
                metadata={"safe": True},
            )
        )

        try:
            canonical_claims_result = self._run_semantic_debug_ir(self._run_canonical_claims(relation_result))
        except Exception as exc:
            self._log_sink.emit(
                LogEvent(
                    phase="canonical_claims",
                    event_type="failed",
                    status="failed",
                    source_context_id=relation_result.get("source_text_id"),
                    exception_category=exc.__class__.__name__,
                    metadata={"safe": False},
                )
            )
            self._active_doc = None
            raise

        self._log_sink.emit(
            LogEvent(
                phase="canonical_claims",
                event_type="completed",
                status="completed",
                source_context_id=canonical_claims_result.get("source_text_id"),
                metadata={"safe": True},
            )
        )

        self._log_sink.emit(
            LogEvent(
                phase="triple_extraction",
                event_type="started",
                status="started",
                source_context_id=canonical_claims_result.get("source_text_id"),
                metadata={"safe": True},
            )
        )

        try:
            triple_result = self._run_triple_extraction(canonical_claims_result)
        except Exception as exc:
            self._log_sink.emit(
                LogEvent(
                    phase="triple_extraction",
                    event_type="failed",
                    status="failed",
                    source_context_id=canonical_claims_result.get("source_text_id"),
                    exception_category=exc.__class__.__name__,
                    metadata={"safe": False},
                )
            )
            self._active_doc = None
            raise

        self._log_sink.emit(
            LogEvent(
                phase="triple_extraction",
                event_type="completed",
                status="completed",
                source_context_id=triple_result.get("source_text_id"),
                metadata={"safe": True},
            )
        )

        self._log_sink.emit(
            LogEvent(
                phase="taxonomy_induction",
                event_type="started",
                status="started",
                source_context_id=triple_result.get("source_text_id"),
                metadata={"safe": True},
            )
        )

        try:
            taxonomy_result = self._run_taxonomy_induction(triple_result)
        except Exception as exc:
            self._log_sink.emit(
                LogEvent(
                    phase="taxonomy_induction",
                    event_type="failed",
                    status="failed",
                    source_context_id=triple_result.get("source_text_id"),
                    exception_category=exc.__class__.__name__,
                    metadata={"safe": False},
                )
            )
            self._active_doc = None
            raise

        self._log_sink.emit(
            LogEvent(
                phase="taxonomy_induction",
                event_type="completed",
                status="completed",
                source_context_id=taxonomy_result.get("source_text_id"),
                metadata={"safe": True},
            )
        )

        self._log_sink.emit(
            LogEvent(
                phase="type_assertion",
                event_type="started",
                status="started",
                source_context_id=taxonomy_result.get("source_text_id"),
                metadata={"safe": True},
            )
        )

        try:
            type_assertion_result = self._run_type_assertion(taxonomy_result)
        except Exception as exc:
            self._log_sink.emit(
                LogEvent(
                    phase="type_assertion",
                    event_type="failed",
                    status="failed",
                    source_context_id=taxonomy_result.get("source_text_id"),
                    exception_category=exc.__class__.__name__,
                    metadata={"safe": False},
                )
            )
            self._active_doc = None
            raise

        self._log_sink.emit(
            LogEvent(
                phase="type_assertion",
                event_type="completed",
                status="completed",
                source_context_id=type_assertion_result.get("source_text_id"),
                metadata={"safe": True},
            )
        )

        self._log_sink.emit(
            LogEvent(
                phase="semantic_quality",
                event_type="started",
                status="started",
                source_context_id=type_assertion_result.get("source_text_id"),
                metadata={"safe": True},
            )
        )

        try:
            semantic_quality_result = self._run_semantic_quality(type_assertion_result)
        except Exception as exc:
            self._log_sink.emit(
                LogEvent(
                    phase="semantic_quality",
                    event_type="failed",
                    status="failed",
                    source_context_id=type_assertion_result.get("source_text_id"),
                    exception_category=exc.__class__.__name__,
                    metadata={"safe": False},
                )
            )
            self._active_doc = None
            raise

        self._log_sink.emit(
            LogEvent(
                phase="semantic_quality",
                event_type="completed",
                status="completed",
                source_context_id=semantic_quality_result.get("source_text_id"),
                metadata={"safe": True},
            )
        )

        self._log_sink.emit(
            LogEvent(
                phase="output_generation",
                event_type="started",
                status="started",
                source_context_id=semantic_quality_result.get("source_text_id"),
                metadata={"safe": True},
            )
        )

        try:
            output_result = self._run_output_generation(semantic_quality_result)
        except Exception as exc:
            self._log_sink.emit(
                LogEvent(
                    phase="output_generation",
                    event_type="failed",
                    status="failed",
                    source_context_id=semantic_quality_result.get("source_text_id"),
                    exception_category=exc.__class__.__name__,
                    metadata={"safe": False},
                )
            )
            self._active_doc = None
            raise

        self._log_sink.emit(
            LogEvent(
                phase="output_generation",
                event_type="completed",
                status="completed",
                source_context_id=output_result.get("source_text_id"),
                metadata={"safe": True},
            )
        )

        self._active_doc = None
        return ORIONResult({k: v for k, v in output_result.items() if not k.startswith("_spacy")})


__all__ = ["ORION", "ORIONConfig", "ORIONResult"]
