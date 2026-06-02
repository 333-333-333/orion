import pytest


# UC-NS-001 MF-1 | FUN-NS-001 AC-1 | CON-NS-001 AC-1 | BR-NS-001 | TB-NS-001
def test_orion_config_sets_namespace_defaults_when_not_provided():
    from orion import ORIONConfig

    cfg = ORIONConfig(spacy_model="en_core_web_lg", output_strategy="rdf")

    assert cfg.base_iri == "https://orion.local/resource/"
    assert cfg.prefixes["rdf"] == "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    assert cfg.prefixes["rdfs"] == "http://www.w3.org/2000/01/rdf-schema#"
    assert cfg.prefixes["owl"] == "http://www.w3.org/2002/07/owl#"
    assert cfg.prefixes["orion"] == cfg.base_iri


# UC-NS-001 AF-1 | FUN-NS-001 AC-2 | CON-NS-001 AC-2 | BR-NS-001 | BR-NS-004 | TB-NS-001
def test_orion_config_accepts_custom_base_iri_and_custom_prefixes_preserving_reserved():
    from orion import ORIONConfig

    cfg = ORIONConfig(
        spacy_model="en_core_web_lg",
        output_strategy="rdf",
        base_iri="https://example.org/kg/",
        prefixes={"ex": "https://example.org/ns#", "orion": "https://example.org/kg/"},
    )

    assert cfg.base_iri == "https://example.org/kg/"
    assert cfg.prefixes["ex"] == "https://example.org/ns#"
    assert cfg.prefixes["rdf"] == "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    assert cfg.prefixes["rdfs"] == "http://www.w3.org/2000/01/rdf-schema#"
    assert cfg.prefixes["owl"] == "http://www.w3.org/2002/07/owl#"


# UC-NS-001 EF-1 | FUN-NS-001 AC-3 | CON-NS-001 AC-3 | BR-NS-001 | BR-NS-003 | TB-NS-001
def test_orion_config_from_mapping_supports_base_iri_and_prefixes():
    from orion import ORIONConfig

    cfg = ORIONConfig.from_mapping(
        {
            "spacy_model": "en_core_web_lg",
            "output_strategy": "owl",
            "base_iri": "https://acme.org/resource/",
            "prefixes": {"acme": "https://acme.org/ns#"},
        }
    )

    assert cfg.base_iri == "https://acme.org/resource/"
    assert cfg.prefixes["acme"] == "https://acme.org/ns#"
