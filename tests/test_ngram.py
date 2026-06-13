"""Tests for the character n-gram scorer (_ngram.py).

These tests verify:
  - Models load without error
  - Unambiguous words from each language score correctly
  - Short tokens and English words return None (no false positives)
  - The confidence hint restriction works correctly
  - Integration: n-gram hits flow through the full analyze() pipeline
"""
from __future__ import annotations

import pytest

from polystring._ngram import available_languages, score


# ---------------------------------------------------------------------------
# Model availability
# ---------------------------------------------------------------------------

def test_models_load():
    langs = available_languages()
    assert len(langs) >= 3, f"Expected 3 models, got {langs}"
    assert "ur-Latn" in langs
    assert "tl" in langs
    assert "sw" in langs


# ---------------------------------------------------------------------------
# Roman Urdu — words not in the lexicon that should score ur-Latn
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("word,xfail_reason", [
    ("shaadi",      None),
    ("taqreeb",     None),
    ("mohabbat",    None),
    ("khwahish",    None),
    ("musafir",     "Arabic loanword shared with Swahili (msafiri); ambiguous by design"),
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
    assert result is not None, f"{word!r} returned None — expected ur-Latn hit"
    lang, conf = result
    assert lang == "ur-Latn", f"{word!r} scored as {lang!r}, expected ur-Latn"
    assert 0.60 <= conf <= 0.95


# ---------------------------------------------------------------------------
# Tagalog — words not in lexicon that should score tl
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("word", [
    "magkasama",    # together
    "pagmamahal",   # love/affection
    "kasalanan",    # sin/fault
    "kapatiran",    # brotherhood
    "pamamahala",   # governance/management
    "naniniwala",   # believes
    "nagtatrabaho", # is working
    "kinakailangan",# needed/required
])
def test_ngram_tagalog_words(word):
    result = score(word)
    assert result is not None, f"{word!r} returned None — expected tl hit"
    lang, conf = result
    assert lang == "tl", f"{word!r} scored as {lang!r}, expected tl"
    assert 0.60 <= conf <= 0.95


# ---------------------------------------------------------------------------
# Swahili — words not in lexicon that should score sw
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("word", [
    "maendeleo",    # development/progress
    "serikali",     # government
    "wananchi",     # citizens
    "mwanafunzi",   # student
    "mazingira",    # environment
    "mwalimu",      # teacher (also in lexicon — tests overlap)
    "uchumi",       # economy
    "elimu",        # education
])
def test_ngram_swahili_words(word):
    result = score(word)
    assert result is not None, f"{word!r} returned None — expected sw hit"
    lang, conf = result
    assert lang == "sw", f"{word!r} scored as {lang!r}, expected sw"
    assert 0.60 <= conf <= 0.95


# ---------------------------------------------------------------------------
# Negative cases — English content words should not score confidently
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("word", [
    "computer",
    "absolutely",
    "beautiful",
    "government",
    "yesterday",
    "important",
    "wonderful",
])
def test_english_words_no_confident_hit(word):
    result = score(word)
    # Either None (no confident winner) or a hit with very low confidence
    # We accept None; we reject any confident non-English classification
    if result is not None:
        lang, conf = result
        # If it does return something it should be low confidence
        assert conf < 0.80, (
            f"English word {word!r} scored {lang!r} with high confidence {conf:.2f}"
        )


# ---------------------------------------------------------------------------
# Short token guard
# ---------------------------------------------------------------------------

def test_too_short_returns_none():
    assert score("ab") is None
    assert score("a") is None
    assert score("") is None


# ---------------------------------------------------------------------------
# Candidate restriction
# ---------------------------------------------------------------------------

def test_candidate_restriction_excludes_language():
    # Restrict to only sw — a ur-Latn word should not win
    result = score("shaadi", candidates=frozenset({"sw"}))
    # Either None (sw doesn't win) or sw (unlikely but valid)
    if result is not None:
        lang, _ = result
        assert lang == "sw"


def test_candidate_restriction_empty_returns_none():
    # No n-gram models in the candidate set → None
    result = score("shaadi", candidates=frozenset({"es", "fr"}))
    assert result is None


def test_candidate_restriction_allows_correct_language():
    result = score("shaadi", candidates=frozenset({"ur-Latn", "tl"}))
    assert result is not None
    lang, _ = result
    assert lang == "ur-Latn"


# ---------------------------------------------------------------------------
# Integration: n-gram words flow through analyze() correctly
# ---------------------------------------------------------------------------

def test_analyze_roman_urdu_content_word():
    """A Roman Urdu content word not in the lexicon should be labelled ur-Latn."""
    from polystring import analyze
    result = analyze("yaar kal shaadi thi bahut mazaa aaya")
    langs = {s.language for s in result.linguistic_spans()}
    assert "ur-Latn" in langs


def test_analyze_tagalog_content_word():
    """A Tagalog content word not in lexicon should be detected."""
    from polystring import analyze
    result = analyze("ang mga wananchi nagtatrabaho araw araw")
    langs = {s.language for s in result.linguistic_spans()}
    # n-gram should label these tl; if absorbed by context that's also fine
    assert "tl" in langs or result.dominant_language == "tl"


def test_analyze_swahili_content_word():
    """A Swahili content word not in lexicon should be detected."""
    from polystring import analyze
    result = analyze("serikali inataka maendeleo kwa wananchi wote")
    langs = {s.language for s in result.linguistic_spans()}
    assert "sw" in langs or result.dominant_language == "sw"
