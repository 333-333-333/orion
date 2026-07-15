from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from observability import JsonlFileLogSink
from orion import ORION
from infosec_pair_case_harness import process_with_pipeline_json_artifacts
from pipeline.step_013_output_generation.rdf_strategy import serialize_graph_to_rdf_xml

_CASE_DIR = Path(__file__).parent
_SMOKE_DIR = Path(__file__).parents[2]
_PARAGRAPH_DIR = _SMOKE_DIR / "fixtures" / "infosec_3k_paragraphs"
_CONTRACT_PATH = _CASE_DIR / "expected_semantic_contract.json"
_ARTIFACT_DIR = _CASE_DIR / "artifacts"
_OBSERVED_PATH = _ARTIFACT_DIR / "observed_p003_p004_semantic_claims.json"
_CANONICAL_COMPAT_PATH = _ARTIFACT_DIR / "observed_p003_p004_canonical_claims.json"
_CAMEL_SPLIT = re.compile(r"([a-z])([A-Z])")
_RDF_NS = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
_OWL_NS = "http://www.w3.org/2002/07/owl#"
_RESOURCE_NS = "https://orion.local/resource/"


def _contract() -> dict[str, Any]:
    return json.loads(_CONTRACT_PATH.read_text(encoding="utf-8"))


def _paragraph_texts() -> dict[str, str]:
    texts = {
        "p003": (_PARAGRAPH_DIR / "p003.txt").read_text(encoding="utf-8").strip(),
        "p004": (_PARAGRAPH_DIR / "p004.txt").read_text(encoding="utf-8").strip(),
    }
    assert "A security policy is a formal document" in texts["p003"]
    assert "The board of directors provides strategic oversight" in texts["p004"]
    return texts


def _norm(value: Any) -> str:
    text = str(value or "").strip()
    if text.startswith("orion:"):
        text = text[len("orion:"):]
    text = text.rsplit("/", 1)[-1].rsplit("#", 1)[-1]
    text = _CAMEL_SPLIT.sub(r"\1_\2", text)
    text = re.sub(r"[^A-Za-z0-9]+", "_", text).strip("_").lower()
    return re.sub(r"_+", "_", text)


def _run_p003_p004(tmp_path: Path) -> dict[str, Any]:
    for path in (_OBSERVED_PATH, _CANONICAL_COMPAT_PATH):
        if path.exists():
            path.unlink()
    _ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    paragraph_texts = _paragraph_texts()
    runtime_log = tmp_path / "p003-p004-semantic-runtime-events.jsonl"
    sut = ORION(config={
        "logging": {"sink": JsonlFileLogSink(runtime_log)},
        "spacy_model": "en_core_web_lg",
        "output_strategy": "rdf",
        "semantic_claims": {"artifact_path": _OBSERVED_PATH, "paragraph_asset_ids": ["p003", "p004"]},
        "canonical_claims": {"artifact_path": _CANONICAL_COMPAT_PATH, "paragraph_asset_ids": ["p003", "p004"]},
    })
    result, _ = process_with_pipeline_json_artifacts(
        sut,
        "\n\n".join(paragraph_texts[key] for key in ("p003", "p004")),
        _ARTIFACT_DIR,
        "p003_p004",
    )
    observed = _observed_payload(result)
    observed.setdefault("contract_required_stage", "semantic_claims")
    observed.setdefault("observed_from_result_keys", sorted(str(key) for key in result.keys()))
    _OBSERVED_PATH.write_text(json.dumps(observed, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    return result


def _observed_payload(result: dict[str, Any]) -> dict[str, Any]:
    if isinstance(result.get("semantic_claims"), dict):
        payload = dict(result["semantic_claims"])
        payload["observed_stage"] = "semantic_claims"
        return payload
    artifacts = result.get("artifacts") if isinstance(result.get("artifacts"), dict) else {}
    if isinstance(artifacts.get("semantic_claims"), dict):
        payload = dict(artifacts["semantic_claims"])
        payload["observed_stage"] = "semantic_claims"
        return payload
    if isinstance(result.get("canonical_claims"), dict):
        payload = dict(result["canonical_claims"])
        payload["observed_stage"] = "canonical_claims"
        return payload
    if _CANONICAL_COMPAT_PATH.exists():
        payload = json.loads(_CANONICAL_COMPAT_PATH.read_text(encoding="utf-8"))
        payload["observed_stage"] = "canonical_claims_artifact"
        return payload
    return {"observed_stage": "missing", "claims": []}


def _semantic_payload(result: dict[str, Any]) -> dict[str, Any]:
    payload = json.loads(_OBSERVED_PATH.read_text(encoding="utf-8"))
    assert payload.get("observed_stage") == "semantic_claims", (
        "semantic_claims stage must exist before triples/RDF; "
        f"observed {payload.get('observed_stage')}"
    )
    return payload


def _claims(payload: dict[str, Any]) -> list[dict[str, Any]]:
    claims = payload.get("claims")
    assert isinstance(claims, list) and claims, "semantic_claims.claims must be a non-empty list"
    assert all(isinstance(item, dict) for item in claims), "each semantic claim must be an object"
    return claims


def _claim_key(claim: dict[str, Any]) -> tuple[str, str, str, str]:
    source = claim.get("source") if isinstance(claim.get("source"), dict) else {}
    paragraph = claim.get("paragraph_id") or source.get("paragraph_id") or source.get("asset_id")
    return (_norm(paragraph), _norm(claim.get("subject")), _norm(claim.get("predicate")), _norm(claim.get("object")))


def _source(claim: dict[str, Any]) -> dict[str, Any]:
    source = claim.get("source")
    assert isinstance(source, dict), "each semantic claim must carry source object"
    return source


def _graph(result: dict[str, Any]) -> dict[str, Any]:
    output = result.get("output") if isinstance(result.get("output"), dict) else {}
    graph = output.get("graph") if isinstance(output.get("graph"), dict) else {}
    assert isinstance(graph, dict), "RDF graph projection must be inspectable as dict"
    return graph


def _combined_text(*values: Any) -> str:
    return json.dumps(values, ensure_ascii=False, sort_keys=True, default=str).lower()


def _term_key(value: Any) -> str:
    return _norm(value).replace("_", "")


def _spo(subject: Any, predicate: Any, obj: Any) -> tuple[str, str, str]:
    return (_term_key(subject), _term_key(predicate), _term_key(obj))


def _semantic_relation_spo(claims: list[dict[str, Any]], *, alternatives: bool = False) -> set[tuple[str, str, str]]:
    return {
        _spo(claim.get("subject"), claim.get("predicate"), claim.get("object"))
        for claim in claims
        if _norm(claim.get("kind")) == "relation"
        and (_norm(claim.get("coordination")) == "or") == alternatives
    }


def _graph_alternative_spo(graph: dict[str, Any]) -> set[tuple[str, str, str]]:
    return {
        _spo(item.get("subject"), item.get("predicate"), item.get("object"))
        for group in graph.get("logical_alternatives", [])
        if isinstance(group, dict) and group.get("operator") == "or"
        for item in group.get("alternatives", [])
        if isinstance(item, dict)
    }


def _graph_fact_spo(graph: dict[str, Any]) -> set[tuple[str, str, str]]:
    facts = graph.get("facts")
    assert isinstance(facts, list), "RDF graph must expose its direct facts as a list"
    return {
        _spo(fact.get("subject"), fact.get("predicate"), fact.get("object"))
        for fact in facts
        if isinstance(fact, dict)
    }


def _rdf_observations(graph: dict[str, Any]) -> tuple[set[tuple[str, str, str]], set[str]]:
    root = ET.fromstring(serialize_graph_to_rdf_xml(graph))
    facts: set[tuple[str, str, str]] = set()
    for description in root.findall(f"{{{_RDF_NS}}}Description"):
        subject = description.attrib.get(f"{{{_RDF_NS}}}about")
        for child in description:
            obj = child.attrib.get(f"{{{_RDF_NS}}}resource")
            if subject and obj and child.tag.startswith(f"{{{_RESOURCE_NS}}}"):
                facts.add(_spo(subject, child.tag, obj))
    classes = {
        _term_key(item.attrib.get(f"{{{_RDF_NS}}}about"))
        for item in root.findall(f"{{{_OWL_NS}}}Class")
        if item.attrib.get(f"{{{_RDF_NS}}}about")
    }
    return facts, classes


def _inflection_variants(token: str) -> set[str]:
    variants = {token}
    if token.endswith("ies") and len(token) > 3:
        variants.add(token[:-3] + "y")
    if token.endswith("es") and len(token) > 2:
        variants.update({token[:-2], token[:-1]})
    if token.endswith("s") and len(token) > 1:
        variants.add(token[:-1])
    return variants


def _term_variants(value: Any) -> set[str]:
    parts = _norm(value).split("_")
    if not parts:
        return set()
    prefix = "_".join(parts[:-1])
    return {
        _term_key(f"{prefix}_{candidate}" if prefix else candidate)
        for candidate in _inflection_variants(parts[-1])
    }


def _predicate_variants(value: Any) -> set[str]:
    parts = _norm(value).split("_")
    head = parts[0] if parts else ""
    suffix = "_".join(parts[1:])
    return {
        _term_key(f"{candidate}_{suffix}" if suffix else candidate)
        for candidate in _inflection_variants(head)
    }


def _assert_same_spo(
    stage: str,
    expected: set[tuple[str, str, str]],
    observed: set[tuple[str, str, str]],
) -> None:
    missing = sorted(expected - observed)
    extra = sorted(observed - expected)
    assert not missing and not extra, (
        f"semantic_claims → triples → RDF contract broken at {stage}: "
        f"missing semantic relations={missing[:5]}, non-semantic residue={extra[:5]}"
    )


def test_p003_p004_semantic_claims_exist_before_triples_or_rdf(tmp_path: Path):
    # TASK-SEMANTIC-CLAIMS-P003-P004 | FUN-SEMANTIC-CLAIMS-P003-P004 AC-1 | CON-SEMANTIC-CLAIMS-P003-P004 AC-1 | BR-SEMANTIC-CLAIMS-P003-P004-001
    result = _run_p003_p004(tmp_path)
    payload = _semantic_payload(result)
    forbidden = set(_contract()["claim_shape"]["forbidden_claim_fields"])

    assert _OBSERVED_PATH.exists(), "test harness must persist observed_p003_p004_semantic_claims.json"
    assert payload.get("stage") == "semantic_claims"
    for claim in _claims(payload):
        present_forbidden = forbidden.intersection(claim)
        assert not present_forbidden, f"semantic claim must not embed RDF/triples/graph fields: {present_forbidden}"


def test_p003_p004_semantic_claims_have_explicit_spo_source_and_resolved_references(tmp_path: Path):
    # TASK-SEMANTIC-CLAIMS-P003-P004 | FUN-SEMANTIC-CLAIMS-P003-P004 AC-2 | CON-SEMANTIC-CLAIMS-P003-P004 AC-2 | BR-SEMANTIC-CLAIMS-P003-P004-002
    result = _run_p003_p004(tmp_path)
    payload = _semantic_payload(result)
    required = set(_contract()["claim_shape"]["required_claim_fields"])
    required_source = set(_contract()["claim_shape"]["required_source_fields"])
    paragraph_seen: dict[str, int] = {"p003": 0, "p004": 0}

    for claim in _claims(payload):
        missing = required - set(claim)
        assert not missing, f"semantic claim missing required fields {missing}: {claim}"
        assert str(claim["subject"]).strip(), "semantic claim subject must be explicit"
        assert str(claim["predicate"]).strip(), "semantic claim predicate must be explicit"
        assert str(claim["object"]).strip(), "semantic claim object must be explicit"
        source = _source(claim)
        source_missing = required_source - set(source)
        assert not source_missing, f"semantic claim source missing {source_missing}: {claim}"
        assert source["asset_id"] == source["paragraph_id"] in paragraph_seen
        assert str(source["sentence_id"]).strip().startswith("sent-")
        assert str(source["evidence"]).strip() in _paragraph_texts()[source["paragraph_id"]]
        paragraph_seen[source["paragraph_id"]] += 1
        compact = _norm(claim["subject"] + "_" + claim["object"])
        assert "policy_policy" not in compact
        assert "resources_security_initiatives" not in compact

    assert all(count > 0 for count in paragraph_seen.values()), f"p003 and p004 both need claims: {paragraph_seen}"


def test_p003_p004_semantic_contract_expected_claims_and_no_chunk_residue(tmp_path: Path):
    # TASK-SEMANTIC-CLAIMS-P003-P004 | FUN-SEMANTIC-CLAIMS-P003-P004 AC-3 | CON-SEMANTIC-CLAIMS-P003-P004 AC-3 | BR-SEMANTIC-CLAIMS-P003-P004-003 | BR-SEMANTIC-CLAIMS-P003-P004-004
    result = _run_p003_p004(tmp_path)
    payload = _semantic_payload(result)
    expected = {(_norm(item["paragraph_id"]), _norm(item["subject"]), _norm(item["predicate"]), _norm(item["object"])) for item in _contract()["expected_claims"]}
    actual = {_claim_key(claim) for claim in _claims(payload)}
    text = _combined_text(payload)

    assert expected <= actual, f"missing semantic claims: {sorted(expected - actual)}"
    banned = [token for token in _contract()["banned_tokens"] if token.lower() in text]
    assert not banned, f"banned chunk/RDF residue in semantic_claims: {banned}"


def test_p003_p004_definitions_are_separate_from_relations(tmp_path: Path):
    # TASK-SEMANTIC-CLAIMS-P003-P004 | FUN-SEMANTIC-CLAIMS-P003-P004 AC-4 | CON-SEMANTIC-CLAIMS-P003-P004 AC-4 | BR-SEMANTIC-CLAIMS-P003-P004-005
    result = _run_p003_p004(tmp_path)
    claims = _claims(_semantic_payload(result))
    definitions = {claim["subject"] for claim in claims if _norm(claim.get("kind")) == "definition"}
    relation_predicates = {_norm(claim.get("predicate")) for claim in claims if _norm(claim.get("kind")) == "relation"}

    assert {_norm(item) for item in _contract()["definition_subjects"]} <= {_norm(item) for item in definitions}
    assert {_norm(item) for item in _contract()["relation_predicates"]} <= relation_predicates
    for claim in claims:
        if _norm(claim.get("kind")) == "definition":
            assert _norm(claim.get("predicate")) == "is_a"
        if _norm(claim.get("kind")) == "relation":
            assert _norm(claim.get("predicate")) != "is_a"


def test_p003_p004_ontology_projection_uses_semantic_claims_not_noun_chunks(tmp_path: Path):
    # TASK-SEMANTIC-CLAIMS-P003-P004 | FUN-SEMANTIC-CLAIMS-P003-P004 AC-5 | CON-SEMANTIC-CLAIMS-P003-P004 AC-5 | BR-SEMANTIC-CLAIMS-P003-P004-006
    result = _run_p003_p004(tmp_path)
    payload = _semantic_payload(result)
    claims = _claims(payload)
    graph = _graph(result)
    projection = graph.get("projection") if isinstance(graph.get("projection"), dict) else {}
    graph_text = _combined_text(graph, result.get("output"))

    assert projection.get("source_stage") == _contract()["projection"]["required_source_stage"], (
        "semantic_claims → triples → RDF contract broken: projection must declare source_stage=semantic_claims"
    )
    for forbidden in _contract()["projection"]["forbidden_source_stages"]:
        assert forbidden not in graph_text, f"ontology projection must not come from {forbidden}"
    residues = sorted(token for token in _contract()["banned_tokens"] if token.lower() in graph_text)
    assert not residues, f"ontology/RDF projection contains known noun-chunk residue: {residues}"

    claim_by_id = {str(claim.get("claim_id")): claim for claim in claims if claim.get("claim_id")}
    assert len(claim_by_id) == len(claims), (
        "semantic_claims → triples contract broken: every claim needs one unique, non-empty claim_id"
    )
    triples = result.get("triples")
    assert isinstance(triples, list) and all(isinstance(item, dict) for item in triples), (
        "semantic_claims → triples contract broken: observable triples list is missing or malformed"
    )
    triple_by_claim_id = {str(item.get("relation_id")): item for item in triples if item.get("relation_id")}
    projected_claim_ids = {
        str(item) for item in projection.get("claim_ids", []) if str(item)
    } if isinstance(projection.get("claim_ids"), list) else set()
    claim_ids = set(claim_by_id)
    assert set(triple_by_claim_id) == claim_ids == projected_claim_ids, (
        "semantic_claims → triples → RDF lineage is incomplete: "
        f"claims_without_triples={sorted(claim_ids - set(triple_by_claim_id))[:5]}, "
        f"foreign_triples={sorted(set(triple_by_claim_id) - claim_ids)[:5]}, "
        f"claims_without_projection={sorted(claim_ids - projected_claim_ids)[:5]}, "
        f"foreign_projected_ids={sorted(projected_claim_ids - claim_ids)[:5]}"
    )
    assert len(triple_by_claim_id) == len(triples), (
        "semantic_claims → triples contract broken: duplicate or missing triple relation_id"
    )
    for claim_id, claim in claim_by_id.items():
        triple = triple_by_claim_id[claim_id]
        refs = {triple.get("subject_ref"), triple.get("predicate_ref"), triple.get("object_ref")}
        assert refs == {claim_id}, (
            f"semantic_claims → triples contract broken for {claim_id}: refs={sorted(str(item) for item in refs)}"
        )
        assert _term_variants(triple.get("subject")) & _term_variants(claim.get("subject")), (
            f"semantic_claims → triples subject changed for {claim_id}: "
            f"claim={claim.get('subject')!r}, triple={triple.get('subject')!r}"
        )
        assert _term_variants(triple.get("object")) & _term_variants(claim.get("object")), (
            f"semantic_claims → triples object changed for {claim_id}: "
            f"claim={claim.get('object')!r}, triple={triple.get('object')!r}"
        )
        assert _term_key(triple.get("predicate")) in _predicate_variants(claim.get("predicate")), (
            f"semantic_claims → triples predicate changed for {claim_id}: "
            f"claim={claim.get('predicate')!r}, triple={triple.get('predicate')!r}"
        )

    semantic_spo = _semantic_relation_spo(claims)
    semantic_alternatives = _semantic_relation_spo(claims, alternatives=True)
    graph_spo = _graph_fact_spo(graph)
    graph_alternatives = _graph_alternative_spo(graph)
    rdf_spo, rdf_classes = _rdf_observations(graph)
    assert semantic_spo, "semantic_claims → RDF contract cannot be verified without semantic relations"
    _assert_same_spo("graph facts", semantic_spo, graph_spo)
    _assert_same_spo("serialized RDF direct facts", semantic_spo, rdf_spo)
    _assert_same_spo("logical alternatives", semantic_alternatives, graph_alternatives)

    must_follow = [claim for claim in claims if _norm(claim.get("predicate")) == "must_follow"]
    assert len(must_follow) == 1 and must_follow[0].get("modality") == "must"
    assert semantic_alternatives and all(
        claim.get("alternative_group") and claim.get("modality") == "disjunctive_alternative"
        for claim in claims if _norm(claim.get("coordination")) == "or"
    )

    semantic_terms = {
        _term_key(claim.get(field))
        for claim in claims
        for field in ("subject", "object")
        if claim.get(field)
    }
    foreign_rdf_classes = sorted(rdf_classes - semantic_terms)
    assert not foreign_rdf_classes, (
        "semantic_claims → RDF contract broken: visible RDF classes not licensed by any semantic claim; "
        f"possible noun-chunk residue={foreign_rdf_classes[:8]}"
    )
