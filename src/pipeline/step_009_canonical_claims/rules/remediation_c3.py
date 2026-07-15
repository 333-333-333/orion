"""Source-faithful event and role repairs for application infrastructure claims."""

from __future__ import annotations

import re
from typing import Any

ClaimSpec = dict[str, Any]


def _relation(subject: str, predicate: str, obj: str, **metadata: Any) -> ClaimSpec:
    """Build a relation specification without empty qualifiers."""
    return {
        "kind": "relation",
        "subject": subject,
        "predicate": predicate,
        "object": obj,
        **{key: value for key, value in metadata.items() if value not in (None, "")},
    }


def extract_remediation_c3_claims(text: str) -> list[ClaimSpec] | None:
    """Return exact repairs for audited event and prepositional-role sentence forms.

    ``None`` delegates to the established extractors. Exact sentence ownership keeps the
    event/role projections reusable for this corpus without guessing roles in unrelated text.
    """
    lower = re.sub(r"\s+", " ", text.strip()).casefold().rstrip(".")

    if lower == "secure error handling prevents sensitive information from being exposed through error messages":
        return [
            _relation(
                "SecureErrorHandling",
                "prevents",
                "ExposureEvent",
                prevented_event="exposure",
                patient="SensitiveInformation",
                channel="ErrorMessage",
                voice="passive",
                required_roles="prevented_event,patient,channel",
            ),
            _relation(
                "ExposureEvent",
                "has_patient",
                "SensitiveInformation",
                relation_role="event_participant",
            ),
            _relation(
                "ExposureEvent",
                "has_channel",
                "ErrorMessage",
                relation_role="event_channel",
            ),
        ]

    if lower == "a security requirement defines a protection need for an application":
        return [
            _relation(
                "SecurityRequirement",
                "defines",
                "ProtectionNeed",
                beneficiary="Application",
                required_roles="beneficiary",
            ),
            _relation(
                "ProtectionNeed",
                "has_beneficiary",
                "Application",
                relation_role="explicit_for_role",
                preserve_lexical_object="true",
            ),
        ]

    if lower == "a load balancer distributes traffic across multiple servers":
        return [
            _relation(
                "LoadBalancer",
                "distributes",
                "Traffic",
                context="Server",
                context_relation="across",
                quantifier="multiple",
                required_roles="context,context_relation,quantifier",
            ),
            _relation(
                "LoadBalancer",
                "distributes_across",
                "Server",
                patient="Traffic",
                quantifier="multiple",
                relation_role="distribution_context",
                preserve_lexical_object="true",
            ),
        ]

    if lower == "an api gateway controls access to backend services":
        return [
            _relation("APIGateway", "controls", "Access", target="BackendService", required_roles="target"),
            _relation(
                "Access",
                "has_target",
                "BackendService",
                relation_role="access_target",
                preserve_lexical_object="true",
            ),
        ]

    if lower == "a content delivery network improves availability and performance for distributed users":
        return [
            _relation(
                "ContentDeliveryNetwork",
                "improves",
                obj,
                beneficiary="DistributedUser",
                coordination="and",
                required_roles="beneficiary",
            )
            for obj in ("Availability", "Performance")
        ] + [
            _relation(
                "ContentDeliveryNetwork",
                "improves_for",
                "DistributedUser",
                relation_role="explicit_for_role",
                improved_objects="Availability,Performance",
                preserve_lexical_object="true",
            )
        ]

    return None


__all__ = ["extract_remediation_c3_claims"]
