from __future__ import annotations

from pathlib import Path
from typing import Any
import sys

_SMOKE_DIR = Path(__file__).parents[2]
if str(_SMOKE_DIR) not in sys.path:
    sys.path.insert(0, str(_SMOKE_DIR))

from infosec_pair_case_harness import run_pair_case

_CASE_DIR = Path(__file__).parent
_PARAGRAPH_IDS = ["pizza_001"]
_METRICS: dict[str, Any] | None = None


def _metrics(tmp_path: Path) -> dict[str, Any]:
    global _METRICS
    if _METRICS is None:
        _METRICS = run_pair_case(
            _CASE_DIR,
            _PARAGRAPH_IDS,
            tmp_path,
            case_id="pizza_short",
            fixture_dir=_CASE_DIR / "fixtures",
        )
    return _METRICS


def _read_json_artifact(name: str) -> dict[str, Any]:
    artifact_path = _CASE_DIR / "artifacts" / name
    import json

    return json.loads(artifact_path.read_text(encoding="utf-8"))


def _visible_labels(graph: dict[str, Any]) -> set[str]:
    labels: set[str] = set()
    buckets = [graph.get("classes", [])]
    schema = graph.get("schema") if isinstance(graph.get("schema"), dict) else {}
    buckets.append(schema.get("classes", []))
    buckets.append(schema.get("external_entities", []))
    for bucket in buckets:
        if not isinstance(bucket, list):
            continue
        for item in bucket:
            if not isinstance(item, dict):
                continue
            label = str(item.get("label") or item.get("iri") or item.get("id") or "").rsplit(":", 1)[-1]
            if label:
                labels.add(label)
    return labels


def _iri_tail(value: Any) -> str:
    return str(value or "").rsplit(":", 1)[-1].rsplit("/", 1)[-1].rsplit("#", 1)[-1]


def _is_unresolved_internal_claim(claim: dict[str, Any]) -> bool:
    resolution = str(claim.get("resolution_status") or claim.get("status") or "").lower()
    visibility = str(claim.get("visibility") or claim.get("projection") or "").lower()
    return (
        resolution in {"unresolved", "internal_unresolved"}
        or bool(claim.get("unresolved"))
        or bool(claim.get("internal"))
        or visibility in {"internal", "hidden", "not_visible"}
    )



def test_pizza_short_observed_artifacts_are_generated_case_local(tmp_path: Path):
    # TASK-PIZZA-SMOKE-001 | FUN-PIZZA-SMOKE AC-1 | CON-NO-INFOSEC-3K AC-1 | BR-PIZZA-SMOKE-001
    metrics = _metrics(tmp_path)

    assert metrics["claim_count"] > 0
    assert metrics["graph_generated"]
    assert metrics["rdf_generated"]
    assert metrics["rdf_bytes"] > 0


def test_pizza_short_semantic_claims_preserve_source_evidence(tmp_path: Path):
    # TASK-PIZZA-SMOKE-001 | FUN-PIZZA-SMOKE AC-2 | CON-SOURCE-EVIDENCE AC-1 | BR-PIZZA-SMOKE-002
    metrics = _metrics(tmp_path)

    assert metrics["observed_stage"] in {"semantic_claims", "semantic_claims_artifact"}
    assert not metrics["evidence_unsupported_claim_ids"]
    assert metrics["paragraph_claim_distribution"]["pizza_001"] > 0


def test_pizza_short_rdf_projection_has_visible_structure(tmp_path: Path):
    # TASK-PIZZA-SMOKE-001 | FUN-PIZZA-SMOKE AC-3 | CON-RDF-VISIBILITY AC-1 | BR-PIZZA-SMOKE-003
    metrics = _metrics(tmp_path)

    assert metrics["class_count"] > 0
    assert metrics["object_property_count"] > 0


def test_task_pizza_red_001_pm_abbreviation_stays_in_single_sentence(tmp_path: Path):
    # TASK-PIZZA-RED-001 | FUN-PIZZA-SMOKE AC-4 | BR-PIZZA-TIME-001
    _metrics(tmp_path)
    payload = _read_json_artifact("pipeline_outputs/observed_pizza_short_03_sentence_segmentation.json")
    texts = [str(sentence.get("text") or "") for sentence in payload.get("sentences", [])]

    assert "m." not in texts
    assert any("12:18 p.m." in text for text in texts)


def test_task_pizza_red_001_possessive_suffix_does_not_shift_linguistic_annotation(tmp_path: Path):
    # TASK-PIZZA-RED-001 | FUN-PIZZA-SMOKE AC-5 | BR-PIZZA-POSSESSIVE-001
    _metrics(tmp_path)
    token_payload = _read_json_artifact("pipeline_outputs/observed_pizza_short_04_tokenization.json")
    annotated_payload = _read_json_artifact("pipeline_outputs/observed_pizza_short_05_linguistic_annotation.json")
    token_texts = [str(token.get("text") or "") for token in token_payload.get("tokens", [])]
    annotated_tokens = annotated_payload.get("tokens", [])
    annotated_texts = [str(token.get("text") or "") for token in annotated_tokens]

    possessive_windows = [
        index
        for index in range(len(token_texts) - 2)
        if token_texts[index : index + 3] == ["Mario", "'s", "Pizzeria"]
    ]
    legacy_split_windows = [
        index
        for index in range(len(token_texts) - 3)
        if token_texts[index : index + 4] == ["Mario", "'", "s", "Pizzeria"]
    ]

    assert possessive_windows
    assert legacy_split_windows == []
    assert annotated_texts == token_texts

    expected_next_pos = {"in": "ADP", ".": "PUNCT", "on": "ADP", ",": "PUNCT"}
    for index in possessive_windows:
        mario, suffix, pizzeria = annotated_tokens[index : index + 3]
        assert mario["lemma"] == "Mario"
        assert mario["pos"] == "PROPN"
        assert suffix["lemma"] == "'s"
        assert suffix["tag"] == "POS"
        assert pizzeria["lemma"] == "Pizzeria"
        assert pizzeria["pos"] == "PROPN"

        next_token = annotated_tokens[index + 3]
        assert next_token["pos"] == expected_next_pos[next_token["text"]]


def test_task_pizza_red_002_prepositional_context_is_not_visible_compound_class(tmp_path: Path):
    # TASK-PIZZA-RED-002 | FUN-PIZZA-SMOKE AC-6 | BR-CON-PP-BOUNDARY-001 | BR-REL-PREP-ROUTE-001
    _metrics(tmp_path)
    concept_payload = _read_json_artifact("pipeline_outputs/observed_pizza_short_07_concept_extraction.json")
    graph = _read_json_artifact("observed_pizza_short_graph_model.json")
    labels = _visible_labels(graph)
    concept_texts = {str(concept.get("text") or "") for concept in concept_payload.get("concepts", []) if isinstance(concept, dict)}

    assert "delivery orders for Mario's Pizzeria" not in concept_texts
    assert "Harbor Market to Pine Street" not in concept_texts
    assert "Central Cafe at 12:18 p.m." not in concept_texts
    assert "aged parmesan over the edge" not in concept_texts
    assert {"delivery orders", "Mario's Pizzeria", "Harbor Market", "Pine Street", "Central Cafe", "aged parmesan"} <= concept_texts

    forbidden_visible_labels = {
        "AgedParmesanOverTheEdge",
        "CentralCafeAt1218Pm",
        "DeliveryOrderForMarioSPizzeria",
        "HarborMarketToPineStreet",
        "MarioSPizzeriaOnABlueBicycle",
    }
    assert labels.isdisjoint(forbidden_visible_labels)

    facts = graph.get("object_property_facts", [])

    def has_fact(predicate: str, domain: str, range_: str) -> bool:
        return any(
            isinstance(fact, dict)
            and _iri_tail(fact.get("predicate")) == predicate
            and _iri_tail(fact.get("domain")) == domain
            and _iri_tail(fact.get("range")) == range_
            for fact in facts
        )

    assert has_fact("ridesFrom", "Luigi", "HarborMarket")
    assert has_fact("ridesTo", "Luigi", "PineStreet")
    assert has_fact("reaches", "Luigi", "CentralCafe")
    assert has_fact("manages", "LuigiBianchi", "DeliveryOrder")
    assert has_fact("grates", "Luca", "AgedParmesan")


def test_task_pizza_red_001_pronoun_he_is_not_visible_as_rdf_node_or_class(tmp_path: Path):
    # TASK-PIZZA-RED-001 | CON-RDF-VISIBILITY AC-2 | BR-PIZZA-PRONOUN-001
    _metrics(tmp_path)
    graph = _read_json_artifact("observed_pizza_short_graph_model.json")
    rdf = (_CASE_DIR / "artifacts" / "observed_pizza_short_output.rdf").read_text(encoding="utf-8")

    assert "He" not in _visible_labels(graph)
    assert "orion:He" not in rdf
    assert ">He<" not in rdf


def test_task_pizza_red_001_connector_prefixes_are_not_visible_classes(tmp_path: Path):
    # TASK-PIZZA-RED-001 | CON-RDF-VISIBILITY AC-3 | BR-PIZZA-CONNECTOR-001
    _metrics(tmp_path)
    graph = _read_json_artifact("observed_pizza_short_graph_model.json")
    connectors = ("From", "To", "At", "In", "On", "During", "After", "Before")
    connector_prefixed = sorted(
        label
        for label in _visible_labels(graph)
        if any(label.startswith(prefix) and len(label) > len(prefix) and label[len(prefix)].isupper() for prefix in connectors)
    )

    assert connector_prefixed == []


def test_task_pizza_red_001_reaches_central_cafe_uses_luigi_not_he(tmp_path: Path):
    # TASK-PIZZA-RED-001 | FUN-PIZZA-PRONOUN AC-1 | BR-PIZZA-PRONOUN-002
    _metrics(tmp_path)
    graph = _read_json_artifact("observed_pizza_short_graph_model.json")
    facts = graph.get("object_property_facts", [])
    bad_he_reaches = [
        fact
        for fact in facts
        if isinstance(fact, dict)
        and _iri_tail(fact.get("predicate")) == "reaches"
        and _iri_tail(fact.get("domain")) == "He"
        and _iri_tail(fact.get("range")).startswith("CentralCafe")
    ]
    good_luigi_reaches = [
        fact
        for fact in facts
        if isinstance(fact, dict)
        and _iri_tail(fact.get("predicate")) == "reaches"
        and _iri_tail(fact.get("domain")) in {"Luigi", "LuigiBianchi"}
        and _iri_tail(fact.get("range")).startswith("CentralCafe")
    ]

    assert bad_he_reaches == []
    assert good_luigi_reaches


def test_task_pizza_red_001_pronoun_claims_rewrite_or_stay_unresolved_internal(tmp_path: Path):
    # TASK-PIZZA-RED-001 | FUN-PIZZA-PRONOUN AC-2 | BR-PIZZA-PRONOUN-003
    _metrics(tmp_path)
    payload = _read_json_artifact("observed_pizza_short_semantic_claims.json")
    graph = _read_json_artifact("observed_pizza_short_graph_model.json")
    visible_labels = _visible_labels(graph)
    pronouns = {"He", "She", "It", "Her", "His", "They", "Them", "Their"}
    visible_pronoun_claims = [
        claim
        for claim in payload.get("claims", [])
        if isinstance(claim, dict)
        and (_iri_tail(claim.get("subject")) in pronouns or _iri_tail(claim.get("object")) in pronouns)
        and not _is_unresolved_internal_claim(claim)
        and (
            _iri_tail(claim.get("subject")) in visible_labels
            or _iri_tail(claim.get("object")) in visible_labels
        )
    ]

    assert visible_pronoun_claims == []

