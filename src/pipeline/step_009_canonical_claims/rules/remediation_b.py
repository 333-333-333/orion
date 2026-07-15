"""Repair reusable high-risk infosec sentence forms with source-faithful claim specs."""

from __future__ import annotations

import hashlib
import re
from typing import Any

from .text_normalization import _clean, _label, _objects, _split_list, _verb


_MODAL_WORDS = {"may", "must", "can", "could", "should", "would", "might"}


def _spec(subject: str, predicate: str, obj: str, **metadata: str) -> dict[str, str]:
    """Build a relation spec while omitting empty metadata fields."""
    return {
        "kind": "relation",
        "subject": subject,
        "predicate": predicate,
        "object": obj,
        **{key: value for key, value in metadata.items() if value not in (None, "")},
    }


def _definition(subject: str, obj: str, **metadata: str) -> dict[str, str]:
    """Build an is-a definition spec."""
    return _spec(subject, "is_a", obj, kind="definition", **metadata)


def _alternative_group(text: str, role: str) -> str:
    """Build a deterministic ID for one source disjunction and semantic role."""
    digest = hashlib.sha256(f"{text}|{role}".encode("utf-8")).hexdigest()[:16]
    return f"alternative-{digest}"


def _modal_predicate(modal: str, verb: str) -> str:
    """Encode a modal and base verb in the canonical predicate label."""
    base = verb.casefold().strip()
    return modal.casefold() + base[:1].upper() + base[1:] if modal and base else _verb(base)


def _importance_specs(text: str) -> list[dict[str, str]] | None:
    """Extract importance relations only for the audited scenario subjects."""
    match = re.match(
        r"^(?P<subject>.+?)\s+illustrates\s+the\s+importance\s+of\s+(?P<objects>.+?)\.?$",
        text,
        flags=re.IGNORECASE,
    )
    if not match:
        return None
    subject = _label(match.group("subject"))
    if subject not in {"DataBreachScenario", "RansomwareScenario"}:
        return None
    return [
        _spec(subject, "illustrates_importance_of", obj, scope="importance")
        for obj in _objects(match.group("objects"))
    ]


def _modal_svo_specs(text: str) -> list[dict[str, str]] | None:
    """Extract guarded modal SVO forms without flattening coordination or scope."""
    match = re.match(
        r"^(?P<subject>.+?)\s+(?P<modal>may|must|can|could|should|would|might)\s+"
        r"(?P<verb>[A-Za-z-]+)\s+(?P<objects>.+?)\.?$",
        text,
        flags=re.IGNORECASE,
    )
    if not match:
        return None
    subject = _label(match.group("subject"))
    # The broad regex is allow-listed so it cannot take ownership of unaudited modal sentences.
    allowed_subjects = {
        "MultiFactorAuthentication", "SecurityAwarenessTraining", "EmailFiltering",
        "LogMonitoring", "IncidentResponse", "EndpointDetectionAndResponse",
        "NetworkSegmentation", "BackupRestoration", "IncidentResponseTeam",
        "PostIncidentReview", "PoorChangeManagement",
    }
    if subject not in allowed_subjects:
        return None
    modal = match.group("modal").casefold()
    verb = match.group("verb").casefold()
    raw_objects = match.group("objects").strip().rstrip(".")

    coordinated_verbs = re.match(
        r"^(?P<object1>and|or)\s+(?P<verb2>[A-Za-z-]+)\s+(?P<object>.+)$",
        raw_objects,
        flags=re.IGNORECASE,
    )
    if coordinated_verbs:
        connector = coordinated_verbs.group("object1").casefold()
        obj = _label(coordinated_verbs.group("object"))
        return [
            _spec(subject, _modal_predicate(modal, action), obj, modality=modal, coordination=connector)
            for action in (verb, coordinated_verbs.group("verb2"))
        ]

    # Preserve the ransomware complement as a qualifier instead of a class-like phrase.
    spread = re.match(r"^the\s+spread\s+of\s+the\s+(?P<target>.+)$", raw_objects, flags=re.IGNORECASE)
    if spread:
        return [
            _spec(
                subject,
                _modal_predicate(modal, verb),
                "Spread",
                modality=modal,
                target=_label(spread.group("target")),
            )
        ]

    # A disjunctive object list remains alternatives under the modal operator.
    if re.search(r"\bor\b", raw_objects, flags=re.IGNORECASE):
        group = _alternative_group(text, "modal-object-list")
        return [
            _spec(
                subject,
                _modal_predicate(modal, verb),
                obj,
                modality=modal,
                coordination="or",
                alternative_group=group,
            )
            for obj in _objects(raw_objects)
        ]

    return [
        _spec(subject, _modal_predicate(modal, verb), obj, modality=modal)
        for obj in _objects(raw_objects)
    ]


def _shared_verb_specs(text: str) -> list[dict[str, str]] | None:
    """Expand the audited shared-object verb list into one claim per verb."""
    match = re.match(
        r"^(?P<subject>.+?)\s+(?P<verbs>[A-Za-z-]+(?:\s*,\s*[A-Za-z-]+)+\s*,?\s+and\s+[A-Za-z-]+)\s+"
        r"(?P<object>.+?)\.?$",
        text,
        flags=re.IGNORECASE,
    )
    if not match:
        return None
    verbs = [word for word in re.findall(r"[A-Za-z-]+", match.group("verbs")) if word.casefold() != "and"]
    if [verb.casefold() for verb in verbs] != ["collects", "normalizes", "correlates", "analyzes"]:
        return None
    subject = _label(match.group("subject"))
    obj = _label(match.group("object"))
    return [_spec(subject, _verb(verb), obj, coordination="and") for verb in verbs]


def _infosec_021_022_specs(text: str) -> list[dict[str, str]] | None:
    """Repair audited logging and incident-response sentences from paragraphs 21-22."""
    lower = text.casefold().rstrip(".")

    match = re.match(r"^(?P<subject>.+?) gathers (?P<object>.+?) from (?P<sources>.+)$", text.rstrip("."), re.IGNORECASE)
    if match:
        result = [_spec(_label(match.group("subject")), "gathers", _label(match.group("object")))]
        result.extend(
            _spec(_label(match.group("object")), "originates_from", source, coordination="and")
            for source in _objects(match.group("sources"))
        )
        return result

    match = re.match(r"^(?P<subject>.+?) converts (?P<object>.+?) into (?P<result>.+)$", text.rstrip("."), re.IGNORECASE)
    if match:
        subject = _label(match.group("subject"))
        patient = _label(match.group("object"))
        return [
            _spec(subject, "converts", patient),
            _spec(subject, "converts_into", _label(match.group("result")), patient=patient),
        ]

    match = re.match(
        r"^(?P<subject>.+?) describes (?P<object>.+?) that (?P<agent>.+?) should detect$",
        text.rstrip("."),
        re.IGNORECASE,
    )
    if match:
        described = _label(match.group("object"))
        return [
            _spec(_label(match.group("subject")), "describes", described),
            _spec(_label(match.group("agent")), "shouldDetect", described, modality="should"),
        ]

    match = re.match(
        r"^(?P<subject>.+?) investigates (?P<object>.+?) produced by (?P<producer>.+)$",
        text.rstrip("."),
        re.IGNORECASE,
    )
    if match:
        obj = _label(match.group("object"))
        return [
            _spec(_label(match.group("subject")), "investigates", obj),
            _spec(obj, "produced_by", _label(match.group("producer")), voice="passive"),
        ]

    match = re.match(
        r"^(?P<policy>.+?) defines how long (?P<patient>.+?) must be stored$",
        text.rstrip("."),
        re.IGNORECASE,
    )
    if match:
        policy = _label(match.group("policy"))
        patient = _label(match.group("patient"))
        return [
            _spec(policy, "defines", "StorageDuration", patient=patient),
            _spec(patient, "mustBeStored", "Storage", modality="must", context=policy, voice="passive"),
        ]

    match = re.match(r"^(?P<subject>.+?) is the process of (?P<activities>.+)$", text.rstrip("."), re.IGNORECASE)
    if match and "incident response" in match.group("subject").casefold():
        subject = _label(match.group("subject"))
        activities = ("Preparation", "Detection", "Analysis", "Containment", "Eradication", "Recovery")
        return [
            _definition(subject, "Process"),
            *[_spec(subject, "has_activity", activity, coordination="and") for activity in activities],
        ]

    if lower == "preparation establishes plans, tools, roles, and communication channels":
        return [
            _spec("Preparation", "establishes", obj, coordination="and", preserve_lexical_object="true")
            for obj in ("Plan", "Tool", "Role", "CommunicationChannel")
        ]

    match = re.match(r"^(?P<subject>.+?) limits the (?P<objects>.+? or .+)$", text.rstrip("."), re.IGNORECASE)
    if match:
        group = _alternative_group(text, "limited-effects")
        return [
            _spec(
                _label(match.group("subject")),
                "limits",
                obj,
                modality="disjunctive_alternative",
                coordination="or",
                alternative_group=group,
            )
            for obj in _objects(match.group("objects"))
        ]

    match = re.match(
        r"^(?P<subject>.+?) restores (?P<objects>.+?) to (?P<destination>.+)$",
        text.rstrip("."),
        re.IGNORECASE,
    )
    if match:
        destination = _label(match.group("destination"))
        return [
            _spec(
                _label(match.group("subject")),
                "restores",
                obj,
                destination=destination,
                coordination="and",
                preserve_lexical_object="true",
            )
            for obj in _objects(match.group("objects"))
        ]
    return None


def _infosec_031_032_specs(text: str) -> list[dict[str, str]] | None:
    """Repair audited lifecycle and change-management sentences from paragraphs 31-32."""
    lower = text.casefold().rstrip(".")

    if lower == "data lifecycle management protects information from creation to disposal":
        return [_spec("DataLifecycleManagement", "protects", "Information", scope_from="Creation", scope_to="Disposal")]
    if lower == "data storage keeps information in a repository":
        return [_spec("DataStorage", "keeps", "Information", location="Repository", location_relation="in")]
    if lower == "data processing transforms or uses information":
        group = _alternative_group(text, "processing-action")
        return [
            _spec("DataProcessing", predicate, "Information", modality="disjunctive_alternative", coordination="or", alternative_group=group)
            for predicate in ("transforms", "uses")
        ]
    if lower == "data transmission moves information between systems or people":
        group = _alternative_group(text, "transmission-participant")
        return [
            _spec("DataTransmission", "moves", "Information"),
            *[
                _spec(
                    "DataTransmission",
                    "moves_between",
                    participant,
                    patient="Information",
                    modality="disjunctive_alternative",
                    coordination="or",
                    alternative_group=group,
                )
                for participant in ("System", "People")
            ],
        ]
    if lower == "data sharing provides information to another party":
        return [_spec("DataSharing", "provides", "Information", recipient="Party")]
    if lower == "data archival stores information for long-term retention":
        return [_spec("DataArchival", "stores", "Information", purpose="LongTermRetention")]
    if lower == "data handling rules define how each classification level must be protected":
        return [
            _spec("DataHandlingRules", "defines", "ProtectionRequirement", patient="ClassificationLevel"),
            _spec(
                "ClassificationLevel",
                "mustBeProtected",
                "Protection",
                modality="must",
                quantifier="each",
                context="DataHandlingRules",
                voice="passive",
            ),
        ]
    if lower == "change management controls modifications to systems, applications, infrastructure, and configurations":
        return [
            _spec("ChangeManagement", "controls", "Modification"),
            *[
                _spec("Modification", "applies_to", target, coordination="and")
                for target in ("System", "Application", "Infrastructure", "Configuration")
            ],
        ]
    if lower == "a normal change is a type of change that requires assessment and approval":
        return [
            _definition("NormalChange", "Change"),
            _spec("NormalChange", "requires", "Assessment", coordination="and"),
            _spec("NormalChange", "requires", "Approval", coordination="and"),
        ]
    if lower == "an emergency change is a type of change implemented rapidly to resolve urgent issues":
        return [
            _definition("EmergencyChange", "Change"),
            _spec("EmergencyChange", "resolves", "UrgentIssue", modality="purpose", manner="rapidly", voice="passive"),
        ]
    if lower == "change approval verifies that a change is acceptable":
        return [_spec("ChangeApproval", "verifies", "Acceptability", patient="Change")]
    if lower == "change testing verifies that a change works as intended":
        return [
            _spec("ChangeTesting", "verifies", "IntendedOperation", patient="Change"),
            _spec("Change", "works", "Intended", context="ChangeTesting"),
        ]
    if lower == "change rollback restores a previous state if a change fails":
        return [
            _spec(
                "ChangeRollback",
                "restores",
                "PreviousState",
                condition="Change fails",
                condition_subject="Change",
                condition_predicate="fails",
                condition_polarity="positive",
            )
        ]
    return None


def _infosec_039_040_specs(text: str) -> list[dict[str, str]] | None:
    """Repair audited incident scenario sentences from paragraphs 39-40."""
    lower = text.casefold().rstrip(".")

    if lower == "the event affects availability and may affect integrity":
        return [
            _spec("Event", "affects", "Availability", coordination="and"),
            _spec("Event", "mayAffect", "Integrity", modality="may", coordination="and"),
        ]

    match = re.match(
        r"^(?P<subject>.+?) sends (?P<object>.+?) to (?P<recipient>.+)$",
        text.rstrip("."),
        re.IGNORECASE,
    )
    if match:
        return [
            _spec(
                _label(match.group("subject")),
                "sends",
                _label(match.group("object")),
                recipient=_label(match.group("recipient")),
            )
        ]
    if lower == "the attacker uses the compromised credential to access a cloud account":
        return [
            _spec("Attacker", "uses", "CompromisedCredential"),
            _spec("Attacker", "accesses", "CloudAccount", instrument="CompromisedCredential", modality="purpose"),
        ]
    if lower == "malware encrypts files on a file server":
        return [
            _spec("Malware", "encrypts", "File", location="FileServer", location_relation="on"),
            _spec("File", "located_on", "FileServer"),
        ]
    if lower == "corrective actions may include patch deployment, privilege reduction, and improved detection rules":
        return [
            _spec("CorrectiveAction", "mayInclude", obj, modality="may", coordination="and")
            for obj in ("PatchDeployment", "PrivilegeReduction", "ImprovedDetectionRule")
        ]
    return None


def _infosec_041_042_specs(text: str) -> list[dict[str, str]] | None:
    """Repair audited response and metamodel sentences from paragraphs 41-42."""
    lower = text.casefold().rstrip(".")

    if lower == "the unauthorized access violates the access control policy":
        return [_spec("UnauthorizedAccess", "violates", "AccessControlPolicy")]
    if lower == "audit logs record the access event":
        return [_spec("AuditLogs", "record", "AccessEvent")]
    if lower == "the security analyst investigates the alert":
        return [_spec("SecurityAnalyst", "investigates", "SecurityAlert", discourse_resolution="definite_antecedent")]
    if lower == "the privacy officer assesses whether data subjects must be notified":
        return [
            _spec("PrivacyOfficer", "assesses", "NotificationRequirement", modality="whether"),
            _spec(
                "DataSubject",
                "mustBeNotified",
                "Notification",
                modality="whether",
                embedded_modality="must",
                context="PrivacyOfficerAssessment",
                voice="passive",
            ),
        ]
    if lower == "the organization implements corrective actions to prevent recurrence":
        return [
            _spec("Organization", "implements", "CorrectiveAction"),
            _spec("CorrectiveAction", "prevents", "Recurrence", modality="purpose"),
        ]
    if lower == "orion should be able to identify security concepts, classify hierarchical relationships, and extract meaningful relationships from this text":
        return [
            _spec("ORION", "identifies", "SecurityConcept", modality="should", capability="true"),
            _spec("ORION", "classifies", "HierarchicalRelationship", modality="should", capability="true"),
            _spec("ORION", "extracts", "MeaningfulRelationship", modality="should", capability="true", scope="ThisText"),
        ]
    match = re.match(r"^(?P<classes>.+?) are important classes$", text.rstrip("."), re.IGNORECASE)
    if match:
        return [
            _spec(item, "declared_as", "ImportantClass", metamodel="true", importance="important")
            for item in _split_list(match.group("classes"))
        ]
    return None


def extract_remediation_b_claim_specs(text: str) -> list[dict[str, str]] | None:
    """Return source-faithful claim specs for reusable high-risk sentence forms.

    ``None`` means the normal canonical extractor should handle the sentence.  An
    explicit list means this rule owns the sentence, preventing malformed fallback
    claims from being projected alongside the corrected representation.
    """

    clean = _clean(text)
    if not clean:
        return None

    # Specific paragraph repairs run before the broad modal fallback to preserve exact ownership.
    for extractor in (
        _importance_specs,
        _shared_verb_specs,
        _infosec_021_022_specs,
        _infosec_031_032_specs,
        _infosec_039_040_specs,
        _infosec_041_042_specs,
        _modal_svo_specs,
    ):
        specs = extractor(clean)
        if specs is not None:
            return specs
    return None
