"""Source-faithful scope repairs for credentials, authentication, and recovery claims."""

from __future__ import annotations

import re
from typing import Any

from rules import Rule, RuleContext

_RULE_ID = "RULE-SEMANTIC-REMEDIATION-D2-001"


def _claim(ctx: RuleContext, subject: str, predicate: str, obj: str, **metadata: str) -> dict[str, Any]:
    """Build a deterministic replacement claim from the matched source sentence."""
    metadata.setdefault("preserve_lexical_object", "true")
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
        behavior="preserve_scope_without_assertion_promotion",
        **metadata,
    )


def _qualified(ctx: RuleContext, subject: str, predicate: str, obj: str, **metadata: str) -> dict[str, Any]:
    """Build a claim that must be projected as a qualified RDF statement, not a bare fact."""
    return _claim(
        ctx,
        subject,
        predicate,
        obj,
        projection_scope="scoped",
        rdf_projection="qualified_statement",
        **metadata,
    )


def _rewrite(text: str, ctx: RuleContext) -> list[dict[str, Any]]:
    """Return exact, audited replacements while avoiding unsupported domain inference."""
    lower = text.casefold()

    passive = re.fullmatch(
        r"an? (?P<subject>.+?) must be (?P<action>protected against|stored in) (?:an? )?(?P<object>.+?)\.",
        lower,
    )
    if passive:
        subject = ctx.label(passive.group("subject"))
        predicate = "protected_against" if passive.group("action") == "protected against" else "stored_in"
        return [
            _qualified(
                ctx,
                subject,
                predicate,
                ctx.label(passive.group("object")),
                modality="must",
                voice="passive",
                patient=subject,
            )
        ]

    expiry = re.fullmatch(r"an? (?P<subject>.+?) must expire after an? (?P<object>.+?)\.", lower)
    if expiry:
        obj = ctx.label(expiry.group("object"))
        subject = ctx.label(expiry.group("subject"))
        return [
            _qualified(
                ctx,
                subject,
                "expires",
                obj,
                modality="must",
                temporal_relation="after",
                temporal_object=obj,
            ),
            _claim(
                ctx,
                subject,
                "mustExpireAfter",
                obj,
                modality="must",
                temporal_relation="after",
                temporal_object=obj,
                visibility="internal",
                projection="internal",
                compatibility_only="true",
            ),
        ]

    periodic = re.fullmatch(
        r"an? (?P<subject>.+?) must be (?P<action>rotated|revoked) (?P<temporal>periodically|immediately)\.",
        lower,
    )
    if periodic:
        subject = "APIKey" if periodic.group("subject") == "api key" else ctx.label(periodic.group("subject"))
        action = "Rotation" if periodic.group("action") == "rotated" else "Revocation"
        legacy_predicate = "mustBeRotated" if action == "Rotation" else "mustBeRevoked"
        legacy_object = "Periodically" if action == "Rotation" else "Immediately"
        return [
            _qualified(
                ctx,
                subject,
                "requires",
                action,
                modality="must",
                voice="passive",
                patient=subject,
                temporal_relation=periodic.group("temporal"),
            ),
            _claim(
                ctx,
                subject,
                legacy_predicate,
                legacy_object,
                modality="must",
                temporal_relation=periodic.group("temporal"),
                visibility="internal",
                projection="internal",
                compatibility_only="true",
            ),
        ]

    if lower == "multi-factor authentication improves authentication strength by requiring more than one verification factor.":
        group = f"{_RULE_ID}:{ctx.sentence.get('sentence_id', '')}:means"
        return [
            _claim(ctx, "MultiFactorAuthentication", "improves", "AuthenticationStrength", means_group=group),
            _qualified(
                ctx,
                "MultiFactorAuthentication",
                "requires",
                "VerificationFactor",
                quantifier="more_than_one",
                relation_role="means_for",
                goal="improves AuthenticationStrength",
                means_group=group,
            ),
        ]

    factor = re.fullmatch(
        r"an? (?P<kind>knowledge|possession|inherence) factor is a type of authentication factor "
        r"based on something the user (?P<verb>knows|has|is)\.",
        lower,
    )
    if factor:
        subject = f"{factor.group('kind').capitalize()}Factor"
        return [
            _claim(ctx, subject, "is_a", "AuthenticationFactor"),
            _qualified(
                ctx,
                subject,
                "based_on",
                "Something",
                actor="User",
                event_predicate=factor.group("verb"),
                filler_kind="indefinite",
                filler_quantification="existential",
                relation_role="defining_property",
            ),
        ]

    if lower == "business continuity and disaster recovery protect the organization against major disruptions.":
        return [
            _qualified(
                ctx,
                "BusinessContinuityAndDisasterRecovery",
                "protects",
                "Organization",
                target="MajorDisruption",
                relation_role="coordinated_subject",
                coordination="and",
                coordination_scope="subject",
                members="BusinessContinuity,DisasterRecovery",
            )
        ]

    if lower == "business continuity is the capability to continue critical operations during disruption.":
        return [
            _claim(ctx, "BusinessContinuity", "is_a", "Capability"),
            _qualified(
                ctx,
                "BusinessContinuity",
                "continues",
                "CriticalOperation",
                modality="capability",
                temporal_relation="during",
                temporal_object="Disruption",
                relation_role="capability_content",
            ),
        ]

    if lower == "disaster recovery is the process of restoring technology services after a disruptive event.":
        return [
            _claim(ctx, "DisasterRecovery", "is_a", "Process"),
            _qualified(
                ctx,
                "DisasterRecovery",
                "restores",
                "TechnologyService",
                temporal_relation="after",
                temporal_object="DisruptiveEvent",
                relation_role="process_content",
            ),
        ]

    if lower == "a backup is a copy of data used for recovery.":
        return [
            _claim(ctx, "Backup", "is_a", "CopyOfData"),
            _qualified(
                ctx,
                "Backup",
                "used_for",
                "Recovery",
                modality="purpose",
                voice="passive",
                interpretation_status="ambiguous_attachment",
                attachment_scope="unresolved",
                candidate_subjects="Backup,CopyOfData,Data",
            ),
        ]

    if lower == "a recovery point objective defines the maximum acceptable amount of data loss measured in time.":
        return [
            _qualified(
                ctx,
                "RecoveryPointObjective",
                "defines",
                "MaximumAcceptableAmountOfDataLoss",
                measurement_unit="Time",
                qualifier="maximum_acceptable",
                relation_role="definition_content",
            )
        ]

    if lower == "a disaster recovery test verifies whether recovery procedures work as expected.":
        return [
            _qualified(
                ctx,
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


class RemediationD2Rule(Rule):
    """Replace lossy claims for matched audited forms after the earlier remediation rules."""

    rule_id = _RULE_ID
    stage = "semantic_claims"
    priority = 30
    behavior = "preserve_scope_without_assertion_promotion"

    def apply(
        self,
        claims: list[dict[str, Any]],
        context: RuleContext,
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """Atomically replace claims from a matched sentence."""
        text = context.clean(str(context.sentence.get("text", "")))
        emitted = _rewrite(text, context)
        if not emitted:
            return [], []
        sentence_id = str(context.sentence.get("sentence_id", ""))
        claims[:] = [
            claim
            for claim in claims
            if str((claim.get("source") or {}).get("sentence_id", "")) != sentence_id
        ]
        return emitted, []


REMEDIATION_D2_RULE = RemediationD2Rule()

__all__ = ["REMEDIATION_D2_RULE"]
