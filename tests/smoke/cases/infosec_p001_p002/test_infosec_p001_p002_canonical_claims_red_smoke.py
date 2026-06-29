from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from observability import JsonlFileLogSink
from orion import ORION
from infosec_pair_case_harness import process_with_pipeline_json_artifacts

_CASE_DIR = Path(__file__).parent
_SMOKE_DIR = Path(__file__).parents[2]
_PARAGRAPH_DIR = _SMOKE_DIR / "fixtures" / "infosec_3k_paragraphs"
_ARTIFACT_DIR = _CASE_DIR / "artifacts"
_ARTIFACT_PATH = _ARTIFACT_DIR / "observed_p001_p002_canonical_claims.json"

_EXPECTED_STATEMENTS_BY_PARAGRAPH: dict[str, set[str]] = {
    "p001": {
        "InformationSecurity is a Discipline",
        "InformationSecurity is focused on protecting InformationAsset",
        "InformationSecurity protects against InternalThreat",
        "InformationSecurity protects against ExternalThreat",
        "InformationAsset is a Resource",
        "InformationAsset has value for Organization",
        "InformationAsset stores Information",
        "InformationAsset processes Information",
        "InformationAsset transmits Information",
        "InformationAsset represents Information",
        "ConfidentialDocument is a type of InformationAsset",
        "CorporateDatabase is a type of InformationAsset",
        "CustomerRecord is a type of InformationAsset",
        "SourceCodeRepository is a type of InformationAsset",
        "SystemConfigurationFile is a type of InformationAsset",
        "BackupArchive is a type of InformationAsset",
        "BusinessReport is a type of InformationAsset",
    },
    "p002": {
        "InformationSecurity preserves Confidentiality",
        "InformationSecurity preserves Integrity",
        "InformationSecurity preserves Availability",
        "Confidentiality is a SecurityProperty",
        "Integrity is a SecurityProperty",
        "Availability is a SecurityProperty",
        "Confidentiality ensures Information is accessible only to AuthorizedEntity",
        "Integrity ensures Information is accurate",
        "Integrity ensures Information is complete",
        "Integrity protects Information against UnauthorizedModification",
        "Availability ensures Information is accessible when needed",
        "Availability ensures System is accessible when needed",
        "SecurityProperty forms CIATriad",
        "CIATriad is a FoundationalModel",
        "CIATriad is a model for InformationSecurity",
    },
}
_EXPECTED_STATEMENTS = set().union(*_EXPECTED_STATEMENTS_BY_PARAGRAPH.values())
_BANNED_RDF_KEYS = {"rdf", "rdf_xml", "graph", "triples", "subclass_facts", "object_properties"}


def _paragraph_texts() -> dict[str, str]:
    texts = {
        "p001": (_PARAGRAPH_DIR / "p001.txt").read_text(encoding="utf-8").strip(),
        "p002": (_PARAGRAPH_DIR / "p002.txt").read_text(encoding="utf-8").strip(),
    }
    assert "Information security is a discipline" in texts["p001"]
    assert "The CIA triad is a foundational model" in texts["p002"]
    return texts


def _run_p001_p002(tmp_path: Path, artifact_path: Path = _ARTIFACT_PATH) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    if artifact_path.exists():
        artifact_path.unlink()
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    paragraph_texts = _paragraph_texts()
    text = "\n\n".join(paragraph_texts[key] for key in ("p001", "p002"))
    runtime_log = tmp_path / "p001-p002-canonical-claims-runtime-events.jsonl"
    sut = ORION(config={"logging": {"sink": JsonlFileLogSink(runtime_log)}, "spacy_model": "en_core_web_lg", "output_strategy": "rdf", "canonical_claims": {"artifact_path": artifact_path, "paragraph_asset_ids": ["p001", "p002"]}})
    result, _ = process_with_pipeline_json_artifacts(sut, text, _ARTIFACT_DIR, "p001_p002")
    events = [json.loads(line) for line in runtime_log.read_text(encoding="utf-8").splitlines() if line.strip()]
    return result, events


def _canonical_claims_payload(result: dict[str, Any]) -> dict[str, Any]:
    candidates = [
        result.get("canonical_claims"),
        result.get("canonical_claims_artifact"),
        result.get("artifacts", {}).get("canonical_claims") if isinstance(result.get("artifacts"), dict) else None,
    ]
    for candidate in candidates:
        if isinstance(candidate, dict):
            return candidate
    assert False, "canonical_claims stage payload missing; pipeline is still deriving downstream output directly without canonical_claims"


def _claims(payload: dict[str, Any]) -> list[dict[str, Any]]:
    raw = payload.get("claims")
    assert isinstance(raw, list) and raw, "canonical_claims.claims must be a non-empty list"
    assert all(isinstance(item, dict) for item in raw), "each canonical claim must be an object"
    return raw


def _statement(claim: dict[str, Any]) -> str:
    value = claim.get("statement") or claim.get("normalized_statement")
    assert isinstance(value, str) and value.strip(), "each canonical claim must expose a normalized statement string"
    return value.strip()


def _paragraph_id(claim: dict[str, Any]) -> str:
    source = claim.get("source") if isinstance(claim.get("source"), dict) else {}
    value = claim.get("paragraph_id") or source.get("paragraph_id") or source.get("asset_id")
    assert value in {"p001", "p002"}, "each canonical claim must preserve source paragraph asset p001 or p002"
    return str(value)


def test_p001_p002_canonical_claims_stage_exists_before_triples_and_rdf(tmp_path: Path):
    # TASK-CANONICAL-CLAIMS-P001-P002 | FUN-CANONICAL-CLAIMS-P001-P002 AC-1 | CON-CANONICAL-CLAIMS-P001-P002 AC-1 | BR-CANONICAL-CLAIMS-P001-P002-001
    result, events = _run_p001_p002(tmp_path)
    payload = _canonical_claims_payload(result)

    assert payload.get("stage") == "canonical_claims"
    phases = [event.get("phase") for event in events if event.get("event_type") in {"started", "completed"}]
    assert "canonical_claims" in phases, "canonical_claims must be an observable intermediate phase"
    assert phases.index("canonical_claims") < phases.index("triple_extraction") < phases.index("output_generation")
    assert _ARTIFACT_PATH.exists(), "canonical_claims JSON artifact must be persisted before RDF output generation"


def test_canonical_claims_artifact_path_comes_from_external_config(tmp_path: Path):
    # TASK-CANONICAL-CLAIMS-P001-P002 | CON-CANONICAL-CLAIMS-P001-P002 AC-1
    custom_artifact_path = tmp_path / "custom-canonical-claims.json"
    result, _ = _run_p001_p002(tmp_path, custom_artifact_path)

    assert custom_artifact_path.exists(), "canonical_claims artifact path must come from harness config"
    artifacts = result.get("artifacts") if isinstance(result.get("artifacts"), dict) else {}
    assert artifacts.get("canonical_claims_path") == str(custom_artifact_path)


def test_p001_p002_canonical_claims_are_explicit_normalized_statements_not_rdf(tmp_path: Path):
    # TASK-CANONICAL-CLAIMS-P001-P002 | FUN-CANONICAL-CLAIMS-P001-P002 AC-2 | CON-CANONICAL-CLAIMS-P001-P002 AC-2 | BR-CANONICAL-CLAIMS-P001-P002-002
    result, _ = _run_p001_p002(tmp_path)
    payload = _canonical_claims_payload(result)
    claims = _claims(payload)
    actual = {_statement(claim) for claim in claims}

    missing = sorted(_EXPECTED_STATEMENTS - actual)
    unexpected = sorted(actual - _EXPECTED_STATEMENTS)
    assert not missing, f"missing canonical claim statements: {missing}"
    assert not unexpected, f"unexpected canonical claim statements: {unexpected}"
    serialized = json.dumps(payload, ensure_ascii=False)
    assert "<rdf:RDF" not in serialized and "rdf:about" not in serialized
    assert not (_BANNED_RDF_KEYS & payload.keys()), "canonical_claims must not be RDF graph/triple artifact"


def test_p001_p002_canonical_claims_preserve_paragraph_assets(tmp_path: Path):
    # TASK-CANONICAL-CLAIMS-P001-P002 | FUN-CANONICAL-CLAIMS-P001-P002 AC-3 | CON-CANONICAL-CLAIMS-P001-P002 AC-3 | BR-CANONICAL-CLAIMS-P001-P002-003
    result, _ = _run_p001_p002(tmp_path)
    claims = _claims(_canonical_claims_payload(result))
    by_paragraph: dict[str, set[str]] = {"p001": set(), "p002": set()}
    for claim in claims:
        by_paragraph[_paragraph_id(claim)].add(_statement(claim))

    assert by_paragraph == _EXPECTED_STATEMENTS_BY_PARAGRAPH
