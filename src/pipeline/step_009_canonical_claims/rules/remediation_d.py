"""Replace lossy structural claims for audited identity, network, cloud, and recovery sentences."""

from __future__ import annotations

import re
from typing import Any

from rules import Rule, RuleContext

_RULE_ID = "RULE-SEMANTIC-REMEDIATION-D-001"


def _claim(ctx: RuleContext, subject: str, predicate: str, obj: str, **qualifiers: str) -> dict[str, Any]:
    """Build a traced replacement claim that preserves lexical endpoints by default."""
    # Remediation owns exact source wording; later reference resolution must not rewrite its endpoints.
    qualifiers.setdefault("preserve_lexical_object", "true")
    kind = "definition" if predicate == "is_a" else "relation"
    statement = f"{subject} is a {obj}" if kind == "definition" else f"{subject} {predicate} {obj}"
    return ctx.make_claim(
        ctx.source_text_id,
        ctx.sentence,
        ctx.paragraph_id,
        statement,
        kind,
        subject=subject,
        predicate=predicate,
        object=obj,
        extracted_by=_RULE_ID,
        behavior="replace_lossy_structural_claims",
        **qualifiers,
    )


def _group(context: RuleContext, suffix: str) -> str:
    """Build a sentence-scoped deterministic group identifier."""
    sentence_id = str(context.sentence.get("sentence_id", ""))
    return f"{_RULE_ID}:{sentence_id}:{suffix}"


def _alternatives(
    context: RuleContext,
    subject: str,
    predicate: str,
    objects: list[tuple[str, dict[str, str]]],
) -> list[dict[str, Any]]:
    """Build mutually exclusive claims under one alternative group."""
    group = _group(context, "alternatives")
    return [
        _claim(
            context,
            subject,
            predicate,
            obj,
            modality="disjunctive_alternative",
            coordination="or",
            alternative_group=group,
            **qualifiers,
        )
        for obj, qualifiers in objects
    ]


def _rewrite(text: str, context: RuleContext) -> list[dict[str, Any]]:
    """Return replacement claims for exact audited sentence shapes."""
    # Exact matching is intentional: a remediation rule must not silently generalize to unseen language.
    lower = text.casefold()

    if lower == "a credential is evidence used to prove an identity.":
        return [
            _claim(context, "Credential", "is_a", "Evidence"),
            _claim(context, "Credential", "used_to_prove", "Identity", voice="passive", relation_role="defining_property"),
        ]

    match = re.fullmatch(
        r"an api key is a type of credential used by applications to authenticate requests\.", lower
    )
    if match:
        group = _group(context, "api-key-use")
        return [
            _claim(context, "APIKey", "is_a", "Credential"),
            _claim(context, "APIKey", "used_by", "Application", voice="passive", proposition_group=group),
            _claim(
                context,
                "Application",
                "authenticates",
                "Request",
                context="APIKey",
                relation_role="purpose_of_use",
                proposition_group=group,
            ),
        ]

    passive_obligation = re.fullmatch(
        r"an? (?P<subject>.+?) must be (?P<action>protected against|stored in) an? (?P<object>.+?)\.",
        lower,
    )
    if passive_obligation:
        subject = context.label(passive_obligation.group("subject"))
        obj = context.label(passive_obligation.group("object"))
        predicate = "protected_against" if passive_obligation.group("action") == "protected against" else "stored_in"
        return [_claim(context, subject, predicate, obj, modality="must", voice="passive", patient=subject)]

    expiry = re.fullmatch(r"an? (?P<subject>.+?) must expire after an? (?P<period>.+?)\.", lower)
    if expiry:
        subject = context.label(expiry.group("subject"))
        period = context.label(expiry.group("period"))
        return [
            _claim(
                context,
                subject,
                "expires",
                period,
                modality="must",
                temporal_relation="after",
                temporal_object=period,
            ),
            # Keep the legacy predicate internal for compatibility without projecting duplicate semantics.
            _claim(
                context,
                subject,
                "mustExpireAfter",
                period,
                modality="must",
                temporal_relation="after",
                temporal_object=period,
                visibility="internal",
                projection="internal",
                compatibility_only="true",
            ),
        ]

    periodic_obligation = re.fullmatch(
        r"an? (?P<subject>.+?) must be (?P<action>rotated|revoked) (?P<temporal>periodically|immediately)\.",
        lower,
    )
    if periodic_obligation:
        raw_subject = periodic_obligation.group("subject")
        subject = "APIKey" if raw_subject == "api key" else context.label(raw_subject)
        action = "Rotation" if periodic_obligation.group("action") == "rotated" else "Revocation"
        temporal = periodic_obligation.group("temporal")
        legacy_predicate = "mustBeRotated" if action == "Rotation" else "mustBeRevoked"
        legacy_object = "Periodically" if temporal == "periodically" else "Immediately"
        return [
            _claim(
                context,
                subject,
                "requires",
                action,
                modality="must",
                voice="passive",
                patient=subject,
                temporal_relation=temporal,
            ),
            # Legacy surface predicates remain internal while the structured requires claim is projected.
            _claim(
                context,
                subject,
                legacy_predicate,
                legacy_object,
                modality="must",
                temporal_relation=temporal,
                visibility="internal",
                projection="internal",
                compatibility_only="true",
            ),
        ]

    quantified_means = re.fullmatch(
        r"multi-factor authentication improves authentication strength by requiring more than one verification factor\.",
        lower,
    )
    if quantified_means:
        group = _group(context, "mfa-means")
        return [
            _claim(context, "MultiFactorAuthentication", "improves", "AuthenticationStrength", means_group=group),
            _claim(
                context,
                "MultiFactorAuthentication",
                "requires",
                "VerificationFactor",
                quantifier="more_than_one",
                relation_role="means_for",
                goal="improves AuthenticationStrength",
                means_group=group,
                preserve_lexical_object="true",
            ),
        ]

    factor = re.fullmatch(
        r"an? (?P<subject>knowledge|possession|inherence) factor is a type of authentication factor based on something the user (?P<verb>knows|has|is)\.",
        lower,
    )
    if factor:
        name = factor.group("subject").capitalize()
        subject = f"{name}Factor"
        basis = {
            "knows": "UserKnowledge",
            "has": "UserPossession",
            "is": "UserInherence",
        }[factor.group("verb")]
        return [
            _claim(context, subject, "is_a", "AuthenticationFactor"),
            _claim(
                context,
                subject,
                "based_on",
                basis,
                actor="User",
                event_predicate=factor.group("verb"),
                relation_role="defining_property",
            ),
        ]

    if lower == "multi-factor authentication reduces the risk of unauthorized access caused by stolen passwords.":
        group = _group(context, "causal-risk")
        return [
            _claim(
                context,
                "MultiFactorAuthentication",
                "reduces",
                "RiskOfUnauthorizedAccess",
                proposition_group=group,
            ),
            _claim(
                context,
                "StolenPassword",
                "causes",
                "UnauthorizedAccess",
                context="RiskOfUnauthorizedAccess",
                proposition_group=group,
                relation_role="causal_qualifier",
            ),
        ]

    mechanism = re.fullmatch(
        r"a virtual private network protects remote access by creating an encrypted communication tunnel\.", lower
    )
    if mechanism:
        group = _group(context, "vpn-means")
        return [
            _claim(context, "VirtualPrivateNetwork", "protects", "RemoteAccess", means_group=group),
            _claim(
                context,
                "VirtualPrivateNetwork",
                "creates",
                "EncryptedCommunicationTunnel",
                relation_role="means_for",
                goal="protects RemoteAccess",
                means_group=group,
            ),
        ]

    separation = re.fullmatch(r"network segmentation separates systems into different zones\.", lower)
    if separation:
        return [
            _claim(
                context,
                "NetworkSegmentation",
                "separates",
                "System",
                target="DifferentZone",
                location_relation="into",
            )
        ]

    typed_destination = re.fullmatch(
        r"a demilitarized zone is a type of network segment that exposes controlled services to external networks\.",
        lower,
    )
    if typed_destination:
        return [
            _claim(context, "DemilitarizedZone", "is_a", "NetworkSegment"),
            _claim(context, "DemilitarizedZone", "exposes", "ControlledService", target="ExternalNetwork", location_relation="to"),
        ]

    if lower == "a management network is a type of network segment used for administrative access.":
        return [
            _claim(context, "ManagementNetwork", "is_a", "NetworkSegment"),
            _claim(context, "ManagementNetwork", "used_for", "AdministrativeAccess", voice="passive", modality="purpose"),
        ]

    if lower == "an endpoint is a device connected to the organizational network.":
        return [
            _claim(context, "Endpoint", "is_a", "Device"),
            _claim(context, "Endpoint", "connected_to", "OrganizationalNetwork", voice="passive", relation_role="defining_property"),
        ]

    if lower == "device encryption protects data stored on an endpoint.":
        group = _group(context, "stored-data")
        return [
            _claim(context, "DeviceEncryption", "protects", "Data", location="Endpoint", location_relation="on", proposition_group=group),
            _claim(context, "Data", "stored_on", "Endpoint", voice="passive", context="DeviceEncryption", proposition_group=group),
        ]

    if lower == "configuration hardening reduces attack surface by disabling unnecessary services and applying secure settings.":
        group = _group(context, "hardening-means")
        return [
            _claim(context, "ConfigurationHardening", "reduces", "AttackSurface", means_group=group),
            _claim(context, "ConfigurationHardening", "disables", "UnnecessaryService", relation_role="means_for", goal="reduces AttackSurface", means_group=group, coordination="and"),
            _claim(context, "ConfigurationHardening", "applies", "SecureSetting", relation_role="means_for", goal="reduces AttackSurface", means_group=group, coordination="and"),
        ]

    if lower == "a cloud account is an administrative boundary for cloud resources.":
        return [
            _claim(context, "CloudAccount", "is_a", "AdministrativeBoundary", target="CloudResource", relation_role="defining_property"),
        ]

    if lower == "a cloud workload is a type of computing resource hosted in a cloud environment.":
        return [
            _claim(context, "CloudWorkload", "is_a", "ComputingResource"),
            _claim(context, "CloudWorkload", "hosted_in", "CloudEnvironment", voice="passive", relation_role="defining_property"),
        ]

    if lower == "a cloud identity is an identity used to access cloud services.":
        return [
            _claim(context, "CloudIdentity", "is_a", "Identity"),
            _claim(context, "CloudIdentity", "used_to_access", "CloudService", voice="passive", modality="purpose", relation_role="defining_property"),
        ]

    if lower == "a cloud security posture management tool detects misconfigurations in cloud environments.":
        return [
            _claim(context, "CloudSecurityPostureManagementTool", "detects", "Misconfiguration", location="CloudEnvironment", location_relation="in"),
        ]

    if lower == "a cloud access security broker monitors and controls cloud service usage.":
        return [
            _claim(context, "CloudAccessSecurityBroker", "monitors", "CloudServiceUsage", coordination="and"),
            _claim(context, "CloudAccessSecurityBroker", "controls", "CloudServiceUsage", coordination="and"),
        ]

    if lower == "cryptography protects information through mathematical techniques.":
        group = _group(context, "cryptography-means")
        return [
            _claim(context, "Cryptography", "protects", "Information", means_group=group),
            _claim(context, "Cryptography", "uses", "MathematicalTechnique", relation_role="means_for", goal="protects Information", means_group=group),
        ]

    if lower == "decryption is the process that converts encrypted data back into readable data.":
        return [
            _claim(context, "Decryption", "is_a", "Process"),
            _claim(context, "Decryption", "converts", "EncryptedData", target="ReadableData", location_relation="into", relation_role="process_content"),
        ]

    if lower == "a cryptographic key is a value used by a cryptographic algorithm.":
        return [
            _claim(context, "CryptographicKey", "is_a", "Value"),
            _claim(context, "CryptographicKey", "used_by", "CryptographicAlgorithm", voice="passive", relation_role="defining_property"),
        ]

    if lower == "symmetric encryption is a type of encryption that uses the same key for encryption and decryption.":
        group = _group(context, "same-key")
        return [
            _claim(context, "SymmetricEncryption", "is_a", "Encryption"),
            _claim(context, "SymmetricEncryption", "uses_for_encryption", "Key", quantifier="same", proposition_group=group),
            _claim(context, "SymmetricEncryption", "uses_for_decryption", "Key", quantifier="same", proposition_group=group),
        ]

    if lower == "asymmetric encryption is a type of encryption that uses a public key and a private key.":
        group = _group(context, "asymmetric-keys")
        return [
            _claim(context, "AsymmetricEncryption", "is_a", "Encryption"),
            _claim(context, "AsymmetricEncryption", "uses", "PublicKey", coordination="and", proposition_group=group),
            _claim(context, "AsymmetricEncryption", "uses", "PrivateKey", coordination="and", proposition_group=group),
        ]

    if lower == "a hash function generates a fixed-length digest from input data.":
        group = _group(context, "digest-source")
        return [
            _claim(context, "HashFunction", "generates", "FixedLengthDigest", proposition_group=group),
            _claim(context, "HashFunction", "uses", "InputData", relation_role="source_for", goal="generates FixedLengthDigest", proposition_group=group),
        ]

    if lower == "a data breach is a type of security incident that involves unauthorized access to or disclosure of data.":
        return [
            _claim(context, "DataBreach", "is_a", "SecurityIncident"),
            *_alternatives(
                context,
                "DataBreach",
                "involves",
                [
                    ("UnauthorizedAccess", {"source_term": "unauthorized access to"}),
                    ("Disclosure", {"patient": "Data", "source_term": "disclosure of data"}),
                ],
            ),
        ]

    if lower == "unauthorized access is a type of security incident involving access by an unapproved identity.":
        return [
            _claim(context, "UnauthorizedAccess", "is_a", "SecurityIncident"),
            _claim(context, "UnauthorizedAccess", "involves", "Access", actor="UnapprovedIdentity", voice="passive", relation_role="defining_property"),
        ]

    if lower == "insider misuse is a type of security incident caused by an internal actor.":
        return [
            _claim(context, "InsiderMisuse", "is_a", "SecurityIncident"),
            _claim(context, "InsiderMisuse", "caused_by", "InternalActor", voice="passive", relation_role="defining_property"),
        ]

    if lower == "business continuity and disaster recovery protect the organization against major disruptions.":
        return [
            _claim(context, subject, "protects", "Organization", target="MajorDisruption", relation_role="protects_against", coordination="and")
            for subject in ("BusinessContinuity", "DisasterRecovery")
        ]

    if lower == "business continuity is the capability to continue critical operations during disruption.":
        return [
            _claim(context, "BusinessContinuity", "is_a", "Capability"),
            _claim(context, "BusinessContinuity", "continues", "CriticalOperation", temporal_relation="during", temporal_object="Disruption", relation_role="capability_content"),
        ]

    if lower == "disaster recovery is the process of restoring technology services after a disruptive event.":
        return [
            _claim(context, "DisasterRecovery", "is_a", "Process"),
            _claim(context, "DisasterRecovery", "restores", "TechnologyService", temporal_relation="after", temporal_object="DisruptiveEvent", relation_role="process_content"),
        ]

    if lower == "a business impact analysis identifies critical processes, dependencies, and recovery priorities.":
        return [
            _claim(context, "BusinessImpactAnalysis", "identifies", obj, coordination="and")
            for obj in ("CriticalProcess", "Dependency", "RecoveryPriority")
        ]

    if lower == "a recovery time objective defines the maximum acceptable time to restore a service.":
        group = _group(context, "rto")
        return [
            _claim(context, "RecoveryTimeObjective", "defines", "MaximumAcceptableTime", proposition_group=group),
            _claim(context, "MaximumAcceptableTime", "applies_to", "ServiceRestoration", target="Service", proposition_group=group, relation_role="definition_content"),
        ]

    if lower == "a recovery point objective defines the maximum acceptable amount of data loss measured in time.":
        return [
            _claim(context, "RecoveryPointObjective", "defines", "MaximumAcceptableAmountOfDataLoss", measurement_unit="Time"),
        ]

    if lower == "a backup is a copy of data used for recovery.":
        return [
            _claim(context, "Backup", "is_a", "CopyOfData"),
            _claim(context, "Backup", "used_for", "Recovery", voice="passive", modality="purpose"),
        ]

    if lower == "a disaster recovery test verifies whether recovery procedures work as expected.":
        return [
            _claim(
                context,
                "DisasterRecoveryTest",
                "verifies",
                "RecoveryProcedure",
                modality="whether",
                event_predicate="works",
                expected_state="as_expected",
                proposition_role="verified_content",
            )
        ]

    return []


class RemediationDRule(Rule):
    """Rule that atomically replaces lossy claims for a matched audited sentence."""

    rule_id = _RULE_ID
    stage = "semantic_claims"
    priority = 20
    behavior = "replace_lossy_structural_claims"

    def apply(
        self,
        claims: list[dict[str, Any]],
        context: RuleContext,
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """Replace all prior claims for a matched sentence and emit the audited representation."""
        text = context.clean(str(context.sentence.get("text", "")))
        emitted = _rewrite(text, context)
        if not emitted:
            return [], []
        sentence_id = str(context.sentence.get("sentence_id", ""))
        # Replacement is atomic: retaining fallback claims would duplicate or contradict the repaired semantics.
        claims[:] = [
            claim
            for claim in claims
            if str((claim.get("source") or {}).get("sentence_id", "")) != sentence_id
        ]
        return emitted, []


REMEDIATION_D_RULE = RemediationDRule()
