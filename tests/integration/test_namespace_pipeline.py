# UC-NS-005 MF-1 | FUN-NS-005 AC-1 | CON-NS-003 AC-1 | BR-NS-011 | TB-NS-001
def test_orion_process_accepts_namespace_config_and_emits_namespace_aware_output():
    from orion import ORION

    sut = ORION(
        config={
            "spacy_model": "en_core_web_lg",
            "output_strategy": "rdf",
            "base_iri": "https://kg.example/resource/",
            "prefixes": {"ex": "https://kg.example/ns#"},
        }
    )

    result = sut.process("John works at Acme.")

    graph = result["output"]["graph"]
    assert set(graph.keys()) == {"facts", "instance_facts", "subclass_facts"}

    for fact in graph["facts"]:
        assert fact["subject"].startswith("https://kg.example/resource/")
        assert fact["predicate"].startswith(("ex:", "orion:"))
        assert fact["predicate"] != "orion:relatedTo"
