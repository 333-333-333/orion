import pytest


# UC-NS-002 EF-1 | FUN-NS-002 AC-1 | CON-NS-002 AC-1 | BR-NS-002 | TB-NS-001
def test_orion_config_rejects_empty_base_iri():
    from orion import ORIONConfig

    with pytest.raises(Exception, match="base_iri"):
        ORIONConfig(spacy_model="en_core_web_lg", output_strategy="rdf", base_iri="")


# UC-NS-002 EF-2 | FUN-NS-002 AC-2 | CON-NS-002 AC-2 | BR-NS-002 | TB-NS-001
def test_orion_config_rejects_non_absolute_or_non_http_base_iri():
    from orion import ORIONConfig

    with pytest.raises(Exception, match="base_iri"):
        ORIONConfig(spacy_model="en_core_web_lg", output_strategy="rdf", base_iri="urn:demo")

    with pytest.raises(Exception, match="base_iri"):
        ORIONConfig(spacy_model="en_core_web_lg", output_strategy="rdf", base_iri="/relative/path")


# UC-NS-002 EF-3 | FUN-NS-002 AC-3 | CON-NS-002 AC-3 | BR-NS-004 | TB-NS-001
def test_orion_config_rejects_empty_prefixes_map_and_empty_prefix_values():
    from orion import ORIONConfig

    with pytest.raises(Exception, match="prefixes"):
        ORIONConfig(spacy_model="en_core_web_lg", output_strategy="rdf", prefixes={})

    with pytest.raises(Exception, match="prefixes"):
        ORIONConfig(spacy_model="en_core_web_lg", output_strategy="rdf", prefixes={"ex": ""})


# UC-NS-002 EF-4 | FUN-NS-002 AC-4 | CON-NS-002 AC-4 | BR-NS-003 | TB-NS-001
def test_orion_config_rejects_overriding_reserved_prefixes_with_invalid_values():
    from orion import ORIONConfig

    with pytest.raises(Exception, match="rdf"):
        ORIONConfig(spacy_model="en_core_web_lg", output_strategy="rdf", prefixes={"rdf": "not-a-uri"})

    with pytest.raises(Exception, match="owl"):
        ORIONConfig(spacy_model="en_core_web_lg", output_strategy="rdf", prefixes={"owl": ""})
