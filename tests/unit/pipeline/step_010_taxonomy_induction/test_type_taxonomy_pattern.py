# TB-ONT-001 | TB-ONT-002

def test_type_taxonomy_pattern_captures_only_real_superclass_and_strips_leading_article():
    from pipeline.step_010_taxonomy_induction import extract_taxonomy_relations_from_payload

    payload = {
        'raw_text': 'A backup archive is a type of information asset. A virtual machine/container/serverless function is a type of cloud workload.',
        'preprocessed_text': 'A backup archive is a type of information asset. A virtual machine/container/serverless function is a type of cloud workload.',
        'source_text_id': 'src-ont-002',
        'sentences': [
            {'sentence_id': 'sent-0001', 'text': 'A backup archive is a type of information asset.', 'index': 0, 'start_offset': 0, 'end_offset': 48},
            {'sentence_id': 'sent-0002', 'text': 'A virtual machine/container/serverless function is a type of cloud workload.', 'index': 1, 'start_offset': 49, 'end_offset': 124},
        ],
        'tokens': [],
        'entities': [
            {'entity_id': 'ent-0001', 'text': 'backup archive', 'normalized_text': 'backup archive', 'sentence_id': 'sent-0001', 'source_text_id': 'src-ont-002'},
            {'entity_id': 'ent-0002', 'text': 'virtual machine', 'normalized_text': 'virtual machine', 'sentence_id': 'sent-0002', 'source_text_id': 'src-ont-002'},
            {'entity_id': 'ent-0003', 'text': 'container', 'normalized_text': 'container', 'sentence_id': 'sent-0002', 'source_text_id': 'src-ont-002'},
            {'entity_id': 'ent-0004', 'text': 'serverless function', 'normalized_text': 'serverless function', 'sentence_id': 'sent-0002', 'source_text_id': 'src-ont-002'},
        ],
        'concepts': [
            {'concept_id': 'con-0001', 'text': 'backup archive', 'normalized_text': 'backup archive', 'sentence_id': 'sent-0001', 'source_text_id': 'src-ont-002'},
            {'concept_id': 'con-0002', 'text': 'information asset', 'normalized_text': 'information asset', 'sentence_id': 'sent-0001', 'source_text_id': 'src-ont-002'},
            {'concept_id': 'con-0003', 'text': 'virtual machine', 'normalized_text': 'virtual machine', 'sentence_id': 'sent-0002', 'source_text_id': 'src-ont-002'},
            {'concept_id': 'con-0004', 'text': 'container', 'normalized_text': 'container', 'sentence_id': 'sent-0002', 'source_text_id': 'src-ont-002'},
            {'concept_id': 'con-0005', 'text': 'serverless function', 'normalized_text': 'serverless function', 'sentence_id': 'sent-0002', 'source_text_id': 'src-ont-002'},
            {'concept_id': 'con-0006', 'text': 'cloud workload', 'normalized_text': 'cloud workload', 'sentence_id': 'sent-0002', 'source_text_id': 'src-ont-002'},
        ],
        'relations': [],
        'triples': [],
    }

    result = extract_taxonomy_relations_from_payload(payload)
    pairs = {(rel['subclass'], rel['superclass']) for rel in result['taxonomy_relations']}

    assert ('backup archive', 'information asset') in pairs
    assert all(not rel['superclass'].startswith('type ') for rel in result['taxonomy_relations'])
    assert all(rel['superclass'] != 'type of information asset' for rel in result['taxonomy_relations'])
    assert all(rel['superclass'] != 'type of cloud workload' for rel in result['taxonomy_relations'])



def test_taxonomy_pattern_reduces_reduced_clause_superclass_to_head_noun():
    from pipeline.step_010_taxonomy_induction import extract_taxonomy_relations_from_payload

    payload = {
        'raw_text': 'An endpoint is a device connected to the organizational network.',
        'preprocessed_text': 'An endpoint is a device connected to the organizational network.',
        'source_text_id': 'src-ont-003',
        'sentences': [
            {'sentence_id': 'sent-0001', 'text': 'An endpoint is a device connected to the organizational network.', 'index': 0, 'start_offset': 0, 'end_offset': 64},
        ],
        'tokens': [],
        'entities': [
            {'entity_id': 'ent-0001', 'text': 'endpoint', 'normalized_text': 'endpoint', 'sentence_id': 'sent-0001', 'source_text_id': 'src-ont-003'},
        ],
        'concepts': [
            {'concept_id': 'con-0001', 'text': 'endpoint', 'normalized_text': 'endpoint', 'sentence_id': 'sent-0001', 'source_text_id': 'src-ont-003'},
            {'concept_id': 'con-0002', 'text': 'device', 'normalized_text': 'device', 'sentence_id': 'sent-0001', 'source_text_id': 'src-ont-003'},
        ],
        'relations': [],
        'triples': [],
    }

    result = extract_taxonomy_relations_from_payload(payload)
    pairs = {(rel['subclass'], rel['superclass']) for rel in result['taxonomy_relations']}

    assert ('endpoint', 'device') in pairs
    assert all('connected to the organizational network' not in rel['superclass'] for rel in result['taxonomy_relations'])
