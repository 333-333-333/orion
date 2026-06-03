from __future__ import annotations

import re
from pathlib import Path

import pytest

from observability import JsonlFileLogSink
from orion import ORION

_PARAGRAPH_DIR = Path(__file__).parent / "fixtures" / "infosec_3k_paragraphs"
_PARAGRAPH_FIXTURES = sorted(_PARAGRAPH_DIR.glob("p*.txt"))


def _paragraph_groups(size: int = 2) -> list[tuple[str, list[Path]]]:
    groups: list[tuple[str, list[Path]]] = []
    for index in range(0, len(_PARAGRAPH_FIXTURES), size):
        chunk = _PARAGRAPH_FIXTURES[index:index + size]
        groups.append(("_".join(path.stem for path in chunk), chunk))
    return groups


def _simple_relation_signal(text: str) -> bool:
    return bool(
        re.search(
            r"\b(?:is|are|was|were|has|have|includes?|contains?|uses?|supports?|protects?|reduces?|causes?|defines?|stores?|processes?|manages?|provides?|enforces?|detects?|prevents?)\b",
            text,
            re.IGNORECASE,
        )
    )


# UC-SMOKE-001 AF-21 | FUN-SMOKE-001 AC-23 | CON-SMOKE-RDF-019 AC-1 | BR-SMOKE-053
@pytest.mark.parametrize("group_id, paragraph_paths", _paragraph_groups(size=2), ids=lambda item: item[0])
def test_infosec_3k_two_paragraph_group_smoke(group_id: str, paragraph_paths: list[Path], tmp_path):
    assert 1 <= len(paragraph_paths) <= 2
    text = "\n\n".join(path.read_text(encoding="utf-8").strip() for path in paragraph_paths)
    assert text, f"paragraph group empty: {group_id}"

    runtime_log = tmp_path / f"{group_id}-runtime-events.jsonl"
    sut = ORION(config={"logging": {"sink": JsonlFileLogSink(runtime_log)}, "spacy_model": "en_core_web_lg", "output_strategy": "rdf"})
    result = sut.process(text)

    output = result.get("output", {})
    graph = output.get("graph", {}) if isinstance(output, dict) else {}
    concepts = result.get("concepts", [])
    schema_classes = graph.get("schema", {}).get("classes", []) if isinstance(graph, dict) else []

    assert output.get("strategy") == "rdf"
    assert graph, f"graph missing for {group_id}"
    assert concepts, f"concepts missing for {group_id}"
    assert schema_classes, f"schema.classes missing for {group_id}"

    if _simple_relation_signal(text):
        relation_total = len(result.get("relations", []))
        triple_total = len(result.get("triples", []))
        fact_total = len(graph.get("facts", [])) + len(graph.get("instance_facts", [])) + len(graph.get("subclass_facts", []))
        assert relation_total + triple_total + fact_total > 0, (
            f"relation signal but no semantic output for {group_id}: "
            f"relations={relation_total} triples={triple_total} facts={fact_total}"
        )
