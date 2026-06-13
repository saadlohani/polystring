import pytest

from polystring._models import Token
from polystring._pipeline.stage5_merge import run


def _tok(text: str, lang: str, start: int, end: int, token_type: str = "text") -> Token:
    return Token(text=text, language=lang, token_type=token_type,
                 confidence=0.85, start=start, end=end)


def test_adjacent_same_language_merged():
    tokens = [
        _tok("hello", "en", 0, 5),
        _tok("world", "en", 6, 11),
    ]
    result = run(tokens, [], "hello world")
    assert len(result.spans) == 1
    assert result.spans[0].language == "en"


def test_different_languages_not_merged():
    tokens = [
        _tok("hello", "en", 0, 5),
        _tok("yaar", "ur-Latn", 6, 10),
    ]
    result = run(tokens, [], "hello yaar")
    assert len(result.spans) == 2


def test_dominant_language_by_coverage():
    tokens = [
        _tok("hello", "en", 0, 5),
        _tok("world", "en", 6, 11),
        _tok("yaar", "ur-Latn", 12, 16),
    ]
    result = run(tokens, [], "hello world yaar")
    assert result.dominant_language == "en"


def test_is_mixed():
    tokens = [
        _tok("hello", "en", 0, 5),
        _tok("yaar", "ur-Latn", 6, 10),
    ]
    result = run(tokens, [], "hello yaar")
    assert result.is_mixed is True


def test_is_not_mixed():
    tokens = [
        _tok("hello", "en", 0, 5),
        _tok("world", "en", 6, 11),
    ]
    result = run(tokens, [], "hello world")
    assert result.is_mixed is False


def test_languages_set_excludes_special():
    tokens = [
        _tok("hello", "en", 0, 5),
        _tok("https://x.com", "url", 6, 19, token_type="url"),
    ]
    result = run(tokens, [], "hello https://x.com")
    assert "url" not in result.languages
    assert "en" in result.languages
