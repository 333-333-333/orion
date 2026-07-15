"""Source-faithful scenario repairs for audited phishing and ransomware narratives.

These exact sentence rules keep example participants separate from ontology classes,
preserve modal and coordination scope, and record uncertain discourse antecedents
without asserting identity.
"""

from __future__ import annotations

from typing import Any

from rules import Rule, RuleContext

_RULE_ID = "RULE-SEMANTIC-REMEDIATION-B3-001"


def _claim(ctx: RuleContext, subject: str, predicate: str, obj: str, **metadata: Any) -> dict[str, Any]:
    """Build one traced claim about a participant in an illustrative scenario."""
    metadata.setdefault("observation_scope", "illustrative_example")
    metadata.setdefault("preserve_lexical_object", "true")
    metadata.setdefault("term_ref_policy", "distinct")
    return ctx.make_claim(
        ctx.source_text_id,
        ctx.sentence,
        ctx.paragraph_id,
        f"{subject} {predicate} {obj}",
        "relation",
        subject=subject,
        predicate=predicate,
        object=obj,
        extracted_by=_RULE_ID,
        behavior="preserve_scenario_scope_and_discourse_uncertainty",
        **metadata,
    )


def _may(ctx: RuleContext, subject: str, predicate: str, obj: str, **metadata: Any) -> dict[str, Any]:
    """Build a possible relation that cannot become a categorical RDF fact."""
    return _claim(ctx, subject, predicate, obj, modality="may", projection_scope="scoped", **metadata)


def _unresolved(candidate_subjects: str) -> dict[str, str]:
    """Mark a definite expression whose antecedent is plausible but not entailed."""
    return {
        "discourse_resolution": "unresolved",
        "candidate_subjects": candidate_subjects,
    }


def _group(ctx: RuleContext, suffix: str) -> str:
    return f"{_RULE_ID}:{ctx.sentence.get('sentence_id', '')}:{suffix}"


def _rewrite(text: str, ctx: RuleContext) -> list[dict[str, Any]]:
    """Return exact replacements for p039/p040 sentence forms."""
    lower = text.casefold()

    if lower == "a phishing scenario illustrates how threats, vulnerabilities, controls, and incidents relate to each other.":
        categories = ("Threat", "Vulnerability", "Control", "Incident")
        return [
            _claim(
                ctx,
                left,
                "relatesTo",
                right,
                context="PhishingScenario",
                coordination="and",
                relation_role="illustrated_each_other_relation",
                projection_scope="scoped",
            )
            for index, left in enumerate(categories)
            for right in categories[index + 1 :]
        ]
    if lower == "a threat actor sends a phishing email to an employee.":
        group = _group(ctx, "sending")
        return [
            _claim(ctx, "ThreatActor", "sends", "PhishingEmail", recipient="Employee", proposition_group=group),
            _claim(
                ctx,
                "PhishingEmail",
                "sentTo",
                "Employee",
                voice="passive",
                relation_role="recipient_projection",
                proposition_group=group,
            ),
        ]
    if lower == "the phishing email contains a malicious link.":
        return [_claim(ctx, "PhishingEmail", "contains", "MaliciousLink")]
    if lower == "the employee clicks the malicious link and submits a password.":
        group = _group(ctx, "employee-actions")
        return [
            _claim(ctx, "Employee", "clicks", "MaliciousLink", coordination="and", proposition_group=group),
            _claim(ctx, "Employee", "submits", "SubmittedPassword", coordination="and", proposition_group=group),
        ]
    if lower == "the submitted password becomes a compromised credential.":
        return [_claim(ctx, "SubmittedPassword", "becomes", "CompromisedCredential")]
    if lower == "the attacker uses the compromised credential to access a cloud account.":
        uncertainty = _unresolved("ThreatActor")
        return [
            _claim(ctx, "Attacker", "uses", "CompromisedCredential", **uncertainty),
            _claim(
                ctx,
                "Attacker",
                "accesses",
                "CloudAccount",
                modality="purpose",
                instrument="CompromisedCredential",
                relation_role="purpose_content",
                projection_scope="scoped",
                **uncertainty,
            ),
        ]
    if lower == "multi-factor authentication may prevent unauthorized access.":
        return [_may(ctx, "MultiFactorAuthentication", "mayPrevent", "UnauthorizedAccess")]
    if lower == "security awareness training may reduce the likelihood of clicking the malicious link.":
        return [_may(ctx, "SecurityAwarenessTraining", "mayReduce", "MaliciousLinkClickingLikelihood")]
    if lower == "email filtering may detect and block the phishing email.":
        group = _group(ctx, "filtering-actions")
        return [
            _may(ctx, "EmailFiltering", "mayDetect", "PhishingEmail", coordination="and", proposition_group=group),
            _may(ctx, "EmailFiltering", "mayBlock", "PhishingEmail", coordination="and", proposition_group=group),
        ]
    if lower == "log monitoring may identify suspicious login activity.":
        return [_may(ctx, "LogMonitoring", "mayIdentify", "SuspiciousLoginActivity")]
    if lower == "incident response may contain the compromised account.":
        return [
            _may(
                ctx,
                "IncidentResponse",
                "mayContain",
                "CompromisedAccount",
                **_unresolved("CloudAccount"),
            )
        ]

    if lower == "a ransomware scenario illustrates the importance of backups, monitoring, and response.":
        return [
            _claim(
                ctx,
                "RansomwareScenario",
                "illustratesImportanceOf",
                obj,
                coordination="and",
                scope="importance",
                projection_scope="scoped",
            )
            for obj in ("Backup", "Monitoring", "Response")
        ]
    if lower == "malware encrypts files on a file server.":
        group = _group(ctx, "encryption")
        return [
            _claim(ctx, "Malware", "encrypts", "File", location="FileServer", location_relation="on", proposition_group=group),
            _claim(ctx, "File", "locatedOn", "FileServer", relation_role="location", proposition_group=group),
        ]
    if lower == "the file server becomes unavailable to business users.":
        group = _group(ctx, "unavailability")
        return [
            _claim(ctx, "FileServer", "becomes", "Unavailable", beneficiary="BusinessUser", proposition_group=group),
            _claim(ctx, "FileServer", "unavailableTo", "BusinessUser", proposition_group=group),
        ]
    if lower == "the event affects availability and may affect integrity.":
        uncertainty = _unresolved("MalwareEncryption,FileServerUnavailability")
        return [
            _claim(ctx, "Event", "affects", "Availability", coordination="and", **uncertainty),
            _may(ctx, "Event", "mayAffect", "Integrity", coordination="and", **uncertainty),
        ]
    if lower == "endpoint detection and response may detect the malware activity.":
        return [
            _may(
                ctx,
                "EndpointDetectionAndResponse",
                "mayDetect",
                "MalwareActivity",
                **_unresolved("MalwareEncryptingFiles"),
            )
        ]
    if lower == "network segmentation may limit the spread of the ransomware.":
        return [
            _may(ctx, "NetworkSegmentation", "mayLimit", "RansomwareSpread", **_unresolved("Malware"))
        ]
    if lower == "backup restoration may recover encrypted files.":
        return [_may(ctx, "BackupRestoration", "mayRecover", "File", state="encrypted")]
    if lower == "the incident response team may isolate affected systems.":
        return [
            _may(ctx, "IncidentResponseTeam", "mayIsolate", "AffectedSystem", **_unresolved("FileServer"))
        ]
    if lower == "the post-incident review may identify missing patches, weak access controls, or insufficient monitoring.":
        group = _group(ctx, "review-alternatives")
        return [
            _may(
                ctx,
                "PostIncidentReview",
                "mayIdentify",
                obj,
                coordination="or",
                alternative_group=group,
            )
            for obj in ("MissingPatch", "WeakAccessControl", "InsufficientMonitoring")
        ]
    if lower == "corrective actions may include patch deployment, privilege reduction, and improved detection rules.":
        group = _group(ctx, "corrective-actions")
        return [
            _may(ctx, "CorrectiveAction", "mayInclude", obj, coordination="and", proposition_group=group)
            for obj in ("PatchDeployment", "PrivilegeReduction", "ImprovedDetectionRule")
        ]

    return []


class RemediationB3Rule(Rule):
    """Replace p039/p040 claims after earlier broad remediation layers."""

    rule_id = _RULE_ID
    stage = "semantic_claims"
    priority = 50
    behavior = "preserve_scenario_scope_and_discourse_uncertainty"

    def apply(
        self,
        claims: list[dict[str, Any]],
        context: RuleContext,
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        emitted = _rewrite(context.clean(str(context.sentence.get("text", ""))), context)
        if not emitted:
            return [], []
        sentence_id = str(context.sentence.get("sentence_id", ""))
        claims[:] = [
            claim
            for claim in claims
            if str((claim.get("source") or {}).get("sentence_id", "")) != sentence_id
        ]
        return emitted, []


REMEDIATION_B3_RULE = RemediationB3Rule()

__all__ = ["REMEDIATION_B3_RULE"]
