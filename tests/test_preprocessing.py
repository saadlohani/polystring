
from polystring._pipeline.stage1_preprocess import run


def test_extracts_url():
    result = run("visit https://example.com today")
    types = [st.token_type for st in result.special_tokens]
    assert "url" in types


def test_extracts_mention():
    result = run("hello @user how are you")
    types = [st.token_type for st in result.special_tokens]
    assert "mention" in types


def test_extracts_hashtag():
    result = run("great #WorldCup game")
    types = [st.token_type for st in result.special_tokens]
    assert "hashtag" in types


def test_url_not_in_linguistic_tokens():
    result = run("visit https://example.com today")
    texts = [t.text for t in result.linguistic_tokens]
    assert not any("http" in t for t in texts)


def test_ne_candidate_mid_sentence():
    result = run("I saw Netflix yesterday")
    ne_tokens = [t for t in result.linguistic_tokens if t.is_ne_candidate]
    assert any(t.text == "Netflix" for t in ne_tokens)


def test_first_token_not_ne_candidate():
    result = run("Netflix is great")
    first = result.linguistic_tokens[0]
    assert not first.is_ne_candidate


def test_nfc_normalisation():
    # cafe with combining accent vs precomposed
    text = "café"  # 'e' + combining acute
    result = run(text, normalize=True)
    assert result.normalized_text == "café"


def test_numbers_extracted():
    result = run("I have 42 apples and 7zip")
    types = [st.token_type for st in result.special_tokens]
    assert "num" in types
