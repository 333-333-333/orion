"""Parse the supported illustrates-how relation construction."""

from __future__ import annotations

import re
from collections.abc import Callable

_ILLUSTRATES_HOW_RELATE_PATTERN = re.compile(
    r'^(?P<subject>.+?)\s+(?P<verb>illustrates)\s+how\s+(?P<objects>.+?)\s+relate\s+to\s+each\s+other\.?$',
    re.IGNORECASE,
)


def extract_illustrates_how_relations(
    text: str,
    label: Callable[[str | None], str],
    verb: Callable[[str | None], str],
) -> tuple[str, str, list[str]] | None:
    """Parse the supported 'illustrates how ... relate' construction into relation components."""
    match = _ILLUSTRATES_HOW_RELATE_PATTERN.match(text)
    if not match:
        return None
    subject = label(match.group('subject'))
    predicate = verb(match.group('verb'))
    raw_items = re.sub(r'\b(?:and|or)\b', ',', match.group('objects'), flags=re.IGNORECASE)
    objects = [item for part in raw_items.split(',') if (item := label(part))]
    if not subject or not predicate or not objects:
        return None
    return subject, predicate, objects
