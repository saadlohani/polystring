
from polystring._models import Token
from polystring._pipeline.stage4_context import run


def _tok(text: str, lang: str, conf: float = 0.85, token_type: str = "text") -> Token:
    return Token(text=text, language=lang, token_type=token_type,
                 confidence=conf, start=0, end=len(text))


def test_und_inherits_from_neighbours():
    tokens = [
        _tok("bugun", "tr"),
        _tok("hava", "und", conf=0.0),
        _tok("guzel", "tr"),
    ]
    result = run(tokens)
    assert result[1].language == "tr"


def test_island_absorbed():
    tokens = [
        _tok("bugun", "tr"),
        _tok("the", "en"),
        _tok("guzel", "tr"),
    ]
    result = run(tokens)
    assert result[1].language == "tr"


def test_amb_resolved_by_context():
    tokens = [
        _tok("yaar", "ur-Latn"),
        _tok("se", "amb", conf=0.0),
        _tok("hai", "ur-Latn"),
    ]
    result = run(tokens)
    assert result[1].language == "ur-Latn"


def test_ne_candidate_inconsistent_with_context():
    tokens = [
        _tok("yaar", "ur-Latn"),
        _tok("Netflix", "en", token_type="ne-candidate"),
        _tok("hai", "ur-Latn"),
    ]
    result = run(tokens)
    assert result[1].language == "ne"
    assert result[1].token_type == "ne"


def test_ne_candidate_consistent_with_context():
    tokens = [
        _tok("hello", "en"),
        _tok("World", "en", token_type="ne-candidate"),
        _tok("today", "en"),
    ]
    result = run(tokens)
    # Consistent with context — stays as text
    assert result[1].token_type == "text"
