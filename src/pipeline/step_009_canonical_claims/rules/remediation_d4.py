"""Preserve ambiguous type coordination and anonymous discourse referents without OWL promotion."""

from __future__ import annotations

from typing import Any

from rules import Rule, RuleContext

_RULE_ID = "RULE-SEMANTIC-REMEDIATION-D4-001"


def _claim(ctx: RuleContext, subject: str, predicate: str, obj: str, **metadata: Any) -> dict[str, Any]:
    """Build a traced claim with distinct semantic term references."""
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
        behavior="preserve_ambiguous_types_and_discourse_referents",
        **metadata,
    )


def _qualified(ctx: RuleContext, subject: str, predicate: str, obj: str, **metadata: Any) -> dict[str, Any]:
    """Build a claim that is visible only through a qualified RDF statement."""
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
    """Return conservative replacements for the two audited source forms."""
    lower = text.casefold()

    if lower == "a lost device incident is a type of physical and information security incident.":
        return [
            _qualified(
                ctx,
                "LostDeviceIncident",
                "is_a",
                "PhysicalAndInformationSecurityIncident",
                interpretation_status="ambiguous_coordination",
                coordination="and",
                coordination_scope="object_type_modifiers",
                coordination_members="Physical,InformationSecurity",
                candidate_interpretations="compound_type,coordinated_type_modifiers",
                object_resource_kind="unresolved_type_expression",
                confidence=0.65,
            )
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
                object_resource_kind="anonymous_referent",
                object_quantification="definite",
            )
        ]

    return []


class RemediationD4Rule(Rule):
    """Replace ontology-committing readings after the earlier D remediation layers."""

    rule_id = _RULE_ID
    stage = "semantic_claims"
    priority = 50
    behavior = "preserve_ambiguous_types_and_discourse_referents"

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


REMEDIATION_D4_RULE = RemediationD4Rule()

__all__ = ["REMEDIATION_D4_RULE"]
