
from polystring._pipeline.stage1_preprocess import RawToken
from polystring._pipeline.stage2_script import run


def _make_token(text: str, start: int = 0) -> RawToken:
    return RawToken(text=text, start=start, end=start + len(text))


def test_devanagari_classified():
    tokens = [_make_token("नमस्ते")]
    classified, latin = run(tokens)
    assert len(classified) == 1
    assert classified[0].language == "hi"
    assert latin == []


def test_cyrillic_classified():
    tokens = [_make_token("Привет")]
    classified, latin = run(tokens)
    assert len(classified) == 1
    assert classified[0].language == "ru"


def test_latin_passes_through():
    tokens = [_make_token("hello")]
    classified, latin = run(tokens)
    assert classified == []
    assert len(latin) == 1


def test_mixed_script_tokens_split():
    tokens = [_make_token("hello", 0), _make_token("नमस्ते", 6)]
    classified, latin = run(tokens)
    assert len(classified) == 1
    assert len(latin) == 1


def test_arabic_classified():
    tokens = [_make_token("مرحبا")]
    classified, latin = run(tokens)
    assert len(classified) == 1
    assert classified[0].language == "ar"
