from __future__ import annotations

import re
from collections.abc import Callable


def explicit_svo_entity_labels_from_evidence(
    evidence: str,
    normalize_label: Callable[[str], str],
    dedupe_values: Callable[[list[str]], list[str]],
) -> list[str]:
    text = re.sub(r'\s+', ' ', str(evidence or '').strip())
    if not text:
        return []
    marker = re.search(r'^The resulting ontology should represent that(?P<body>.+)', text, flags=re.IGNORECASE)
    if not marker:
        return []
    body = marker.group('body')
    body = re.split(r'\b(?:should|also)\s+represent\s+that\b', body, maxsplit=1, flags=re.IGNORECASE)[0]
    body = re.split(r'[.;:]', body, maxsplit=1)[0]
    clauses = [re.sub(r'^(?:and|or)\s+', '', part.strip(), flags=re.IGNORECASE) for part in re.split(r',\s+|\s+and\s+', body) if part.strip()]
    labels: list[str] = []
    for clause in clauses:
        match = re.match(
            r'^(?P<subject>[a-z][a-z0-9 -]*?)\s+(?P<predicate>access|include|reduce|exploit|affect|process|define|provide|evaluate|protect|support|detect)s?\s+(?P<object>[a-z][a-z0-9 -]*?)$',
            clause,
            flags=re.IGNORECASE,
        )
        if match:
            labels.extend([match.group('subject'), match.group('object')])
            continue
        passive = re.match(
            r'^(?P<subject>[a-z][a-z0-9 -]*?)\s+are\s+satisfied\s+by\s+(?P<object>[a-z][a-z0-9 -]*?)$',
            clause,
            flags=re.IGNORECASE,
        )
        if passive:
            labels.extend([passive.group('subject'), passive.group('object')])
    return dedupe_values([normalize_label(label) for label in labels if label])
