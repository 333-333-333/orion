# UC-REL-002 MF-1 | CON-REL-001 AC-1 | BR-REL-003 | TB-REL-001
def test_subject_object_refs_map_to_existing_entity_or_concept_when_available():
    from pipeline.step_008_relation_extraction import extract_relations_from_payload

    payload = {
        "raw_text": "Barack Obama leads initiatives.",
        "preprocessed_text": "Barack Obama leads initiatives.",
        "source_text_id": "src-rel-003",
        "sentences": [{"sentence_id": "sent-0001", "text": "Barack Obama leads initiatives.", "index": 0, "start_offset": 0, "end_offset": 31}],
        "tokens": [
            {"token_id": "tok-0001", "text": "Barack Obama", "lemma": "Barack Obama", "pos": "PROPN", "tag": "NNP", "dependency": "nsubj", "head_text": "leads", "start_offset": 0, "end_offset": 12, "sentence_id": "sent-0001", "source_text_id": "src-rel-003"},
            {"token_id": "tok-0002", "text": "leads", "lemma": "lead", "pos": "VERB", "tag": "VBZ", "dependency": "ROOT", "head_text": "leads", "start_offset": 13, "end_offset": 18, "sentence_id": "sent-0001", "source_text_id": "src-rel-003"},
            {"token_id": "tok-0003", "text": "initiatives", "lemma": "initiative", "pos": "NOUN", "tag": "NNS", "dependency": "dobj", "head_text": "leads", "start_offset": 19, "end_offset": 30, "sentence_id": "sent-0001", "source_text_id": "src-rel-003"},
        ],
        "entities": [{"entity_id": "ent-0001", "text": "Barack Obama", "label": "PERSON", "start_offset": 0, "end_offset": 12, "sentence_id": "sent-0001", "source_text_id": "src-rel-003"}],
        "concepts": [{"concept_id": "con-0001", "text": "initiatives", "lemma": "initiative", "source": "noun_chunk", "start_offset": 19, "end_offset": 30, "sentence_id": "sent-0001", "source_text_id": "src-rel-003", "confidence": 0.9}],
    }

    result = extract_relations_from_payload(payload)

    rel = result["relations"][0]
    assert rel["subject_ref"] == "ent-0001"
    assert rel["object_ref"] == "con-0001"
