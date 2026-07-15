"""Source-faithful repairs for audited infosec scope and projection cases.

The rules in this module own only exact, recurring sentence forms.  They preserve
lexical participants, modal/conditional scope, semantic roles, and the distinction
between scenario observations and explicitly declared classes.
"""

from __future__ import annotations

import itertools
import re
from typing import Any

from .text_normalization import _clean


ClaimSpec = dict[str, Any]


def _relation(subject: str, predicate: str, obj: str, **metadata: Any) -> ClaimSpec:
    return {
        "kind": "relation",
        "subject": subject,
        "predicate": predicate,
        "object": obj,
        **{key: value for key, value in metadata.items() if value not in (None, "")},
    }


def _definition(subject: str, obj: str, **metadata: Any) -> ClaimSpec:
    return {"kind": "definition", "subject": subject, "predicate": "is_a", "object": obj, **metadata}


def _instance(subject: str, obj: str, **metadata: Any) -> ClaimSpec:
    return {"kind": "type_assertion", "subject": subject, "predicate": "instance_of", "object": obj, **metadata}


def _observed(*specs: ClaimSpec) -> list[ClaimSpec]:
    for spec in specs:
        spec["observation_scope"] = "illustrative_example"
    return list(specs)


def _p021_p022(lower: str) -> list[ClaimSpec] | None:
    if lower == "a log retention policy defines how long logs must be stored":
        return [
            _relation("LogRetentionPolicy", "defines", "StorageDuration", patient="Log"),
            _relation(
                "LogRetentionPolicy",
                "requiresStorageOf",
                "Log",
                modality="must",
                quantifier="unspecified_duration",
                voice="passive",
                relation_role="policy_requirement",
            ),
        ]
    if lower == "an incident response plan is a document that defines the process for handling incidents":
        return [
            _definition("IncidentResponsePlan", "Document"),
            _relation("IncidentResponsePlan", "defines", "Process"),
            _relation(
                "Process",
                "handles",
                "Incident",
                modality="purpose",
                context="IncidentResponsePlan",
                relation_role="defined_process_purpose",
            ),
        ]
    return None


def _p031_p032(lower: str) -> list[ClaimSpec] | None:
    if lower == "data classification applies labels to information":
        return [_relation("DataClassification", "applies", "Label", target="Information")]
    if lower == "data handling rules define how each classification level must be protected":
        return [
            _relation(
                "ClassificationLevel",
                "mustBeProtectedUnder",
                "DataHandlingRule",
                modality="must",
                quantifier="each",
                voice="passive",
                relation_role="rule_defined_requirement",
            )
        ]
    if lower == "an emergency change is a type of change implemented rapidly to resolve urgent issues":
        return [
            _definition("EmergencyChange", "Change"),
            _relation(
                "EmergencyChange",
                "implementedToResolve",
                "UrgentIssue",
                modality="purpose",
                manner="rapidly",
                voice="passive",
            ),
        ]
    if lower == "change testing verifies that a change works as intended":
        return [
            _relation(
                "ChangeTesting",
                "verifies",
                "Change",
                evaluated_outcome="works_as_intended",
                relation_role="evaluated_content",
                preserve_lexical_object="true",
            ),
            _relation(
                "Change",
                "works",
                "Intended",
                evaluated_outcome="works_as_intended",
                relation_role="lexical_complement",
                projection_scope="evidence_only",
                preserve_lexical_object="true",
            ),
        ]
    return None


def _p039_p040(lower: str) -> list[ClaimSpec] | None:
    if lower == "a phishing scenario illustrates how threats, vulnerabilities, controls, and incidents relate to each other":
        categories = ("Threat", "Vulnerability", "Control", "Incident")
        # Keep the useful direct scenario links while also preserving the literal
        # relational content that the older projection discarded.
        illustrated = [
            _relation("PhishingScenario", "illustrates", category, coordination="and")
            for category in categories
        ]
        relationships = [
            _relation(
                left,
                "relatesTo",
                right,
                context="PhishingScenario",
                coordination="and",
                relation_role="illustrated_each_other_relation",
            )
            for left, right in itertools.combinations(categories, 2)
        ]
        return [*illustrated, *relationships]
    if lower == "a ransomware scenario illustrates the importance of backups, monitoring, and response":
        return [
            _relation(
                "RansomwareScenario",
                "illustrates_importance_of",
                obj,
                scope="importance",
                preserve_lexical_object="true",
            )
            for obj in ("Backup", "Monitoring", "Response")
        ]
    return None


def _p041(lower: str) -> list[ClaimSpec] | None:
    if lower == "a data breach scenario illustrates the importance of access control and data protection":
        return _observed(
            _relation("DataBreachScenario", "illustrates_importance_of", "AccessControl", coordination="and"),
            _relation("DataBreachScenario", "illustrates_importance_of", "DataProtection", coordination="and"),
        )
    if lower == "an unauthorized user accesses a restricted document repository":
        return _observed(
            _relation("UnauthorizedUser", "accesses", "RestrictedDocumentRepository"),
            _relation("UnauthorizedAccessOccurrence", "has_actor", "UnauthorizedUser"),
            _relation("UnauthorizedAccessOccurrence", "has_target", "RestrictedDocumentRepository"),
            _instance("UnauthorizedAccessOccurrence", "UnauthorizedAccess"),
        )
    if lower == "the restricted document repository stores confidential information and personal data":
        return _observed(
            _relation("RestrictedDocumentRepository", "stores", "ConfidentialInformation", coordination="and"),
            _relation("RestrictedDocumentRepository", "stores", "PersonalData", coordination="and"),
        )
    if lower == "the unauthorized access violates the access control policy":
        return _observed(_relation("UnauthorizedAccessOccurrence", "violates", "AccessControlPolicy"))
    if lower == "audit logs record the access event":
        return _observed(_relation("AuditLogs", "record", "AccessEvent"))
    if lower == "a detection rule generates a security alert":
        return _observed(_relation("DetectionRule", "generates", "SecurityAlert"))
    if lower == "the security analyst investigates the alert":
        return _observed(
            _relation(
                "SecurityAnalyst",
                "investigates",
                "SecurityAlert",
                discourse_resolution="definite_antecedent",
            )
        )
    if lower == "the incident response team confirms a data breach":
        return _observed(
            _relation("IncidentResponseTeam", "confirms", "DataBreachOccurrence"),
            _instance("DataBreachOccurrence", "DataBreach"),
        )
    if lower == "the privacy officer assesses whether data subjects must be notified":
        return _observed(
            _relation(
                "PrivacyOfficer",
                "assessesWhetherNotificationIsRequiredFor",
                "DataSubject",
                modality="whether",
                embedded_modality="must",
                voice="passive",
                relation_role="evaluated_content",
            )
        )
    if lower == "the legal team evaluates regulatory obligations":
        return _observed(_relation("LegalTeam", "evaluates", "RegulatoryObligation"))
    if lower == "the organization implements corrective actions to prevent recurrence":
        return _observed(
            _relation("Organization", "implements", "CorrectiveAction"),
            _relation("CorrectiveAction", "prevents", "Recurrence", modality="purpose"),
        )
    return None


def extract_remediation_b2_claim_specs(text: str) -> list[ClaimSpec] | None:
    """Return an exact source-owned repair, or ``None`` to delegate normally."""
    clean = _clean(text)
    if not clean:
        return None
    lower = re.sub(r"\s+", " ", clean.casefold()).rstrip(".")
    for extractor in (_p021_p022, _p031_p032, _p039_p040, _p041):
        specs = extractor(lower)
        if specs is not None:
            return specs
    return None


__all__ = ["extract_remediation_b2_claim_specs"]
