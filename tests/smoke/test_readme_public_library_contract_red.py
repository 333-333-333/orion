from __future__ import annotations

from pathlib import Path


def _readme_config() -> dict[str, object]:
    return {
        "language": "en",
        "spacy_model_size": "lg",
        "output_formats": ["ttl", "rdfxml", "jsonld", "nt"],
        "traceability": True,
    }


def test_readme_public_api_accepts_documented_library_config():
    # README-PUBLIC-API | FUN-README-PUBLIC-API AC-1 | CON-README-CONFIG AC-1 | BR-README-CONTRACT-001
    from orion import ORION

    orion = ORION(config=_readme_config())

    assert orion.config["language"] == "en"
    assert orion.config["spacy_model_size"] == "lg"
    assert orion.config["output_formats"] == ["ttl", "rdfxml", "jsonld", "nt"]
    assert orion.config["traceability"] is True


def test_readme_public_api_process_returns_documented_result_object(tmp_path: Path):
    # README-PUBLIC-API | FUN-README-PUBLIC-API AC-2 | CON-README-OUTPUT AC-1 | BR-README-CONTRACT-002
    from orion import ORION

    orion = ORION(config=_readme_config())

    result = orion.process("A customer creates a reservation.")

    expected_attrs = ["ontology", "serialized", "deterministic_triples", "inferred_triples"]
    missing_attrs = [name for name in expected_attrs if not hasattr(result, name)]
    assert missing_attrs == []

    serialized = result.serialized
    assert set(serialized) == {"ttl", "rdfxml", "jsonld", "nt"}
    assert all(isinstance(serialized[name], str) for name in ("ttl", "rdfxml", "jsonld", "nt"))
