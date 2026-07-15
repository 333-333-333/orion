"""Resolve supported relative pronouns with dependency and distance evidence."""

from __future__ import annotations

from typing import Any

COREF_RELATIVE_PRONOUNS = {"that", "which", "who"}
_BR_COREF_MIN_CONFIDENCE = 0.6


def normalize_text(value: str) -> str:
    """Case-fold and trim text for deterministic coreference comparison."""
    return value.casefold().strip()


def noun_chunks_for_sentence(noun_chunks: list[dict[str, Any]], sentence_id: str) -> list[dict[str, Any]]:
    """Return noun chunks for one sentence in deterministic source order."""
    chunks = [c for c in noun_chunks if c.get("sentence_id") == sentence_id]
    return sorted(chunks, key=lambda c: (c.get("start_offset", -1), c.get("end_offset", -1), normalize_text(c.get("text", ""))))


def _distance_score(mention_start: int, antecedent_end: int) -> float:
    """Score antecedent proximity within the bounded coreference distance window."""
    if antecedent_end > mention_start:
        return 0.0
    gap = mention_start - antecedent_end
    return max(0.0, 1.0 - min(gap, 80) / 80)


def _position_score(mention_start: int, mention_end: int, antecedent_start: int, antecedent_end: int) -> float:
    """Score whether an antecedent occurs before or overlaps a mention."""
    if antecedent_end <= mention_start:
        return 1.0
    if antecedent_start >= mention_end:
        return 0.0
    return 0.2


def _score_candidate(mention: dict[str, Any], chunk: dict[str, Any]) -> tuple[float, dict[str, float]]:
    """Score a coreference antecedent candidate and return an auditable breakdown."""
    mention_start = mention.get("start_offset", -1)
    mention_end = mention.get("end_offset", -1)
    antecedent_start = chunk.get("start_offset", -1)
    antecedent_end = chunk.get("end_offset", -1)

    distance = _distance_score(mention_start, antecedent_end)
    position = _position_score(mention_start, mention_end, antecedent_start, antecedent_end)
    noun_bonus = 0.1 if chunk.get("text", "").strip() else 0.0

    # Recency dominates; position rejects following mentions and the noun bonus breaks valid ties.
    score = round((distance * 0.7) + (position * 0.2) + noun_bonus, 6)
    breakdown = {
        "distance": round(distance, 6),
        "position": round(position, 6),
        "noun_bonus": round(noun_bonus, 6),
        "total": score,
    }
    return score, breakdown


def resolve_syntactic_relative(mention: dict[str, Any], sentence_tokens: list[dict[str, Any]]) -> dict[str, Any] | None:
    """Resolve a relative pronoun through its dependency head chain when explicit."""
    mention_start = int(mention.get("start_offset", -1))
    mention_end = int(mention.get("end_offset", -1))
    mention_text = str(mention.get("text", ""))
    prior_tokens = [token for token in sentence_tokens if int(token.get("end_offset", -1)) <= mention_start]

    head_text = str(mention.get("head_text", ""))
    current = next(
        (
            token for token in sorted(sentence_tokens, key=lambda token: abs(int(token.get("start_offset", 0)) - mention_start))
            if str(token.get("text", "")) == head_text
        ),
        None,
    )
    visited: set[tuple[int, int]] = set()
    antecedent_head: dict[str, Any] | None = None
    # Dependency chains should be shallow; the cap and visited set contain malformed parser cycles.
    for _ in range(5):
        if current is None:
            break
        key = (int(current.get("start_offset", -1)), int(current.get("end_offset", -1)))
        if key in visited:
            break
        visited.add(key)
        if current.get("dependency") == "relcl":
            antecedent_text = str(current.get("head_text", ""))
            antecedent_head = next(
                (
                    token for token in reversed(prior_tokens)
                    if str(token.get("text", "")) == antecedent_text and token.get("pos") in {"NOUN", "PROPN"}
                ),
                None,
            )
            break
        next_head = str(current.get("head_text", ""))
        if not next_head or next_head == str(current.get("text", "")):
            break
        current = next(
            (
                token for token in reversed(prior_tokens)
                if str(token.get("text", "")) == next_head
            ),
            None,
        )

    if antecedent_head is None:
        return None
    modifier_lower_bound = -1
    # In "type of X that ...", X is the semantic antecedent rather than the scaffold word "type".
    if str(antecedent_head.get("text", "")).casefold() in {"type", "kind", "category", "form"}:
        of_tokens = [token for token in prior_tokens if str(token.get("text", "")).casefold() == "of"]
        if of_tokens:
            last_of_end = int(of_tokens[-1].get("end_offset", -1))
            parent_heads = [
                token for token in prior_tokens
                if int(token.get("start_offset", -1)) >= last_of_end
                and token.get("pos") in {"NOUN", "PROPN"}
            ]
            if parent_heads:
                antecedent_head = parent_heads[-1]
                modifier_lower_bound = last_of_end
    head_start = int(antecedent_head.get("start_offset", -1))
    head_end = int(antecedent_head.get("end_offset", -1))
    modifiers = [
        token for token in prior_tokens
        if token.get("head_text") == antecedent_head.get("text")
        and token.get("dependency") in {"amod", "compound", "nummod", "poss"}
        and int(token.get("start_offset", -1)) >= modifier_lower_bound
        and int(token.get("end_offset", -1)) <= head_start
    ]
    phrase = sorted([*modifiers, antecedent_head], key=lambda token: int(token.get("start_offset", 0)))
    antecedent = " ".join(str(token.get("text", "")) for token in phrase).strip()
    antecedent_start = int(phrase[0].get("start_offset", head_start))
    return {
        "mention": mention_text,
        "mention_span": {"start_offset": mention_start, "end_offset": mention_end},
        "antecedent": antecedent,
        "antecedent_span": {"start_offset": antecedent_start, "end_offset": head_end},
        "confidence": 0.95,
        "score_breakdown": {"distance": 1.0, "position": 1.0, "noun_bonus": 0.1, "total": 0.95},
        "evidence_span": {"start_offset": antecedent_start, "end_offset": mention_end},
        "status": "resolved",
        "reason": "resolved_relative_dependency_head",
        "resolution_reason": "resolved_relative_dependency_head",
    }


def resolve_mention(mention: dict[str, Any], sentence_chunks: list[dict[str, Any]]) -> dict[str, Any]:
    """Resolve a mention to the highest-scoring prior noun chunk or return an unresolved record."""
    mention_text = mention.get("text", "")
    mention_start = mention.get("start_offset", -1)
    mention_end = mention.get("end_offset", -1)
    normalized = normalize_text(mention_text)

    candidates: list[tuple[float, dict[str, float], dict[str, Any]]] = []
    for chunk in sentence_chunks:
        if not isinstance(chunk.get("text"), str) or chunk.get("text", "").strip() == "":
            continue
        score, breakdown = _score_candidate(mention, chunk)
        candidates.append((score, breakdown, chunk))

    # Stable lexical tie-breakers keep resolution reproducible when candidates score equally.
    candidates.sort(
        key=lambda item: (
            item[0],
            item[2].get("end_offset", -1),
            item[2].get("start_offset", -1),
            normalize_text(item[2].get("text", "")),
        ),
        reverse=True,
    )

    if not candidates:
        return {
            "mention": mention_text,
            "mention_span": {"start_offset": mention_start, "end_offset": mention_end},
            "antecedent": "",
            "antecedent_span": {"start_offset": -1, "end_offset": -1},
            "confidence": 0.0,
            "score_breakdown": {"distance": 0.0, "position": 0.0, "noun_bonus": 0.0, "total": 0.0},
            "evidence_span": {"start_offset": mention_start, "end_offset": mention_end},
            "status": "unresolved",
            "reason": f"no_antecedent_for_{normalized}",
            "resolution_reason": f"no_antecedent_for_{normalized}",
        }

    best_score, best_breakdown, best_chunk = candidates[0]
    antecedent_text = best_chunk.get("text", "")
    antecedent_start = best_chunk.get("start_offset", -1)
    antecedent_end = best_chunk.get("end_offset", -1)
    confidence = round(best_score, 6)

    unresolved_relative = normalized in {"who", "which"} and confidence < _BR_COREF_MIN_CONFIDENCE
    if unresolved_relative:
        reason = f"low_confidence_{normalized}"
        return {
            "mention": mention_text,
            "mention_span": {"start_offset": mention_start, "end_offset": mention_end},
            "antecedent": "",
            "antecedent_span": {"start_offset": -1, "end_offset": -1},
            "confidence": confidence,
            "score_breakdown": best_breakdown,
            "evidence_span": {"start_offset": min(antecedent_start, mention_start), "end_offset": max(antecedent_end, mention_end)},
            "status": "unresolved",
            "reason": reason,
            "resolution_reason": reason,
        }

    return {
        "mention": mention_text,
        "mention_span": {"start_offset": mention_start, "end_offset": mention_end},
        "antecedent": antecedent_text,
        "antecedent_span": {"start_offset": antecedent_start, "end_offset": antecedent_end},
        "confidence": confidence,
        "score_breakdown": best_breakdown,
        "evidence_span": {"start_offset": min(antecedent_start, mention_start), "end_offset": max(antecedent_end, mention_end)},
        "status": "resolved",
        "reason": "resolved_nearest_noun_chunk",
        "resolution_reason": "resolved_nearest_noun_chunk",
    }
