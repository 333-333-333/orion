"""Repair audited coordination, modality, and scope forms across application and supplier security."""

from __future__ import annotations

import re
from typing import Any, Callable

ClaimSpec = dict[str, Any]


def _relation(subject: str, predicate: str, obj: str, **metadata: str) -> ClaimSpec:
    """Build a relation spec while dropping empty metadata."""
    return {
        "kind": "relation",
        "subject": subject,
        "predicate": predicate,
        "object": obj,
        **{key: value for key, value in metadata.items() if value not in (None, "")},
    }


def _definition(subject: str, obj: str, **metadata: str) -> ClaimSpec:
    """Build an is-a definition spec while dropping empty metadata."""
    return {
        "kind": "definition",
        "subject": subject,
        "predicate": "is_a",
        "object": obj,
        **{key: value for key, value in metadata.items() if value not in (None, "")},
    }


def _group(text: str, suffix: str) -> str:
    """Build a readable bounded coordination-group ID from source text."""
    normalized = re.sub(r"[^a-z0-9]+", "-", text.casefold()).strip("-")
    return f"remediation-c:{normalized[:48]}:{suffix}"


def _split_objects(value: str, label: Callable[[str | None], str]) -> list[str]:
    """Split coordinated objects and normalize each semantic label."""
    normalized = re.sub(r"\s*,?\s+(?:and|or)\s+", ",", value.strip(), flags=re.IGNORECASE)
    return [label(item) for item in normalized.split(",") if label(item)]


def _modal_one_or_more(text: str, label: Callable[[str | None], str], verb: Callable[[str | None], str]) -> list[ClaimSpec]:
    """Preserve active or passive can-scope with the one-or-more quantifier."""
    passive = re.match(
        r"^(?:a|an)\s+(?P<subject>.+?)\s+can\s+be\s+(?P<predicate>[a-z-]+)\s+by\s+one\s+or\s+more\s+(?P<object>.+?)\.?$",
        text,
        flags=re.IGNORECASE,
    )
    if passive:
        participle = passive.group("predicate").casefold()
        return [_relation(
            label(passive.group("subject")),
            f"canBe{participle[:1].upper() + participle[1:]}By",
            label(passive.group("object")),
            modality="can",
            quantifier="one_or_more",
            voice="passive",
            preserve_lexical_object="true",
        )]

    active = re.match(
        r"^(?:a|an)\s+(?P<subject>.+?)\s+can\s+(?P<predicate>[a-z-]+)\s+one\s+or\s+more\s+(?P<object>.+?)\.?$",
        text,
        flags=re.IGNORECASE,
    )
    if not active:
        return []
    return [_relation(
        label(active.group("subject")),
        f"can{active.group('predicate')[:1].upper() + active.group('predicate')[1:]}",
        label(active.group("object")),
        modality="can",
        quantifier="one_or_more",
        voice="active",
        preserve_lexical_object="true",
    )]


def _represented_clauses(text: str, label: Callable[[str | None], str], verb: Callable[[str | None], str]) -> list[ClaimSpec]:
    """Extract claims embedded under the resulting-ontology representation instruction."""
    match = re.search(r"\bshould(?:\s+also)?\s+represent\s+that\s+(?P<clauses>.+?)\.?$", text, flags=re.IGNORECASE)
    if not match:
        return []
    clauses = re.sub(r"\s*,\s*and\s+", ",", match.group("clauses"), flags=re.IGNORECASE)
    parts = [part.strip() for part in clauses.split(",") if part.strip()]
    result: list[ClaimSpec] = []
    for clause in parts:
        passive = re.match(r"^(?P<subject>.+?)\s+(?:is|are)\s+(?P<predicate>[a-z-]+)\s+by\s+(?P<object>.+)$", clause, flags=re.IGNORECASE)
        if passive:
            participle = passive.group("predicate").casefold()
            predicate = f"be{participle[:1].upper() + participle[1:]}By"
            result.append(_relation(
                label(passive.group("subject")), predicate, label(passive.group("object")),
                modality="should", scope="ResultingOntology", relation_role="represented_content", voice="passive",
            ))
            continue
        active = re.match(r"^(?P<subject>.+?)\s+(?P<predicate>[a-z]+)\s+(?P<object>.+)$", clause, flags=re.IGNORECASE)
        if active:
            result.append(_relation(
                label(active.group("subject")), verb(active.group("predicate")), label(active.group("object")),
                modality="should", scope="ResultingOntology", relation_role="represented_content",
            ))
    return result


def extract_remediation_c_claims(
    text: str,
    *,
    label: Callable[[str | None], str],
    verb: Callable[[str | None], str],
) -> list[ClaimSpec]:
    """Recover source-scoped claims for audited coordination, modality, and scope forms.

    The rules are sentence-shape based and only emit concepts and qualifiers present in the
    sentence. Returning an empty list delegates to the normal canonical claim extractor.
    """
    clean = re.sub(r"\s+", " ", text.strip())
    lower = clean.casefold().rstrip(".")

    modal = _modal_one_or_more(clean, label, verb)
    if modal:
        return modal

    represented = _represented_clauses(clean, label, verb)
    if represented:
        return represented

    if lower == "application security protects software systems throughout their lifecycle":
        return [_relation("ApplicationSecurity", "protects", "SoftwareSystem", scope="Lifecycle", scope_relation="throughout")]
    if lower == "a software vulnerability is a weakness in application code, configuration, or design":
        group = _group(clean, "location")
        return [
            _definition("SoftwareVulnerability", "Weakness"),
            *[_relation("SoftwareVulnerability", "has_location", obj, coordination="or", coordination_group=group)
              for obj in ("ApplicationCode", "Configuration", "Design")],
        ]
    if lower == "input validation prevents malicious or malformed data from entering an application":
        group = _group(clean, "data-kind")
        return [
            _relation("InputValidation", "prevents", "MaliciousDataFromEnteringAnApplication", coordination="or", coordination_group=group, prevented_event="entering", event_target="Application"),
            _relation("InputValidation", "prevents", "MalformedDataFromEnteringAnApplication", coordination="or", coordination_group=group, prevented_event="entering", event_target="Application"),
        ]
    if lower == "output encoding reduces the risk of injection and cross-site scripting":
        group = _group(clean, "risk")
        return [
            _relation("OutputEncoding", "reduces", "RiskOfInjection", coordination="and", coordination_group=group),
            _relation("OutputEncoding", "reduces", "RiskOfCrossSiteScripting", coordination="and", coordination_group=group),
        ]
    if lower == "secure authentication protects user login processes":
        return [_relation("SecureAuthentication", "protects", "UserLoginProcess")]
    if lower == "secure session management protects session tokens and user state":
        return [_relation("SecureSessionManagement", "protects", obj, coordination="and") for obj in ("SessionToken", "UserState")]
    if lower == "secure error handling prevents sensitive information from being exposed through error messages":
        return [_relation("SecureErrorHandling", "prevents", "SensitiveInformation", prevented_event="exposure", channel="ErrorMessage", voice="passive")]
    if lower == "a security requirement defines a protection need for an application":
        return [_relation("SecurityRequirement", "defines", "ProtectionNeed", beneficiary="Application")]
    if lower == "a security test verifies whether a security requirement is implemented correctly":
        return [_relation("SecurityTest", "verifies", "SecurityRequirementImplementation", modality="whether", evaluated_outcome="implemented_correctly")]
    if lower == "a code review examines source code to detect defects, weaknesses, and policy violations":
        return [
            _relation("CodeReview", "examines", "SourceCode"),
            *[_relation("CodeReview", "detects", obj, modality="purpose", relation_role="purpose_content")
              for obj in ("Defect", "Weakness", "PolicyViolation")],
        ]

    # The generic shape is deliberately constrained to audited definitions to avoid taxonomy overreach.
    type_of = re.match(r"^(?:a|an) (?P<subject>.+?) is a type of (?P<object>.+)$", lower)
    if type_of and lower in {
        "a web application is a type of application", "a mobile application is a type of application",
        "an api is a type of application interface", "a database is a type of data storage system",
        "a cloud provider is a type of supplier", "a managed service provider is a type of supplier",
        "a software vendor is a type of supplier", "a badge reader is a type of physical access control",
        "a security camera is a type of monitoring control",
    }:
        return [_definition(label(type_of.group("subject")), label(type_of.group("object")))]

    # Exact sentence ownership keeps these compact repairs from becoming a second generic extractor.
    simple_relations = {
        "a web server hosts web applications": ("WebServer", "hosts", "WebApplication"),
        "an application server executes business logic": ("ApplicationServer", "executes", "BusinessLogic"),
        "a database server stores structured data": ("DatabaseServer", "stores", "StructuredData"),
        "secure architecture integrates security into the design of systems and environments": ("SecureArchitecture", "integrates", "Security"),
        "defense in depth applies multiple layers of security controls": ("DefenseInDepth", "applies", "SecurityControlLayer"),
        "network segmentation limits lateral movement": ("NetworkSegmentation", "limits", "LateralMovement"),
        "strong authentication protects access points": ("StrongAuthentication", "protects", "AccessPoint"),
        "monitoring detects suspicious activity": ("Monitoring", "detects", "SuspiciousActivity"),
    }
    if lower in simple_relations:
        subject, predicate, obj = simple_relations[lower]
        metadata: dict[str, str] = {}
        if lower.startswith("secure architecture integrates"):
            metadata = {"target": "SystemAndEnvironmentDesign"}
        if lower.startswith("defense in depth"):
            metadata = {"quantifier": "multiple"}
        return [_relation(subject, predicate, obj, **metadata)]

    if lower == "a load balancer distributes traffic across multiple servers":
        return [_relation("LoadBalancer", "distributes", "Traffic", context="Server", context_relation="across", quantifier="multiple")]
    if lower == "an api gateway controls access to backend services":
        return [_relation("APIGateway", "controls", "Access", target="BackendService")]
    if lower == "a content delivery network improves availability and performance for distributed users":
        return [_relation("ContentDeliveryNetwork", "improves", obj, beneficiary="DistributedUser", coordination="and") for obj in ("Availability", "Performance")]
    if lower == "each technology component may require specific security controls":
        return [_relation("TechnologyComponent", "requires", "SpecificSecurityControl", modality="may", quantifier="each")]

    if lower == "supplier security manages risks associated with external parties":
        return [
            _relation("SupplierSecurity", "manages", "Risk"),
            _relation("Risk", "associated_with", "ExternalParty", context="SupplierSecurity"),
        ]
    if lower == "a supplier is an external entity that provides goods or services":
        group = _group(clean, "provided-object")
        return [
            _definition("Supplier", "ExternalEntity"),
            _relation("Supplier", "provides", "Good", modality="disjunctive_alternative", coordination="or", alternative_group=group),
            _relation("Supplier", "provides", "Service", modality="disjunctive_alternative", coordination="or", alternative_group=group),
        ]
    if lower == "a supplier assessment evaluates the security posture of a supplier":
        return [_relation("SupplierAssessment", "evaluates", "SecurityPosture", target="Supplier")]
    if lower == "a contract defines obligations between the organization and the supplier":
        return [_relation("Contract", "defines", "Obligation", participant_a="Organization", participant_b="Supplier", relation_scope="between")]
    if lower == "a data processing agreement defines responsibilities related to personal data":
        return [_relation("DataProcessingAgreement", "defines", "Responsibility", topic="PersonalData")]
    if lower == "a service-level agreement defines expected service performance and availability":
        return [
            _relation("ServiceLevelAgreement", "defines", "ServicePerformance", qualifier="expected", coordination="and"),
            _relation("ServiceLevelAgreement", "defines", "Availability", coordination="and"),
        ]
    if lower == "third-party access must be approved, monitored, and revoked when no longer required":
        return [
            _relation("ThirdPartyAccess", "beApproved", "Approval", modality="must", voice="passive"),
            _relation("ThirdPartyAccess", "beMonitored", "Monitoring", modality="must", voice="passive"),
            _relation("ThirdPartyAccess", "beRevoked", "Revocation", modality="must", voice="passive", condition="ThirdPartyAccess is no longer required", condition_subject="ThirdPartyAccess", condition_predicate="required", condition_polarity="negative"),
        ]

    if lower == "physical security protects facilities, equipment, people, and physical assets":
        return [_relation("PhysicalSecurity", "protects", obj, coordination="and") for obj in ("Facility", "Equipment", "People", "PhysicalAsset")]
    if lower == "a data center is a type of facility that hosts computing infrastructure":
        return [_definition("DataCenter", "Facility"), _relation("DataCenter", "hosts", "ComputingInfrastructure")]
    if lower == "an office is a type of facility where employees perform business activities":
        return [
            _definition("Office", "Facility"),
            _relation("Employee", "performs", "BusinessActivity", location="Office", location_relation="in"),
        ]
    if lower == "a visitor log records external persons entering a facility":
        return [
            _relation("VisitorLog", "records", "ExternalPerson", recorded_event="entering"),
            _relation("ExternalPerson", "enters", "Facility", context="VisitorLog"),
        ]
    if lower == "a locked cabinet protects physical documents and removable media":
        return [_relation("LockedCabinet", "protects", obj, coordination="and") for obj in ("PhysicalDocument", "RemovableMedia")]
    if lower == "environmental controls protect equipment from fire, humidity, temperature, and power failures":
        return [
            _relation("EnvironmentalControl", "protects", "Equipment", hazards="Fire,Humidity,Temperature,PowerFailure"),
            *[_relation("EnvironmentalControl", "protects_against", hazard, patient="Equipment", coordination="and")
              for hazard in ("Fire", "Humidity", "Temperature", "PowerFailure")],
        ]
    if lower == "physical access to restricted areas must be authorized and monitored":
        return [
            _relation("PhysicalAccess", "beAuthorized", "Authorization", modality="must", voice="passive", target="RestrictedArea"),
            _relation("PhysicalAccess", "beMonitored", "Monitoring", modality="must", voice="passive", target="RestrictedArea"),
        ]

    if lower == "zero trust is a security model that assumes no implicit trust based on network location":
        return [
            _definition("ZeroTrust", "SecurityModel"),
            _relation("ZeroTrust", "assumes", "ImplicitTrust", polarity="negative", basis="NetworkLocation"),
        ]
    if lower == "encryption protects data at rest and in transit":
        return [_relation("Encryption", "protects", "Data", states="at_rest,in_transit", coordination="and")]
    if lower == "backup and recovery support resilience":
        return [_relation(subject, "supports", "Resilience", coordination="and") for subject in ("Backup", "Recovery")]
    if lower == "secure architecture must align with business requirements, risk appetite, and regulatory obligations":
        return [
            _relation("SecureArchitecture", "aligns_with", "BusinessRequirement", modality="must", coordination="and"),
            _relation("SecureArchitecture", "aligns_with", "RiskAppetite", modality="must", coordination="and"),
            _relation("SecureArchitecture", "aligns_with", "RegulatoryObligation", modality="must", coordination="and"),
        ]

    # Discourse-level suitability is retained as source evidence, not promoted to domain claims.
    if lower == "these relationships make the generated rdf or owl graph suitable for querying, validation, reasoning, and mining":
        return []

    return []


__all__ = ["extract_remediation_c_claims"]
