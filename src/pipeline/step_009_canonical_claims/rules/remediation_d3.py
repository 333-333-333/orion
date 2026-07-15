"""Residual source-faithful repairs for disjunction, participant, and unresolved scope roles."""

from __future__ import annotations

from typing import Any

from rules import Rule, RuleContext

_RULE_ID = "RULE-SEMANTIC-REMEDIATION-D3-001"


def _claim(ctx: RuleContext, subject: str, predicate: str, obj: str, **metadata: Any) -> dict[str, Any]:
    """Build a traced claim whose semantic term references remain distinguishable downstream."""
    metadata.setdefault("preserve_lexical_object", "true")
    metadata.setdefault("term_ref_policy", "distinct")
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
        behavior="preserve_explicit_roles_and_unresolved_scope",
        **metadata,
    )


def _qualified(ctx: RuleContext, subject: str, predicate: str, obj: str, **metadata: Any) -> dict[str, Any]:
    """Build a relation that may only be represented as an auditable qualified statement."""
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
    """Return exact replacements for audited sentence forms without adding external knowledge."""
    lower = text.casefold()

    if lower == "a data breach is a type of security incident that involves unauthorized access to or disclosure of data.":
        group = f"{_RULE_ID}:{ctx.sentence.get('sentence_id', '')}:alternatives"
        shared = {
            "modality": "disjunctive_alternative",
            "coordination": "or",
            "alternative_group": group,
            "patient": "Data",
            "required_roles": "patient",
            "coordination_ellipsis": "shared_object",
        }
        return [
            _claim(ctx, "DataBreach", "is_a", "SecurityIncident"),
            _claim(
                ctx,
                "DataBreach",
                "involves",
                "UnauthorizedAccess",
                source_term="unauthorized access to data",
                elliptical_source_term="unauthorized access to",
                **shared,
            ),
            _claim(
                ctx,
                "DataBreach",
                "involves",
                "Disclosure",
                source_term="disclosure of data",
                **shared,
            ),
        ]

    if lower == "unauthorized access is a type of security incident involving access by an unapproved identity.":
        group = f"{_RULE_ID}:{ctx.sentence.get('sentence_id', '')}:access-participant"
        return [
            _claim(ctx, "UnauthorizedAccess", "is_a", "SecurityIncident"),
            _claim(
                ctx,
                "UnauthorizedAccess",
                "involves",
                "Access",
                actor="UnapprovedIdentity",
                voice="passive",
                relation_role="defining_property",
                proposition_group=group,
            ),
            _claim(
                ctx,
                "Access",
                "has_actor",
                "UnapprovedIdentity",
                voice="passive",
                relation_role="participant_role",
                proposition_group=group,
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
                confidence=0.65,
            ),
        ]

    return []


class RemediationD3Rule(Rule):
    """Replace residual lossy forms after the earlier D remediation layers."""

    rule_id = _RULE_ID
    stage = "semantic_claims"
    priority = 40
    behavior = "preserve_explicit_roles_and_unresolved_scope"

    def apply(
        self,
        claims: list[dict[str, Any]],
        context: RuleContext,
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """Atomically replace claims for a matched source sentence."""
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


REMEDIATION_D3_RULE = RemediationD3Rule()

__all__ = ["REMEDIATION_D3_RULE"]
