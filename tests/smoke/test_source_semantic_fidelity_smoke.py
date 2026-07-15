from __future__ import annotations

import json
from pathlib import Path

_CASES_DIR = Path(__file__).parent / "cases"


def _claims_for(case: str, artifact: str, evidence: str) -> set[tuple[str, str, str]]:
    payload = json.loads((_CASES_DIR / case / "artifacts" / artifact).read_text(encoding="utf-8"))
    return {
        (str(claim.get("subject")), str(claim.get("predicate")), str(claim.get("object")))
        for claim in payload.get("claims", [])
        if isinstance(claim, dict) and str((claim.get("source") or {}).get("evidence")) == evidence
    }


def test_dependency_fallback_preserves_uncovered_source_relations_without_replacing_existing_claims():
    contracts = [
        (
            "infosec_p009_p010",
            "observed_p009_p010_semantic_claims.json",
            "An access token must expire after a defined period.",
            {("AccessToken", "mustExpireAfter", "DefinedPeriod")},
        ),
        (
            "infosec_p009_p010",
            "observed_p009_p010_semantic_claims.json",
            "An API key must be rotated periodically.",
            {("APIKey", "mustBeRotated", "Periodically")},
        ),
        (
            "infosec_p009_p010",
            "observed_p009_p010_semantic_claims.json",
            "A compromised credential must be revoked immediately.",
            {("CompromisedCredential", "mustBeRevoked", "Immediately")},
        ),
        (
            "infosec_p011_p012",
            "observed_p011_p012_semantic_claims.json",
            "Access certification confirms that access remains appropriate.",
            {("Access", "remains", "Appropriate")},
        ),
        (
            "infosec_p031_p032",
            "observed_p031_p032_semantic_claims.json",
            "Change testing verifies that a change works as intended.",
            {("Change", "works", "Intended")},
        ),
        (
            "infosec_p035_p036",
            "observed_p035_p036_semantic_claims.json",
            "A security control can protect one or more assets.",
            {("SecurityControl", "canProtect", "Asset")},
        ),
        (
            "infosec_p035_p036",
            "observed_p035_p036_semantic_claims.json",
            "An asset can be affected by one or more risks.",
            {("Asset", "canBeAffectedBy", "Risk")},
        ),
        (
            "infosec_p035_p036",
            "observed_p035_p036_semantic_claims.json",
            "A requirement can be satisfied by one or more controls.",
            {("Requirement", "canBeSatisfiedBy", "Control")},
        ),
        (
            "infosec_p039_p040",
            "observed_p039_p040_semantic_claims.json",
            "Email filtering may detect and block the phishing email.",
            {
                ("EmailFiltering", "mayDetect", "PhishingEmail"),
                ("EmailFiltering", "mayBlock", "PhishingEmail"),
            },
        ),
        (
            "infosec_p043",
            "observed_p043_semantic_claims.json",
            "The resulting ontology should represent that users access systems, roles include permissions, controls reduce risks, threats exploit vulnerabilities, incidents affect assets, systems process information assets, policies define requirements, requirements are satisfied by controls, suppliers provide services, and auditors evaluate compliance.",
            {
                ("Role", "includes", "Permission"),
                ("Control", "reduces", "Risk"),
                ("Threat", "exploits", "Vulnerability"),
                ("Incident", "affects", "Asset"),
                ("Policy", "defines", "Requirement"),
                ("Requirement", "beSatisfiedBy", "Control"),
                ("Supplier", "provides", "Service"),
                ("Auditor", "evaluates", "Compliance"),
            },
        ),
    ]

    violations: list[str] = []
    for case, artifact, evidence, expected in contracts:
        observed = _claims_for(case, artifact, evidence)
        missing = sorted(expected - observed)
        if missing:
            violations.append(f"{case}: missing={missing} for {evidence}")
    assert not violations, "source semantic dependency fallback broken:\n" + "\n".join(violations)


def test_core_definitions_keep_atomic_parent_classes_instead_of_clause_resources():
    contracts = [
        (
            "infosec_p007_p008",
            "observed_p007_p008_semantic_claims.json",
            "Confidential information is a type of information whose unauthorized disclosure may harm the organization, customers, employees, or partners.",
            ("ConfidentialInformation", "is_a", "Information"),
        ),
        (
            "infosec_p017_p018",
            "observed_p017_p018_semantic_claims.json",
            "A cloud workload is a type of computing resource hosted in a cloud environment.",
            ("CloudWorkload", "is_a", "ComputingResource"),
        ),
        (
            "infosec_p025_p026",
            "observed_p025_p026_semantic_claims.json",
            "An office is a type of facility where employees perform business activities.",
            ("Office", "is_a", "Facility"),
        ),
        (
            "infosec_p029_p030",
            "observed_p029_p030_semantic_claims.json",
            "A legal requirement is a type of compliance requirement derived from law.",
            ("LegalRequirement", "is_a", "ComplianceRequirement"),
        ),
        (
            "infosec_p029_p030",
            "observed_p029_p030_semantic_claims.json",
            "A data subject is a person whose personal data is processed.",
            ("DataSubject", "is_a", "Person"),
        ),
        (
            "infosec_p031_p032",
            "observed_p031_p032_semantic_claims.json",
            "An emergency change is a type of change implemented rapidly to resolve urgent issues.",
            ("EmergencyChange", "is_a", "Change"),
        ),
    ]

    violations: list[str] = []
    for case, artifact, evidence, expected in contracts:
        observed = _claims_for(case, artifact, evidence)
        if expected not in observed:
            violations.append(f"{case}: missing atomic definition={expected} for {evidence}")
    assert not violations, "atomic definition core rule broken:\n" + "\n".join(violations)


def test_core_discourse_frames_do_not_become_domain_resources_or_meta_facts():
    p037_evidence = "For example, a customer database stores personal data and financial data."
    p037 = _claims_for(
        "infosec_p037_p038",
        "observed_p037_p038_semantic_claims.json",
        p037_evidence,
    )
    assert ("CustomerDatabase", "stores", "PersonalData") in p037
    assert all(not subject.startswith("ForExample") for subject, _, _ in p037)

    pizza_evidence = "Inside the kitchen, the wood oven named Dante burns oak logs and holds a temperature near 430 degrees Celsius."
    pizza = _claims_for("pizza_short", "observed_pizza_short_semantic_claims.json", pizza_evidence)
    assert ("WoodOvenNamedDante", "burns", "OakLog") in pizza
    assert all(not subject.startswith("InsideTheKitchen") for subject, _, _ in pizza)

    another_example = _claims_for(
        "infosec_p037_p038",
        "observed_p037_p038_semantic_claims.json",
        "Another example involves remote access.",
    )
    assert another_example == set()

    discourse_result = _claims_for(
        "infosec_p043",
        "observed_p043_semantic_claims.json",
        "These relationships make the generated RDF or OWL graph suitable for querying, validation, reasoning, and mining.",
    )
    assert discourse_result == {
        ("GeneratedGraph", "suitable_for", "Querying"),
        ("GeneratedGraph", "suitable_for", "Validation"),
        ("GeneratedGraph", "suitable_for", "Reasoning"),
        ("GeneratedGraph", "suitable_for", "Mining"),
    }
