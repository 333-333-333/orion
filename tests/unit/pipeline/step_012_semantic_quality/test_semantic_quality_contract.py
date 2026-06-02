# UC-SQ-001 MF-1 | FUN-SQ-001 AC-1 | BR-SQ-001 | BR-SQ-002 | TB-SQ-001
def test_semantic_quality_report_detects_entity_acronym_noise_and_preserves_original_payload():
    from pipeline.step_012_semantic_quality import assess_semantic_quality_from_payload

    payload = {
        "raw_text": "CIA API RDF OWL IAM MFA SAST DAST are critical.",
        "source_text_id": "src-sq-001",
        "entities": [
            {"entity_id": "ent-1", "text": "CIA", "normalized_text": "cia", "label": "ORG"},
            {"entity_id": "ent-2", "text": "API", "normalized_text": "api", "label": "ORG"},
            {"entity_id": "ent-3", "text": "RDF", "normalized_text": "rdf", "label": "ORG"},
            {"entity_id": "ent-4", "text": "OWL", "normalized_text": "owl", "label": "ORG"},
            {"entity_id": "ent-5", "text": "IAM", "normalized_text": "iam", "label": "ORG"},
            {"entity_id": "ent-6", "text": "MFA", "normalized_text": "mfa", "label": "ORG"},
            {"entity_id": "ent-7", "text": "SAST", "normalized_text": "sast", "label": "ORG"},
            {"entity_id": "ent-8", "text": "DAST", "normalized_text": "dast", "label": "ORG"},
        ],
        "concepts": [],
        "relations": [],
        "triples": [],
        "taxonomy_relations": [],
        "type_assertions": [],
        "custom_marker": {"keep": True},
    }

    out = assess_semantic_quality_from_payload(payload)

    assert "semantic_quality_report" in out
    report = out["semantic_quality_report"]
    assert isinstance(report.get("entity_noise"), list)
    noisy_texts = {x.get("text") for x in report["entity_noise"] if isinstance(x, dict)}
    assert {"CIA", "API", "RDF", "OWL", "IAM", "MFA", "SAST", "DAST"}.issubset(noisy_texts)
    assert isinstance(report.get("excluded_entities"), list)
    assert {"CIA", "API", "RDF", "OWL", "IAM", "MFA", "SAST", "DAST"}.issubset(set(report["excluded_entities"]))
    assert isinstance(report.get("quality_score"), (int, float))

    assert out["raw_text"] == payload["raw_text"]
    assert out["entities"] == payload["entities"]
    assert out["custom_marker"] == payload["custom_marker"]


# UC-SQ-001 AF-1 | FUN-SQ-001 AC-2 | BR-SQ-003 | BR-SQ-004 | TB-SQ-001
def test_semantic_quality_report_detects_concept_noise_and_long_text_warnings():
    from pipeline.step_012_semantic_quality import assess_semantic_quality_from_payload

    long_chunk = "x" * 260
    payload = {
        "raw_text": "# Header. very long text.",
        "source_text_id": "src-sq-002",
        "entities": [],
        "concepts": [
            {"concept_id": "con-1", "text": "# Header", "normalized_text": "header", "superclass": "thing"},
            {"concept_id": "con-2", "text": long_chunk, "normalized_text": long_chunk, "superclass": "collection"},
            {"concept_id": "con-3", "text": "type", "normalized_text": "type", "superclass": "factor"},
        ],
        "relations": [],
        "triples": [],
        "taxonomy_relations": [],
        "type_assertions": [],
    }

    out = assess_semantic_quality_from_payload(payload)
    report = out["semantic_quality_report"]

    assert isinstance(report.get("concept_noise"), list)
    concept_noise_values = {x.get("text", x.get("normalized_text")) for x in report["concept_noise"] if isinstance(x, dict)}
    assert "# Header" in concept_noise_values
    assert "type" in concept_noise_values
    assert isinstance(report.get("excluded_concepts"), list)
    assert any(v in report["excluded_concepts"] for v in ["# Header", "type", "thing", "collection", "factor"])

    assert isinstance(report.get("warnings"), list)
    assert "long_text_without_relations" in report["warnings"]
    assert "long_text_without_triples" in report["warnings"]


# UC-SQ-001 AF-2 | FUN-SQ-001 AC-3 | BR-SQ-005 | TB-SQ-001
def test_semantic_quality_report_sets_rdf_readiness_true_when_semantic_signal_exists():
    from pipeline.step_012_semantic_quality import assess_semantic_quality_from_payload

    base = {
        "raw_text": "signal",
        "source_text_id": "src-sq-003",
        "entities": [],
        "concepts": [],
        "relations": [],
        "taxonomy_relations": [],
    }

    out_type = assess_semantic_quality_from_payload({**base, "type_assertions": [{"instance": "john", "class": "person"}], "triples": []})
    out_tax = assess_semantic_quality_from_payload({**base, "type_assertions": [], "taxonomy_relations": [{"child": "robin", "parent": "bird"}], "triples": []})
    out_tri = assess_semantic_quality_from_payload({**base, "type_assertions": [], "triples": [{"subject": "john", "predicate": "uses", "object": "api"}]})
    out_none = assess_semantic_quality_from_payload({**base, "type_assertions": [], "triples": []})

    assert out_type["semantic_quality_report"]["rdf_readiness"] is True
    assert out_tax["semantic_quality_report"]["rdf_readiness"] is True
    assert out_tri["semantic_quality_report"]["rdf_readiness"] is True
    assert out_none["semantic_quality_report"]["rdf_readiness"] is False


# UC-SQ-001 EF-1 | FUN-SQ-001 AC-4 | BR-SQ-006 | TB-SQ-001
def test_semantic_quality_report_exposes_relation_gaps_key_even_when_empty():
    from pipeline.step_012_semantic_quality import assess_semantic_quality_from_payload

    payload = {
        "raw_text": "no relations",
        "source_text_id": "src-sq-004",
        "entities": [],
        "concepts": [{"concept_id": "con-1", "text": "identity", "normalized_text": "identity"}],
        "relations": [],
        "triples": [],
        "taxonomy_relations": [],
        "type_assertions": [],
    }

    out = assess_semantic_quality_from_payload(payload)
    report = out["semantic_quality_report"]
    assert "relation_gaps" in report
    assert isinstance(report["relation_gaps"], list)
