# UC-NS-004 MF-1 | FUN-NS-004 AC-1 | BR-NS-008 | BR-NS-009 | TB-NS-001
def test_rdf_output_uses_stable_iris_and_compact_reserved_predicates():
    from pipeline.step_013_output_generation.orchestrator import generate_output_from_payload

    payload = {
        "triples": [{"subject": "john doe", "predicate": "works at", "object": "acme inc"}],
        "type_assertions": [{"entity": "john doe", "type": "person"}],
        "taxonomy_relations": [{"child": "person", "parent": "agent"}],
        "metadata": {},
    }

    out = generate_output_from_payload(payload, "rdf")
    facts = out["output"]["graph"]["facts"]
    instance_facts = out["output"]["graph"]["instance_facts"]
    subclass_facts = out["output"]["graph"]["subclass_facts"]

    assert facts == [
        {
            "subject": "https://orion.local/resource/john-doe",
            "predicate": "orion:worksAt",
            "object": "https://orion.local/resource/acme-inc",
        }
    ]
    assert instance_facts == [
        {
            "subject": "https://orion.local/resource/john-doe",
            "predicate": "rdf:type",
            "object": "orion:Person",
        }
    ]
    assert subclass_facts == [
        {
            "subject": "orion:Person",
            "predicate": "rdfs:subClassOf",
            "object": "orion:Agent",
        }
    ]


# UC-NS-004 AF-1 | FUN-NS-004 AC-2 | NFR-NS-001 AC-1 | BR-NS-010 | TB-NS-001
def test_owl_output_uses_namespace_aware_iris_for_classes_individuals_and_properties():
    from pipeline.step_013_output_generation.orchestrator import generate_output_from_payload

    payload = {
        "concepts": [{"normalized_text": "person"}],
        "entities": [{"normalized_text": "john doe"}],
        "relations": [{"predicate": "works at"}],
        "triples": [{"predicate": "manages"}],
        "type_assertions": [{"entity": "john doe", "type": "person"}],
        "taxonomy_relations": [{"child": "person", "parent": "agent"}],
        "metadata": {},
    }

    out = generate_output_from_payload(payload, "owl")
    ontology = out["output"]["ontology"]

    assert ontology["classes"] == ["orion:Person"]
    assert ontology["individuals"] == ["orion:john-doe"]
    assert ontology["object_properties"] == ["orion:worksAt", "orion:manages"]
    assert ontology["class_assertions"] == [{"individual": "orion:john-doe", "class": "orion:Person"}]
    assert ontology["subclass_axioms"] == [{"child": "orion:Person", "parent": "orion:Agent"}]
