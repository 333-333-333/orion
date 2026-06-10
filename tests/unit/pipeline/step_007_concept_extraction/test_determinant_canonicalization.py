# TB-ONT-001 | TB-ONT-002

def test_concept_extraction_canonicalizes_leading_determinants_without_touching_surface_text():
    from pipeline.step_007_concept_extraction import extract_concepts_from_payload

    class FakeChunk:
        def __init__(self, text, start_char, end_char, root):
            self.text = text
            self.start_char = start_char
            self.end_char = end_char
            self.root = root

    class FakeRoot:
        def __init__(self, lemma_):
            self.lemma_ = lemma_

    class FakeDoc:
        noun_chunks = [
            FakeChunk('A backup archive', 0, 16, FakeRoot('archive')),
            FakeChunk('A virtual machine', 17, 34, FakeRoot('machine')),
            FakeChunk('A container', 35, 46, FakeRoot('container')),
            FakeChunk('A serverless function', 47, 68, FakeRoot('function')),
            FakeChunk('A type of information asset', 69, 96, FakeRoot('asset')),
            FakeChunk('A type of cloud workload', 97, 122, FakeRoot('workload')),
        ]

    payload = {
        'raw_text': 'A backup archive is a type of information asset. A virtual machine/container/serverless function is a type of cloud workload.',
        'preprocessed_text': 'A backup archive is a type of information asset. A virtual machine/container/serverless function is a type of cloud workload.',
        'source_text_id': 'src-ont-001',
        'sentences': [
            {'sentence_id': 'sent-0001', 'text': 'A backup archive is a type of information asset.', 'index': 0, 'start_offset': 0, 'end_offset': 48},
            {'sentence_id': 'sent-0002', 'text': 'A virtual machine/container/serverless function is a type of cloud workload.', 'index': 1, 'start_offset': 49, 'end_offset': 124},
        ],
        'tokens': [],
        'entities': [],
    }

    result = extract_concepts_from_payload(payload, FakeDoc())
    by_text = {concept['text']: concept for concept in result['concepts']}

    assert by_text['A backup archive']['normalized_text'] == 'backup archive'
    assert by_text['A virtual machine']['normalized_text'] == 'virtual machine'
    assert by_text['A container']['normalized_text'] == 'container'
    assert by_text['A serverless function']['normalized_text'] == 'serverless function'
    assert by_text['A type of information asset']['normalized_text'] == 'type of information asset'
    assert by_text['A type of cloud workload']['normalized_text'] == 'type of cloud workload'
    assert all(concept['text'].startswith('A ') for concept in result['concepts'])
