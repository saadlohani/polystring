"""Integration tests for the full analyze() pipeline."""
import json
import pathlib

import pytest

from polystring import analyze
from polystring._exceptions import InputTooShortError, UnsupportedLanguageError

FIXTURES = json.loads(
    (pathlib.Path(__file__).parent / "fixtures" / "mixed_text_samples.json").read_text(
        encoding="utf-8"
    )
)


def test_returns_result():
    result = analyze("hello world this is a test sentence")
    assert result is not None
    assert len(result.spans) > 0


def test_dominant_language_set():
    result = analyze("hello world this is a test sentence")
    assert result.dominant_language != ""


def test_is_mixed_false_for_single_language():
    result = analyze("hello world this is a simple english sentence")
    assert result.is_mixed is False


def test_mixed_detected():
    result = analyze("yaar aaj subah se kuch nahi khaya, ama gun cok guzel")
    assert result.is_mixed is True


def test_url_in_output():
    result = analyze("visit https://example.com for more info please")
    url_spans = [s for s in result.spans if s.token_type == "url"]
    assert len(url_spans) == 1
    assert "https://example.com" in url_spans[0].text


def test_mention_in_output():
    result = analyze("hello @user how are you doing today")
    mention_spans = [s for s in result.spans if s.token_type == "mention"]
    assert len(mention_spans) >= 1


def test_hashtag_in_output():
    result = analyze("great #WorldCup game today very exciting")
    hashtag_spans = [s for s in result.spans if s.token_type == "hashtag"]
    assert len(hashtag_spans) >= 1


def test_too_short_raises():
    with pytest.raises(InputTooShortError):
        analyze("hi")


def test_unsupported_language_raises():
    with pytest.raises(UnsupportedLanguageError):
        analyze("some text here", languages=["xx"])


def test_type_error_non_string():
    with pytest.raises(TypeError):
        analyze(12345)  # type: ignore[arg-type]


def test_granularity_token_populates_tokens():
    result = analyze("hello world this is english", granularity="token")
    assert result.tokens is not None
    assert len(result.tokens) > 0


def test_granularity_span_tokens_none():
    result = analyze("hello world this is english")
    assert result.tokens is None


def test_languages_hint():
    result = analyze("bugun hava cok guzel ama", languages=["tr", "en"])
    assert "tr" in result.languages


def test_custom_lexicon():
    result = analyze(
        "testword123unique hello world this is text",
        custom_lexicon={"de": ["testword123unique"]},
    )
    # The custom word should be recognized as German
    de_spans = [s for s in result.spans if s.language == "de"]
    assert len(de_spans) >= 1


def test_to_dict():
    result = analyze("hello world this is a simple sentence")
    d = result.to_dict()
    assert "spans" in d
    assert "dominant_language" in d
    assert "is_mixed" in d


def test_linguistic_spans_filter():
    result = analyze("visit https://example.com hello world sentence here")
    linguistic = result.linguistic_spans()
    assert all(s.token_type == "text" for s in linguistic)


def test_low_accuracy_mode():
    result = analyze("yaar aaj bahut mushkil hai kuch nahi", low_accuracy_mode=True)
    assert result is not None
    assert len(result.spans) > 0


def test_design_doc_example():
    result = analyze("yaar aaj subah se kuch nahi khaya, ama gun cok guzel")
    languages = result.languages
    assert "tr" in languages or "ur-Latn" in languages


def test_empty_string_raises():
    with pytest.raises(InputTooShortError):
        analyze("")


def test_only_spaces_raises():
    with pytest.raises(InputTooShortError):
        analyze("   ")


def test_only_url_raises():
    with pytest.raises(InputTooShortError):
        analyze("https://example.com")


def test_only_emoji_raises():
    with pytest.raises(InputTooShortError):
        analyze("😂😂😂")


def test_only_numbers_raises():
    with pytest.raises(InputTooShortError):
        analyze("12345")


def test_null_bytes_stripped():
    result = analyze("hello\x00world this is a sentence with words")
    assert result is not None
    assert len(result.spans) > 0


def test_only_punctuation_raises():
    with pytest.raises(InputTooShortError):
        analyze("... !! ??")


def test_repeated_words():
    result = analyze("hello hello hello hello hello hello")
    assert result is not None
    assert result.dominant_language != ""


def test_confidence_averaging_correct():
    result = analyze("hello world this is english text here nice")
    for span in result.spans:
        assert 0.0 <= span.confidence <= 1.0


def test_token_to_dict():
    result = analyze("hello world this is english", granularity="token")
    assert result.tokens is not None
    d = result.tokens[0].to_dict()
    assert "text" in d
    assert "language" in d
    assert "confidence" in d


def test_span_to_dict():
    result = analyze("hello world this is english text sentence")
    d = result.spans[0].to_dict()
    assert "text" in d
    assert "language" in d
    assert "is_foreign" in d
