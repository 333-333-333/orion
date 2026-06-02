from __future__ import annotations

from hashlib import sha256
from typing import Any


def build_source_text_id(raw_text: str, source_kind: str, config: dict[str, Any]) -> str:
    config_fingerprint = repr(sorted(config.items()))
    stable_base = f"{source_kind}|{raw_text}|{config_fingerprint}"
    return sha256(stable_base.encode('utf-8')).hexdigest()
