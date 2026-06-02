import pytest


# UC-002 MF-2 | UC-003 MF-2 | FUN-003 AC-1 | FUN-004 AC-1 | FUN-013 AC-1 | TASK-PRP-001 | TB-PRP-001
def test_preprocessing_contract_preserves_raw_text_and_source_metadata_and_adds_outputs():
    from pipeline.step_002_preprocessing import preprocess_input

    input_payload = {
        "raw_text": "Árbol  grande\nMUNDO",
        "source_text_id": "src-abc-123",
        "metadata": {"source": {"kind": "string", "start_offset": 0, "end_offset": 18}},
    }

    result = preprocess_input(input_payload)

    assert result["raw_text"] == input_payload["raw_text"]
    assert result["source_text_id"] == input_payload["source_text_id"]
    assert result["metadata"] == input_payload["metadata"]
    assert "preprocessed_text" in result
    assert isinstance(result["operations_applied"], list)


# UC-002 MF-2 | UC-006 MF-4 | NFR-001 AC-1 | NFR-002 AC-1 | TASK-PRP-001 | TB-PRP-001
def test_preprocessing_contract_keeps_case_intact_and_does_not_lowercase_text():
    from pipeline.step_002_preprocessing import preprocess_input

    input_payload = {
        "raw_text": "Árbol y NASA en MUNDO",
        "source_text_id": "src-case-001",
        "metadata": {"source": {"kind": "string", "start_offset": 0, "end_offset": 20}},
    }

    result = preprocess_input(input_payload)

    assert "NASA" in result["preprocessed_text"]
    assert "MUNDO" in result["preprocessed_text"]
    assert "Árbol" in result["preprocessed_text"]
