# TB-ONT-001 | TB-ONT-002

def test_taxonomic_sentences_do_not_turn_into_instance_of_assertions():
    from pipeline.step_011_type_assertion import extract_type_assertions_from_payload

    payload = {
        'raw_text': 'A backup archive is a type of information asset. A virtual machine/container/serverless function is a type of cloud workload.',
        'preprocessed_text': 'A backup archive is a type of information asset. A virtual machine/container/serverless function is a type of cloud workload.',
        'source_text_id': 'src-ont-003',
        'sentences': [
            {'sentence_id': 'sent-0001', 'text': 'A backup archive is a type of information asset.', 'index': 0, 'start_offset': 0, 'end_offset': 48},
            {'sentence_id': 'sent-0002', 'text': 'A virtual machine/container/serverless function is a type of cloud workload.', 'index': 1, 'start_offset': 49, 'end_offset': 124},
        ],
        'tokens': [],
        'entities': [
            {'entity_id': 'ent-0001', 'text': 'backup archive', 'normalized_text': 'backup archive', 'sentence_id': 'sent-0001', 'source_text_id': 'src-ont-003'},
            {'entity_id': 'ent-0002', 'text': 'virtual machine', 'normalized_text': 'virtual machine', 'sentence_id': 'sent-0002', 'source_text_id': 'src-ont-003'},
            {'entity_id': 'ent-0003', 'text': 'container', 'normalized_text': 'container', 'sentence_id': 'sent-0002', 'source_text_id': 'src-ont-003'},
            {'entity_id': 'ent-0004', 'text': 'serverless function', 'normalized_text': 'serverless function', 'sentence_id': 'sent-0002', 'source_text_id': 'src-ont-003'},
        ],
        'concepts': [
            {'concept_id': 'con-0001', 'text': 'backup archive', 'normalized_text': 'backup archive', 'sentence_id': 'sent-0001', 'source_text_id': 'src-ont-003'},
            {'concept_id': 'con-0002', 'text': 'information asset', 'normalized_text': 'information asset', 'sentence_id': 'sent-0001', 'source_text_id': 'src-ont-003'},
            {'concept_id': 'con-0003', 'text': 'virtual machine', 'normalized_text': 'virtual machine', 'sentence_id': 'sent-0002', 'source_text_id': 'src-ont-003'},
            {'concept_id': 'con-0004', 'text': 'container', 'normalized_text': 'container', 'sentence_id': 'sent-0002', 'source_text_id': 'src-ont-003'},
            {'concept_id': 'con-0005', 'text': 'serverless function', 'normalized_text': 'serverless function', 'sentence_id': 'sent-0002', 'source_text_id': 'src-ont-003'},
            {'concept_id': 'con-0006', 'text': 'cloud workload', 'normalized_text': 'cloud workload', 'sentence_id': 'sent-0002', 'source_text_id': 'src-ont-003'},
        ],
        'relations': [],
        'triples': [],
        'taxonomy_relations': [],
    }

    result = extract_type_assertions_from_payload(payload)

    assert result['type_assertions'] == []
