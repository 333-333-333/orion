import xml.etree.ElementTree as ET

# UC-OUT-002 MF-1 | FUN-OUT-002 AC-1 | BR-OUT-002 | BR-OUT-003 | TB-OUT-001
def test_rdf_output_strategy_builds_graph_with_expected_predicates_and_shape():
    from pipeline.step_013_output_generation.rdf_strategy import RdfOutputStrategy

    payload = {
        "raw_text": "John is a person. A robin is a bird.",
        "source_text_id": "src-out-001",
        "triples": [
            {"subject": "john", "predicate": "works at", "object": "apple", "sentence_id": "sent-1"},
            {"subject": "john", "predicate": "works at", "object": "apple", "sentence_id": "sent-2"},
        ],
        "type_assertions": [
            {"entity": "john", "type": "person"},
            {"entity": "john", "type": "person"},
        ],
        "taxonomy_relations": [
            {"child": "robin", "parent": "bird"},
            {"child": "robin", "parent": "bird"},
        ],
        "concepts": [],
        "entities": [],
        "metadata": {"pipeline_version": "1"},
    }

    out = RdfOutputStrategy().generate(payload)

    assert out["output"]["strategy"] == "rdf"
    assert out["output"]["format"] == "rdf"
    assert isinstance(out["output"]["graph"], dict)
    assert out["output"]["metadata"] == payload["metadata"]
    assert out["output"]["graph"]["facts"] == [
        {"subject": "john", "predicate": "works_at", "object": "apple"}
    ]
    assert out["output"]["graph"]["instance_facts"] == [
        {"subject": "john", "predicate": "rdf:type", "object": "person"}
    ]
    assert out["output"]["graph"]["subclass_facts"] == [
        {"subject": "robin", "predicate": "rdfs:subClassOf", "object": "bird"}
    ]


# UC-OUT-002 AF-1 | FUN-OUT-002 AC-2 | NFR-OUT-001 AC-1 | BR-OUT-004 | TB-OUT-001
def test_rdf_output_strategy_preserves_previous_payload_complete_and_is_deterministic():
    from pipeline.step_013_output_generation.rdf_strategy import RdfOutputStrategy

    payload = {
        "raw_text": "same",
        "preprocessed_text": "same",
        "source_text_id": "src-out-002",
        "sentences": [],
        "tokens": [],
        "entities": [{"entity_id": "ent-1", "normalized_text": "john"}],
        "concepts": [{"concept_id": "con-1", "normalized_text": "person"}],
        "relations": [],
        "triples": [{"subject": "john", "predicate": "is a", "object": "person"}],
        "taxonomy_relations": [{"child": "person", "parent": "agent"}],
        "type_assertions": [{"entity": "john", "type": "person"}],
        "metadata": {"x": 1},
        "custom_marker": {"keep": True},
    }

    r1 = RdfOutputStrategy().generate(payload)
    r2 = RdfOutputStrategy().generate(payload)

    assert r1 == r2
    assert r1["custom_marker"] == payload["custom_marker"]
    assert r1["triples"] == payload["triples"]
    assert r1["taxonomy_relations"] == payload["taxonomy_relations"]
    assert r1["type_assertions"] == payload["type_assertions"]


# UC-OUT-002 EF-2 | FUN-OUT-002 AC-4 | CON-OUT-002 AC-1 | BR-OUT-009 | BR-OUT-010 | TB-OUT-001
def test_rdf_output_strategy_namespace_mode_does_not_invent_relatedto_when_no_real_signal():
    from pipeline.step_013_output_generation.rdf_strategy import RdfOutputStrategy

    payload = {
        "raw_text": "seed only without facts",
        "source_text_id": "src-out-003",
        "entities": [
            {"entity_id": "ent-1", "normalized_text": "alpha"},
            {"entity_id": "ent-2", "normalized_text": "beta"},
        ],
        "concepts": [],
        "triples": [],
        "type_assertions": [],
        "taxonomy_relations": [],
        "metadata": {"pipeline_version": "1"},
    }

    out = RdfOutputStrategy(base_iri="https://orion.local/resource/").generate(payload)

    assert out["output"]["graph"]["facts"] == []
    assert out["output"]["graph"]["instance_facts"] == []
    assert out["output"]["graph"]["subclass_facts"] == []


# UC-OUT-002 AF-2 | FUN-OUT-002 AC-5 | CON-OUT-002 AC-2 | BR-OUT-009 | BR-OUT-010 | TB-OUT-001
def test_rdf_output_strategy_namespace_mode_keeps_real_semantic_signal_without_fallback_fact():
    from pipeline.step_013_output_generation.rdf_strategy import RdfOutputStrategy

    payload = {
        "raw_text": "john is person",
        "source_text_id": "src-out-004",
        "entities": [],
        "concepts": [],
        "triples": [],
        "type_assertions": [{"entity": "john", "type": "person"}],
        "taxonomy_relations": [],
        "metadata": {"pipeline_version": "1"},
    }

    out = RdfOutputStrategy(base_iri="https://orion.local/resource/").generate(payload)

    assert out["output"]["graph"]["facts"] == []
    assert out["output"]["graph"]["instance_facts"]
    assert all(fact["predicate"] != "orion:relatedTo" for fact in out["output"]["graph"]["facts"])


# UC-OUT-002 EF-3 | FUN-OUT-002 AC-6 | CON-SMOKE-RDF-002 AC-1 | BR-SMOKE-010
def test_serialize_graph_to_rdf_xml_maps_domain_predicates_from_existing_facts():
    from pipeline.step_013_output_generation.rdf_strategy import serialize_graph_to_rdf_xml

    graph = {
        "facts": [
            {"subject": "orion:encryption", "predicate": "orion:protect", "object": "orion:data"},
            {"subject": "orion:vulnerability", "predicate": "orion:affect", "object": "orion:system"},
            {"subject": "orion:control", "predicate": "orion:require", "object": "orion:policy"},
            {"subject": "orion:hardening", "predicate": "orion:prevent", "object": "orion:attack"},
        ],
        "instance_facts": [],
        "subclass_facts": [],
    }

    rdf_xml = serialize_graph_to_rdf_xml(graph)

    assert '<orion:' not in rdf_xml
    assert 'xmlns:orion' not in rdf_xml
    assert '<owl:ObjectProperty rdf:about=' not in rdf_xml
    assert '<rdf:Statement' in rdf_xml
    assert 'https://orion.local/resource/protect' in rdf_xml
    assert 'https://orion.local/resource/affect' in rdf_xml
    assert 'https://orion.local/resource/require' in rdf_xml
    assert 'https://orion.local/resource/prevent' in rdf_xml


# UC-OUT-002 AF-9 | FUN-SMOKE-001 AC-10 | CON-SMOKE-RDF-003 AC-1 | BR-SMOKE-011
def test_rdf_output_strategy_filters_massive_subclassof_type_fallback_and_preserves_real_hierarchy():
    from pipeline.step_013_output_generation.rdf_strategy import RdfOutputStrategy

    payload = {
        "raw_text": "taxonomy",
        "source_text_id": "src-out-005",
        "triples": [],
        "type_assertions": [],
        "taxonomy_relations": [
            {"child": "laptop", "parent": "type"},
            {"child": "laptop", "parent": "endpoint"},
            {"child": "endpoint", "parent": "device"},
            {"child": "vulnerability", "parent": "weakness"},
            {"child": "server", "parent": "orion:Type"},
        ],
        "concepts": [],
        "entities": [],
        "metadata": {"pipeline_version": "1"},
    }

    out = RdfOutputStrategy(base_iri="https://orion.local/resource/").generate(payload)

    assert out["output"]["graph"]["subclass_facts"] == [
        {"subject": "orion:Laptop", "predicate": "rdfs:subClassOf", "object": "orion:Endpoint"},
        {"subject": "orion:Endpoint", "predicate": "rdfs:subClassOf", "object": "orion:Device"},
        {"subject": "orion:Vulnerability", "predicate": "rdfs:subClassOf", "object": "orion:Weakness"},
    ]


# UC-OUT-002 AF-10 | FUN-SMOKE-001 AC-11 | CON-SMOKE-RDF-004 AC-1 | BR-SMOKE-012
def test_serialize_graph_to_rdf_xml_promotes_present_key_concept_to_useful_type():
    from pipeline.step_013_output_generation.rdf_strategy import serialize_graph_to_rdf_xml

    graph = {
        "facts": [
            {"subject": "orion:control", "predicate": "orion:protect", "object": "orion:asset"},
        ],
        "instance_facts": [],
        "subclass_facts": [],
    }

    rdf_xml = serialize_graph_to_rdf_xml(graph)

    root = ET.fromstring(rdf_xml)
    ns = {
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "owl": "http://www.w3.org/2002/07/owl#",
    }

    statements = root.findall("rdf:Statement", ns)
    assert len(statements) == 1
    assert not root.findall('.//owl:ObjectProperty', ns)


# UC-SMOKE-001 AF-20 | FUN-SMOKE-001 AC-22 | CON-SMOKE-RDF-018 AC-1 | BR-SMOKE-051 | BR-SMOKE-052
def test_serialize_graph_to_rdf_xml_reified_statement_has_visual_type_and_webvowl_fallback_names():
    from pipeline.step_013_output_generation.rdf_strategy import serialize_graph_to_rdf_xml

    graph = {
        "facts": [
            {"subject": "orion:alpha", "predicate": "orion:relatesTo", "object": "orion:beta", "confidence": 0.9},
        ],
        "instance_facts": [],
        "subclass_facts": [],
    }

    rdf_xml = serialize_graph_to_rdf_xml(graph)

    assert 'xmlns:skos="http://www.w3.org/2004/02/skos/core#"' in rdf_xml
    assert '<rdf:Statement rdf:about=' in rdf_xml
    assert '<rdf:type rdf:resource="https://orion.local/resource/ReifiedRelation"/>' in rdf_xml
    assert '<skos:prefLabel>' in rdf_xml
    assert '<rdfs:comment>' in rdf_xml
    assert '<rdfs:label>' in rdf_xml
    assert '<meta:confidence>0.9</meta:confidence>' in rdf_xml

# TB-ONT-001 | TB-ONT-002

def test_rdf_output_strategy_canonicalizes_determiners_and_skips_taxonomy_scaffolds():
    from pipeline.step_013_output_generation.rdf_strategy import RdfOutputStrategy

    payload = {
        'raw_text': 'A backup archive is a type of information asset. A virtual machine/container/serverless function is a type of cloud workload.',
        'source_text_id': 'src-ont-004',
        'triples': [],
        'type_assertions': [],
        'taxonomy_relations': [
            {'child': 'backup archive', 'parent': 'information asset'},
            {'child': 'virtual machine', 'parent': 'cloud workload'},
            {'child': 'container', 'parent': 'cloud workload'},
            {'child': 'serverless function', 'parent': 'cloud workload'},
        ],
        'concepts': [
            {'concept_id': 'con-0001', 'text': 'A backup archive', 'normalized_text': 'a backup archive'},
            {'concept_id': 'con-0002', 'text': 'A virtual machine', 'normalized_text': 'a virtual machine'},
            {'concept_id': 'con-0003', 'text': 'A container', 'normalized_text': 'a container'},
            {'concept_id': 'con-0004', 'text': 'A serverless function', 'normalized_text': 'a serverless function'},
            {'concept_id': 'con-0005', 'text': 'A type of information asset', 'normalized_text': 'a type of information asset'},
            {'concept_id': 'con-0006', 'text': 'A type of cloud workload', 'normalized_text': 'a type of cloud workload'},
        ],
        'entities': [],
        'metadata': {'pipeline_version': '1'},
    }

    out = RdfOutputStrategy(base_iri='https://orion.local/resource/').generate(payload)
    graph = out['output']['graph']
    schema_rows = graph['schema']['classes']
    schema_iris = {row['iri'] for row in schema_rows}
    schema_labels = {row['label'] for row in schema_rows}
    subclass_facts = {(row['subject'], row['object']) for row in graph['subclass_facts']}

    assert {'BackupArchive', 'InformationAsset', 'VirtualMachine', 'Container', 'ServerlessFunction', 'CloudWorkload'} <= schema_labels
    assert all('TypeOfInformationAsset' not in row['label'] for row in schema_rows)
    assert all('TypeOfCloudWorkload' not in row['label'] for row in schema_rows)
    assert all('/a-' not in iri for iri in schema_iris)
    assert all('/type-of-' not in iri for iri in schema_iris)
    assert ('orion:BackupArchive', 'orion:InformationAsset') in subclass_facts
    assert ('orion:VirtualMachine', 'orion:CloudWorkload') in subclass_facts
    assert ('orion:Container', 'orion:CloudWorkload') in subclass_facts
    assert ('orion:ServerlessFunction', 'orion:CloudWorkload') in subclass_facts

