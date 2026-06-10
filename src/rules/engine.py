from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class RuleContext:
    source_text_id: str
    sentence: dict[str, Any]
    paragraph_id: str
    clean: Callable[[str | None], str]
    label: Callable[[str | None], str]
    verb: Callable[[str | None], str]
    make_claim: Callable[..., dict[str, Any]]


class Rule:
    rule_id: str = ''
    stage: str = ''
    languages: tuple[str, ...] = ('en',)
    priority: int = 100
    enabled: bool = True
    behavior: str = ''

    def apply(self, claims: list[dict[str, Any]], context: RuleContext) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        return [], []


class RuleEngine:
    def __init__(self, stage: str) -> None:
        self._stage = stage
        self._registry: list[Rule] = []

    def register(self, rule: Rule) -> Rule:
        self._registry.append(rule)
        return rule

    def run(
        self,
        claims: list[dict[str, Any]],
        input_payload: dict[str, Any],
        config: dict[str, Any],
        paragraphs: dict[str, str],
        context_factory: Callable[[dict[str, Any], str], RuleContext],
    ) -> list[dict[str, Any]]:
        if config.get('rules_enabled', True) is False:
            return []
        language = self._language(config, input_payload)
        rejected: list[dict[str, Any]] = []
        rules = sorted(self._registry, key=lambda rule: (self._rule_config(config, rule.rule_id).get('priority', rule.priority), rule.rule_id))
        for rule in rules:
            if rule.stage != self._stage or language not in rule.languages or not self._rule_enabled(rule, config):
                continue
            for sentence in [item for item in input_payload.get('sentences', []) if isinstance(item, dict)]:
                new_claims, new_rejected = rule.apply(claims, context_factory(sentence, paragraphs.get(str(sentence.get('sentence_id', '')), '')))
                for claim in new_claims:
                    if claim.get('statement') not in {existing.get('statement') for existing in claims}:
                        claims.append(claim)
                rejected.extend(new_rejected)
        return rejected

    def _rule_config(self, config: dict[str, Any], rule_id: str) -> dict[str, Any]:
        rules = config.get('rules')
        if not isinstance(rules, dict):
            return {}
        value = rules.get(rule_id)
        return value if isinstance(value, dict) else {}

    def _rule_enabled(self, rule: Rule, config: dict[str, Any]) -> bool:
        local = self._rule_config(config, rule.rule_id)
        enabled = local.get('enabled', rule.enabled)
        enabled_rules = self._config_list(config, 'enabled_rules')
        disabled_rules = self._config_list(config, 'disabled_rules')
        if enabled_rules and rule.rule_id not in enabled_rules:
            return False
        return bool(enabled) and rule.rule_id not in disabled_rules

    @staticmethod
    def _config_list(config: dict[str, Any], key: str) -> set[str]:
        value = config.get(key)
        if not isinstance(value, list):
            return set()
        return {str(item).strip() for item in value if str(item).strip()}

    @staticmethod
    def _language(config: dict[str, Any], input_payload: dict[str, Any]) -> str:
        raw = config.get('language') or input_payload.get('language') or input_payload.get('lang') or 'en'
        return str(raw).split('-', 1)[0].casefold()
