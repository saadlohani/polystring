from __future__ import annotations

import pytest

from polystring._ngram import available_languages, score


def test_models_load():
    langs = available_languages()
    assert len(langs) >= 3, f"Expected 3 models, got {langs}"
    assert "ur-Latn" in langs
    assert "tl" in langs
    assert "sw" in langs


@pytest.mark.parametrize("word,xfail_reason", [
    ("shaadi",      None),
    ("taqreeb",     None),
    ("mohabbat",    None),
    ("khwahish",    None),
    ("musafir",     "Arabic loanword shared with Swahili msafiri; genuinely ambiguous"),
    ("rozgaar",     None),
    ("rishtedaar",  None),
    ("mukhtalif",   None),
    ("mazaaq",      None),
    ("zindabad",    None),
])
def test_ngram_roman_urdu_words(word, xfail_reason):
    if xfail_reason:
        pytest.xfail(xfail_reason)
    result = score(word)
    assert result is not None, f"{word!r} returned None, expected ur-Latn hit"
    lang, conf = result
    assert lang == "ur-Latn", f"{word!r} scored as {lang!r}, expected ur-Latn"
    assert 0.60 <= conf <= 0.95


@pytest.mark.parametrize("word", [
    "magkasama",
    "pagmamahal",
    "kasalanan",
    "kapatiran",
    "pamamahala",
    "naniniwala",
    "nagtatrabaho",
    "kinakailangan",
])
def test_ngram_tagalog_words(word):
    result = score(word)
    assert result is not None, f"{word!r} returned None, expected tl hit"
    lang, conf = result
    assert lang == "tl", f"{word!r} scored as {lang!r}, expected tl"
    assert 0.60 <= conf <= 0.95


@pytest.mark.parametrize("word", [
    "maendeleo",
    "serikali",
    "wananchi",
    "mwanafunzi",
    "mazingira",
    "mwalimu",
    "uchumi",
    "elimu",
])
def test_ngram_swahili_words(word):
    result = score(word)
    assert result is not None, f"{word!r} returned None, expected sw hit"
    lang, conf = result
    assert lang == "sw", f"{word!r} scored as {lang!r}, expected sw"
    assert 0.60 <= conf <= 0.95


@pytest.mark.parametrize("word", [
    "computer",
    "absolutely",
    "beautiful",
    "government",
    "yesterday",
    "important",
    "wonderful",
])
def test_english_words_not_confident(word):
    result = score(word)
    if result is not None:
        lang, conf = result
        assert conf < 0.80, f"{word!r} scored {lang!r} with confidence {conf:.2f}"


def test_too_short_returns_none():
    assert score("ab") is None
    assert score("a") is None
    assert score("") is None


def test_candidate_restriction_excludes_language():
    result = score("shaadi", candidates=frozenset({"sw"}))
    if result is not None:
        lang, _ = result
        assert lang == "sw"


def test_candidate_restriction_empty_returns_none():
    result = score("shaadi", candidates=frozenset({"es", "fr"}))
    assert result is None


def test_candidate_restriction_allows_correct_language():
    result = score("shaadi", candidates=frozenset({"ur-Latn", "tl"}))
    assert result is not None
    lang, _ = result
    assert lang == "ur-Latn"


def test_analyze_roman_urdu_content_word():
    from polystring import analyze
    result = analyze("yaar kal shaadi thi bahut mazaa aaya")
    langs = {s.language for s in result.linguistic_spans()}
    assert "ur-Latn" in langs


def test_analyze_tagalog_content_word():
    from polystring import analyze
    result = analyze("ang mga wananchi nagtatrabaho araw araw")
    langs = {s.language for s in result.linguistic_spans()}
    assert "tl" in langs or result.dominant_language == "tl"


def test_analyze_swahili_content_word():
    from polystring import analyze
    result = analyze("serikali inataka maendeleo kwa wananchi wote")
    langs = {s.language for s in result.linguistic_spans()}
    assert "sw" in langs or result.dominant_language == "sw"
