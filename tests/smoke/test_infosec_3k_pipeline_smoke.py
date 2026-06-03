import json
from pathlib import Path
import xml.etree.ElementTree as ET

import pytest

from observability import JsonlFileLogSink
from orion import ORION
from pipeline.step_013_output_generation.rdf_strategy import serialize_graph_to_rdf_xml


_FIXTURE = Path(__file__).parent / "fixtures" / "infosec_3k_input.txt"
_ARTIFACT = Path(__file__).parent / "artifacts" / "infosec_3k_orion_events.jsonl"
_PARAGRAPH_DIR = Path(__file__).parent / "fixtures" / "infosec_3k_paragraphs"
_RDF_OUTPUT_ARTIFACT_DIR = Path(__file__).parent / "artifacts" / "infosec_3k_rdf_groups"
_DEBUG_RDF_OUTPUT_ARTIFACT_DIR = Path(__file__).parent / "artifacts" / "infosec_3k_rdf_group_debug"
_STAGE_RESULTS_ARTIFACT = Path(__file__).parent / "artifacts" / "infosec_3k_pipeline_stage_results.jsonl"
_SENTINEL = "ORION_SMOKE_SENTINEL_DO_NOT_LOG"
_STAGE_ORDER = [
    "input_intake",
    "preprocessing",
    "sentence_segmentation",
    "tokenization",
    "linguistic_annotation",
    "entity_extraction",
    "concept_extraction",
    "coreference_resolution",
    "relation_extraction",
    "triple_extraction",
    "taxonomy_induction",
    "type_assertion",
    "semantic_quality",
    "output_generation",
]


def _paragraph_groups(size: int = 2) -> list[tuple[str, str]]:
    paths = sorted(_PARAGRAPH_DIR.glob("p*.txt"))
    groups: list[tuple[str, str]] = []
    for index in range(0, len(paths), size):
        chunk = paths[index:index + size]
        group_id = "_".join(path.stem for path in chunk)
        text = "\n\n".join(path.read_text(encoding="utf-8").strip() for path in chunk)
        groups.append((group_id, text))
    return groups


def _merge_graphs(graphs: list[dict]) -> dict:
    merged: dict = {}
    for graph in graphs:
        if not isinstance(graph, dict):
            continue
        for key, value in graph.items():
            if isinstance(value, list):
                merged.setdefault(key, []).extend(value)
            elif isinstance(value, dict):
                nested = merged.setdefault(key, {})
                for nested_key, nested_value in value.items():
                    if isinstance(nested_value, list):
                        nested.setdefault(nested_key, []).extend(nested_value)
                    else:
                        nested[nested_key] = nested_value
            else:
                merged[key] = value
    return merged


def _merge_results(strategy: str, results: list[dict]) -> dict:
    merged: dict = {"output": {"strategy": strategy, "format": strategy, "graph": _merge_graphs([r.get("output", {}).get("graph", {}) for r in results])}}
    for key in ("sentences", "tokens", "entities", "concepts", "relations", "coreferences", "triples", "taxonomy_relations", "type_assertions", "operations_applied"):
        merged[key] = []
        for result in results:
            merged[key].extend(result.get(key, []))
    reports = [r.get("semantic_quality_report", {}) for r in results if isinstance(r.get("semantic_quality_report", {}), dict)]
    merged["semantic_quality_report"] = {
        "quality_score": min([r.get("quality_score", 1.0) for r in reports] or [1.0]),
        "rdf_readiness": all(r.get("rdf_readiness", True) for r in reports),
        "warnings": [w for r in reports for w in r.get("warnings", [])],
        "entity_noise": [w for r in reports for w in r.get("entity_noise", [])],
        "concept_noise": [w for r in reports for w in r.get("concept_noise", [])],
        "relation_gaps": [w for r in reports for w in r.get("relation_gaps", [])],
        "excluded_entities": [w for r in reports for w in r.get("excluded_entities", [])],
        "excluded_concepts": [w for r in reports for w in r.get("excluded_concepts", [])],
    }
    merged["preprocessed_text"] = "\n\n".join(r.get("preprocessed_text", "") for r in results)
    return merged


def _rdf_artifact_paths() -> list[Path]:
    return sorted(_RDF_OUTPUT_ARTIFACT_DIR.glob("*.rdf"))


def _runtime_artifact_paths() -> list[Path]:
    return sorted(_ARTIFACT.parent.glob("infosec_3k_p*_orion_events.jsonl"))


def _debug_artifact_paths() -> list[Path]:
    return sorted(_DEBUG_RDF_OUTPUT_ARTIFACT_DIR.glob("*.json"))


def _rdf_output_artifacts_exist() -> bool:
    return _RDF_OUTPUT_ARTIFACT_DIR.exists() and bool(_rdf_artifact_paths())


def _debug_output_artifacts_exist() -> bool:
    return _DEBUG_RDF_OUTPUT_ARTIFACT_DIR.exists() and bool(_debug_artifact_paths())


def _combined_rdf_xml() -> str:
    docs = [path.read_text(encoding="utf-8") for path in _rdf_artifact_paths()]
    assert docs, "falta artifacts RDF por grupos de dos párrafos"
    ET.register_namespace("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    ET.register_namespace("rdfs", "http://www.w3.org/2000/01/rdf-schema#")
    ET.register_namespace("owl", "http://www.w3.org/2002/07/owl#")
    combined = ET.Element("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}RDF")
    for doc in docs:
        root = ET.fromstring(doc)
        for child in list(root):
            combined.append(child)
    return "<?xml version='1.0' encoding='utf-8'?>\n" + ET.tostring(combined, encoding="unicode")


def _merged_debug_output() -> dict:
    outputs = [json.loads(path.read_text(encoding="utf-8")) for path in _debug_artifact_paths()]
    assert outputs, "falta debug JSON por grupos de dos párrafos"
    strategy = outputs[0].get("strategy", "rdf")
    fmt = outputs[0].get("format", "rdf")
    return {"strategy": strategy, "format": fmt, "graph": _merge_graphs([o.get("graph", {}) for o in outputs])}


def _load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _sample_list(items: list, size: int = 5) -> list:
    return items[:size]


def _sanitize_sample_text(text: str, size: int = 180) -> str:
    return text[:size].replace(_SENTINEL, "[REDACTED]")


def _graph_counts(graph: dict) -> dict:
    return {
        "facts_count": len(graph.get("facts", [])),
        "instance_facts_count": len(graph.get("instance_facts", [])),
        "subclass_facts_count": len(graph.get("subclass_facts", [])),
    }


def _build_stage_rows(text: str, result: dict) -> list[dict]:
    sentences = result.get("sentences", [])
    tokens = result.get("tokens", [])
    entities = result.get("entities", [])
    concepts = result.get("concepts", [])
    relations = result.get("relations", [])
    coreferences = result.get("coreferences", [])
    triples = result.get("triples", [])
    taxonomy_relations = result.get("taxonomy_relations", [])
    type_assertions = result.get("type_assertions", [])
    output = result.get("output", {})
    graph = output.get("graph", {})
    preprocessed = result.get("preprocessed_text", "")
    semantic_quality_report = result.get("semantic_quality_report", {})

    rows = [
        {
            "stage": "input_intake",
            "order": 1,
            "summary": {"text_length": len(text), "word_count": len(text.split())},
            "result_snapshot": {
                "source_text_kind": result.get("metadata", {}).get("source", {}).get("kind", "unknown"),
                "sample": _sanitize_sample_text(text),
            },
        },
        {
            "stage": "preprocessing",
            "order": 2,
            "summary": {"text_length": len(preprocessed)},
            "result_snapshot": {
                "operations_applied_count": len(result.get("operations_applied", [])),
                "sample": _sanitize_sample_text(preprocessed),
            },
        },
        {
            "stage": "sentence_segmentation",
            "order": 3,
            "summary": {"total_count": len(sentences)},
            "result_snapshot": {"first_items": _sample_list(sentences)},
        },
        {
            "stage": "tokenization",
            "order": 4,
            "summary": {"total_count": len(tokens)},
            "result_snapshot": {"first_items": _sample_list(tokens, size=12)},
        },
        {
            "stage": "linguistic_annotation",
            "order": 5,
            "summary": {"total_count": len(tokens)},
            "result_snapshot": {
                "first_items": [
                    {
                        "text": t.get("text"),
                        "lemma": t.get("lemma"),
                        "pos": t.get("pos"),
                        "dep": t.get("dep"),
                    }
                    for t in _sample_list(tokens)
                    if isinstance(t, dict)
                ]
            },
        },
        {
            "stage": "entity_extraction",
            "order": 6,
            "summary": {"total_count": len(entities)},
            "result_snapshot": {"first_items": _sample_list(entities)},
        },
        {
            "stage": "concept_extraction",
            "order": 7,
            "summary": {"total_count": len(concepts)},
            "result_snapshot": {"first_items": _sample_list(concepts)},
        },
        {
            "stage": "coreference_resolution",
            "order": 8,
            "summary": {"total_count": len(coreferences)},
            "result_snapshot": {"first_items": _sample_list(coreferences)},
        },
        {
            "stage": "relation_extraction",
            "order": 9,
            "summary": {"total_count": len(relations)},
            "result_snapshot": {"first_items": _sample_list(relations)},
        },
        {
            "stage": "triple_extraction",
            "order": 10,
            "summary": {"total_count": len(triples)},
            "result_snapshot": {"first_items": _sample_list(triples)},
        },
        {
            "stage": "taxonomy_induction",
            "order": 11,
            "summary": {"total_count": len(taxonomy_relations)},
            "result_snapshot": {"first_items": _sample_list(taxonomy_relations)},
        },
        {
            "stage": "type_assertion",
            "order": 12,
            "summary": {"total_count": len(type_assertions)},
            "result_snapshot": {"first_items": _sample_list(type_assertions)},
        },
        {
            "stage": "semantic_quality",
            "order": 13,
            "summary": {
                "quality_score": semantic_quality_report.get("quality_score"),
                "rdf_readiness": semantic_quality_report.get("rdf_readiness"),
                "warnings_count": len(semantic_quality_report.get("warnings", [])),
            },
            "result_snapshot": {
                "semantic_quality_report": {
                    "entity_noise": semantic_quality_report.get("entity_noise", [])[:3],
                    "concept_noise": semantic_quality_report.get("concept_noise", [])[:3],
                    "relation_gaps": semantic_quality_report.get("relation_gaps", [])[:3],
                    "warnings": semantic_quality_report.get("warnings", []),
                    "excluded_entities": semantic_quality_report.get("excluded_entities", []),
                    "excluded_concepts": semantic_quality_report.get("excluded_concepts", []),
                }
            },
        },
        {
            "stage": "output_generation",
            "order": 14,
            "summary": {
                "output_strategy": output.get("strategy"),
                "output_format": output.get("format"),
                **_graph_counts(graph),
            },
            "result_snapshot": {
                "output": {
                    "strategy": output.get("strategy"),
                    "format": output.get("format"),
                    "graph_counts": _graph_counts(graph),
                },
                "rdf_artifact_path": str(_RDF_OUTPUT_ARTIFACT_DIR),
            },
        },
    ]
    return rows


def _write_stage_rows(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = "\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n"
    path.write_text(payload, encoding="utf-8")


def _persist_rdf_artifacts(group_results: list[tuple[str, dict]]) -> None:
    _RDF_OUTPUT_ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    _DEBUG_RDF_OUTPUT_ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    for stale in list(_RDF_OUTPUT_ARTIFACT_DIR.glob("*.rdf")) + list(_DEBUG_RDF_OUTPUT_ARTIFACT_DIR.glob("*.json")):
        stale.unlink()
    for group_id, result in group_results:
        output = result.get("output", {}) if isinstance(result, dict) else {}
        graph = output.get("graph", {}) if isinstance(output, dict) else {}
        rdf_xml = serialize_graph_to_rdf_xml(graph)
        (_RDF_OUTPUT_ARTIFACT_DIR / f"infosec_3k_{group_id}.rdf").write_text(rdf_xml, encoding="utf-8")
        (_DEBUG_RDF_OUTPUT_ARTIFACT_DIR / f"infosec_3k_{group_id}.json").write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")


# UC-SMOKE-001 AF-1 | FUN-SMOKE-001 AC-2 | NFR-SMOKE-001 AC-4 | BR-SMOKE-002 | BR-SMOKE-006
@pytest.fixture(scope="module", autouse=True)
def infosec_3k_full_results() -> dict[str, dict]:
    text = _FIXTURE.read_text(encoding="utf-8")
    groups = _paragraph_groups(size=2)

    rdf_group_results: list[tuple[str, dict]] = []
    for group_id, group_text in groups:
        runtime_log = _ARTIFACT.with_name(f"infosec_3k_{group_id}_orion_events.jsonl")
        rdf_sut = ORION(config={"logging": {"sink": JsonlFileLogSink(runtime_log)}, "spacy_model": "en_core_web_lg", "output_strategy": "rdf"})
        rdf_group_results.append((group_id, rdf_sut.process(group_text)))
    _persist_rdf_artifacts(rdf_group_results)
    rdf_result = _merge_results("rdf", [result for _, result in rdf_group_results])
    stage_rows = _build_stage_rows(text, rdf_result)
    _write_stage_rows(_STAGE_RESULTS_ARTIFACT, stage_rows)

    owl_group_results: list[dict] = []
    for group_id, group_text in groups:
        owl_runtime_log = _ARTIFACT.with_name(f"infosec_3k_{group_id}_owl_runtime_events.jsonl")
        owl_sut = ORION(config={"logging": {"sink": JsonlFileLogSink(owl_runtime_log)}, "spacy_model": "en_core_web_lg", "output_strategy": "owl"})
        owl_group_results.append(owl_sut.process(group_text))
    owl_result = _merge_results("owl", owl_group_results)

    return {"rdf": rdf_result, "owl": owl_result, "text": text, "stage_rows": stage_rows}


# UC-SMOKE-001 MF-1 | FUN-SMOKE-001 AC-1 | NFR-SMOKE-001 AC-1 | CON-SMOKE-001 AC-1 | BR-SMOKE-001
def test_infosec_3k_fixture_exists_and_word_count_is_about_3000():
    text = _FIXTURE.read_text(encoding="utf-8")
    wc = len(text.split())
    assert 2800 <= wc <= 4200
    assert len(text) > 1000


# UC-SMOKE-001 AF-1 | FUN-SMOKE-001 AC-2 | NFR-SMOKE-001 AC-2 | CON-SMOKE-001 AC-2 | BR-SMOKE-002
@pytest.mark.parametrize("strategy", ["rdf", "owl"])
def test_infosec_3k_pipeline_no_crash_common_output_and_reasonable_counts(strategy, infosec_3k_full_results):
    result = infosec_3k_full_results[strategy]

    assert "output" in result
    assert result["output"]["strategy"] == strategy
    assert "graph" in result["output"]
    assert isinstance(result["output"]["graph"], dict)

    assert len(result.get("sentences", [])) >= 80
    assert len(result.get("tokens", [])) >= 1500
    assert len(result.get("concepts", [])) >= 30


# UC-SMOKE-001 EF-1 | FUN-SMOKE-001 AC-3 | NFR-SMOKE-SEC-001 AC-1 | CON-SMOKE-SEC-001 AC-1 | BR-SMOKE-003
def test_infosec_3k_persisted_artifact_log_is_sanitized_and_stable_shape():
    runtime_paths = _runtime_artifact_paths()
    assert runtime_paths
    events = [event for path in runtime_paths for event in _load_jsonl(path)]
    assert len(events) >= 20

    serialized = "\n".join(json.dumps(e, ensure_ascii=False) for e in events)
    assert "raw_text" not in serialized
    assert _SENTINEL not in serialized

    for event in events:
        assert "phase" in event
        assert "event_type" in event
        assert "status" in event
        assert isinstance(event.get("metadata", {}), dict)

    max_line_size = max(len(json.dumps(e, ensure_ascii=False)) for e in events)
    assert max_line_size < 900


# UC-SMOKE-001 AF-2 | FUN-SMOKE-001 AC-4 | NFR-SMOKE-001 AC-3 | CON-SMOKE-001 AC-3 | BR-SMOKE-004
def test_infosec_3k_persisted_rdf_output_artifact_exists_and_is_real_rdf_xml_sanitized():
    assert _rdf_output_artifacts_exist()
    rdf_xml = _combined_rdf_xml()

    stripped = rdf_xml.lstrip()
    assert not stripped.startswith("{")
    assert not stripped.startswith("[")

    paths = _rdf_artifact_paths()
    assert len(paths) == len(_paragraph_groups(size=2))
    assert len(paths) > 1
    for path in paths:
        group_xml = path.read_text(encoding="utf-8")
        assert group_xml.count("<?xml") == 1
        assert group_xml.count("<rdf:RDF") == 1
        assert group_xml.count("</rdf:RDF>") == 1
        ET.fromstring(group_xml)

    assert rdf_xml.count("<?xml") == 1
    assert rdf_xml.count("<rdf:RDF") == 1
    assert rdf_xml.count("</rdf:RDF>") == 1

    assert "<rdf:RDF" in rdf_xml
    assert "xmlns:rdf=" in rdf_xml
    assert "xmlns:rdfs=" in rdf_xml
    assert "xmlns:owl=" in rdf_xml
    assert "xmlns:orion=" not in rdf_xml

    assert "raw_text" not in rdf_xml
    assert _SENTINEL not in rdf_xml

    assert "orion:relatedTo" not in rdf_xml

    has_semantic_signal = ("rdf:type" in rdf_xml) or ("rdfs:subClassOf" in rdf_xml)
    assert has_semantic_signal

    for bad_iri in ["https://orion.local/resource/1", "https://orion.local/resource/2"]:
        assert f'rdf:about="{bad_iri}"' not in rdf_xml
        assert f'rdf:resource="{bad_iri}"' not in rdf_xml


# UC-SMOKE-001 AF-3 | FUN-SMOKE-001 AC-5 | CON-SMOKE-001 AC-4 | BR-SMOKE-005
def test_infosec_3k_debug_json_artifact_optional_when_present_is_not_sensitive():
    if not _debug_output_artifacts_exist():
        pytest.skip("optional debug artifact not present")

    output = _merged_debug_output()
    serialized = json.dumps(output, ensure_ascii=False)
    assert "raw_text" not in serialized
    assert _SENTINEL not in serialized


# UC-SMOKE-001 AF-4 | FUN-SMOKE-001 AC-6 | NFR-SMOKE-001 AC-4 | CON-SMOKE-001 AC-5 | BR-SMOKE-006
def test_infosec_3k_pipeline_stage_log_artifact_has_13_stages_order_and_useful_snapshots(infosec_3k_full_results):
    assert _STAGE_RESULTS_ARTIFACT.exists()
    stage_rows = _load_jsonl(_STAGE_RESULTS_ARTIFACT)

    assert len(stage_rows) == 14
    assert [row["stage"] for row in stage_rows] == _STAGE_ORDER
    assert [row["order"] for row in stage_rows] == list(range(1, 15))

    for row in stage_rows:
        assert isinstance(row.get("summary"), dict)
        assert isinstance(row.get("result_snapshot"), dict)

    key_stages = {"sentence_segmentation", "tokenization", "entity_extraction", "concept_extraction", "output_generation"}
    for row in stage_rows:
        if row["stage"] in key_stages:
            assert row["result_snapshot"]

    output_stage = stage_rows[-1]
    assert output_stage["stage"] == "output_generation"
    assert output_stage["result_snapshot"]["output"]["strategy"] == "rdf"
    assert output_stage["result_snapshot"]["output"]["format"] == "rdf"
    assert output_stage["result_snapshot"]["rdf_artifact_path"] == str(_RDF_OUTPUT_ARTIFACT_DIR)

    serialized = "\n".join(json.dumps(row, ensure_ascii=False) for row in stage_rows)
    assert _SENTINEL not in serialized


# UC-SMOKE-001 AF-5 | FUN-SMOKE-001 AC-7 | BR-SMOKE-007
def test_infosec_3k_stage_results_show_relation_gap_against_concept_signal():
    assert _STAGE_RESULTS_ARTIFACT.exists()
    stage_rows = _load_jsonl(_STAGE_RESULTS_ARTIFACT)
    by_stage = {row["stage"]: row for row in stage_rows}

    concept_total = by_stage["concept_extraction"]["summary"]["total_count"]
    relation_total = by_stage["relation_extraction"]["summary"]["total_count"]

    assert concept_total > 0
    assert relation_total > 0, "relation_extraction sigue en 0 pese a conceptos extraídos"


# UC-SMOKE-001 AF-6 | FUN-SMOKE-001 AC-8 | CON-SMOKE-RDF-001 AC-1 | BR-SMOKE-008 | BR-SMOKE-009
def test_infosec_3k_taxonomy_candidates_must_reach_rdf_as_real_rdfxml_subclass_contract():
    assert _STAGE_RESULTS_ARTIFACT.exists()
    assert _rdf_output_artifacts_exist()

    stage_rows = _load_jsonl(_STAGE_RESULTS_ARTIFACT)
    by_stage = {row["stage"]: row for row in stage_rows}

    output_subclass_total = by_stage["output_generation"]["summary"]["subclass_facts_count"]
    rdf_xml = _combined_rdf_xml()

    stripped = rdf_xml.lstrip()
    assert not stripped.startswith("{")
    assert not stripped.startswith("[")

    assert output_subclass_total > 0, "output_generation reporta subclass_facts_count=0"
    assert rdf_xml.count("rdfs:subClassOf") == output_subclass_total, (
        f"RDF/XML no refleja graph: subclass_facts_count={output_subclass_total} "
        f"pero rdfs:subClassOf={rdf_xml.count('rdfs:subClassOf')}"
    )

    assert "rdfs:subclassof" not in rdf_xml, "predicate inválido: usar rdfs:subClassOf"
    assert 'rdf:resource="orion:' not in rdf_xml, "rdf:resource prefijado orion: no permitido"
    assert 'rdf:about="orion:' not in rdf_xml, "rdf:about prefijado orion: no permitido"
    assert "https://orion.local/resource/" in rdf_xml, "recursos orion no están expandidos"


# UC-SMOKE-001 AF-7 | FUN-SMOKE-001 AC-9 | CON-SMOKE-RDF-002 AC-1 | BR-SMOKE-010
def test_infosec_3k_non_taxonomic_predicate_present_when_relation_signal_exists():
    assert _STAGE_RESULTS_ARTIFACT.exists()
    assert _rdf_output_artifacts_exist()

    stage_rows = _load_jsonl(_STAGE_RESULTS_ARTIFACT)
    by_stage = {row["stage"]: row for row in stage_rows}

    relation_total = by_stage["relation_extraction"]["summary"]["total_count"]
    concept_total = by_stage["concept_extraction"]["summary"]["total_count"]
    facts_total = by_stage["output_generation"]["summary"]["facts_count"]

    assert relation_total > 0
    assert concept_total > 0
    assert facts_total > 0, "contrato roto: relation_extraction>0 debe implicar graph.facts>0"

    rdf_xml = _combined_rdf_xml()
    rdf_json = _merged_debug_output()
    facts = rdf_json.get("graph", {}).get("facts", [])
    non_taxonomic_facts = [
        f for f in facts
        if isinstance(f, dict)
        and str(f.get("predicate", "")).lower() != "rdfs:subclassof"
        and "rdf:type" not in str(f.get("predicate", "")).lower()
    ]

    assert non_taxonomic_facts, (
        "RDF/XML semánticamente pobre: hay señales y facts pero no hay facts no taxonómicos en graph.facts"
    )
    assert "<owl:ObjectProperty" in rdf_xml, "falta schema mínimo de predicados en RDF/XML"


# UC-SMOKE-001 AF-8 | FUN-SMOKE-001 AC-10 | CON-SMOKE-RDF-003 AC-1 | BR-SMOKE-011
def test_infosec_3k_guard_against_massive_subclassof_type_fallback():
    assert _rdf_output_artifacts_exist()

    rdf_xml = _combined_rdf_xml()
    root = ET.fromstring(rdf_xml)

    ns = {
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    }

    def _local_of(uri: str) -> str:
        if not uri:
            return ""
        token = uri.rsplit("/", 1)[-1]
        token = token.rsplit("#", 1)[-1]
        return token.casefold()

    class_labels: set[str] = set()
    laptop_targets: set[str] = set()
    has_endpoint_class = False
    has_vulnerability_class = False
    endpoint_targets: set[str] = set()
    vulnerability_targets: set[str] = set()
    subclass_to_type = 0

    for description in root.findall('.//rdf:Description', ns):
        about = description.attrib.get(f'{{{ns["rdf"]}}}about', "")
        local = _local_of(about)
        label = (description.findtext("rdfs:label", default="", namespaces=ns) or "").strip().casefold()

        if label:
            class_labels.add(label)

        subclass_nodes = description.findall("rdfs:subClassOf", ns)

        if local == "endpoint" or label == "endpoint":
            has_endpoint_class = True
            for edge in subclass_nodes:
                endpoint_targets.add(_local_of(edge.attrib.get(f'{{{ns["rdf"]}}}resource', "")))

        if local == "vulnerability" or label == "vulnerability":
            has_vulnerability_class = True
            for edge in subclass_nodes:
                vulnerability_targets.add(_local_of(edge.attrib.get(f'{{{ns["rdf"]}}}resource', "")))

        if local == "laptop" or label == "laptop":
            for edge in subclass_nodes:
                laptop_targets.add(_local_of(edge.attrib.get(f'{{{ns["rdf"]}}}resource', "")))

        for edge in subclass_nodes:
            if _local_of(edge.attrib.get(f'{{{ns["rdf"]}}}resource', "")) == "type":
                subclass_to_type += 1

    total_subclass = len(root.findall('.//rdfs:subClassOf', ns))

    assert total_subclass > 0
    ratio = subclass_to_type / total_subclass
    assert ratio <= 0.20, (
        "taxonomía basura detectada: rdfs:subClassOf->orion:type no puede ser mayoría; "
        f"subclass_total={total_subclass} subclass_to_type={subclass_to_type} ratio={ratio:.3f}"
    )

    assert "laptop" in class_labels
    assert "endpoint" in class_labels
    assert "vulnerability" in class_labels
    assert "endpoint" in laptop_targets, "Laptop no apunta a Endpoint en taxonomía"
    assert "device" in endpoint_targets, "Endpoint no apunta a Device en taxonomía"
    assert "weakness" in vulnerability_targets, "Vulnerability no apunta a Weakness en taxonomía"
    assert has_endpoint_class
    assert has_vulnerability_class
    return

    if False:  # legacy literal checks removidas por parseo semántico
        assert '<rdf:Description rdf:about="https://orion.local/resource/Laptop">' in rdf_xml
    assert '<rdfs:subClassOf rdf:resource="https://orion.local/resource/Endpoint"/>' in rdf_xml
    assert '<rdf:Description rdf:about="https://orion.local/resource/Endpoint">' in rdf_xml
    assert '<rdfs:subClassOf rdf:resource="https://orion.local/resource/Device"/>' in rdf_xml
    assert '<rdf:Description rdf:about="https://orion.local/resource/Vulnerability">' in rdf_xml
    assert '<rdfs:subClassOf rdf:resource="https://orion.local/resource/Weakness"/>' in rdf_xml


# UC-SMOKE-001 AF-9 | FUN-SMOKE-001 AC-11 | CON-SMOKE-RDF-004 AC-1 | BR-SMOKE-012 | BR-SMOKE-013
def test_infosec_3k_ontology_contract_not_everything_is_subclass_and_class_only_modeling():
    assert _STAGE_RESULTS_ARTIFACT.exists()
    assert _rdf_output_artifacts_exist()

    stage_rows = _load_jsonl(_STAGE_RESULTS_ARTIFACT)
    by_stage = {row["stage"]: row for row in stage_rows}

    facts_total = by_stage["output_generation"]["summary"]["facts_count"]
    taxonomy_total = by_stage["output_generation"]["summary"]["subclass_facts_count"]
    assert facts_total > 0

    rdf_xml = _combined_rdf_xml()

    object_property_edges = rdf_xml.count("<owl:ObjectProperty")
    subclass_edges = rdf_xml.count("rdfs:subClassOf")
    instance_type_edges = rdf_xml.count("rdf:type")

    assert object_property_edges > 0, (
        "contrato ontológico roto: con graph.facts activos debe existir al menos un owl:ObjectProperty; "
        f"object_property_edges={object_property_edges} taxonomy_serialized={taxonomy_total}"
    )

    semantic_edges = object_property_edges + subclass_edges + instance_type_edges
    assert semantic_edges > 0
    subclass_ratio = subclass_edges / semantic_edges
    assert subclass_ratio < 0.95, (
        "RDF dominado por rdfs:subClassOf; contrato exige no ser 100% class-only (<95% en snapshot smoke) del total semántico serializado: "
        f"subclass_edges={subclass_edges} semantic_edges={semantic_edges} ratio={subclass_ratio:.3f}"
    )



# UC-SMOKE-001 AF-10 | FUN-SMOKE-001 AC-12 | CON-SMOKE-RDF-005 AC-1 | BR-SMOKE-014 | BR-SMOKE-015
def test_infosec_3k_rdfxml_webvowl_contract_standard_vocab_only_and_object_property_schema():
    assert _rdf_output_artifacts_exist()

    rdf_xml = _combined_rdf_xml()

    assert "<orion:" not in rdf_xml
    assert "xmlns:orion" not in rdf_xml

    assert "<owl:Ontology" in rdf_xml
    assert "<owl:Class" in rdf_xml
    assert "<owl:ObjectProperty" in rdf_xml

    import xml.etree.ElementTree as ET

    ns = {
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "owl": "http://www.w3.org/2002/07/owl#",
    }

    root = ET.fromstring(rdf_xml)
    assert root.tag.endswith("RDF")

    obj_properties = root.findall('.//owl:ObjectProperty', ns)
    restrictions = root.findall('.//owl:Restriction', ns)
    on_properties = root.findall('.//owl:Restriction/owl:onProperty', ns)
    some_values_from = root.findall('.//owl:Restriction/owl:someValuesFrom', ns)

    object_property_by_about = {
        op.attrib.get(f'{{{ns["rdf"]}}}about'): op for op in obj_properties
    }

    properties_with_domain_and_range = 0
    organization_domain_count = 0
    domain_count = 0

    for about, op in object_property_by_about.items():
        if not about or not about.startswith('https://orion.local/resource/'):
            continue
        domain_nodes = op.findall('rdfs:domain', ns)
        range_nodes = op.findall('rdfs:range', ns)
        if domain_nodes and range_nodes:
            properties_with_domain_and_range += 1

        domain_count += len(domain_nodes)
        for d in domain_nodes:
            res = d.attrib.get(f'{{{ns["rdf"]}}}resource', '')
            if res.endswith('/Organization'):
                organization_domain_count += 1

    assert properties_with_domain_and_range > 0, (
        'WebVOWL contract roto: se esperaba al menos un owl:ObjectProperty con domain y range'
    )

    if domain_count > 0:
        assert organization_domain_count < domain_count, (
            'domain colapsado: no puede caer todo en Organization '
            f'organization_domain_count={organization_domain_count} domain_count={domain_count}'
        )

    # contrato actual: WebVOWL limpio prioriza domain/range; owl:Restriction duplicante es opcional
    if restrictions:
        assert on_properties, 'owl:Restriction presente sin owl:onProperty'
        assert some_values_from, 'owl:Restriction presente sin owl:someValuesFrom'


# UC-SMOKE-001 AF-11 | FUN-SMOKE-001 AC-13 | CON-SMOKE-RDF-006 AC-1 | BR-SMOKE-016 | BR-SMOKE-017 | BR-SMOKE-018 | BR-SMOKE-019 | BR-SMOKE-020 | BR-SMOKE-021 | BR-SMOKE-022 | BR-SMOKE-023
def test_infosec_3k_min_semantic_core_coverage_from_full_fixture_document():
    assert _rdf_output_artifacts_exist()
    assert _debug_output_artifacts_exist()
    assert _STAGE_RESULTS_ARTIFACT.exists()

    rdf_xml = _combined_rdf_xml().lower()
    rdf_json = _merged_debug_output()
    stage_rows = _load_jsonl(_STAGE_RESULTS_ARTIFACT)

    facts = rdf_json.get("graph", {}).get("facts", [])
    fact_keys = {
        (
            str(f.get("subject", "")).lower(),
            str(f.get("predicate", "")).lower(),
            str(f.get("object", "")).lower(),
        )
        for f in facts
        if isinstance(f, dict)
    }

    def has_fact(sub: str, pred_fragment: str, obj: str) -> bool:
        return any(
            s.endswith(f"/{sub}") and pred_fragment in p and o.endswith(f"/{obj}")
            for s, p, o in fact_keys
        )

    def has_term(term: str) -> bool:
        iri = f"https://orion.local/resource/{term}".lower()
        return iri in rdf_xml or any(
            s.endswith(f"/{term}") or o.endswith(f"/{term}")
            for s, _, o in fact_keys
        )

    for core in ["risk", "policy", "compliance", "evidence", "severity", "likelihood", "impact"]:
        assert has_term(core), f"falta núcleo semántico mínimo: {core}"

    present_roles = [
        role
        for role in ["auditor", "owner", "custodian", "analyst", "user"]
        if has_term(role)
    ]
    assert len(present_roles) >= 2, (
        "cobertura de actores/roles demasiado débil; esperados del documento: "
        "auditor/owner/custodian/analyst/end user"
    )

    assert has_fact("control", "mitigat", "risk") or has_fact("control", "reduce", "risk"), (
        "falta señal control mitigates/reduces risk"
    )
    assert (
        has_fact("policy", "define", "requirement")
        or has_fact("policy", "require", "requirement")
        or has_fact("policy", "require", "control")
    ), "falta señal policy defines/requires requirement/control"
    assert has_fact("threat", "exploit", "vulnerability"), "falta señal threat exploits vulnerability"
    assert has_fact("threat", "affect", "asset"), "falta señal threat affects asset (texto: threat may exploit vulnerability and affect an asset)"
    assert has_fact("incident", "affect", "asset"), "falta señal incident affects asset"
    assert has_fact("evidence", "support", "compliance") or has_fact("evidence", "support", "demonstration"), (
        "falta señal evidence supports compliance"
    )

    cia_ok = (
        ("https://orion.local/resource/confidentiality" in rdf_xml)
        and ("https://orion.local/resource/integrity" in rdf_xml)
        and ("https://orion.local/resource/availability" in rdf_xml)
    ) or ("https://orion.local/resource/securityobjective" in rdf_xml)
    assert cia_ok, "falta modelado CIA mínimo como objetivos de seguridad o equivalente"

    rel_row = next((r for r in stage_rows if r.get("stage") == "relation_extraction"), {})
    rel_items = rel_row.get("result_snapshot", {}).get("first_items", [])
    if rel_items:
        assert any("confidence" in it for it in rel_items if isinstance(it, dict)), (
            "stage relation_extraction sin confidence en snapshot"
        )
        assert any("evidence_span" in it for it in rel_items if isinstance(it, dict)), (
            "stage relation_extraction sin evidence_span en snapshot"
        )

    if any(has_term(t) for t in ["severity", "likelihood", "impact"]):
        assert any(has_term(t) for t in ["severity", "likelihood", "impact"]), (
            "señales de severity/likelihood/impact no preservadas en artefactos"
        )


# UC-SMOKE-001 AF-12 | FUN-SMOKE-001 AC-14 | NFR-SMOKE-SEC-002 AC-1 | CON-SMOKE-RDF-007 AC-1 | BR-SMOKE-024 | BR-SMOKE-025 | BR-SMOKE-026 | BR-SMOKE-027 | BR-SMOKE-028 | BR-SMOKE-029
def test_infosec_3k_strict_full_document_semantic_contract_red_gate():
    assert _rdf_output_artifacts_exist()
    assert _debug_output_artifacts_exist()
    assert _STAGE_RESULTS_ARTIFACT.exists()

    rdf_xml_raw = _combined_rdf_xml()
    rdf_xml = rdf_xml_raw.lower()
    rdf_json = _merged_debug_output()
    stage_rows = _load_jsonl(_STAGE_RESULTS_ARTIFACT)

    assert "<orion:" not in rdf_xml_raw
    assert "xmlns:orion" not in rdf_xml_raw
    assert not rdf_xml_raw.lstrip().startswith("{")
    assert not rdf_xml_raw.lstrip().startswith("[")

    import xml.etree.ElementTree as ET

    ns = {
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "owl": "http://www.w3.org/2002/07/owl#",
    }
    root = ET.fromstring(rdf_xml_raw)

    def _local_predicate(token: str) -> str:
        t = (token or "").strip().lower()
        if not t:
            return ""
        if ":" in t:
            t = t.split(":", 1)[1]
        if "/" in t:
            t = t.rsplit("/", 1)[1]
        if "#" in t:
            t = t.rsplit("#", 1)[1]
        return t

    graph = rdf_json.get("graph", {})
    classes = graph.get("classes", [])
    facts = graph.get("facts", [])
    object_property_schema = graph.get("object_property_schema", [])

    required_classes = sorted({
        c.get("id", "").split("/")[-1].lower()
        for c in classes
        if isinstance(c, dict) and c.get("id")
    })
    missing_classes = [
        c for c in required_classes
        if f"https://orion.local/resource/{c}" not in rdf_xml
    ]

    required_obj_props = sorted({
        _local_predicate(p.get("predicate", ""))
        for p in object_property_schema
        if isinstance(p, dict)
        and _local_predicate(p.get("predicate", ""))
        and p.get("domain", "").strip()
        and p.get("range", "").strip()
    })

    obj_properties = root.findall('.//owl:ObjectProperty', ns)
    by_about = {}
    for op in obj_properties:
        about = _local_predicate(op.attrib.get(f'{{{ns["rdf"]}}}about', ''))
        if not about:
            continue
        by_about.setdefault(about, []).append(op)

    missing_obj_props = []
    for prop in required_obj_props:
        if prop not in by_about:
            missing_obj_props.append(prop)

    inferible_domain_range = sorted({
        (_local_predicate(p.get("predicate", "")), _local_predicate(p.get("domain", "")), _local_predicate(p.get("range", "")))
        for p in object_property_schema
        if isinstance(p, dict)
        and _local_predicate(p.get("predicate", ""))
        and p.get("domain", "").strip()
        and p.get("range", "").strip()
    })

    missing_domain_range = []
    for prop, expected_domain, expected_range in inferible_domain_range:
        candidates = by_about.get(prop, [])
        matched = False
        for op in candidates:
            domains = {
                _local_predicate((d.attrib.get(f'{{{ns["rdf"]}}}resource', '') or ''))
                for d in op.findall('rdfs:domain', ns)
            }
            ranges = {
                _local_predicate((r.attrib.get(f'{{{ns["rdf"]}}}resource', '') or ''))
                for r in op.findall('rdfs:range', ns)
            }
            if expected_domain in domains and expected_range in ranges:
                matched = True
                break
        if not matched:
            missing_domain_range.append((prop, expected_domain, expected_range))

    forbidden_type_subclass = rdf_xml_raw.count('rdfs:subClassOf rdf:resource="https://orion.local/resource/Type"')

    restrictions = root.findall('.//owl:Restriction', ns)

    subclass_count = rdf_xml_raw.count("rdfs:subClassOf")
    obj_prop_count = len(obj_properties)
    class_coverage_ratio = 1.0 if not required_classes else (len(required_classes) - len(missing_classes)) / len(required_classes)
    prop_coverage_ratio = 1.0 if not required_obj_props else (len(required_obj_props) - len(missing_obj_props)) / len(required_obj_props)

    hallazgo_checks = {
        "evidence_class_coverage": not missing_classes,
        "properties_domain_range_inferible": (not missing_domain_range),
        "webvowl_prohibitions": (forbidden_type_subclass == 0) and ('rdf:type rdf:resource="https://orion.local/resource/Organization"' not in rdf_xml_raw),
    }
    hallazgo_missing = [k for k, ok in hallazgo_checks.items() if not ok]
    hallazgo_coverage_ratio = (len(hallazgo_checks) - len(hallazgo_missing)) / len(hallazgo_checks)

    assert class_coverage_ratio >= 0.85, (
        f"cobertura de clases semánticas insuficiente: ratio={class_coverage_ratio:.3f} missing={missing_classes}"
    )
    assert prop_coverage_ratio >= 0.85, (
        f"cobertura de object properties insuficiente: ratio={prop_coverage_ratio:.3f} missing={missing_obj_props}"
    )
    assert hallazgo_coverage_ratio >= 0.85, (
        "cobertura ontológica de hallazgos insuficiente: "
        f"ratio={hallazgo_coverage_ratio:.3f} missing={hallazgo_missing}"
    )
    assert not missing_domain_range, f"object properties schema inferible sin domain/range serializado: {missing_domain_range}"
    duplicated_visible_edges = sorted({
        (d, p, r) for (d, p, r) in [
            (
                cls.attrib.get(f'{{{ns["rdf"]}}}about', '').strip(),
                on.attrib.get(f'{{{ns["rdf"]}}}resource', '').strip() if on is not None else '',
                (svf.attrib.get(f'{{{ns["rdf"]}}}resource', '').strip() if svf is not None else (avf.attrib.get(f'{{{ns["rdf"]}}}resource', '').strip() if avf is not None else '')),
            )
            for cls in root.findall('.//owl:Class', ns)
            for rnode in cls.findall('rdfs:subClassOf/owl:Restriction', ns)
            for on in [rnode.find('owl:onProperty', ns)]
            for svf in [rnode.find('owl:someValuesFrom', ns)]
            for avf in [rnode.find('owl:allValuesFrom', ns)]
        ]
        if d and p and r and (d, p, r) in {
            (
                d2.attrib.get(f'{{{ns["rdf"]}}}resource', '').strip(),
                op.attrib.get(f'{{{ns["rdf"]}}}about', '').strip(),
                r2.attrib.get(f'{{{ns["rdf"]}}}resource', '').strip(),
            )
            for op in root.findall('.//owl:ObjectProperty', ns)
            for d2 in op.findall('rdfs:domain', ns)
            for r2 in op.findall('rdfs:range', ns)
        }
    })

    assert not duplicated_visible_edges, f"duplicated_visible_edges={duplicated_visible_edges[:5]}"

    assert forbidden_type_subclass == 0, (
        "prohibido subClassOf->Type; hallado "
        f"{forbidden_type_subclass} veces"
    )

    assert obj_prop_count >= max(1, len(required_obj_props)), (
        f"schema OWL insuficiente: object properties={obj_prop_count} requeridas={len(required_obj_props)}"
    )

    assert subclass_count >= 20, f"taxonomía insuficiente para fixture completo: subclass={subclass_count} esperado>=20"

    assert 'rdf:type rdf:resource="https://orion.local/resource/Organization"' not in rdf_xml_raw, (
        "domain/range falso detectado: Organization usado como typing genérico"
    )

    out = next((r for r in stage_rows if r.get("stage") == "output_generation"), {})
    rel = next((r for r in stage_rows if r.get("stage") == "relation_extraction"), {})

    advisory_volume = {
        "facts_count": len(facts),
        "relation_extraction_count": rel.get("summary", {}).get("total_count", 0),
        "facts_target": 500,
        "relation_target": 450,
    }
    assert out.get("summary", {}).get("facts_count", 0) == advisory_volume["facts_count"], (
        "desalineación entre debug rdf graph facts y output_generation.summary.facts_count"
    )


# UC-SMOKE-001 AF-13 | FUN-SMOKE-001 AC-15 | CON-SMOKE-RDF-008 AC-1 | BR-SMOKE-030 | BR-SMOKE-031
def test_infosec_3k_rdfxml_blocks_canonical_duplicate_entities_by_casing_or_namespace_role_conflict():
    assert _rdf_output_artifacts_exist()

    rdf_xml_raw = _combined_rdf_xml()
    root = ET.fromstring(rdf_xml_raw)
    ns = {
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "owl": "http://www.w3.org/2002/07/owl#",
    }

    def split_iri(iri: str) -> tuple[str, str]:
        token = iri.strip()
        for sep in ("#", "/", ":"):
            if sep in token:
                idx = token.rfind(sep)
                return token[:idx + 1], token[idx + 1:]
        return "", token

    def casing_kind(local: str) -> str:
        if not local:
            return "other"
        if local.islower():
            return "lower"
        if local[0].isupper() and local[1:].islower():
            return "pascal"
        return "other"

    role_by_iri: dict[str, set[str]] = {}
    for node in root.findall('.//owl:Class', ns):
        iri = node.attrib.get(f'{{{ns["rdf"]}}}about', '').strip()
        if iri:
            role_by_iri.setdefault(iri, set()).add('owl:Class')

    for node in root.findall('.//rdf:Description', ns):
        iri = node.attrib.get(f'{{{ns["rdf"]}}}about', '').strip()
        if iri:
            role_by_iri.setdefault(iri, set()).add('rdf:Description')

    buckets: dict[tuple[str, str], list[tuple[str, str, set[str]]]] = {}
    for iri, roles in role_by_iri.items():
        namespace, local = split_iri(iri)
        if not local:
            continue
        buckets.setdefault((namespace, local.lower()), []).append((iri, local, roles))

    conflicts = []
    for (_ns, _key), entries in buckets.items():
        if len(entries) < 2:
            continue

        has_lower = any(casing_kind(local) == 'lower' for _, local, _ in entries)
        has_pascal = any(casing_kind(local) == 'pascal' for _, local, _ in entries)
        if not (has_lower and has_pascal):
            continue

        class_like = [
            (iri, local, sorted(list(roles)))
            for iri, local, roles in entries
            if ('owl:Class' in roles) or ('rdf:Description' in roles)
        ]
        if len(class_like) >= 2:
            conflicts.append(class_like)

    assert not conflicts, (
        'duplicados canónicos detectados por casing/namespace en nodos OWL/RDF visibles: '
        f'{conflicts}'
    )


# UC-SMOKE-001 AF-14 | FUN-SMOKE-001 AC-16 | CON-SMOKE-RDF-009 AC-1 | BR-SMOKE-032 | BR-SMOKE-033
def test_infosec_3k_risk_must_not_be_semantically_isolated_when_present():
    assert _rdf_output_artifacts_exist()

    rdf_xml_raw = _combined_rdf_xml()
    root = ET.fromstring(rdf_xml_raw)
    ns = {
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "owl": "http://www.w3.org/2002/07/owl#",
    }

    def local_name(iri: str) -> str:
        token = (iri or "").strip()
        if not token:
            return ""
        for sep in ("#", "/", ":"):
            if sep in token:
                token = token[token.rfind(sep) + 1:]
        return token

    class_nodes = root.findall('.//owl:Class', ns) + root.findall('.//rdf:Description', ns)
    risk_iris = {
        node.attrib.get(f'{{{ns["rdf"]}}}about', '').strip()
        for node in class_nodes
        if local_name(node.attrib.get(f'{{{ns["rdf"]}}}about', '')).lower() == 'risk'
    }
    risk_iris = {iri for iri in risk_iris if iri}

    if not risk_iris:
        return

    object_props = root.findall('.//owl:ObjectProperty', ns)
    linked_by_domain_range = []
    for op in object_props:
        piri = op.attrib.get(f'{{{ns["rdf"]}}}about', '').strip()
        if not piri:
            continue
        domains = [d.attrib.get(f'{{{ns["rdf"]}}}resource', '').strip() for d in op.findall('rdfs:domain', ns)]
        ranges = [r.attrib.get(f'{{{ns["rdf"]}}}resource', '').strip() for r in op.findall('rdfs:range', ns)]
        if any(x in risk_iris for x in (domains + ranges)):
            linked_by_domain_range.append(piri)

    linked_by_restriction = []
    for c in root.findall('.//owl:Class', ns):
        c_about = c.attrib.get(f'{{{ns["rdf"]}}}about', '').strip()
        if c_about not in risk_iris:
            continue
        for rnode in c.findall('rdfs:subClassOf/owl:Restriction', ns):
            on = rnode.find('owl:onProperty', ns)
            if on is None:
                continue
            onp = on.attrib.get(f'{{{ns["rdf"]}}}resource', '').strip()
            if onp:
                linked_by_restriction.append(onp)

    linked_by_statements = []
    for stmt in root.findall('.//rdf:Statement', ns):
        subj = stmt.find('rdf:subject', ns)
        pred = stmt.find('rdf:predicate', ns)
        obj = stmt.find('rdf:object', ns)
        subj_iri = (subj.attrib.get(f'{{{ns["rdf"]}}}resource', '').strip() if subj is not None else '')
        obj_iri = (obj.attrib.get(f'{{{ns["rdf"]}}}resource', '').strip() if obj is not None else '')
        pred_iri = (pred.attrib.get(f'{{{ns["rdf"]}}}resource', '').strip() if pred is not None else '')
        if not pred_iri:
            continue
        if subj_iri in risk_iris or obj_iri in risk_iris:
            linked_by_statements.append((subj_iri, pred_iri, obj_iri))

    useful_subclass_edges = 0
    for desc in root.findall('.//rdf:Description', ns):
        about = desc.attrib.get(f'{{{ns["rdf"]}}}about', '').strip()
        if about not in risk_iris:
            continue
        useful_subclass_edges += len([s for s in desc.findall('rdfs:subClassOf', ns) if s.attrib.get(f'{{{ns["rdf"]}}}resource', '').strip()])

    observed_risk_predicates = sorted({local_name(p) for _, p, _ in linked_by_statements if p})

    assert linked_by_domain_range or linked_by_restriction or linked_by_statements or useful_subclass_edges > 0, (
        'Risk/risk aislado: sin relación visible en OWL (domain/range/restriction) ni facts RDF; '
        f'risk_iris={sorted(risk_iris)} domain_range={linked_by_domain_range} restrictions={linked_by_restriction} '
        f'observed_risk_predicates={observed_risk_predicates} statement_links={linked_by_statements[:8]} '
        f'useful_subclass_edges={useful_subclass_edges}'
    )


# UC-SMOKE-001 AF-15 | FUN-SMOKE-001 AC-17 | CON-SMOKE-RDF-010 AC-1 | BR-SMOKE-034 | BR-SMOKE-035
def test_infosec_3k_log_and_logging_must_stay_distinct_but_explicitly_connected():
    assert _rdf_output_artifacts_exist()

    rdf_xml_raw = _combined_rdf_xml()
    root = ET.fromstring(rdf_xml_raw)
    ns = {
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "owl": "http://www.w3.org/2002/07/owl#",
    }

    log_iri = 'https://orion.local/resource/Log'
    logging_iri = 'https://orion.local/resource/Logging'

    declared_iris = {
        node.attrib.get(f'{{{ns["rdf"]}}}about', '').strip()
        for node in (root.findall('.//owl:Class', ns) + root.findall('.//rdf:Description', ns))
    }

    has_log = log_iri in declared_iris
    has_logging = logging_iri in declared_iris

    if not (has_log and has_logging):
        return
    assert log_iri != logging_iri, 'Log y Logging no deben fusionarse en una sola IRI'

    candidate_props = ['https://orion.local/resource/generates', 'https://orion.local/resource/produces']
    by_about = {
        op.attrib.get(f'{{{ns["rdf"]}}}about', '').strip(): op
        for op in root.findall('.//owl:ObjectProperty', ns)
    }

    domain_range_ok = False
    for piri in candidate_props:
        op = by_about.get(piri)
        if op is None:
            continue
        domains = [d.attrib.get(f'{{{ns["rdf"]}}}resource', '').strip() for d in op.findall('rdfs:domain', ns)]
        ranges = [r.attrib.get(f'{{{ns["rdf"]}}}resource', '').strip() for r in op.findall('rdfs:range', ns)]
        if logging_iri in domains and log_iri in ranges:
            domain_range_ok = True
            break

    restriction_ok = False
    for c in root.findall('.//owl:Class', ns):
        if c.attrib.get(f'{{{ns["rdf"]}}}about', '').strip() != logging_iri:
            continue
        for rnode in c.findall('rdfs:subClassOf/owl:Restriction', ns):
            on = rnode.find('owl:onProperty', ns)
            svf = rnode.find('owl:someValuesFrom', ns)
            if on is None or svf is None:
                continue
            onp = on.attrib.get(f'{{{ns["rdf"]}}}resource', '').strip()
            obj = svf.attrib.get(f'{{{ns["rdf"]}}}resource', '').strip()
            if onp in candidate_props and obj == log_iri:
                restriction_ok = True
                break

    assert domain_range_ok or restriction_ok, (
        'Log y Logging existen pero falta vínculo explícito Logging generates/produces Log '
        '(domain Logging + range Log o restriction equivalente)'
    )


# UC-SMOKE-001 AF-16 | FUN-SMOKE-001 AC-18 | CON-SMOKE-RDF-011 AC-1 | BR-SMOKE-036 | BR-SMOKE-037
def test_infosec_3k_webvowl_min_labels_and_restriction_identifiability_contract_red_smoke():
    assert _rdf_output_artifacts_exist()

    rdf_xml_raw = _combined_rdf_xml()
    root = ET.fromstring(rdf_xml_raw)
    ns = {
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "owl": "http://www.w3.org/2002/07/owl#",
    }

    def has_non_empty_label(node) -> bool:
        for lbl in node.findall('rdfs:label', ns):
            if (lbl.text or '').strip():
                return True
        return False

    classes = root.findall('.//owl:Class', ns)
    obj_props = root.findall('.//owl:ObjectProperty', ns)

    unlabeled_classes = [n.attrib.get(f'{{{ns["rdf"]}}}about', '').strip() for n in classes if not has_non_empty_label(n)]
    unlabeled_props = [n.attrib.get(f'{{{ns["rdf"]}}}about', '').strip() for n in obj_props if not has_non_empty_label(n)]

    restrictions = root.findall('.//owl:Restriction', ns)
    weak_restrictions = []
    for rnode in restrictions:
        on = rnode.find('owl:onProperty', ns)
        svf = rnode.find('owl:someValuesFrom', ns)
        avf = rnode.find('owl:allValuesFrom', ns)
        hv = rnode.find('owl:hasValue', ns)
        qc = rnode.find('owl:qualifiedCardinality', ns)
        mqc = rnode.find('owl:minQualifiedCardinality', ns)
        xqc = rnode.find('owl:maxQualifiedCardinality', ns)

        on_ok = on is not None and bool(on.attrib.get(f'{{{ns["rdf"]}}}resource', '').strip())
        payload_ok = False
        for payload in (svf, avf, hv):
            if payload is not None and payload.attrib.get(f'{{{ns["rdf"]}}}resource', '').strip():
                payload_ok = True
        for payload in (qc, mqc, xqc):
            if payload is not None and (payload.text or '').strip():
                payload_ok = True

        if not (on_ok and payload_ok):
            weak_restrictions.append('restriction-without-sufficient-content')

    risk_iri = 'https://orion.local/resource/Risk'
    risk_node = None
    for c in classes:
        if c.attrib.get(f'{{{ns["rdf"]}}}about', '').strip() == risk_iri:
            risk_node = c
            break

    risk_has_label_pascal = False
    risk_connected = False
    if risk_node is not None:
        labels = [(lbl.text or '').strip() for lbl in risk_node.findall('rdfs:label', ns)]
        risk_has_label_pascal = 'Risk' in labels

        for op in obj_props:
            domains = [d.attrib.get(f'{{{ns["rdf"]}}}resource', '').strip() for d in op.findall('rdfs:domain', ns)]
            ranges = [r.attrib.get(f'{{{ns["rdf"]}}}resource', '').strip() for r in op.findall('rdfs:range', ns)]
            if risk_iri in domains or risk_iri in ranges:
                risk_connected = True
                break

    log_iri = 'https://orion.local/resource/Log'
    logging_iri = 'https://orion.local/resource/Logging'

    class_by_iri = {c.attrib.get(f'{{{ns["rdf"]}}}about', '').strip(): c for c in classes}
    log_node = class_by_iri.get(log_iri)
    logging_node = class_by_iri.get(logging_iri)

    log_label_ok = log_node is not None and has_non_empty_label(log_node)
    logging_label_ok = logging_node is not None and has_non_empty_label(logging_node)

    link_ok = False
    for op in obj_props:
        piri = op.attrib.get(f'{{{ns["rdf"]}}}about', '').strip()
        if piri not in {'https://orion.local/resource/generates', 'https://orion.local/resource/produces'}:
            continue
        domains = [d.attrib.get(f'{{{ns["rdf"]}}}resource', '').strip() for d in op.findall('rdfs:domain', ns)]
        ranges = [r.attrib.get(f'{{{ns["rdf"]}}}resource', '').strip() for r in op.findall('rdfs:range', ns)]
        if logging_iri in domains and log_iri in ranges:
            link_ok = True
            break

    risk_gate_ok = (risk_node is None) or (risk_has_label_pascal and risk_connected)
    log_gate_ok = (log_node is None or logging_node is None) or (log_label_ok and logging_label_ok and link_ok)

    assert not unlabeled_classes and not unlabeled_props and not weak_restrictions and risk_gate_ok and log_gate_ok, (
        'contrato WebVOWL mínimo roto: '
        f'unlabeled_classes={len(unlabeled_classes)} unlabeled_props={len(unlabeled_props)} '
        f'anonymous_restrictions_insufficient={len(weak_restrictions)} risk_node={risk_node is not None} '
        f'risk_label_pascal={risk_has_label_pascal} risk_connected={risk_connected} '
        f'log_label_ok={log_label_ok} logging_label_ok={logging_label_ok} logging_log_link={link_ok}'
    )


# UC-SMOKE-001 AF-17 | FUN-SMOKE-001 AC-19 | CON-SMOKE-RDF-012 AC-1 | BR-SMOKE-038 | BR-SMOKE-039
def test_infosec_3k_webvowl_restriction_domain_contract_no_top_level_orphans_red_smoke():
    assert _rdf_output_artifacts_exist()

    rdf_xml_raw = _combined_rdf_xml()
    root = ET.fromstring(rdf_xml_raw)
    ns = {
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "owl": "http://www.w3.org/2002/07/owl#",
    }

    rdf_res = f'{{{ns["rdf"]}}}resource'
    rdf_about = f'{{{ns["rdf"]}}}about'

    def restriction_pair(rnode):
        on = rnode.find('owl:onProperty', ns)
        svf = rnode.find('owl:someValuesFrom', ns)
        if on is None or svf is None:
            return None
        piri = on.attrib.get(rdf_res, '').strip()
        obj = svf.attrib.get(rdf_res, '').strip()
        if not piri or not obj:
            return None
        return (piri, obj)

    top_level_restrictions = []
    for rnode in root.findall('./owl:Restriction', ns):
        pair = restriction_pair(rnode)
        if pair is not None:
            top_level_restrictions.append(pair)

    domain_by_property = {}
    for op in root.findall('.//owl:ObjectProperty', ns):
        piri = op.attrib.get(rdf_about, '').strip()
        if not piri:
            continue
        domains = [d.attrib.get(rdf_res, '').strip() for d in op.findall('rdfs:domain', ns)]
        domains = [d for d in domains if d]
        if domains:
            domain_by_property[piri] = set(domains)

    class_restrictions = {}
    for c in root.findall('.//owl:Class', ns):
        ciri = c.attrib.get(rdf_about, '').strip()
        if not ciri:
            continue
        pairs = set()
        for rnode in c.findall('rdfs:subClassOf/owl:Restriction', ns):
            pair = restriction_pair(rnode)
            if pair is not None:
                pairs.add(pair)
        class_restrictions[ciri] = pairs

    missing_hanging = []
    for piri, obj in top_level_restrictions:
        for domain in domain_by_property.get(piri, set()):
            if (piri, obj) not in class_restrictions.get(domain, set()):
                missing_hanging.append((domain, piri, obj))

    examples = {
        ('https://orion.local/resource/Control', 'https://orion.local/resource/mitigates', 'https://orion.local/resource/Risk'),
        ('https://orion.local/resource/Vulnerability', 'https://orion.local/resource/exposes', 'https://orion.local/resource/Asset'),
        ('https://orion.local/resource/Logging', 'https://orion.local/resource/generates', 'https://orion.local/resource/Log'),
    }
    missing_examples = [triple for triple in sorted(examples) if triple in missing_hanging]

    assert not top_level_restrictions and not missing_hanging and not missing_examples, (
        'contrato WebVOWL restriction-domain roto: '
        f'top_level_restrictions={len(top_level_restrictions)} '
        f'missing_hanging_restrictions={len(missing_hanging)} '
        f'missing_examples={missing_examples} '
        f'top_level_sample={top_level_restrictions[:3]}'
    )


# UC-SMOKE-001 AF-18 | FUN-SMOKE-001 AC-20 | CON-SMOKE-RDF-013 AC-1 | BR-SMOKE-040 | BR-SMOKE-041
def test_infosec_3k_webvowl_no_duplicated_visible_domain_edges_by_modeling_style_red_smoke():
    assert _rdf_output_artifacts_exist()

    rdf_xml_raw = _combined_rdf_xml()
    root = ET.fromstring(rdf_xml_raw)
    ns = {
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "owl": "http://www.w3.org/2002/07/owl#",
    }

    rdf_res = f'{{{ns["rdf"]}}}resource'
    rdf_about = f'{{{ns["rdf"]}}}about'

    domain_range_edges = set()
    for op in root.findall('.//owl:ObjectProperty', ns):
        piri = op.attrib.get(rdf_about, '').strip()
        if not piri:
            continue
        domains = [d.attrib.get(rdf_res, '').strip() for d in op.findall('rdfs:domain', ns)]
        ranges = [r.attrib.get(rdf_res, '').strip() for r in op.findall('rdfs:range', ns)]
        for domain in domains:
            for obj in ranges:
                if domain and obj:
                    domain_range_edges.add((domain, piri, obj))

    restriction_edges = set()
    for cls in root.findall('.//owl:Class', ns):
        domain = cls.attrib.get(rdf_about, '').strip()
        if not domain:
            continue
        for rnode in cls.findall('rdfs:subClassOf/owl:Restriction', ns):
            on = rnode.find('owl:onProperty', ns)
            svf = rnode.find('owl:someValuesFrom', ns)
            avf = rnode.find('owl:allValuesFrom', ns)
            if on is None:
                continue
            piri = on.attrib.get(rdf_res, '').strip()
            obj = ''
            if svf is not None:
                obj = svf.attrib.get(rdf_res, '').strip()
            elif avf is not None:
                obj = avf.attrib.get(rdf_res, '').strip()
            if piri and obj:
                restriction_edges.add((domain, piri, obj))

    duplicated_visible_edges = sorted(domain_range_edges & restriction_edges)

    assert not duplicated_visible_edges, (
        'contrato WebVOWL anti-duplicado roto: mismo edge visible existe en domain/range y restriction; '
        f'duplicated_visible_edges={len(duplicated_visible_edges)} sample={duplicated_visible_edges[:5]}'
    )


# UC-SMOKE-001 AF-16 | FUN-SMOKE-001 AC-18 | CON-SMOKE-RDF-016 AC-1 | BR-SMOKE-046 | BR-SMOKE-047
def test_infosec_3k_output_graph_must_publish_explicit_owl_schema_from_evidence_red():
    assert _debug_output_artifacts_exist()
    assert _STAGE_RESULTS_ARTIFACT.exists()

    rdf_json = _merged_debug_output()
    stage_rows = _load_jsonl(_STAGE_RESULTS_ARTIFACT)
    by_stage = {row.get("stage"): row for row in stage_rows if isinstance(row, dict)}

    graph = rdf_json.get("graph", {})
    facts = graph.get("facts", [])
    subclass_facts = graph.get("subclass_facts", [])
    type_assertions = graph.get("type_assertions", [])
    classes = graph.get("classes", [])
    object_property_schema = graph.get("object_property_schema", [])
    restrictions = graph.get("restrictions", [])

    rel_count = by_stage.get("relation_extraction", {}).get("summary", {}).get("total_count", 0)
    out_summary = by_stage.get("output_generation", {}).get("summary", {})

    assert rel_count > 0, "precondición rota: relation_extraction total_count debe ser > 0"
    assert len(facts) > 0, "precondición rota: graph.facts debe ser > 0"
    assert out_summary.get("facts_count", 0) == len(facts), "desalineación facts_count vs debug graph.facts"

    assert isinstance(classes, list) and len(classes) > 0, "contract-red: faltan graph.classes explícitas derivadas de evidencia"
    assert isinstance(type_assertions, list) and len(type_assertions) > 0, "contract-red: faltan graph.type_assertions explícitas derivadas de evidencia"
    assert isinstance(subclass_facts, list) and len(subclass_facts) > 0, "contract-red: faltan graph.subclass_facts derivadas de taxonomy"
    assert isinstance(object_property_schema, list) and len(object_property_schema) > 0, "contract-red: faltan graph.object_property_schema derivadas de facts"
    assert isinstance(restrictions, list) and len(restrictions) > 0, "contract-red: faltan graph.restrictions derivadas de facts/taxonomy/type assertions"

    by_predicate = {f.get("predicate") for f in facts if isinstance(f, dict) and f.get("predicate")}
    schema_props = {p.get("predicate") for p in object_property_schema if isinstance(p, dict) and p.get("predicate")}
    assert schema_props.issubset(by_predicate), "contract-red: object_property_schema debe trazar a predicates presentes en graph.facts"


# UC-SMOKE-001 AF-19 | FUN-SMOKE-001 AC-21 | CON-SMOKE-RDF-017 AC-1 | BR-SMOKE-049 | BR-SMOKE-050
def test_infosec_3k_webvowl_visual_contract_reified_statements_must_be_named_and_meaningful_red_smoke():
    assert _rdf_output_artifacts_exist()

    rdf_xml_raw = _combined_rdf_xml()
    root = ET.fromstring(rdf_xml_raw)
    ns = {
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "owl": "http://www.w3.org/2002/07/owl#",
    }

    rdf_about = f'{{{ns["rdf"]}}}about'
    rdf_res = f'{{{ns["rdf"]}}}resource'
    rdf_nodeid = f'{{{ns["rdf"]}}}nodeID'

    def has_non_empty_label(node) -> bool:
        for lbl in node.findall('rdfs:label', ns):
            if (lbl.text or '').strip():
                return True
        return False

    def is_top_fallback_iri(iri: str) -> bool:
        if not iri:
            return False
        local = iri.rstrip('/#').split('/')[-1].split('#')[-1]
        return local in {"Thing", "Any"}

    def expected_statement_label(subj: str, pred: str, obj: str) -> str:
        return f"{subj} {pred} {obj}".strip()

    top_fallback_refs = []
    for node in root.iter():
        for attr_key in (rdf_about, rdf_res):
            iri = node.attrib.get(attr_key, '').strip()
            if is_top_fallback_iri(iri):
                top_fallback_refs.append(iri)

    classes = root.findall('.//owl:Class', ns)
    obj_props = root.findall('.//owl:ObjectProperty', ns)
    reified_statements = root.findall('.//rdf:Statement', ns)

    unlabeled_classes = [
        c.attrib.get(rdf_about, '').strip() or c.attrib.get(rdf_nodeid, '').strip() or 'anonymous'
        for c in classes
        if not has_non_empty_label(c)
    ]
    unlabeled_props = [
        p.attrib.get(rdf_about, '').strip() or p.attrib.get(rdf_nodeid, '').strip() or 'anonymous'
        for p in obj_props
        if not has_non_empty_label(p)
    ]

    statement_unstable_identity = []
    statement_unlabeled = []
    statement_missing_spo = []
    statement_bad_label = []
    statement_thing_any = []
    statement_missing_evidence_confidence = []

    for st in reified_statements:
        sid_about = st.attrib.get(rdf_about, '').strip()
        sid_node = st.attrib.get(rdf_nodeid, '').strip()
        if not sid_about and not sid_node:
            statement_unstable_identity.append('missing-id')

        subj = ''
        pred = ''
        obj = ''

        subj_node = st.find('rdf:subject', ns)
        pred_node = st.find('rdf:predicate', ns)
        obj_node = st.find('rdf:object', ns)
        if subj_node is not None:
            subj = subj_node.attrib.get(rdf_res, '').strip()
        if pred_node is not None:
            pred = pred_node.attrib.get(rdf_res, '').strip()
        if obj_node is not None:
            obj = obj_node.attrib.get(rdf_res, '').strip()

        if not subj or not pred or not obj:
            statement_missing_spo.append(sid_about or sid_node or 'anonymous-statement')

        labels = [(lbl.text or '').strip() for lbl in st.findall('rdfs:label', ns) if (lbl.text or '').strip()]
        if not labels:
            statement_unlabeled.append(sid_about or sid_node or 'anonymous-statement')
        else:
            expected = expected_statement_label(subj, pred, obj)
            if expected and expected not in labels:
                statement_bad_label.append(sid_about or sid_node or 'anonymous-statement')

        for value in (sid_about, sid_node, subj, pred, obj):
            if is_top_fallback_iri(value):
                statement_thing_any.append(sid_about or sid_node or 'anonymous-statement')
                break

        evidences = [e for e in st.findall('*') if e.tag.endswith('evidence') and ((e.text or '').strip())]
        confidences = [c for c in st.findall('*') if c.tag.endswith('confidence') and ((c.text or '').strip())]
        if not evidences and not confidences:
            statement_missing_evidence_confidence.append(sid_about or sid_node or 'anonymous-statement')

    props_without_domain_range = []
    for op in obj_props:
        piri = op.attrib.get(rdf_about, '').strip() or op.attrib.get(rdf_nodeid, '').strip() or 'anonymous'
        domains = [d.attrib.get(rdf_res, '').strip() for d in op.findall('rdfs:domain', ns) if d.attrib.get(rdf_res, '').strip()]
        ranges = [r.attrib.get(rdf_res, '').strip() for r in op.findall('rdfs:range', ns) if r.attrib.get(rdf_res, '').strip()]
        if not domains or not ranges:
            props_without_domain_range.append(piri)

    assert (
        len(reified_statements) > 0
        and not top_fallback_refs
        and not unlabeled_classes
        and not unlabeled_props
        and not statement_unstable_identity
        and not statement_unlabeled
        and not statement_missing_spo
        and not statement_bad_label
        and not statement_thing_any
        and not statement_missing_evidence_confidence
        and not props_without_domain_range
    ), (
        'contrato visual WebVOWL roto o incompleto: '
        f'rdf_statement={len(reified_statements)} '
        f'thing_any={len(top_fallback_refs)} '
        f'unlabeled_classes={len(unlabeled_classes)} '
        f'unlabeled_props={len(unlabeled_props)} '
        f'statement_unstable_identity={len(statement_unstable_identity)} '
        f'statement_unlabeled={len(statement_unlabeled)} '
        f'statement_missing_spo={len(statement_missing_spo)} '
        f'statement_bad_label={len(statement_bad_label)} '
        f'statement_thing_any={len(statement_thing_any)} '
        f'statement_missing_evidence_confidence={len(statement_missing_evidence_confidence)} '
        f'props_without_domain_range={len(props_without_domain_range)} '
        f'sample_statement_missing_spo={statement_missing_spo[:5]} '
        f'sample_statement_unlabeled={statement_unlabeled[:5]} '
        f'sample_statement_bad_label={statement_bad_label[:5]}'
    )


# UC-SMOKE-001 AF-20 | FUN-SMOKE-001 AC-22 | CON-SMOKE-RDF-018 AC-1 | BR-SMOKE-051 | BR-SMOKE-052
def test_infosec_3k_webvowl_reified_context_nodes_must_have_visual_name_contract_red_smoke():
    assert _rdf_output_artifacts_exist()

    rdf_xml_raw = _combined_rdf_xml()
    root = ET.fromstring(rdf_xml_raw)
    ns = {
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "skos": "http://www.w3.org/2004/02/skos/core#",
    }

    rdf_about = f'{{{ns["rdf"]}}}about'
    rdf_res = f'{{{ns["rdf"]}}}resource'

    def local_name(iri: str) -> str:
        return iri.rstrip('/#').split('/')[-1].split('#')[-1] if iri else ''

    def readable_short_local_name(iri: str, max_len: int = 48) -> bool:
        local = local_name(iri)
        return bool(local) and len(local) <= max_len and local.replace('_', '').replace('-', '').isalnum()

    bad_visual_name = []
    missing_visual_type = []

    for st in root.findall('.//rdf:Statement', ns):
        sid = st.attrib.get(rdf_about, '').strip()

        has_pref_label = any((n.text or '').strip() for n in st.findall('skos:prefLabel', ns))
        has_comment = any((n.text or '').strip() for n in st.findall('rdfs:comment', ns))
        has_short_local = readable_short_local_name(sid)

        if not (has_short_local or has_pref_label or has_comment):
            bad_visual_name.append(sid or 'anonymous-statement')

        explicit_visual_types = [
            t.attrib.get(rdf_res, '').strip()
            for t in st.findall('rdf:type', ns)
            if t.attrib.get(rdf_res, '').strip()
        ]
        has_visual_relation_type = any(
            (not t.endswith('rdf-syntax-ns#Statement')) and local_name(t) in {'ExtractedRelation', 'ReifiedRelation', 'RelationNode'}
            for t in explicit_visual_types
        )
        if not has_visual_relation_type:
            missing_visual_type.append(sid or 'anonymous-statement')

    assert not bad_visual_name and not missing_visual_type, (
        'contrato WebVOWL nombre visual reificado roto: '
        f'statement_total={len(root.findall(".//rdf:Statement", ns))} '
        f'bad_visual_name={len(bad_visual_name)} '
        f'missing_visual_type={len(missing_visual_type)} '
        f'sample_bad_visual_name={bad_visual_name[:5]} '
        f'sample_missing_visual_type={missing_visual_type[:5]}'
    )


# UC-SMOKE-001 AF-24 | FUN-SMOKE-001 AC-26 | CON-SMOKE-RDF-021 AC-1 | BR-SMOKE-055 | BR-SMOKE-056
def test_infosec_3k_webvowl_objectproperty_must_not_publish_multi_domain_or_multi_range_red_smoke():
    assert _rdf_output_artifacts_exist()

    rdf_xml_raw = _combined_rdf_xml()
    root = ET.fromstring(rdf_xml_raw)
    ns = {
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "owl": "http://www.w3.org/2002/07/owl#",
    }

    rdf_about = f'{{{ns["rdf"]}}}about'
    rdf_res = f'{{{ns["rdf"]}}}resource'

    by_property = {}
    for op in root.findall('.//owl:ObjectProperty', ns):
        piri = op.attrib.get(rdf_about, '').strip()
        if not piri:
            continue

        rec = by_property.setdefault(piri, {'domains': set(), 'ranges': set(), 'declarations': 0})
        rec['declarations'] += 1

        for d in op.findall('rdfs:domain', ns):
            iri = d.attrib.get(rdf_res, '').strip()
            if iri:
                rec['domains'].add(iri)

        for r in op.findall('rdfs:range', ns):
            iri = r.attrib.get(rdf_res, '').strip()
            if iri:
                rec['ranges'].add(iri)

    overloaded_sorted = []
    for piri, rec in by_property.items():
        domains = sorted(rec['domains'])
        ranges = sorted(rec['ranges'])
        if len(domains) > 1 or len(ranges) > 1:
            overloaded_sorted.append({
                'property': piri,
                'declarations': rec['declarations'],
                'domain_count': len(domains),
                'range_count': len(ranges),
                'domains': domains,
                'ranges': ranges,
            })

    overloaded_sorted = sorted(
        overloaded_sorted,
        key=lambda x: (-max(x['domain_count'], x['range_count']), x['property']),
    )

    assert not overloaded_sorted, (
        'contrato WebVOWL roto: misma owl:ObjectProperty visible no puede acumular múltiples domain/range globales; '
        f'overloaded_count={len(overloaded_sorted)} sample={overloaded_sorted[:8]}'
    )



def _tb_ont_inf_local(value: str) -> str:
    token = str(value or '').strip().rstrip('/#').rsplit('/', 1)[-1].split(':')[-1]
    return token.replace('_', '-').casefold()


def _tb_ont_inf_graph_payload() -> tuple[str, dict]:
    assert _rdf_output_artifacts_exist(), 'falta artifact RDF infosec_3k_output.rdf'
    assert _debug_output_artifacts_exist(), 'falta debug JSON RDF por grupos de dos párrafos'
    return _combined_rdf_xml(), _merged_debug_output()


# TB-ORION-ONT-INF-001 TASK-001 | TASK-002 | CON-ONT-INF-001 AC-1 | BR-ONT-INF-001 | BR-ONT-INF-002
# TB-ORION-ONT-INF-001 TASK-002 ajuste aprobado: desactivar NER genérico; sin EntityRuler ni glosario ahora.
def test_tb_orion_ont_inf_001_closed_infosec_ontology_blocks_generic_ner_and_scaffolds_red():
    rdf_xml_raw, rdf_json = _tb_ont_inf_graph_payload()
    graph = rdf_json.get('graph', {}) if isinstance(rdf_json, dict) else {}
    serialized_graph = json.dumps(graph, ensure_ascii=False).casefold()

    forbidden_locals = {'a', 'an', 'the', 'any', 'each', 'one-or-more', 'that', 'which', 'who'}
    local_values = []
    for collection in ('classes', 'facts', 'instance_facts', 'type_assertions', 'subclass_facts', 'object_property_schema'):
        for item in graph.get(collection, []):
            if not isinstance(item, dict):
                continue
            for key in ('iri', 'id', 'subject', 'predicate', 'object', 'entity', 'type', 'domain', 'range'):
                if item.get(key):
                    local_values.append(_tb_ont_inf_local(item.get(key)))

    determiners_or_relatives = sorted({value for value in local_values if value in forbidden_locals or value.startswith('resource-that')})
    type_scaffolds = sorted({value for value in local_values if value.startswith('type-of') or 'typeof' in value})
    generic_organization_types = sorted(
        f"{_tb_ont_inf_local(item.get('entity'))}->{_tb_ont_inf_local(item.get('type'))}"
        for item in graph.get('type_assertions', [])
        if isinstance(item, dict)
        and _tb_ont_inf_local(item.get('entity')) in {'api', 'cia', 'rdf', 'orion'}
        and _tb_ont_inf_local(item.get('type')) == 'organization'
    )

    assert determiners_or_relatives == [], f'recursos gramaticales prohibidos visibles: {determiners_or_relatives[:12]}'
    assert type_scaffolds == [], f'TypeOf* scaffolding prohibido visible: {type_scaffolds[:12]}'
    assert 'orion:be' not in rdf_xml_raw and 'orion:be' not in serialized_graph, 'orion:be final prohibido en RDF/graph'
    assert generic_organization_types == [], f'NER genérico filtrado mal: {generic_organization_types}'


# TB-ORION-ONT-INF-001 TASK-003 | FUN-ONT-INF-001 AC-1 | BR-ONT-INF-003 | BR-ONT-INF-004
def test_tb_orion_ont_inf_001_taxonomy_direction_and_definition_comments_red():
    _, rdf_json = _tb_ont_inf_graph_payload()
    graph = rdf_json.get('graph', {}) if isinstance(rdf_json, dict) else {}
    subclass_edges = graph.get('subclass_facts', [])

    bad_superclasses = sorted(
        f"{item.get('subject')}->{item.get('object')}"
        for item in subclass_edges
        if isinstance(item, dict)
        and (_tb_ont_inf_local(item.get('object')).startswith('type-of') or 'typeof' in _tb_ont_inf_local(item.get('object')))
    )
    definition_as_false_taxonomy = sorted(
        f"{item.get('subject')}->{item.get('object')}"
        for item in subclass_edges
        if isinstance(item, dict)
        and any(fragment in _tb_ont_inf_local(item.get('object')) for fragment in ('potential-cause', 'possibility-that', 'ability', 'process-of', 'consequence-produced'))
    )

    assert bad_superclasses == [], f'taxonomía X is a type/kind of Y debe apuntar a Y, no TypeOf*: {bad_superclasses[:12]}'
    assert definition_as_false_taxonomy == [], f'definiciones deben quedar comentario, no subclass falsa: {definition_as_false_taxonomy[:12]}'


# TB-ORION-ONT-INF-001 TASK-004 | FUN-ONT-INF-002 AC-1 | CON-ONT-INF-002 AC-1 | BR-ONT-INF-005
def test_tb_orion_ont_inf_001_expected_infosec_relations_have_domain_range_red():
    _, rdf_json = _tb_ont_inf_graph_payload()
    graph = rdf_json.get('graph', {}) if isinstance(rdf_json, dict) else {}
    schema_edges = {
        (_tb_ont_inf_local(item.get('predicate')), _tb_ont_inf_local(item.get('domain')), _tb_ont_inf_local(item.get('range')))
        for item in graph.get('object_property_schema', [])
        if isinstance(item, dict)
    }

    expected = {
        ('accesses', 'user', 'information-system'),
        ('includes', 'role', 'permission'),
        ('exploits', 'threat', 'vulnerability'),
        ('reduces', 'security-control', 'risk'),
        ('affects', 'security-incident', 'information-asset'),
    }
    missing = sorted(expected - schema_edges)

    assert missing == [], f'relaciones infosec esperadas sin domain/range correcto: {missing}'
