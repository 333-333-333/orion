"""Recover source-faithful SVO claims from dependency annotations."""

from __future__ import annotations

from typing import Any, Callable

_NOMINAL_DEPS = {"amod", "compound", "nummod", "poss"}
_OBJECT_DEPS = {"dobj", "obj", "attr", "oprd", "acomp", "advcl"}
_MODAL_WORDS = {"may", "must", "can", "could", "should", "would", "might"}
_REPORTING_VERBS = {"represent", "state", "report", "say", "tell", "indicate", "note"}


def _tokens_for_sentence(input_payload: dict[str, Any], sentence_id: str) -> list[dict[str, Any]]:
    """Return one sentence's tokens in deterministic source order."""
    return sorted(
        [
            token
            for token in input_payload.get("tokens", [])
            if isinstance(token, dict) and token.get("sentence_id") == sentence_id
        ],
        key=lambda token: (int(token.get("start_offset", 0)), int(token.get("end_offset", 0))),
    )


def _phrase(tokens: list[dict[str, Any]], head: dict[str, Any], label: Callable[[str | None], str]) -> str:
    """Build a normalized label for a dependency head and its nominal modifiers."""
    head_text = str(head.get("text", ""))
    phrase_tokens = [
        token
        for token in tokens
        if token is head
        or (
            token.get("head_text") == head_text
            and token.get("dependency") in _NOMINAL_DEPS
            and int(token.get("end_offset", 0)) <= int(head.get("start_offset", 0))
        )
    ]
    phrase_tokens.sort(key=lambda token: int(token.get("start_offset", 0)))
    result = label(" ".join(str(token.get("text", "")) for token in phrase_tokens))
    if result or len(phrase_tokens) != 1:
        return result
    atomic = "".join(character for character in str(head.get("text") or head.get("lemma") or "") if character.isalnum())
    return atomic[:1].upper() + atomic[1:] if atomic else ""


def _children(tokens: list[dict[str, Any]], head: dict[str, Any], dependencies: set[str]) -> list[dict[str, Any]]:
    """Return dependency children of a head whose labels are allowed."""
    head_text = str(head.get("text", ""))
    return [
        token
        for token in tokens
        if token.get("head_text") == head_text and token.get("dependency") in dependencies
    ]


def _crosses_clause_boundary(tokens: list[dict[str, Any]], left: dict[str, Any], right: dict[str, Any]) -> bool:
    """Return whether punctuation separates two dependency tokens into different clauses."""
    start = min(int(left.get("end_offset", 0)), int(right.get("end_offset", 0)))
    end = max(int(left.get("start_offset", 0)), int(right.get("start_offset", 0)))
    return any(
        token.get("pos") == "PUNCT"
        and token.get("text") in {",", ";"}
        and start <= int(token.get("start_offset", 0)) <= end
        for token in tokens
    )


def _conjuncts(tokens: list[dict[str, Any]], head: dict[str, Any], allowed_pos: set[str]) -> list[dict[str, Any]]:
    """Return same-clause conjuncts with one of the allowed parts of speech."""
    head_text = str(head.get("text", ""))
    return [
        token
        for token in tokens
        if token.get("head_text") == head_text
        and token.get("dependency") == "conj"
        and token.get("pos") in allowed_pos
        and not _crosses_clause_boundary(tokens, head, token)
    ]


def _modal_for(tokens: list[dict[str, Any]], verb: dict[str, Any]) -> str:
    """Resolve the modal auxiliary governing a verb or its coordination head."""
    candidates = [verb]
    if verb.get("dependency") == "conj":
        head_text = str(verb.get("head_text", ""))
        candidates.extend(token for token in tokens if token.get("text") == head_text and token.get("pos") == "VERB")
    for candidate in candidates:
        for token in _children(tokens, candidate, {"aux"}):
            modal = str(token.get("lemma") or token.get("text") or "").casefold()
            if modal in _MODAL_WORDS:
                return modal
    return ""


def _modal_predicate(modal: str, base: str) -> str:
    """Combine a modal and base verb into the canonical predicate label."""
    base = base.casefold()
    return modal + base[:1].upper() + base[1:] if modal and base else ""


def _passive_predicate(modal: str, participle: str, preposition: str) -> str:
    """Build a canonical predicate from passive modality, participle, and preposition."""
    words = [modal.casefold(), "be", participle.casefold(), preposition.casefold()]
    words = [word for word in words if word]
    if not words:
        return ""
    return words[0] + "".join(word[:1].upper() + word[1:] for word in words[1:])


def _object_heads(tokens: list[dict[str, Any]], verb: dict[str, Any]) -> list[dict[str, Any]]:
    """Return direct and coordinated object heads for a verb."""
    direct = _children(tokens, verb, _OBJECT_DEPS)
    if direct:
        heads = list(direct)
    else:
        heads = []
        for conjunct in _conjuncts(tokens, verb, {"VERB"}):
            heads.extend(_children(tokens, conjunct, _OBJECT_DEPS))
    expanded: list[dict[str, Any]] = []
    for head in heads:
        expanded.append(head)
        expanded.extend(_conjuncts(tokens, head, {"NOUN", "PROPN", "PRON"}))
    return expanded


def _subjects(tokens: list[dict[str, Any]], verb: dict[str, Any], dependency: str) -> list[dict[str, Any]]:
    """Return direct, inherited, or relative-clause subjects for a verb."""
    direct = _children(tokens, verb, {dependency})
    if direct:
        heads = list(direct)
    elif verb.get("dependency") == "conj":
        head_text = str(verb.get("head_text", ""))
        heads = [
            token
            for token in tokens
            if token.get("head_text") == head_text and token.get("dependency") == dependency
        ]
    elif dependency == "nsubj" and verb.get("dependency") in {"acl", "relcl"}:
        head_text = str(verb.get("head_text", ""))
        candidates = [
            token
            for token in tokens
            if token.get("head_text") == head_text
            and token.get("dependency") in {"conj", "nsubj"}
            and token.get("pos") in {"NOUN", "PROPN", "PRON"}
            and int(token.get("end_offset", 0)) <= int(verb.get("start_offset", 0))
            and not _crosses_clause_boundary(tokens, token, verb)
        ]
        heads = sorted(candidates, key=lambda token: int(token.get("end_offset", 0)), reverse=True)[:1]
    else:
        heads = []
    expanded: list[dict[str, Any]] = []
    for head in heads:
        expanded.append(head)
        expanded.extend(_conjuncts(tokens, head, {"NOUN", "PROPN", "PRON"}))
    return expanded


def _prepositional_objects(tokens: list[dict[str, Any]], verb: dict[str, Any]) -> tuple[str, list[dict[str, Any]]]:
    """Return the first dependency preposition and its object tokens."""
    for prep in _children(tokens, verb, {"prep"}):
        objects = [
            token
            for token in tokens
            if token.get("head_text") == prep.get("text") and token.get("dependency") == "pobj"
        ]
        if objects:
            return str(prep.get("lemma") or prep.get("text") or "").casefold(), objects
    return "", []


def _passive_agents(tokens: list[dict[str, Any]], verb: dict[str, Any]) -> tuple[str, list[dict[str, Any]]]:
    """Return the supported passive preposition and its object agents."""
    for prep in _children(tokens, verb, {"agent", "prep"}):
        prep_text = str(prep.get("lemma") or prep.get("text") or "").casefold()
        if prep_text not in {"by", "against", "in", "on", "to", "from"}:
            continue
        objects = [
            token
            for token in tokens
            if token.get("head_text") == prep.get("text") and token.get("dependency") == "pobj"
        ]
        if objects:
            return prep_text, objects
    return "", []


def _relation(subject: str, predicate: str, obj: str, *, modality: str = "", voice: str = "active") -> dict[str, str]:
    """Build a dependency-derived relation record with provenance metadata."""
    return {
        "subject": subject,
        "predicate": predicate,
        "object": obj,
        "modality": modality,
        "voice": voice,
        "extracted_by": "CORE-SEM-DEPENDENCY-001",
    }


def extract_dependency_relations(
    input_payload: dict[str, Any],
    sentence: dict[str, Any],
    *,
    label: Callable[[str | None], str],
    verb_form: Callable[[str | None], str],
) -> list[dict[str, str]]:
    """Recover source-faithful SVO relations from dependency annotations for one sentence."""
    tokens = _tokens_for_sentence(input_payload, str(sentence.get("sentence_id", "")))
    if not tokens:
        return []
    text = str(sentence.get("text", ""))
    represented = " represent that " in f" {text.casefold()} "
    relations: list[dict[str, str]] = []

    for verb in [token for token in tokens if token.get("pos") == "VERB"]:
        lemma = str(verb.get("lemma") or verb.get("text") or "").casefold()
        if not lemma or (represented and lemma in _REPORTING_VERBS):
            continue
        modal = _modal_for(tokens, verb)
        passive_subjects = _subjects(tokens, verb, "nsubjpass")
        if passive_subjects:
            preposition, agents = _passive_agents(tokens, verb)
            passive_objects = agents or _children(tokens, verb, {"advmod"})
            if passive_objects:
                predicate = _passive_predicate(modal, str(verb.get("text") or lemma), preposition)
                for subject_head in passive_subjects:
                    subject = _phrase(tokens, subject_head, label)
                    for object_head in passive_objects:
                        obj = _phrase(tokens, object_head, label)
                        if subject and predicate and obj:
                            relations.append(_relation(subject, predicate, obj, modality=modal, voice="passive"))
            continue

        subjects = _subjects(tokens, verb, "nsubj")
        objects = _object_heads(tokens, verb)
        preposition = ""
        if not objects:
            preposition, objects = _prepositional_objects(tokens, verb)
        if not subjects or not objects:
            continue
        base_predicate = _modal_predicate(modal, lemma) if modal else verb_form(lemma)
        predicate = base_predicate + preposition[:1].upper() + preposition[1:] if preposition else base_predicate
        for subject_head in subjects:
            subject = _phrase(tokens, subject_head, label)
            for object_head in objects:
                obj = _phrase(tokens, object_head, label)
                if subject and predicate and obj:
                    relations.append(_relation(subject, predicate, obj, modality=modal))

    # Recover a narrow coordinated-subject form when spaCy nominalizes the finite verb.
    roots = [token for token in tokens if token.get("dependency") == "ROOT" and token.get("pos") == "NOUN"]
    for root in roots:
        predicates = [
            token
            for token in tokens
            if token.get("head_text") == root.get("text")
            and token.get("dependency") == "compound"
            and token.get("pos") == "NOUN"
        ]
        for predicate_head in predicates:
            right_subjects = [
                token
                for token in tokens
                if token.get("head_text") == predicate_head.get("text")
                and token.get("dependency") == "compound"
                and token.get("pos") in {"NOUN", "PROPN"}
            ]
            left_subjects = [
                token
                for token in tokens
                if token.get("head_text") == root.get("text")
                and token.get("dependency") == "nmod"
                and int(token.get("start_offset", 0)) < int(predicate_head.get("start_offset", 0))
            ]
            predicate = verb_form(str(predicate_head.get("lemma") or predicate_head.get("text") or ""))
            obj = _phrase(tokens, root, label)
            for subject_head in [*left_subjects, *right_subjects]:
                subject = _phrase(tokens, subject_head, label)
                if subject and predicate and obj:
                    relations.append(_relation(subject, predicate, obj))

    # spaCy may represent "requirements are satisfied by controls" with an AUX root and ADJ complement.
    for copula in [token for token in tokens if token.get("pos") == "AUX" and token.get("lemma") == "be"]:
        subjects = _children(tokens, copula, {"nsubjpass", "nsubj"})
        complements = _children(tokens, copula, {"acomp"})
        for complement in complements:
            preposition, agents = _passive_agents(tokens, complement)
            if not agents:
                continue
            modal = _modal_for(tokens, copula)
            predicate = _passive_predicate(modal, str(complement.get("text") or ""), preposition)
            for subject_head in subjects:
                subject = _phrase(tokens, subject_head, label)
                for object_head in agents:
                    obj = _phrase(tokens, object_head, label)
                    if subject and predicate and obj:
                        relations.append(_relation(subject, predicate, obj, modality=modal, voice="passive"))

    unique: list[dict[str, str]] = []
    seen: set[tuple[str, str, str]] = set()
    for item in relations:
        key = (item["subject"], item["predicate"], item["object"])
        if key not in seen:
            seen.add(key)
            unique.append(item)
    return unique
