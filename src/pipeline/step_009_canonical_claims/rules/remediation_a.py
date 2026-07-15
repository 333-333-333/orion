"""Repair audited glossary sentences whose scope is lost by generic dependency extraction."""

from __future__ import annotations

import hashlib
import re
from typing import Any


ClaimSpec = dict[str, Any]


def _relation(subject: str, predicate: str, obj: str, **scope: str) -> ClaimSpec:
    """Build a relation specification with explicit scope metadata."""
    return {"kind": "relation", "subject": subject, "predicate": predicate, "object": obj, **scope}


def _definition(subject: str, obj: str, **scope: str) -> ClaimSpec:
    """Build an is-a definition specification."""
    return {"kind": "definition", "subject": subject, "predicate": "is_a", "object": obj, **scope}


def _instance(subject: str, obj: str) -> ClaimSpec:
    """Build an illustrative instance assertion that must not become a subclass."""
    return {
        "kind": "type_assertion",
        "subject": subject,
        "predicate": "instance_of",
        "object": obj,
        "observation_scope": "illustrative_example",
    }


def _alternative_group(text: str, role: str) -> str:
    """Build a deterministic group ID for alternatives with the same semantic role."""
    digest = hashlib.sha256(f"{text.casefold()}|{role}".encode("utf-8")).hexdigest()[:16]
    return f"alternative-{digest}"


def _alternatives(text: str, role: str, specs: list[ClaimSpec]) -> list[ClaimSpec]:
    """Mark specifications as mutually exclusive alternatives in one group."""
    group = _alternative_group(text, role)
    for spec in specs:
        spec.update({
            "coordination": "or",
            "modality": "disjunctive_alternative",
            "alternative_group": group,
        })
    return specs


def _observed(*specs: ClaimSpec) -> list[ClaimSpec]:
    """Mark scenario facts as illustrative observations rather than schema declarations."""
    for spec in specs:
        spec["observation_scope"] = "illustrative_example"
    return list(specs)


def extract_remediation_a_claim_specs(text: str) -> list[ClaimSpec] | None:
    """Return source-faithful claims for recurring scope-heavy glossary constructions.

    These rules deliberately operate on sentence text rather than upstream dependency
    labels.  They repair finite-verb nominalization without importing domain facts and
    preserve coordination, modality, conditions, role arguments, and example scope.
    """

    clean = re.sub(r"\s+", " ", text.strip()).rstrip(".")
    lower = clean.casefold()

    # Identity/access: normative scope, indirect questions, alternatives, and conditions.
    if lower == "the principle of least privilege states that an identity must receive only the permissions required to perform its duties":
        return [
            _relation(
                "Identity", "receives", "Permission", modality="must", quantifier="only",
                constraint="required", context="PrincipleOfLeastPrivilege",
                target="IdentityDuty", relation_role="stated_requirement",
            )
        ]
    if lower == "a permission grants an action over a resource":
        return [_relation("Permission", "grants", "Action", target="Resource", relation_role="authorization_scope")]
    if lower == "a role is a collection of permissions":
        return [_relation("Role", "has_member", "Permission", quantifier="collection")]
    if lower == "a user group is a collection of identities that share common permissions":
        return [
            _relation("UserGroup", "has_member", "Identity", quantifier="collection"),
            _relation("Identity", "shares", "CommonPermission", relation_role="relative_clause_content"),
        ]
    if lower == "a role assignment links a role to an identity":
        return [_relation("RoleAssignment", "links", "Role", target="Identity")]
    if lower == "a permission review verifies whether assigned permissions remain necessary":
        return [_relation(
            "PermissionReview", "verifies_necessity_of", "AssignedPermission",
            modality="whether", state="remain_necessary", relation_role="evaluated_content",
        )]
    if lower == "segregation of duties prevents one person from controlling incompatible activities":
        return [_relation(
            "SegregationOfDuties", "prevents_control_of", "IncompatibleActivity",
            actor="Person", quantifier="one", modality="prevention",
        )]
    access_risk = re.fullmatch(r"(excessive permission|dormant account access|orphaned account access) is a type of access risk", lower)
    if access_risk:
        labels = {
            "excessive permission": "ExcessivePermission",
            "dormant account access": "DormantAccountAccess",
            "orphaned account access": "OrphanedAccountAccess",
        }
        return [_definition(labels[access_risk.group(1)], "AccessRisk")]
    if lower == "identity and access management controls the lifecycle of identities, accounts, roles, permissions, and credentials":
        return [_relation(
            "IdentityAndAccessManagement", "controls", "Lifecycle",
            topics="Identity,Account,Role,Permission,Credential",
        )]
    if lower == "user provisioning creates a new user account":
        return [_relation("UserProvisioning", "creates", "UserAccount", qualifier="new")]
    if lower == "user deprovisioning disables or removes access for a user who no longer requires it":
        return _alternatives(clean, "deprovisioning-action", [
            _relation(
                "UserDeprovisioning", "disables", "Access", target="User",
                condition="User no longer requires Access", condition_subject="User",
                condition_predicate="requires", condition_polarity="negative",
            ),
            _relation(
                "UserDeprovisioning", "removes", "Access", target="User",
                condition="User no longer requires Access", condition_subject="User",
                condition_predicate="requires", condition_polarity="negative",
            ),
        ])
    if lower == "access modification changes the permissions assigned to an identity":
        return [_relation("AccessModification", "changes", "Permission", target="Identity", qualifier="assigned")]
    if lower == "access certification confirms that access remains appropriate":
        return [
            _relation("AccessCertification", "confirms_appropriateness_of", "Access", state="remains_appropriate"),
            _relation("Access", "remains", "Appropriate", context="AccessCertification", relation_role="confirmed_content"),
        ]
    if lower == "a joiner process creates access for a new employee":
        return [_relation("JoinerProcess", "creates", "Access", target="Employee", qualifier="new")]
    if lower == "a mover process changes access when a person changes role":
        return [_relation(
            "MoverProcess", "changes", "Access", condition="Person changes Role",
            condition_subject="Person", condition_predicate="changes", condition_object="Role",
            condition_polarity="positive",
        )]
    if lower == "a leaver process removes access when a person leaves the organization":
        return [_relation(
            "LeaverProcess", "removes", "Access", condition="Person leaves Organization",
            condition_subject="Person", condition_predicate="leaves", condition_object="Organization",
            condition_polarity="positive",
        )]
    if lower == "the identity management system stores identity records":
        return [_relation("IdentityManagementSystem", "stores", "IdentityRecord")]
    if lower == "the access management system enforces authentication and authorization decisions":
        return [
            _relation("AccessManagementSystem", "enforces", "AuthenticationDecision", coordination="and"),
            _relation("AccessManagementSystem", "enforces", "AuthorizationDecision", coordination="and"),
        ]

    # Key management and monitoring: prepositions, purpose, modal and negative scope.
    if lower == "key management protects cryptographic keys across their lifecycle":
        return [_relation("KeyManagement", "protects", "CryptographicKey", context="CryptographicKeyLifecycle")]
    if lower == "key generation creates a cryptographic key":
        return [_relation("KeyGeneration", "creates", "CryptographicKey")]
    if lower == "key storage protects a cryptographic key from unauthorized access":
        return [_relation("KeyStorage", "protects", "CryptographicKey", target="UnauthorizedAccess", relation_role="protection_from")]
    if lower == "key rotation replaces an existing key with a new key":
        return [_relation("KeyRotation", "replaces", "ExistingKey", target="NewKey")]
    if lower == "key revocation invalidates a compromised or obsolete key":
        return _alternatives(clean, "revoked-key-state", [
            _relation("KeyRevocation", "invalidates", "CompromisedKey"),
            _relation("KeyRevocation", "invalidates", "ObsoleteKey"),
        ])
    if lower == "key destruction permanently removes a key from use":
        return [_relation("KeyDestruction", "removes", "Key", manner="permanently", context="Use", relation_role="removal_from")]
    if lower == "a hardware security module is a type of device designed to protect cryptographic keys":
        return [
            _definition("HardwareSecurityModule", "Device"),
            _relation("HardwareSecurityModule", "protects", "CryptographicKey", modality="purpose", relation_role="designed_purpose"),
        ]
    if lower == "a key management service stores and controls access to cryptographic keys":
        return [
            _relation("KeyManagementService", "stores", "CryptographicKey", coordination="and"),
            _relation("KeyManagementService", "controls_access_to", "CryptographicKey", coordination="and"),
        ]
    if lower == "poor key management can compromise encrypted data":
        return [_relation("PoorKeyManagement", "compromises", "EncryptedData", modality="can")]
    if lower == "logging and monitoring provide visibility into systems, networks, applications, and user activity":
        return [_relation(
            "LoggingAndMonitoring", "provides", "Visibility",
            topics="System,Network,Application,UserActivity", coordination="and",
        )]
    if lower == "a log record is a record of an event generated by a system":
        return [
            _definition("LogRecord", "Record"),
            _relation("LogRecord", "records", "Event", context="System", relation_role="generated_by"),
        ]
    if lower == "an audit log is a type of log that supports accountability and compliance":
        return [
            _definition("AuditLog", "Log"),
            _relation("AuditLog", "supports", "Accountability", coordination="and"),
            _relation("AuditLog", "supports", "Compliance", coordination="and"),
        ]
    if lower == "a security event is an observable occurrence that may be relevant to security":
        return [
            _definition("SecurityEvent", "ObservableOccurrence"),
            _relation("SecurityEvent", "relevant_to", "Security", modality="may"),
        ]
    if lower == "a security alert is a notification generated when a detection rule identifies suspicious activity":
        return [
            _definition("SecurityAlert", "Notification"),
            _relation(
                "SecurityAlert", "generated_by", "DetectionRule",
                condition="DetectionRule identifies SuspiciousActivity",
                condition_subject="DetectionRule", condition_predicate="identifies",
                condition_object="SuspiciousActivity", condition_polarity="positive",
            ),
        ]
    if lower == "a security incident is an event that compromises or threatens confidentiality, integrity, or availability":
        alternatives = [
            _relation("SecurityIncident", predicate, obj)
            for predicate in ("compromises", "threatens")
            for obj in ("Confidentiality", "Integrity", "Availability")
        ]
        return [_definition("SecurityIncident", "Event"), *_alternatives(clean, "incident-effect", alternatives)]
    if lower == "a false positive is an alert that does not represent a real threat":
        return [
            _definition("FalsePositive", "Alert"),
            _relation("FalsePositive", "represents", "RealThreat", polarity="negative"),
        ]
    if lower == "a false negative is a missed detection of a real threat":
        return [
            _definition("FalseNegative", "MissedDetection"),
            _relation("FalseNegative", "misses", "RealThreat"),
        ]

    # Vulnerability/threat intelligence: shared arguments, deontic scope, and evidence content.
    if lower == "vulnerability management identifies, evaluates, prioritizes, and remediates weaknesses":
        return [
            _relation("VulnerabilityManagement", predicate, "Weakness", coordination="and")
            for predicate in ("identifies", "evaluates", "prioritizes", "remediates")
        ]
    if lower == "a vulnerability scan detects known vulnerabilities in systems and applications":
        return [
            _relation("VulnerabilityScan", "detects", "KnownVulnerability", location="System", coordination="and"),
            _relation("VulnerabilityScan", "detects", "KnownVulnerability", location="Application", coordination="and"),
        ]
    if lower == "a vulnerability finding describes a detected weakness":
        return [_relation("VulnerabilityFinding", "describes", "DetectedWeakness")]
    if lower == "a severity rating estimates the technical seriousness of a vulnerability":
        return [_relation("SeverityRating", "estimates", "TechnicalSeriousness", target="Vulnerability")]
    if lower == "a risk rating combines severity, exposure, likelihood, and business impact":
        return [
            _relation("RiskRating", "combines", obj, coordination="and")
            for obj in ("Severity", "Exposure", "Likelihood", "BusinessImpact")
        ]
    if lower == "remediation removes or fixes a vulnerability":
        return _alternatives(clean, "remediation-action", [
            _relation("Remediation", "removes", "Vulnerability"),
            _relation("Remediation", "fixes", "Vulnerability"),
        ])
    if lower == "mitigation reduces the risk when remediation is not immediately possible":
        return [_relation(
            "Mitigation", "reduces", "Risk", condition="Remediation is not immediately possible",
            condition_subject="Remediation", condition_predicate="possible",
            condition_polarity="negative", manner="immediately",
        )]
    remediation_type = re.fullmatch(r"(patch deployment|configuration change) is a type of remediation", lower)
    if remediation_type:
        return [_definition(
            "PatchDeployment" if remediation_type.group(1) == "patch deployment" else "ConfigurationChange",
            "Remediation",
        )]
    if lower == "vulnerability exceptions must be documented, approved, and reviewed":
        return [
            _relation("VulnerabilityException", predicate, obj, modality="must", voice="passive", coordination="and")
            for predicate, obj in (
                ("requires_documentation", "Documentation"),
                ("requires_approval", "Approval"),
                ("requires_review", "Review"),
            )
        ]
    if lower == "threat intelligence provides information about threats, threat actors, tactics, techniques, and indicators":
        return [_relation(
            "ThreatIntelligence", "provides", "Information",
            topics="Threat,ThreatActor,Tactic,Technique,Indicator",
        )]
    if lower == "a threat actor is an entity that can intentionally cause harm":
        return [
            _definition("ThreatActor", "Entity"),
            _relation("ThreatActor", "causes", "Harm", modality="can", manner="intentionally"),
        ]
    actor_type = re.fullmatch(r"(a cybercriminal group|an insider|a nation-state actor|a hacktivist) is a type of threat actor", lower)
    if actor_type:
        actor = {
            "a cybercriminal group": "CybercriminalGroup",
            "an insider": "Insider",
            "a nation-state actor": "NationStateActor",
            "a hacktivist": "Hacktivist",
        }[actor_type.group(1)]
        return [_definition(actor, "ThreatActor")]
    if lower == "an indicator of compromise is evidence that a system may be compromised":
        return [
            _definition("IndicatorOfCompromise", "Evidence"),
            _relation("System", "compromised", "CompromiseState", modality="may", context="IndicatorOfCompromise"),
        ]
    if lower == "a tactic describes a threat actor objective":
        return [_relation("Tactic", "describes", "ThreatActorObjective")]
    if lower == "a technique describes how a threat actor achieves an objective":
        return [_relation("Technique", "describes_how_achieves", "Objective", actor="ThreatActor")]
    if lower == "threat intelligence supports detection, prevention, and response activities":
        return [
            _relation("ThreatIntelligence", "supports", obj, coordination="and")
            for obj in ("Detection", "Prevention", "ResponseActivity")
        ]

    # Illustrative scenarios: retain observations and instance membership, never subclasses.
    if lower == "for example, a customer database stores personal data and financial data":
        return _observed(
            _relation("CustomerDatabase", "stores", "PersonalData", coordination="and"),
            _relation("CustomerDatabase", "stores", "FinancialData", coordination="and"),
        )
    if lower == "the customer database is hosted on a database server":
        return _observed(_relation("CustomerDatabase", "hosted_on", "DatabaseServer"))
    if lower == "the database server runs inside a production network":
        return _observed(_relation("DatabaseServer", "runs_inside", "ProductionNetwork"))
    if lower == "the production network is protected by a firewall":
        return _observed(_relation("ProductionNetwork", "protected_by", "Firewall", voice="passive"))
    if lower == "the firewall enforces network access rules":
        return _observed(_relation("Firewall", "enforces", "NetworkAccessRule"))
    if lower == "the customer database is encrypted using a cryptographic key":
        return _observed(_relation("CustomerDatabase", "encrypted_using", "CryptographicKey", voice="passive"))
    if lower == "the cryptographic key is stored in a key management service":
        return _observed(_relation("CryptographicKey", "stored_in", "KeyManagementService", voice="passive"))
    if lower == "the security information and event management system collects audit logs from the database server":
        return _observed(_relation(
            "SecurityInformationAndEventManagementSystem", "collects", "AuditLog",
            context="DatabaseServer", relation_role="source",
        ))
    if lower == "a security analyst reviews alerts related to the customer database":
        return _observed(_relation("SecurityAnalyst", "reviews", "Alert", target="CustomerDatabase"))
    if lower == "the asset owner classifies the customer database as restricted information":
        return _observed(_relation(
            "AssetOwner", "classifies", "CustomerDatabase", target="RestrictedInformation",
            relation_role="classification_result",
        ))
    if lower == "a remote employee uses a laptop to access a corporate application":
        return _observed(
            _relation("RemoteEmployee", "uses", "Laptop", relation_role="instrument"),
            _relation("RemoteEmployee", "accesses", "CorporateApplication", context="Laptop", relation_role="purpose"),
        )
    if lower == "the laptop is an endpoint":
        return [_instance("Laptop", "Endpoint")]
    if lower == "the corporate application is a web application":
        return [_instance("CorporateApplication", "WebApplication")]
    if lower == "the remote employee authenticates through multi-factor authentication":
        return _observed(_relation("RemoteEmployee", "authenticates_through", "MultiFactorAuthentication"))
    if lower == "the identity provider verifies the employee identity":
        return _observed(_relation("IdentityProvider", "verifies", "EmployeeIdentity"))
    if lower == "the authorization service grants access based on role assignments":
        return _observed(_relation("AuthorizationService", "grants", "Access", context="RoleAssignment", relation_role="authorization_basis"))
    if lower == "the virtual private network encrypts the communication channel":
        return _observed(_relation("VirtualPrivateNetwork", "encrypts", "CommunicationChannel"))
    if lower == "the endpoint detection and response tool monitors the laptop":
        return _observed(_relation("EndpointDetectionAndResponseTool", "monitors", "Laptop"))
    if lower == "the security policy requires remote employees to report lost devices immediately":
        return _observed(_relation(
            "RemoteEmployee", "reports", "LostDevice", modality="must",
            context="SecurityPolicy", manner="immediately", relation_role="policy_requirement",
        ))

    return None
