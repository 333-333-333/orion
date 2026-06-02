# UC-SQ-002 MF-1 | FUN-SQ-002 AC-1 | CON-SQ-001 AC-1 | BR-SQ-007 | TB-SQ-001
def test_rdf_output_generation_step_013_filters_excluded_acronyms_and_keeps_payload():
    from pipeline.step_013_output_generation.rdf_strategy import RdfOutputStrategy

    payload = {
        "raw_text": "CIA uses API",
        "source_text_id": "src-sq-out-001",
        "entities": [
            {"entity_id": "ent-1", "text": "CIA", "normalized_text": "cia", "label": "ORG"},
            {"entity_id": "ent-2", "text": "API", "normalized_text": "api", "label": "ORG"},
            {"entity_id": "ent-3", "text": "OpenAI", "normalized_text": "openai", "label": "ORG"},
        ],
        "concepts": [{"concept_id": "con-1", "normalized_text": "type"}, {"concept_id": "con-2", "normalized_text": "security_control"}],
        "triples": [
            {"subject": "cia", "predicate": "uses", "object": "api"},
            {"subject": "openai", "predicate": "uses", "object": "security_control"},
        ],
        "taxonomy_relations": [],
        "type_assertions": [],
        "semantic_quality_report": {
            "excluded_entities": ["CIA", "API"],
            "excluded_concepts": ["type"],
            "entity_noise": [],
            "concept_noise": [],
            "relation_gaps": [],
            "rdf_readiness": True,
            "warnings": [],
            "quality_score": 0.6,
        },
    }

    out = RdfOutputStrategy().generate(payload)

    facts = out["output"]["graph"]["facts"]
    fact_serialized = str(facts).lower()
    assert "cia" not in fact_serialized
    assert "api" not in fact_serialized
    assert "type" not in fact_serialized
    assert "openai" in fact_serialized
    assert "security_control" in fact_serialized

    assert out["raw_text"] == payload["raw_text"]
    assert out["semantic_quality_report"] == payload["semantic_quality_report"]
