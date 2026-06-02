import pytest


# UC-001 MF-2 | FUN-002 AC-1 | CON-008 AC-1 | BR-LING-001 | TB-LING-001
def test_orion_config_uses_en_core_web_lg_when_spacy_model_is_none():
    from orion import ORIONConfig

    cfg = ORIONConfig(spacy_model=None)

    assert cfg.spacy_model == "en_core_web_lg"


# UC-001 EF-1 | FUN-013 AC-1 | CON-008 AC-2 | BR-LING-001 | TB-LING-001
def test_orion_config_rejects_empty_spacy_model_string():
    from orion import ORIONConfig

    with pytest.raises(Exception):
        ORIONConfig(spacy_model="")


# UC-001 AF-1 | FUN-002 AC-1 | CON-008 AC-3 | BR-LING-001 | TB-LING-001
def test_orion_config_accepts_non_empty_spacy_model_string():
    from orion import ORIONConfig

    cfg = ORIONConfig(spacy_model="es_core_news_lg")

    assert cfg.spacy_model == "es_core_news_lg"


# UC-OUT-001 MF-1 | FUN-OUT-001 AC-1 | CON-OUT-001 AC-1 | BR-OUT-001 | TB-OUT-001
def test_orion_config_sets_default_output_strategy_to_rdf():
    from orion import ORIONConfig

    cfg = ORIONConfig(spacy_model="en_core_web_lg")

    assert cfg.output_strategy == "rdf"


# UC-OUT-001 AF-1 | FUN-OUT-001 AC-2 | CON-OUT-001 AC-2 | BR-OUT-001 | TB-OUT-001
def test_orion_config_accepts_output_strategy_rdf_and_owl():
    from orion import ORIONConfig

    rdf_cfg = ORIONConfig(spacy_model="en_core_web_lg", output_strategy="rdf")
    owl_cfg = ORIONConfig(spacy_model="en_core_web_lg", output_strategy="owl")

    assert rdf_cfg.output_strategy == "rdf"
    assert owl_cfg.output_strategy == "owl"


# UC-OUT-001 EF-1 | FUN-OUT-001 AC-3 | CON-OUT-001 AC-3 | BR-OUT-001 | TB-OUT-001
def test_orion_config_rejects_invalid_output_strategy_with_clear_orion_error():
    from orion import ORIONConfig

    with pytest.raises(Exception, match="ORION config error: output_strategy must be one of: rdf, owl"):
        ORIONConfig(spacy_model="en_core_web_lg", output_strategy="ttl")
