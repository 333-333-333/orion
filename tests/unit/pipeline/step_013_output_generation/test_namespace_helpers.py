# UC-NS-003 MF-1 | FUN-NS-003 AC-1 | BR-NS-005 | TB-NS-001
def test_slugify_iri_part_supports_pascal_case_camel_case_and_individual_style():
    from pipeline.step_013_output_generation.namespace import slugify_iri_part

    assert slugify_iri_part("customer account", style="class") == "CustomerAccount"
    assert slugify_iri_part("works at", style="predicate") == "worksAt"
    assert slugify_iri_part("John Doe #1", style="individual") == "john-doe-1"


# UC-NS-003 AF-1 | FUN-NS-003 AC-2 | BR-NS-006 | TB-NS-001
def test_make_iri_builds_stable_class_predicate_individual_iris():
    from pipeline.step_013_output_generation.namespace import make_iri

    assert make_iri("person", kind="class") == "https://orion.local/resource/Person"
    assert make_iri("works at", kind="predicate") == "https://orion.local/resource/worksAt"
    assert make_iri("john doe", kind="individual") == "https://orion.local/resource/john-doe"


# UC-NS-003 EF-1 | FUN-NS-003 AC-3 | BR-NS-007 | TB-NS-001
def test_compact_iri_uses_known_prefixes_and_keeps_unknown_full_iri():
    from pipeline.step_013_output_generation.namespace import compact_iri

    assert compact_iri("http://www.w3.org/1999/02/22-rdf-syntax-ns#type") == "rdf:type"
    assert compact_iri("https://orion.local/resource/Person") == "orion:Person"
    assert compact_iri("https://unknown.example/x") == "https://unknown.example/x"
