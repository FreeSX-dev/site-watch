"""Хранение последнего известного хэша для каждого URL — простой JSON-файл."""

from __future__ import annotations

import json
from pathlib import Path


class HashStore:
    def __init__(self, path: Path | str = "hashes.json"):
        self.path = Path(path)
        self._data: dict[str, str] = self._load()

    def _load(self) -> dict[str, str]:
        if not self.path.exists():
            return {}
        return json.loads(self.path.read_text())

    def _save(self) -> None:
        self.path.write_text(json.dumps(self._data, indent=2))

    def get(self, url: str) -> str | None:
        return self._data.get(url)

    def set(self, url: str, value: str) -> None:
        self._data[url] = value
        self._save()
