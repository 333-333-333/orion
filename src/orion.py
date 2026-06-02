from __future__ import annotations

import importlib
from dataclasses import dataclass
from typing import Any

from observability import JsonlFileLogSink, LogEvent, LogSink, NullLogSink
from pipeline.step_013_output_generation.namespace import validate_and_resolve_prefixes, validate_base_iri
from pipeline.step_007_concept_extraction import extract_concepts_from_payload
from pipeline.step_006_entity_extraction import extract_entities_from_doc
from pipeline.step_001_input_intake import OrionError, process_input_intake
from pipeline.step_008_coreference_resolution import resolve_coreferences_from_payload
from pipeline.step_008_relation_extraction import extract_relations_from_payload
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


@dataclass(frozen=True)
class ORIONConfig:
    spacy_model: str = _BR_DEFAULT_SPACY_MODEL
    output_strategy: str = 'rdf'
    base_iri: str = _BR_DEFAULT_BASE_IRI
    prefixes: dict[str, str] | None = None

    def __init__(
        self,
        spacy_model: str | None = None,
        output_strategy: str | None = None,
        base_iri: str | None = None,
        prefixes: dict[str, str] | None = None,
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

    @classmethod
    def from_mapping(cls, config: dict[str, Any]) -> "ORIONConfig":
        if not isinstance(config, dict):
            raise OrionError("ORION config error: config must be a dict")
        return cls(
            spacy_model=config.get("spacy_model"),
            output_strategy=config.get("output_strategy"),
            base_iri=config.get('base_iri'),
            prefixes=config.get('prefixes'),
        )


class ORION:
    def __init__(self, config: dict[str, Any] | None = None, log_sink: LogSink | None = None) -> None:
        active_sink = self._resolve_sink(config=config if isinstance(config, dict) else None, log_sink=log_sink)
        if not isinstance(active_sink, JsonlFileLogSink):
            active_sink.emit(LogEvent(phase="orion_initialization", event_type="started", status="started", metadata={"safe": True}))
        try:
            if config is None or not isinstance(config, dict):
                raise ValueError("config must be a dict")
            self.config = config
            self._orion_config = ORIONConfig.from_mapping(config)
            self._log_sink = active_sink
            self._nlp_model: Any | None = None
            if not isinstance(active_sink, JsonlFileLogSink):
                active_sink.emit(LogEvent(phase="orion_initialization", event_type="completed", status="completed", metadata={"safe": True}))
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
        self._log_sink.emit(LogEvent(phase="input_intake", event_type="started", status="started", metadata={"safe": True}))

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
                phase="triple_extraction",
                event_type="started",
                status="started",
                source_context_id=relation_result.get("source_text_id"),
                metadata={"safe": True},
            )
        )

        try:
            triple_result = self._run_triple_extraction(relation_result)
        except Exception as exc:
            self._log_sink.emit(
                LogEvent(
                    phase="triple_extraction",
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
        return {k: v for k, v in output_result.items() if not k.startswith("_spacy")}


__all__ = ["ORION", "ORIONConfig"]
