import pytest


# UC-002 E1 | FUN-013 AC-1 | US-013 AC-1 | TASK-PRP-003 | TB-PRP-001
def test_preprocessing_raises_orion_error_when_cleanup_results_in_empty_text():
    from orion import OrionError
    from pipeline.step_002_preprocessing import preprocess_input

    payload = {
        "raw_text": "   \n\t  ",
        "source_text_id": "src-empty-001",
        "metadata": {"source": {"kind": "string", "start_offset": 0, "end_offset": 6}},
    }

    with pytest.raises(OrionError):
        preprocess_input(payload)
