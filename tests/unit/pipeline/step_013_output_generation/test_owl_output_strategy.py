# UC-OUT-003 MF-1 | FUN-OUT-003 AC-1 | BR-OUT-005 | BR-OUT-006 | TB-OUT-001
def test_owl_output_strategy_builds_common_output_graph_shape_with_expected_owl_sections():
    from pipeline.step_013_output_generation.owl_strategy import OwlOutputStrategy

    payload = {
        "raw_text": "text",
        "source_text_id": "src-out-003",
        "concepts": [
            {"normalized_text": "person"},
            {"normalized_text": "organization"},
            {"normalized_text": "person"},
        ],
        "entities": [
            {"normalized_text": "john"},
            {"normalized_text": "apple"},
            {"normalized_text": "john"},
        ],
        "relations": [{"predicate": "works at"}],
        "triples": [{"predicate": "manages"}, {"predicate": "works at"}],
        "type_assertions": [
            {"entity": "john", "type": "person"},
            {"entity": "john", "type": "person"},
        ],
        "taxonomy_relations": [
            {"child": "person", "parent": "agent"},
            {"child": "person", "parent": "agent"},
        ],
        "metadata": {"pipeline_version": "1"},
    }

    out = OwlOutputStrategy().generate(payload)

    assert out["output"]["strategy"] == "owl"
    assert out["output"]["format"] == "owl"
    assert out["output"]["metadata"] == payload["metadata"]
    assert isinstance(out["output"]["graph"], dict)
    assert out["output"]["graph"]["classes"] == ["person", "organization"]
    assert out["output"]["graph"]["individuals"] == ["john", "apple"]
    assert out["output"]["graph"]["object_properties"] == ["works_at", "manages"]
    assert out["output"]["graph"]["class_assertions"] == [{"individual": "john", "class": "person"}]
    assert out["output"]["graph"]["subclass_axioms"] == [{"child": "person", "parent": "agent"}]


# UC-OUT-003 EF-1 | FUN-OUT-003 AC-2 | NFR-OUT-001 AC-2 | BR-OUT-007 | TB-OUT-001
def test_owl_output_strategy_deterministic_and_payload_preservation():
    from pipeline.step_013_output_generation.owl_strategy import OwlOutputStrategy

    payload = {
        "raw_text": "same",
        "preprocessed_text": "same",
        "source_text_id": "src-out-004",
        "sentences": [],
        "tokens": [],
        "entities": [{"normalized_text": "john"}],
        "concepts": [{"normalized_text": "person"}],
        "relations": [],
        "triples": [],
        "taxonomy_relations": [],
        "type_assertions": [{"entity": "john", "type": "person"}],
        "metadata": {},
        "custom_marker": {"keep": True},
    }

    r1 = OwlOutputStrategy().generate(payload)
    r2 = OwlOutputStrategy().generate(payload)

    assert r1 == r2
    assert r1["custom_marker"] == payload["custom_marker"]
    assert r1["entities"] == payload["entities"]
    assert r1["concepts"] == payload["concepts"]
