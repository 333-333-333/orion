from __future__ import annotations

from typing import Any

COREF_RELATIVE_PRONOUNS = {"that", "which", "who"}
_BR_COREF_MIN_CONFIDENCE = 0.6


def normalize_text(value: str) -> str:
    return value.casefold().strip()


def noun_chunks_for_sentence(noun_chunks: list[dict[str, Any]], sentence_id: str) -> list[dict[str, Any]]:
    chunks = [c for c in noun_chunks if c.get("sentence_id") == sentence_id]
    return sorted(chunks, key=lambda c: (c.get("start_offset", -1), c.get("end_offset", -1), normalize_text(c.get("text", ""))))


def _distance_score(mention_start: int, antecedent_end: int) -> float:
    if antecedent_end > mention_start:
        return 0.0
    gap = mention_start - antecedent_end
    return max(0.0, 1.0 - min(gap, 80) / 80)


def _position_score(mention_start: int, mention_end: int, antecedent_start: int, antecedent_end: int) -> float:
    if antecedent_end <= mention_start:
        return 1.0
    if antecedent_start >= mention_end:
        return 0.0
    return 0.2


def _score_candidate(mention: dict[str, Any], chunk: dict[str, Any]) -> tuple[float, dict[str, float]]:
    mention_start = mention.get("start_offset", -1)
    mention_end = mention.get("end_offset", -1)
    antecedent_start = chunk.get("start_offset", -1)
    antecedent_end = chunk.get("end_offset", -1)

    distance = _distance_score(mention_start, antecedent_end)
    position = _position_score(mention_start, mention_end, antecedent_start, antecedent_end)
    noun_bonus = 0.1 if chunk.get("text", "").strip() else 0.0

    score = round((distance * 0.7) + (position * 0.2) + noun_bonus, 6)
    breakdown = {
        "distance": round(distance, 6),
        "position": round(position, 6),
        "noun_bonus": round(noun_bonus, 6),
        "total": score,
    }
    return score, breakdown


def resolve_mention(mention: dict[str, Any], sentence_chunks: list[dict[str, Any]]) -> dict[str, Any]:
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
