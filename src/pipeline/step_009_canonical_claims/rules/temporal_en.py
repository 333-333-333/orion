from __future__ import annotations

import re
from typing import Any

from rules import Rule, RuleContext

_TEMPORAL_RULE_ID = 'RULE-SEMANTIC-TEMPORAL-EN-001'
_TEMPORAL_SCOPE_PATTERN = re.compile(
    r'^(?P<subject>.+?)\s+(?P<verb>[A-Za-z]+(?:s|es|ies))\s+(?P<object>.+?)\s+(?P<scopes>before\s*,\s*during\s*,\s*(?:and\s*)?after|before\s+and\s+after|before|during|after)\s+(?P<context>.+?)\.?$',
    re.IGNORECASE,
)
_TEMPORAL_SCOPE_PREDICATES = {'before': 'applies_before', 'during': 'applies_during', 'after': 'applies_after'}


class TemporalScopeRule(Rule):
    rule_id = _TEMPORAL_RULE_ID
    stage = 'semantic_claims'
    priority = 10
    behavior = 'decompose_temporal_scope'

    def apply(self, claims: list[dict[str, Any]], context: RuleContext) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        text = context.clean(str(context.sentence.get('text', '')))
        match = _TEMPORAL_SCOPE_PATTERN.match(text)
        if not match:
            return [], []
        subject = context.label(match.group('subject'))
        predicate = context.verb(match.group('verb'))
        obj = context.label(match.group('object'))
        scope_context = context.label(match.group('context'))
        if not subject or not predicate or not obj or not scope_context:
            return [], []
        base = context.make_claim(
            context.source_text_id,
            context.sentence,
            context.paragraph_id,
            f'{subject} {predicate} {obj}',
            'relation',
            subject=subject,
            predicate=predicate,
            object=obj,
            extracted_by=self.rule_id,
            behavior=self.behavior,
        )
        emitted = [base]
        for scope in ('before', 'during', 'after'):
            if re.search(rf'\b{scope}\b', match.group('scopes'), flags=re.IGNORECASE):
                emitted.append(context.make_claim(
                    context.source_text_id,
                    context.sentence,
                    context.paragraph_id,
                    f'{obj} {_TEMPORAL_SCOPE_PREDICATES[scope]} {scope_context}',
                    'relation',
                    subject=obj,
                    predicate=_TEMPORAL_SCOPE_PREDICATES[scope],
                    object=scope_context,
                    extracted_by=self.rule_id,
                    behavior=self.behavior,
                    derivation=f'temporal_scope:{scope}',
                    source_claim_id=str(base.get('claim_id', '')),
                ))
        rejected = []
        sentence_id = str(context.sentence.get('sentence_id', ''))
        for claim in claims:
            if claim.get('source', {}).get('sentence_id') == sentence_id and claim.get('subject') == subject and claim.get('predicate') == predicate:
                rejected.append({
                    'type': 'temporal_scope_superseded',
                    'claim_id': claim.get('claim_id'),
                    'statement': claim.get('statement'),
                    'extracted_by': self.rule_id,
                    'behavior': self.behavior,
                    'source_sentence': text,
                })
        claims[:] = [
            claim for claim in claims
            if not (claim.get('source', {}).get('sentence_id') == sentence_id and claim.get('subject') == subject and claim.get('predicate') == predicate)
        ]
        return emitted, rejected


TEMPORAL_SCOPE_RULE = TemporalScopeRule()
