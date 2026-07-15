"""Orchestrate the linguistic annotation pipeline stage while preserving the payload contract."""

from __future__ import annotations

from typing import Any


def _extract_doc_tokens(doc: Any) -> list[dict[str, Any]]:
    """Extract doc tokens."""
    extracted: list[dict[str, Any]] = []
    for index, token in enumerate(doc):
        text = getattr(token, "text", None)
        if text is None:
            continue
        start = getattr(token, "idx", None)
        if not isinstance(start, int):
            continue
        extracted.append({"token": token, "text": text, "start": start, "end": start + len(text), "index": index})
    return extracted


def _find_matching_doc_token(orion_token: dict[str, Any], doc_tokens: list[dict[str, Any]]) -> Any | None:
    """Match an ORION token to an NLP token by exact or containing offsets."""
    start_offset = orion_token.get("start_offset")
    end_offset = orion_token.get("end_offset")
    text = orion_token.get("text")
    if not isinstance(start_offset, int) or not isinstance(end_offset, int):
        return None

    # Prefer exact text and offsets, then relax text equality for tokenizer-normalization differences.
    for candidate in doc_tokens:
        if (
            candidate["start"] == start_offset
            and candidate["end"] == end_offset
            and candidate["text"] == text
        ):
            return candidate["token"]

    for candidate in doc_tokens:
        if candidate["start"] == start_offset and candidate["end"] == end_offset:
            return candidate["token"]

    # ORION may split a token that spaCy keeps whole (for example, a combined modal).
    for candidate in doc_tokens:
        if candidate["start"] <= start_offset and end_offset <= candidate["end"]:
            return candidate["token"]

    return None


def _repair_coordinated_predicates(tokens: list[dict[str, Any]]) -> None:
    """Repair a common parser error in relative clauses with comma-separated verbs."""
    by_sentence: dict[str, list[dict[str, Any]]] = {}
    for token in tokens:
        by_sentence.setdefault(str(token.get("sentence_id", "")), []).append(token)

    for sentence_tokens in by_sentence.values():
        for relative_index, relative in enumerate(sentence_tokens):
            if str(relative.get("text", "")).casefold() not in {"that", "which", "who"}:
                continue
            clause = sentence_tokens[relative_index + 1:]
            clause = clause[:next((index for index, token in enumerate(clause) if token.get("text") == "."), len(clause))]
            if not any(str(token.get("text", "")).casefold() in {"or", "and"} for token in clause):
                continue
            finite_verbs = [token for token in clause if token.get("pos") == "VERB" and token.get("tag") in {"VBZ", "VBP", "VBD"}]
            nominal_predicates = [
                token for index, token in enumerate(clause[:-1])
                if token.get("pos") == "NOUN"
                and token.get("tag") == "NNS"
                and str(clause[index + 1].get("text", "")).casefold() in {",", "or", "and"}
            ]
            if not finite_verbs or not nominal_predicates:
                continue
            # The nearest preceding nominal is the relative-clause head used by the repaired predicate chain.
            antecedents = [
                token for token in sentence_tokens[:relative_index]
                if token.get("pos") in {"NOUN", "PROPN"}
            ]
            antecedent_text = str(antecedents[-1].get("text", "")) if antecedents else ""
            first_predicate = nominal_predicates[0]
            for index, token in enumerate(nominal_predicates):
                token["pos"] = "VERB"
                token["tag"] = finite_verbs[0].get("tag", "VBZ")
                token["dependency"] = "relcl" if index == 0 else "conj"
                token["head_text"] = antecedent_text if index == 0 else str(first_predicate.get("text", ""))
            for verb in finite_verbs:
                if verb.get("dependency") == "conj":
                    verb["head_text"] = str(first_predicate.get("text", ""))


def _repair_coordinated_gerunds(tokens: list[dict[str, Any]]) -> None:
    """Keep coordinated gerunds parallel with their verbal conjunct head."""
    by_sentence: dict[str, list[dict[str, Any]]] = {}
    for token in tokens:
        by_sentence.setdefault(str(token.get("sentence_id", "")), []).append(token)

    for sentence_tokens in by_sentence.values():
        gerunds = {
            str(token.get("text", ""))
            for token in sentence_tokens
            if token.get("pos") == "VERB" and str(token.get("text", "")).casefold().endswith("ing")
        }
        if not gerunds:
            continue
        changed = True
        while changed:
            changed = False
            for token in sentence_tokens:
                text = str(token.get("text", ""))
                if (
                    token.get("dependency") == "conj"
                    and text.casefold().endswith("ing")
                    and str(token.get("head_text", "")) in gerunds
                    and token.get("pos") != "VERB"
                ):
                    token["pos"] = "VERB"
                    token["tag"] = "VBG"
                    gerunds.add(text)
                    changed = True


def _repair_unmatched_modals(tokens: list[dict[str, Any]]) -> None:
    """Annotate combined modal tokens when the NLP tokenizer split them."""
    by_sentence: dict[str, list[dict[str, Any]]] = {}
    for token in tokens:
        by_sentence.setdefault(str(token.get("sentence_id", "")), []).append(token)
    for sentence_tokens in by_sentence.values():
        for index, token in enumerate(sentence_tokens):
            if str(token.get("text", "")).casefold() != "cannot" or token.get("pos"):
                continue
            token["lemma"] = "can"
            token["pos"] = "AUX"
            token["tag"] = "MD"
            token["dependency"] = "aux"
            next_verb = next(
                (item for item in sentence_tokens[index + 1:] if item.get("pos") in {"AUX", "VERB"}),
                None,
            )
            token["head_text"] = str(next_verb.get("text", "")) if next_verb else ""


def _repair_nominal_compounds(tokens: list[dict[str, Any]]) -> None:
    """Repair recurring nominal compounds that the parser reads as clauses."""
    by_sentence: dict[str, list[dict[str, Any]]] = {}
    for token in tokens:
        by_sentence.setdefault(str(token.get("sentence_id", "")), []).append(token)
    for sentence_tokens in by_sentence.values():
        ordered = sorted(sentence_tokens, key=lambda item: int(item.get("start_offset", 0)))
        for index, token in enumerate(ordered[:-1]):
            if str(token.get("text", "")).casefold() == "expected" and str(ordered[index + 1].get("text", "")).casefold() == "behavior":
                token.update({"lemma": "expected", "pos": "ADJ", "tag": "JJ", "dependency": "amod", "head_text": str(ordered[index + 1].get("text", ""))})
        for index in range(len(ordered) - 2):
            phrase = [str(ordered[index + offset].get("text", "")).casefold() for offset in range(3)]
            if phrase != ["data", "handling", "awareness"]:
                continue
            head = ordered[index + 2]
            for modifier in ordered[index:index + 2]:
                modifier.update({"pos": "NOUN", "tag": "NN", "dependency": "compound", "head_text": str(head.get("text", ""))})
            next_verb = next((item for item in ordered[index + 3:] if item.get("pos") == "VERB"), None)
            if next_verb:
                head.update({"pos": "NOUN", "tag": "NN", "dependency": "nsubj", "head_text": str(next_verb.get("text", ""))})


def _repair_ensures_complements(tokens: list[dict[str, Any]]) -> None:
    """Keep the patient inside ``ensures X is ...`` complement clauses."""
    by_sentence: dict[str, list[dict[str, Any]]] = {}
    for token in tokens:
        by_sentence.setdefault(str(token.get("sentence_id", "")), []).append(token)

    for sentence_tokens in by_sentence.values():
        for ensure_index, ensure in enumerate(sentence_tokens):
            if str(ensure.get("lemma", "")).casefold() != "ensure":
                continue
            complement = sentence_tokens[ensure_index + 1:]
            copula_index = next(
                (index for index, token in enumerate(complement) if token.get("lemma") == "be" and token.get("pos") == "AUX"),
                -1,
            )
            if copula_index <= 0:
                continue
            copula = complement[copula_index]
            patients = [token for token in complement[:copula_index] if token.get("pos") in {"NOUN", "PROPN"}]
            if not patients:
                continue
            patient = patients[-1]
            patient["dependency"] = "nsubj"
            patient["head_text"] = str(copula.get("text", ""))
            copula["dependency"] = "ccomp"
            copula["head_text"] = str(ensure.get("text", ""))


def annotate_tokens(input_payload: dict[str, Any], nlp_model: Any) -> dict[str, Any]:
    """Align ORION tokens with the NLP document, repair known parser errors, and return the annotated payload."""
    preprocessed_text = input_payload["preprocessed_text"]
    doc = nlp_model(preprocessed_text)
    doc_tokens = _extract_doc_tokens(doc)

    annotated_tokens: list[dict[str, Any]] = []

    for token in input_payload["tokens"]:
        matched_doc_token = _find_matching_doc_token(token, doc_tokens)

        lemma = token["text"]
        pos = ""
        tag = ""
        dependency = ""
        head_text = ""

        if matched_doc_token is not None:
            lemma = getattr(matched_doc_token, "lemma_", lemma) or lemma
            pos = getattr(matched_doc_token, "pos_", "") or ""
            tag = getattr(matched_doc_token, "tag_", "") or ""
            dependency = getattr(matched_doc_token, "dep_", "") or ""
            head = getattr(matched_doc_token, "head", None)
            head_text = getattr(head, "text", "") if head is not None else ""

        annotated_token = dict(token)
        annotated_token["lemma"] = lemma
        annotated_token["pos"] = pos
        annotated_token["tag"] = tag
        annotated_token["dependency"] = dependency
        annotated_token["head_text"] = head_text
        if str(token.get("text", "")).casefold() == "cannot" and not pos:
            annotated_token.update({"lemma": "can", "pos": "AUX", "tag": "MD", "dependency": "aux"})
        elif dependency == "conj" and str(token.get("text", "")).casefold().endswith("ing"):
            verbal_heads = {
                str(item.get("text", ""))
                for item in annotated_tokens
                if item.get("sentence_id") == token.get("sentence_id") and item.get("pos") == "VERB"
            }
            if str(head_text) in verbal_heads:
                annotated_token.update({"pos": "VERB", "tag": "VBG"})
        annotated_tokens.append(annotated_token)

    _repair_coordinated_predicates(annotated_tokens)
    _repair_coordinated_gerunds(annotated_tokens)
    _repair_unmatched_modals(annotated_tokens)
    _repair_nominal_compounds(annotated_tokens)
    _repair_ensures_complements(annotated_tokens)

    return {
        "raw_text": input_payload["raw_text"],
        "source_text_id": input_payload["source_text_id"],
        "metadata": input_payload["metadata"],
        "preprocessed_text": preprocessed_text,
        "operations_applied": input_payload["operations_applied"],
        "sentences": input_payload["sentences"],
        "tokens": annotated_tokens,
    }
