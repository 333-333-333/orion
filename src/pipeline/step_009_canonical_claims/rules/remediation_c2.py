"""Source-faithful repairs for audited application, architecture, and ontology discourse forms."""

from __future__ import annotations

import re
from typing import Any

ClaimSpec = dict[str, Any]


def _relation(subject: str, predicate: str, obj: str, **metadata: str) -> ClaimSpec:
    """Build a compact relation specification."""
    return {
        "kind": "relation",
        "subject": subject,
        "predicate": predicate,
        "object": obj,
        **{key: value for key, value in metadata.items() if value not in (None, "")},
    }


def _definition(subject: str, obj: str) -> ClaimSpec:
    """Build a compact definition specification."""
    return {"kind": "definition", "subject": subject, "predicate": "is_a", "object": obj}


def _group(sentence_id: str, role: str) -> str:
    """Build a deterministic sentence-local semantic group identifier."""
    return f"remediation-c2:{sentence_id}:{role}"


def extract_remediation_c2_claims(text: str, *, sentence_id: str) -> list[ClaimSpec]:
    """Return replacements for exact audited sentence forms, or an empty list.

    Exact matching prevents these structural repairs from silently adding domain knowledge to
    superficially similar language.
    """
    clean = re.sub(r"\s+", " ", text.strip())
    lower = clean.casefold().rstrip(".")

    if lower == "application security protects software systems throughout their lifecycle":
        return [
            _relation(
                "ApplicationSecurity",
                "protects",
                "SoftwareSystem",
                scope="Lifecycle",
                scope_relation="throughout",
                scope_owner="SoftwareSystem",
                scope_owner_relation="lifecycle_of",
            ),
            _relation(
                "Lifecycle",
                "lifecycle_of",
                "SoftwareSystem",
                relation_role="scope_ownership",
            ),
        ]

    if lower == "a software vulnerability is a weakness in application code, configuration, or design":
        group = _group(sentence_id, "location-alternatives")
        return [
            _definition("SoftwareVulnerability", "Weakness"),
            *[
                _relation(
                    "SoftwareVulnerability",
                    "has_location",
                    obj,
                    modality="disjunctive_alternative",
                    coordination="or",
                    alternative_group=group,
                )
                for obj in ("ApplicationCode", "Configuration", "Design")
            ],
        ]

    if lower == "input validation prevents malicious or malformed data from entering an application":
        group = _group(sentence_id, "entering-data-alternatives")
        return [
            _relation(
                "InputValidation",
                "prevents",
                "EnteringEvent",
                prevented_event="entering",
                event_target="Application",
                proposition_group=_group(sentence_id, "prevented-event"),
            ),
            *[
                _relation(
                    "EnteringEvent",
                    "has_patient",
                    obj,
                    modality="disjunctive_alternative",
                    coordination="or",
                    alternative_group=group,
                    relation_role="event_participant",
                )
                for obj in ("MaliciousData", "MalformedData")
            ],
            _relation(
                "EnteringEvent",
                "has_target",
                "Application",
                relation_role="event_target",
                preserve_lexical_object="true",
            ),
        ]

    if lower == "backup and recovery support resilience":
        return [
            _relation(
                "BackupAndRecovery",
                "supports",
                "Resilience",
                coordination="and",
                coordination_scope="subject",
                members="Backup,Recovery",
                relation_role="coordinated_subject",
                projection_scope="scoped",
            )
        ]

    if lower == "these relationships make the generated rdf or owl graph suitable for querying, validation, reasoning, and mining":
        group = _group(sentence_id, "graph-format-alternatives")
        return [
            _relation(
                "GeneratedGraph",
                "suitable_for",
                purpose,
                coordination="and",
                relation_role="discourse_consequence",
                projection_scope="scoped",
                antecedent_scope="represented_relationships",
                graph_format_alternatives="RDF,OWL",
                graph_format_operator="or",
                graph_format_group=group,
            )
            for purpose in ("Querying", "Validation", "Reasoning", "Mining")
        ]

    return []


__all__ = ["extract_remediation_c2_claims"]
