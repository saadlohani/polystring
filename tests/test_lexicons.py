import pytest

from polystring.lexicons import CONFLICT_WORDS, LANGUAGE_LEXICONS, lexicon_lookup


def test_roman_urdu_unambiguous():
    result = lexicon_lookup("yaar")
    assert result == ("ur-Latn", 0.90)


def test_turkish_unambiguous():
    result = lexicon_lookup("merhaba")
    assert result == ("tr", 0.90)


def test_tagalog_unambiguous():
    result = lexicon_lookup("salamat")
    assert result == ("tl", 0.90)


def test_swahili_unambiguous():
    result = lexicon_lookup("asante")
    assert result == ("sw", 0.90)


def test_french_unambiguous():
    result = lexicon_lookup("bonjour")
    assert result == ("fr", 0.90)


def test_conflict_word():
    result = lexicon_lookup("se")
    assert result is not None
    assert result[0] == "amb"


def test_unknown_word():
    result = lexicon_lookup("helicopter")
    assert result is None


def test_case_insensitive():
    result = lexicon_lookup("YAAR")
    assert result == ("ur-Latn", 0.90)


def test_strip_punctuation():
    result = lexicon_lookup("yaar,")
    assert result == ("ur-Latn", 0.90)


def test_spanish_unambiguous():
    result = lexicon_lookup("gracias")
    assert result == ("es", 0.90)


def test_portuguese_unambiguous():
    result = lexicon_lookup("obrigado")
    assert result == ("pt", 0.90)


def test_italian_unambiguous():
    result = lexicon_lookup("ciao")
    assert result == ("it", 0.90)


def test_german_unambiguous():
    result = lexicon_lookup("danke")
    assert result == ("de", 0.90)


def test_conflict_words_not_in_lexicons():
    # No conflict word should silently match a language (would be wrong assignment)
    for word in CONFLICT_WORDS:
        for lang, words in LANGUAGE_LEXICONS.items():
            assert word not in words, f"{word!r} is both conflict and in {lang} lexicon"
