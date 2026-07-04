import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sitewatch.diffing import content_hash, extract_text  # noqa: E402


def test_extract_text_strips_tags():
    html = "<html><body><h1>Привет</h1><p>Текст</p></body></html>"
    assert extract_text(html) == "Привет Текст"


def test_extract_text_strips_scripts_and_styles():
    html = "<div>Видимый<script>var x = 1;</script><style>.a{color:red}</style>текст</div>"
    assert "var x" not in extract_text(html)
    assert "color:red" not in extract_text(html)
    assert "Видимый" in extract_text(html)


def test_content_hash_stable_for_same_text():
    html_a = "<p>Одинаковый текст</p>"
    html_b = "<div>Одинаковый   текст</div>"
    assert content_hash(html_a) == content_hash(html_b)


def test_content_hash_changes_when_text_changes():
    html_a = "<p>Версия 1</p>"
    html_b = "<p>Версия 2</p>"
    assert content_hash(html_a) != content_hash(html_b)


if __name__ == "__main__":
    import pytest

    raise SystemExit(pytest.main([__file__, "-v"]))
