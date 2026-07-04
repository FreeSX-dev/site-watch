"""Хэширование содержимого страницы и извлечение читаемого текста для сравнения."""

from __future__ import annotations

import hashlib
import re

TAG_RE = re.compile(r"<(script|style)[^>]*>.*?</\1>", re.DOTALL | re.IGNORECASE)
STRIP_TAGS_RE = re.compile(r"<[^>]+>")
WHITESPACE_RE = re.compile(r"\s+")


def extract_text(html: str) -> str:
    """Грубая но надёжная очистка HTML до текста — без внешних библиотек парсинга."""
    without_scripts = TAG_RE.sub(" ", html)
    without_tags = STRIP_TAGS_RE.sub(" ", without_scripts)
    return WHITESPACE_RE.sub(" ", without_tags).strip()


def content_hash(html: str) -> str:
    text = extract_text(html)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
