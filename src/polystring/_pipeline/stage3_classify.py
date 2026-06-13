"""
Stage 3: classify each Latin-script token with a language label.

This module has two modes:

  MODEL mode (default, accurate):
    Calls _lid_model.predict(), which runs the fine-tuned XLM-RoBERTa
    ONNX model. The model reads the entire sentence bidirectionally, so
    every token's label reflects full sentence context. No hand-written
    rules needed.

  FALLBACK mode (legacy, used only if model unavailable):
    The original lexicon + lingua + heuristics pipeline. Kept for
    environments where the model cannot be downloaded. Accuracy is
    significantly lower for code-switched sentences.
"""

from __future__ import annotations

from polystring._models import Token
from polystring._pipeline.stage1_preprocess import RawToken

_NEAR_IDENTICAL_PAIRS: frozenset[frozenset[str]] = frozenset({
    frozenset({"es", "pt"}), frozenset({"es", "it"}), frozenset({"pt", "it"}),
    frozenset({"nb", "da"}), frozenset({"nb", "sv"}), frozenset({"da", "sv"}),
    frozenset({"id", "ms"}), frozenset({"hr", "sr"}), frozenset({"bs", "hr"}),
})


def _is_near_identical(lang1: str, lang2: str) -> bool:
    return frozenset({lang1, lang2}) in _NEAR_IDENTICAL_PAIRS


# Label values the model may return that map to our Token.language field.
# The model can return ISO 639-1 codes plus these special values.
_MODEL_OTHER = "OTHER"
_MODEL_NE = "NE"
_MODEL_MIX = "MIX"
_MODEL_AMB = "AMB"

# Map model's special labels → Token.language values
_SPECIAL_MAP: dict[str, str] = {
    _MODEL_OTHER: "und",
    _MODEL_NE: "ne",
    _MODEL_MIX: "und",    # mixed morphology → treat as undetermined for now
    _MODEL_AMB: "und",
}

# Confidence assigned to model predictions.
# The model outputs probabilities; we use the max softmax probability.
# For now we use a fixed value since the ONNX path doesn't expose probs
# in a convenient form. A future improvement: return actual softmax probs.
_MODEL_CONFIDENCE = 0.85


def run(
    latin_tokens: list[RawToken],
    languages_hint: frozenset[str] | None = None,
    min_confidence: float = 0.70,
    use_model: bool = True,
) -> list[Token]:
    """
    Classify each token in latin_tokens.

    Parameters
    ----------
    latin_tokens:
        Tokens from stage2 that use Latin script.
    languages_hint:
        If provided, restrict detection to these language codes.
        Passed to the fallback path; the model ignores hints (it produces
        accurate labels from context alone).
    min_confidence:
        Minimum confidence threshold for non-model path.
    use_model:
        If False, use the legacy fallback pipeline. Primarily for testing.
    """
    if not latin_tokens:
        return []

    if use_model:
        try:
            return _run_model(latin_tokens)
        except Exception as exc:
            import warnings
            warnings.warn(
                f"[polystring] Model inference failed ({exc}); "
                "falling back to legacy pipeline. "
                "Run 'pip install optimum[onnxruntime]' and ensure the model "
                "has been downloaded.",
                RuntimeWarning,
                stacklevel=3,
            )

    return _run_fallback(latin_tokens, languages_hint, min_confidence)


# ---------------------------------------------------------------------------
# Model path
# ---------------------------------------------------------------------------

def _run_model(latin_tokens: list[RawToken]) -> list[Token]:
    from polystring._lid_model import predict

    words = [rt.text for rt in latin_tokens]
    raw_labels = predict(words)

    result: list[Token] = []
    for rt, raw_label in zip(latin_tokens, raw_labels):
        lang = _SPECIAL_MAP.get(raw_label, raw_label)
        token_type = "text"
        conf = _MODEL_CONFIDENCE if lang not in ("und", "ne") else 0.0

        if lang == "ne":
            token_type = "ne"

        # The model was trained on LinCE which labels Roman-script Hindi/Urdu
        # as "hi". Since latin_tokens are already confirmed Latin-script,
        # remap "hi" → "ur-Latn" (Roman Urdu/Hinglish convention).
        if lang == "hi":
            lang = "ur-Latn"

        result.append(Token(
            text=rt.text,
            language=lang,
            token_type=token_type,
            confidence=conf,
            start=rt.start,
            end=rt.end,
        ))

    return result


# ---------------------------------------------------------------------------
# Legacy fallback path (kept for environments without the model)
# ---------------------------------------------------------------------------

# Kept here so the fallback still works if imported
_EN_STOPWORDS: frozenset[str] = frozenset({
    "the", "a", "an", "and", "but", "or", "for", "of", "in", "on", "at",
    "to", "by", "with", "from", "that", "this", "it", "is", "was", "are",
    "be", "been", "have", "has", "had", "do", "did", "will", "would",
    "could", "should", "may", "might", "not", "no", "so", "as", "up",
    "if", "my", "your", "his", "her", "our", "their", "its",
    "you", "he", "she", "we", "they", "i", "me", "him", "us", "them",
    "what", "which", "who", "how", "when", "where", "why",
    "very", "just", "also", "too", "more", "most", "than", "then",
    "there", "here", "out", "about", "into", "after", "before",
})


def _run_fallback(
    latin_tokens: list[RawToken],
    languages_hint: frozenset[str] | None,
    min_confidence: float,
) -> list[Token]:
    from polystring._detector import lingua_top2
    from polystring._ngram import NGRAM_LANGUAGES
    from polystring._ngram import score as ngram_score
    from polystring.lexicons import lexicon_lookup

    _CONFIDENCE_GAP = 0.15
    _WINDOW = 4
    _LINGUA_SKIP = NGRAM_LANGUAGES

    def _window_text(tokens: list[RawToken], idx: int) -> str:
        half = _WINDOW // 2
        start = max(0, idx - half)
        end = min(len(tokens), idx + half + 1)
        return " ".join(t.text for t in tokens[start:end])

    if languages_hint is not None:
        ngram_candidates: frozenset[str] | None = languages_hint & NGRAM_LANGUAGES
        if not ngram_candidates:
            ngram_candidates = None
    else:
        ngram_candidates = None

    result: list[Token] = []
    for idx, rt in enumerate(latin_tokens):
        lex = lexicon_lookup(rt.text)
        if lex is not None:
            lang, conf = lex
            if lang == "amb":
                result.append(Token(
                    text=rt.text, language="amb", token_type="text",
                    confidence=0.0, start=rt.start, end=rt.end,
                    ambiguous_candidates=[],
                ))
                continue
            tok = Token(
                text=rt.text, language=lang, token_type="text",
                confidence=conf, start=rt.start, end=rt.end,
            )
            if rt.is_ne_candidate and lang not in ("und", "amb"):
                tok.token_type = "ne-candidate"
            result.append(tok)
            continue

        ng = ngram_score(rt.text, ngram_candidates)
        if ng is not None:
            lang, conf = ng
            if conf >= min_confidence:
                tok = Token(
                    text=rt.text, language=lang, token_type="text",
                    confidence=conf, start=rt.start, end=rt.end,
                )
                if rt.is_ne_candidate and lang not in ("und", "amb"):
                    tok.token_type = "ne-candidate"
                result.append(tok)
                continue

        skip_lingua = (
            languages_hint is not None and languages_hint.issubset(_LINGUA_SKIP)
        )
        if skip_lingua:
            result.append(Token(
                text=rt.text, language="und", token_type="text",
                confidence=0.0, start=rt.start, end=rt.end,
            ))
            continue

        window = _window_text(latin_tokens, idx)
        top2 = lingua_top2(window, languages_hint)

        if top2 and rt.text.lower() in _EN_STOPWORDS:
            if top2[0][0] in _LINGUA_SKIP:
                result.append(Token(
                    text=rt.text, language="und", token_type="text",
                    confidence=0.0, start=rt.start, end=rt.end,
                ))
                continue

        lang, conf = (top2[0][0], top2[0][1]) if top2 else ("und", 0.0)

        if len(top2) >= 2:
            l1, c1 = top2[0]
            l2, c2 = top2[1]
            if _is_near_identical(l1, l2) and (c1 - c2) < _CONFIDENCE_GAP:
                result.append(Token(
                    text=rt.text, language="und", token_type="text",
                    confidence=0.0, start=rt.start, end=rt.end,
                    ambiguous_candidates=[l1, l2],
                ))
                continue

        if conf < min_confidence or lang == "und":
            result.append(Token(
                text=rt.text, language="und", token_type="text",
                confidence=conf, start=rt.start, end=rt.end,
            ))
            continue

        tok = Token(
            text=rt.text, language=lang, token_type="text",
            confidence=conf, start=rt.start, end=rt.end,
        )
        if rt.is_ne_candidate and lang not in ("und", "amb"):
            tok.token_type = "ne-candidate"
        result.append(tok)

    return result
