from __future__ import annotations

import hashlib
from typing import Any

_BR_REL_CONFIDENCE_SVO = 0.9
_BR_REL_CONFIDENCE_COPULA = 0.88


def _normalize_text(value: str) -> str:
    return value.casefold().strip()


def _build_relation_id(source_text_id: str, sentence_id: str, subject_text: str, predicate: str, object_text: str) -> str:
    stable_key = f"{source_text_id}|{sentence_id}|{_normalize_text(subject_text)}|{_normalize_text(predicate)}|{_normalize_text(object_text)}".encode("utf-8")
    digest = hashlib.sha256(stable_key).hexdigest()[:16]
    return f"rel-{digest}"


def _make_ref_lookup(input_payload: dict[str, Any]) -> dict[tuple[int, int, str], str]:
    lookup: dict[tuple[int, int, str], str] = {}
    for entity in input_payload.get("entities", []):
        key = (entity.get("start_offset", -1), entity.get("end_offset", -1), _normalize_text(entity.get("text", "")))
        lookup[key] = entity.get("entity_id", "")
    for concept in input_payload.get("concepts", []):
        key = (concept.get("start_offset", -1), concept.get("end_offset", -1), _normalize_text(concept.get("text", "")))
        if key not in lookup:
            lookup[key] = concept.get("concept_id", "")
    return lookup


def _resolve_ref(lookup: dict[tuple[int, int, str], str], text: str, start_offset: int, end_offset: int) -> str:
    direct = lookup.get((start_offset, end_offset, _normalize_text(text)))
    if direct:
        return direct
    for (start, end, norm_text), ref_id in lookup.items():
        if start == start_offset and end == end_offset:
            return ref_id
        if norm_text == _normalize_text(text):
            return ref_id
    return ""




def _make_coref_lookup(input_payload: dict[str, Any]) -> dict[tuple[int, int, str], dict[str, Any]]:
    lookup: dict[tuple[int, int, str], dict[str, Any]] = {}
    for coref in input_payload.get("coreferences", []):
        if coref.get("status") != "resolved":
            continue
        mention = coref.get("mention", "")
        mention_span = coref.get("mention_span", {})
        key = (
            mention_span.get("start_offset", -1),
            mention_span.get("end_offset", -1),
            _normalize_text(mention),
        )
        lookup[key] = coref
    return lookup


def _resolve_subject_from_coreference(subject: dict[str, Any], coref_lookup: dict[tuple[int, int, str], dict[str, Any]]) -> tuple[str, int, int]:
    key = (
        subject.get("start_offset", -1),
        subject.get("end_offset", -1),
        _normalize_text(subject.get("text", "")),
    )
    coref = coref_lookup.get(key)
    if not coref:
        return subject.get("text", ""), subject.get("start_offset", -1), subject.get("end_offset", -1)
    return (
        coref.get("antecedent", subject.get("text", "")),
        coref.get("antecedent_span", {}).get("start_offset", subject.get("start_offset", -1)),
        coref.get("antecedent_span", {}).get("end_offset", subject.get("end_offset", -1)),
    )

def _group_tokens_by_sentence(tokens: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for token in tokens:
        grouped.setdefault(token.get("sentence_id", ""), []).append(token)
    for sentence_id in grouped:
        grouped[sentence_id] = sorted(grouped[sentence_id], key=lambda t: (t.get("start_offset", 0), t.get("end_offset", 0), t.get("token_id", "")))
    return grouped


def _extract_svo_relations(input_payload: dict[str, Any]) -> list[dict[str, Any]]:
    source_text_id = input_payload["source_text_id"]
    tokens = input_payload.get("tokens", [])
    ref_lookup = _make_ref_lookup(input_payload)
    coref_lookup = _make_coref_lookup(input_payload)
    grouped = _group_tokens_by_sentence(tokens)
    relations: list[dict[str, Any]] = []

    for sentence_id, sentence_tokens in grouped.items():
        verbs = [t for t in sentence_tokens if t.get("pos") == "VERB"]
        sentence_start = min((t.get("start_offset", 0) for t in sentence_tokens), default=0)
        sentence_end = max((t.get("end_offset", 0) for t in sentence_tokens), default=0)

        def _subjects_for(verb_token: dict[str, Any]) -> list[dict[str, Any]]:
            verb_text = verb_token.get("text", "")
            direct = [t for t in sentence_tokens if t.get("dependency") in {"nsubj", "nsubjpass"} and t.get("head_text") == verb_text]
            if direct:
                return direct
            if verb_token.get("dependency") == "conj":
                head_text = verb_token.get("head_text", "")
                return [t for t in sentence_tokens if t.get("dependency") in {"nsubj", "nsubjpass"} and t.get("head_text") == head_text]
            return []

        for verb in verbs:
            verb_head = verb.get("text", "")
            subjects = _subjects_for(verb)
            active_subjects = [s for s in subjects if s.get("dependency") == "nsubj"]
            passive_subjects = [s for s in subjects if s.get("dependency") == "nsubjpass"]
            objects = [t for t in sentence_tokens if t.get("dependency") in {"dobj", "obj", "pobj"} and t.get("head_text") == verb_head]

            for subject in active_subjects:
                resolved_subject_text, resolved_subject_start, resolved_subject_end = _resolve_subject_from_coreference(subject, coref_lookup)
                for obj in objects:
                    relations.append(
                        {
                            "relation_id": _build_relation_id(source_text_id, sentence_id, resolved_subject_text, verb.get("lemma", verb.get("text", "")), obj.get("text", "")),
                            "subject_text": resolved_subject_text,
                            "subject_ref": _resolve_ref(ref_lookup, resolved_subject_text, resolved_subject_start, resolved_subject_end),
                            "predicate": verb.get("lemma", verb.get("text", "")),
                            "object_text": obj.get("text", ""),
                            "object_ref": _resolve_ref(ref_lookup, obj.get("text", ""), obj.get("start_offset", -1), obj.get("end_offset", -1)),
                            "sentence_id": sentence_id,
                            "source_text_id": source_text_id,
                            "confidence": _BR_REL_CONFIDENCE_SVO,
                            "evidence_span": {"start_offset": sentence_start, "end_offset": sentence_end},
                            "start_offset": sentence_start,
                            "end_offset": sentence_end,
                        }
                    )

            if passive_subjects:
                agents = [t for t in sentence_tokens if t.get("dependency") == "pobj" and t.get("head_text") == "by"]
                for passive_subject in passive_subjects:
                    for agent in agents:
                        relations.append(
                            {
                                "relation_id": _build_relation_id(source_text_id, sentence_id, agent.get("lemma", agent.get("text", "")), verb.get("lemma", verb.get("text", "")), passive_subject.get("lemma", passive_subject.get("text", ""))),
                                "subject_text": agent.get("lemma", agent.get("text", "")),
                                "subject_ref": _resolve_ref(ref_lookup, agent.get("text", ""), agent.get("start_offset", -1), agent.get("end_offset", -1)),
                                "predicate": verb.get("lemma", verb.get("text", "")),
                                "object_text": passive_subject.get("lemma", passive_subject.get("text", "")),
                                "object_ref": _resolve_ref(ref_lookup, passive_subject.get("text", ""), passive_subject.get("start_offset", -1), passive_subject.get("end_offset", -1)),
                                "sentence_id": sentence_id,
                                "source_text_id": source_text_id,
                                "confidence": _BR_REL_CONFIDENCE_SVO,
                                "evidence_span": {"start_offset": sentence_start, "end_offset": sentence_end},
                                "start_offset": sentence_start,
                                "end_offset": sentence_end,
                            }
                        )
    return relations


def _extract_copula_relations(input_payload: dict[str, Any]) -> list[dict[str, Any]]:
    source_text_id = input_payload["source_text_id"]
    tokens = input_payload.get("tokens", [])
    ref_lookup = _make_ref_lookup(input_payload)
    grouped = _group_tokens_by_sentence(tokens)
    relations: list[dict[str, Any]] = []

    for sentence_id, sentence_tokens in grouped.items():
        copulas = [t for t in sentence_tokens if t.get("lemma") == "be" and t.get("pos") in {"AUX", "VERB"}]
        for copula in copulas:
            copula_head = copula.get("text", "")
            subjects = [t for t in sentence_tokens if t.get("dependency") == "nsubj" and t.get("head_text") == copula_head]
            attrs = [t for t in sentence_tokens if t.get("dependency") in {"attr", "acomp"} and t.get("head_text") == copula_head]
            for subject in subjects:
                for attr in attrs:
                    start_offset = min(subject.get("start_offset", 0), copula.get("start_offset", 0), attr.get("start_offset", 0))
                    end_offset = max(subject.get("end_offset", 0), copula.get("end_offset", 0), attr.get("end_offset", 0))
                    relations.append(
                        {
                            "relation_id": _build_relation_id(source_text_id, sentence_id, subject.get("text", ""), copula.get("lemma", copula.get("text", "")), attr.get("text", "")),
                            "subject_text": subject.get("text", ""),
                            "subject_ref": _resolve_ref(ref_lookup, subject.get("text", ""), subject.get("start_offset", -1), subject.get("end_offset", -1)),
                            "predicate": copula.get("lemma", copula.get("text", "")),
                            "object_text": attr.get("text", ""),
                            "object_ref": _resolve_ref(ref_lookup, attr.get("text", ""), attr.get("start_offset", -1), attr.get("end_offset", -1)),
                            "sentence_id": sentence_id,
                            "source_text_id": source_text_id,
                            "confidence": _BR_REL_CONFIDENCE_COPULA,
                            "evidence_span": {"start_offset": start_offset, "end_offset": end_offset},
                            "start_offset": start_offset,
                            "end_offset": end_offset,
                        }
                    )
    return relations


def _dedupe_stable(relations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    unique: list[dict[str, Any]] = []
    seen: set[str] = set()
    sorted_relations = sorted(relations, key=lambda r: (r["sentence_id"], r["start_offset"], r["end_offset"], r["relation_id"]))
    for relation in sorted_relations:
        key = f"{_normalize_text(relation['subject_text'])}|{_normalize_text(relation['predicate'])}|{_normalize_text(relation['object_text'])}"
        if key in seen:
            continue
        seen.add(key)
        unique.append(relation)
    return unique


def extract_relations_from_payload(input_payload: dict[str, Any]) -> dict[str, Any]:
    candidates = []
    candidates.extend(_extract_svo_relations(input_payload))
    candidates.extend(_extract_copula_relations(input_payload))
    relations = _dedupe_stable(candidates)

    result = {k: v for k, v in input_payload.items() if not k.startswith("_spacy")}
    result["relations"] = relations
    return result
