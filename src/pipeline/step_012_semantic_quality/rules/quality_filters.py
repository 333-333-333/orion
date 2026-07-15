"""Detect entity, concept, and structural noise in semantic payloads."""

from __future__ import annotations

import re
from typing import Any

_BR_SQ_TECH_ACRONYMS = {"CIA", "API", "RDF", "OWL", "IAM", "MFA", "SAST", "DAST"}
_BR_SQ_GENERIC_SUPERCLASSES = {"type", "thing", "collection", "factor"}
_BR_SQ_LONG_CONCEPT_TEXT_THRESHOLD = 256
_BR_SQ_LONG_TEXT_WARNING_THRESHOLD = 120


def _normalize(value: str | None) -> str:
    """Trim an optional value without changing its case."""
    return (value or "").strip()


def _normalize_casefold(value: str | None) -> str:
    """Normalize casefold."""
    return _normalize(value).casefold()


def _is_long_text(payload: dict[str, Any]) -> bool:
    """Return whether raw input reaches the configured long-text warning threshold."""
    raw_text = payload.get("raw_text")
    if not isinstance(raw_text, str):
        return False
    return len(raw_text.strip()) >= _BR_SQ_LONG_TEXT_WARNING_THRESHOLD


def _has_overlong_concept(payload: dict[str, Any]) -> bool:
    """Return whether any concept reaches the configured overlong-text threshold."""
    for concept in payload.get("concepts", []):
        if not isinstance(concept, dict):
            continue
        concept_text = _normalize(concept.get("text") or concept.get("normalized_text") or concept.get("lemma"))
        if len(concept_text) >= _BR_SQ_LONG_CONCEPT_TEXT_THRESHOLD:
            return True
    return False


def _build_entity_noise(payload: dict[str, Any]) -> tuple[list[dict[str, Any]], list[str]]:
    """Build entity noise."""
    noise: list[dict[str, Any]] = []
    excluded_entities: list[str] = []
    for entity in payload.get("entities", []):
        if not isinstance(entity, dict):
            continue
        label = _normalize(entity.get("label"))
        text = _normalize(entity.get("text"))
        normalized_text = _normalize(entity.get("normalized_text"))
        candidate = text or normalized_text
        if label != "ORG" or not candidate:
            continue
        if candidate.upper() not in _BR_SQ_TECH_ACRONYMS:
            continue
        noise.append({
            "entity_id": entity.get("entity_id"),
            "text": text or normalized_text,
            "normalized_text": normalized_text or _normalize_casefold(text),
            "label": label,
            "reason": "technical_acronym_misclassified_as_org",
        })
        excluded_entities.append(text or normalized_text)
    return noise, list(dict.fromkeys(excluded_entities))


def _build_concept_noise(payload: dict[str, Any]) -> tuple[list[dict[str, Any]], list[str]]:
    """Build concept noise."""
    noise: list[dict[str, Any]] = []
    excluded_concepts: list[str] = []
    tokens = [token for token in payload.get("tokens", []) if isinstance(token, dict)]
    verbal_boundaries = {"acl", "relcl", "advcl", "pcomp", "xcomp"}

    artifact = payload.get("semantic_claims")
    if not isinstance(artifact, dict):
        artifact = payload.get("canonical_claims") if isinstance(payload.get("canonical_claims"), dict) else {}
    claim_patterns_by_sentence: dict[str, list[str]] = {}
    for claim in artifact.get("claims", []):
        if not isinstance(claim, dict):
            continue
        source = claim.get("source") if isinstance(claim.get("source"), dict) else {}
        sentence_id = str(source.get("sentence_id", ""))
        subject = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", str(claim.get("subject", "")))
        predicate = str(claim.get("predicate", "")).replace("_", " ")
        pattern = re.sub(r"[^a-z0-9]+", " ", f"{subject} {predicate}".casefold()).strip()
        if sentence_id and pattern:
            claim_patterns_by_sentence.setdefault(sentence_id, []).append(pattern)
    for concept in payload.get("concepts", []):
        if not isinstance(concept, dict):
            continue
        concept_text = _normalize(concept.get("text"))
        normalized_text = _normalize(concept.get("normalized_text") or concept.get("lemma") or concept.get("text"))
        superclass = _normalize_casefold(concept.get("superclass"))
        start = int(concept.get("start_offset", -1) or -1)
        end = int(concept.get("end_offset", -1) or -1)
        enclosed = sorted(
            [
                token for token in tokens
                if int(token.get("start_offset", -1)) >= start and int(token.get("end_offset", -1)) <= end
            ],
            key=lambda token: int(token.get("start_offset", 0)),
        )
        boundary_tokens = enclosed[:1] + enclosed[-1:] if enclosed else []
        normalized_phrase = re.sub(r"[^a-z0-9]+", " ", normalized_text.casefold()).strip()
        sentence_id = str(concept.get("sentence_id", ""))
        propositional_chunk = any(
            normalized_phrase == pattern or normalized_phrase.startswith(f"{pattern} ")
            for pattern in claim_patterns_by_sentence.get(sentence_id, [])
        )
        if propositional_chunk:
            noise.append({
                "concept_id": concept.get("concept_id"),
                "text": concept_text,
                "normalized_text": normalized_text,
                "reason": "canonical_subject_predicate_chunk_noise",
            })
            excluded_concepts.append(concept_text or normalized_text)

        coordinated_verbal_head = bool(
            len(enclosed) == 1
            and enclosed[0].get("pos") == "NOUN"
            and enclosed[0].get("tag") == "NNS"
            and enclosed[0].get("dependency") in {"relcl", "conj"}
            and any(
                token.get("sentence_id") == enclosed[0].get("sentence_id")
                and token.get("pos") == "VERB"
                and token.get("dependency") == "conj"
                and token.get("head_text") == enclosed[0].get("text")
                for token in tokens
            )
        )
        if coordinated_verbal_head:
            noise.append({
                "concept_id": concept.get("concept_id"),
                "text": concept_text,
                "normalized_text": normalized_text,
                "reason": "coordinated_predicate_misclassified_as_concept",
            })
            excluded_concepts.append(concept_text or normalized_text)

        if any(token.get("pos") == "VERB" and token.get("dependency") in verbal_boundaries for token in boundary_tokens):
            noise.append({
                "concept_id": concept.get("concept_id"),
                "text": concept_text,
                "normalized_text": normalized_text,
                "reason": "verbal_clause_boundary_noise",
            })
            excluded_concepts.append(concept_text or normalized_text)

        if concept_text.startswith("#"):
            noise.append({"concept_id": concept.get("concept_id"), "text": concept_text, "normalized_text": normalized_text, "reason": "header_chunk_noise"})
            excluded_concepts.append(concept_text)

        if len(concept_text or normalized_text) >= _BR_SQ_LONG_CONCEPT_TEXT_THRESHOLD:
            noise.append({"concept_id": concept.get("concept_id"), "text": concept_text, "normalized_text": normalized_text, "reason": "overlong_chunk_noise"})
            excluded_concepts.append(concept_text or normalized_text)

        if superclass in _BR_SQ_GENERIC_SUPERCLASSES:
            noise.append({"concept_id": concept.get("concept_id"), "text": concept_text, "normalized_text": normalized_text, "superclass": superclass, "reason": "generic_superclass_noise"})
            excluded_concepts.append(superclass)
            if normalized_text:
                excluded_concepts.append(normalized_text)

    return noise, list(dict.fromkeys([value for value in excluded_concepts if value]))
