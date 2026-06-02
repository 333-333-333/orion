# UC-TAX-001 MF-1 | UC-TAX-001 AF-1 | UC-TAX-001 AF-2 | FUN-TAX-001 AC-1 | FUN-TAX-001 AC-2 | BR-TAX-001 | BR-TAX-002 | BR-TAX-003 | TB-TAX-001
def test_extracts_taxonomy_relations_from_supported_patterns_and_rejects_instance_case():
    from pipeline.step_010_taxonomy_induction import extract_taxonomy_relations_from_payload

    payload = {
        "raw_text": "A robin is a bird. Birds such as robins migrate. Mammals including dogs are warm-blooded. John is a person.",
        "preprocessed_text": "A robin is a bird. Birds such as robins migrate. Mammals including dogs are warm-blooded. John is a person.",
        "source_text_id": "src-tax-001",
        "sentences": [
            {"sentence_id": "sent-0001", "text": "A robin is a bird.", "index": 0, "start_offset": 0, "end_offset": 18},
            {"sentence_id": "sent-0002", "text": "Birds such as robins migrate.", "index": 1, "start_offset": 19, "end_offset": 47},
            {"sentence_id": "sent-0003", "text": "Mammals including dogs are warm-blooded.", "index": 2, "start_offset": 48, "end_offset": 88},
            {"sentence_id": "sent-0004", "text": "John is a person.", "index": 3, "start_offset": 89, "end_offset": 106},
        ],
        "tokens": [
            {"token_id": "tok-0001", "text": "robin", "lemma": "robin", "pos": "NOUN", "sentence_id": "sent-0001", "source_text_id": "src-tax-001"},
            {"token_id": "tok-0002", "text": "bird", "lemma": "bird", "pos": "NOUN", "sentence_id": "sent-0001", "source_text_id": "src-tax-001"},
            {"token_id": "tok-0003", "text": "Birds", "lemma": "bird", "pos": "NOUN", "sentence_id": "sent-0002", "source_text_id": "src-tax-001"},
            {"token_id": "tok-0004", "text": "robins", "lemma": "robin", "pos": "NOUN", "sentence_id": "sent-0002", "source_text_id": "src-tax-001"},
            {"token_id": "tok-0005", "text": "Mammals", "lemma": "mammal", "pos": "NOUN", "sentence_id": "sent-0003", "source_text_id": "src-tax-001"},
            {"token_id": "tok-0006", "text": "dogs", "lemma": "dog", "pos": "NOUN", "sentence_id": "sent-0003", "source_text_id": "src-tax-001"},
            {"token_id": "tok-0007", "text": "John", "lemma": "John", "pos": "PROPN", "sentence_id": "sent-0004", "source_text_id": "src-tax-001"},
            {"token_id": "tok-0008", "text": "person", "lemma": "person", "pos": "NOUN", "sentence_id": "sent-0004", "source_text_id": "src-tax-001"},
        ],
        "concepts": [
            {"concept_id": "con-0001", "text": "robin", "lemma": "robin", "normalized_text": "robin", "sentence_id": "sent-0001", "source_text_id": "src-tax-001"},
            {"concept_id": "con-0002", "text": "bird", "lemma": "bird", "normalized_text": "bird", "sentence_id": "sent-0001", "source_text_id": "src-tax-001"},
            {"concept_id": "con-0003", "text": "mammal", "lemma": "mammal", "normalized_text": "mammal", "sentence_id": "sent-0003", "source_text_id": "src-tax-001"},
            {"concept_id": "con-0004", "text": "dog", "lemma": "dog", "normalized_text": "dog", "sentence_id": "sent-0003", "source_text_id": "src-tax-001"},
            {"concept_id": "con-0005", "text": "person", "lemma": "person", "normalized_text": "person", "sentence_id": "sent-0004", "source_text_id": "src-tax-001"},
        ],
        "relations": [],
        "triples": [],
        "entities": [
            {"entity_id": "ent-0001", "text": "John", "normalized_text": "john", "sentence_id": "sent-0004", "source_text_id": "src-tax-001"}
        ],
    }

    result = extract_taxonomy_relations_from_payload(payload)

    assert "taxonomy_relations" in result
    required = {
        "taxonomy_relation_id", "subclass", "superclass", "subclass_ref", "superclass_ref",
        "relation_type", "source", "sentence_id", "source_text_id", "confidence", "evidence_span"
    }
    for rel in result["taxonomy_relations"]:
        assert required.issubset(rel.keys())
        assert rel["relation_type"] == "subclass_of"
        assert rel["source"] in {"copula_pattern", "such_as_pattern", "relation_pattern"}

    pairs = {(r["subclass"], r["superclass"]) for r in result["taxonomy_relations"]}
    assert ("robin", "bird") in pairs
    assert ("dog", "mammal") in pairs
    assert ("john", "person") not in pairs
