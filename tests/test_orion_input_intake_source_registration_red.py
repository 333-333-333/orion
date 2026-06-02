import pytest

# Contrato esperado fase 1 ORION
from orion import ORION, OrionError  # noqa: F401


def _new_orion():
    return ORION(config={})


# UC-002 MF-1 | FUN-003 AC-1 | TASK-ORION-001-001
def test_process_string_returns_raw_text_exact_without_preprocessing():
    sut = _new_orion()
    text = "  Hola\nMundo\t"
    result = sut.process(text)

    assert isinstance(result, dict)
    assert result["raw_text"] == text


# UC-002 MF-4 | NFR-001 AC-1 | TASK-ORION-001-005
def test_process_string_source_text_id_is_deterministic_same_input():
    sut = _new_orion()
    text = "Deterministic source id"

    r1 = sut.process(text)
    r2 = sut.process(text)

    assert r1["source_text_id"] == r2["source_text_id"]


# UC-006 MF-4 | NFR-002 AC-1 | TASK-ORION-001-005
def test_process_string_exposes_base_traceability_metadata_for_offsets():
    sut = _new_orion()
    text = "ABC DEF"
    result = sut.process(text)

    assert "metadata" in result
    md = result["metadata"]
    assert "source" in md
    assert md["source"]["kind"] == "string"
    assert md["source"]["start_offset"] == 0
    assert md["source"]["end_offset"] == len(text)


# UC-003 MF-1 | FUN-004 AC-1 | TASK-ORION-001-003
def test_process_txt_path_reads_and_keeps_raw_text_exact(tmp_path):
    sut = _new_orion()
    file_path = tmp_path / "input.txt"
    text = "Linea 1\nLinea 2\n"
    file_path.write_text(text, encoding="utf-8")

    result = sut.process(file_path)

    assert result["raw_text"] == text
    assert result["metadata"]["source"]["kind"] == "file"
    assert result["metadata"]["source"]["path"] == str(file_path)


# UC-002 EF-1 | FUN-003 AC-2 | FUN-013 AC-1 | TASK-ORION-001-001
def test_process_empty_string_raises_orion_exception():
    sut = _new_orion()

    with pytest.raises(OrionError):
        sut.process("")


# UC-002 EF-1 | FUN-013 AC-1 | TASK-ORION-001-001
def test_process_invalid_type_raises_orion_exception():
    sut = _new_orion()

    with pytest.raises(OrionError):
        sut.process(123)


# UC-003 E1 | FUN-004 AC-2 | CON-006 AC-2 | FUN-013 AC-1 | TASK-ORION-001-003
def test_process_non_txt_extension_raises_orion_exception(tmp_path):
    sut = _new_orion()
    file_path = tmp_path / "input.md"
    file_path.write_text("hola", encoding="utf-8")

    with pytest.raises(OrionError):
        sut.process(file_path)


# UC-003 E2 | FUN-004 AC-3 | FUN-013 AC-1 | TASK-ORION-001-003
def test_process_nonexistent_path_raises_orion_exception(tmp_path):
    sut = _new_orion()
    missing = tmp_path / "missing.txt"

    with pytest.raises(OrionError):
        sut.process(missing)
