import pytest


# UC-TAX-004 MF-1 | FUN-014 AC-2 | FUN-016 AC-1 | NFR-007 AC-2 | BR-TAX-006 | TB-TAX-001
def test_taxonomy_induction_events_started_completed_and_no_raw_text_memory_sink():
    from observability import MemoryLogSink
    from orion import ORION

    sink = MemoryLogSink()
    sut = ORION(config={"logging": {"sink": sink}, "spacy_model": "en_core_web_lg"})

    sut.process("A robin is a bird.")

    events = [e.to_dict() for e in sink.events if e.phase == "taxonomy_induction"]
    assert any(e["event_type"] == "started" for e in events)
    assert any(e["event_type"] == "completed" for e in events)
    assert all("raw_text" not in e for e in events)
    assert all("raw_text" not in e.get("metadata", {}) for e in events)


# UC-TAX-004 EF-1 | FUN-014 AC-3 | FUN-016 AC-2 | NFR-007 AC-2 | BR-TAX-006 | TB-TAX-001
def test_taxonomy_induction_failed_event_and_no_raw_text_jsonl(tmp_path):
    import json
    from observability import JsonlFileLogSink
    from orion import ORION

    class _ExplodeTaxonomyInductionORION(ORION):
        def _run_taxonomy_induction(self, payload):
            raise RuntimeError("boom-taxonomy-induction")

    out_file = tmp_path / "taxonomy-events.jsonl"
    sut = _ExplodeTaxonomyInductionORION(config={"logging": {"sink": JsonlFileLogSink(out_file)}, "spacy_model": "en_core_web_lg"})

    with pytest.raises(RuntimeError):
        sut.process("A robin is a bird.")

    payloads = [json.loads(line) for line in out_file.read_text(encoding="utf-8").splitlines()]
    tax = [p for p in payloads if p["phase"] == "taxonomy_induction"]

    assert any(e["event_type"] == "started" for e in tax)
    assert any(e["event_type"] == "failed" for e in tax)
    assert all("raw_text" not in p for p in tax)
    assert all("raw_text" not in p.get("metadata", {}) for p in tax)
