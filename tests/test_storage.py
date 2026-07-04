import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sitewatch.storage import HashStore  # noqa: E402


def test_store_returns_none_for_unknown_url(tmp_path):
    store = HashStore(tmp_path / "hashes.json")
    assert store.get("https://example.com") is None


def test_store_persists_across_instances(tmp_path):
    file_path = tmp_path / "hashes.json"
    store = HashStore(file_path)
    store.set("https://example.com", "abc123")

    reloaded = HashStore(file_path)
    assert reloaded.get("https://example.com") == "abc123"


if __name__ == "__main__":
    import pytest

    raise SystemExit(pytest.main([__file__, "-v"]))
