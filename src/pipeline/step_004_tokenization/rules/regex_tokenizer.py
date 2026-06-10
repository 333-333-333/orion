from __future__ import annotations

import hashlib
import re

TOKEN_PATTERN = re.compile(r"\w+|[^\w\s]", re.UNICODE)


def build_token_id(source_text_id: str, index: int, sentence_id: str, start_offset: int, end_offset: int, text: str) -> str:
    stable_key = f"{source_text_id}|{index}|{sentence_id}|{start_offset}|{end_offset}|{text}".encode("utf-8")
    digest = hashlib.sha256(stable_key).hexdigest()[:16]
    return f"tok-{digest}"
