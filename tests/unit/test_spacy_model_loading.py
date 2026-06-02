import pytest


# UC-001 EF-2 | FUN-013 AC-1 | CON-005 AC-1 | BR-LING-002 | TB-LING-001
def test_spacy_model_load_missing_raises_orion_exception_not_raw_import_or_os_error(monkeypatch):
    import importlib

    from orion import ORION

    real_import_module = importlib.import_module

    def fake_import_module(name, package=None):
        module = real_import_module(name, package)
        if name == "spacy":
            class FakeSpacy:
                @staticmethod
                def load(_model_name):
                    raise OSError("can't find model")

            return FakeSpacy()
        return module

    monkeypatch.setattr(importlib, "import_module", fake_import_module)

    sut = ORION(config={"spacy_model": "en_core_web_lg"})

    with pytest.raises(Exception) as exc_info:
        sut.process("Birds fly.")

    assert "ORION" in str(exc_info.value).upper()
    assert not isinstance(exc_info.value, ImportError)
    assert not isinstance(exc_info.value, OSError)
