from __future__ import annotations

from polystring._detector import lingua_top2
from polystring._models import Token
from polystring._ngram import NGRAM_LANGUAGES
from polystring._ngram import score as ngram_score
from polystring._pipeline.stage1_preprocess import RawToken
from polystring.lexicons import lexicon_lookup

NEAR_IDENTICAL_PAIRS: frozenset[frozenset[str]] = frozenset({
    frozenset({"es", "pt"}),
    frozenset({"es", "it"}),
    frozenset({"pt", "it"}),
    frozenset({"nb", "da"}),
    frozenset({"nb", "sv"}),
    frozenset({"da", "sv"}),
    frozenset({"id", "ms"}),
    frozenset({"hr", "sr"}),
    frozenset({"bs", "hr"}),
})

_CONFIDENCE_GAP = 0.15
_MIN_CONFIDENCE = 0.70
_WINDOW = 4

# Languages for which lingua adds noise rather than signal.  For these we use
# the n-gram model as primary classifier and skip lingua entirely.
_LINGUA_SKIP = NGRAM_LANGUAGES   # {"ur-Latn", "tl", "sw"}


def _window_text(tokens: list[RawToken], idx: int) -> str:
    half = _WINDOW // 2
    start = max(0, idx - half)
    end = min(len(tokens), idx + half + 1)
    return " ".join(t.text for t in tokens[start:end])


def _is_near_identical(lang1: str, lang2: str) -> bool:
    return frozenset({lang1, lang2}) in NEAR_IDENTICAL_PAIRS


def run(
    latin_tokens: list[RawToken],
    languages_hint: frozenset[str] | None = None,
    min_confidence: float = _MIN_CONFIDENCE,
) -> list[Token]:
    result: list[Token] = []

    # Determine which n-gram languages are in scope given the caller's hint.
    # If the caller restricted to e.g. ["es", "en"], n-gram languages not in
    # that set are excluded from scoring.
    if languages_hint is not None:
        ngram_candidates: frozenset[str] | None = languages_hint & NGRAM_LANGUAGES
        # If the hint contains no n-gram languages, pass None so ngram_score
        # knows to skip rather than returning wrong results.
        if not ngram_candidates:
            ngram_candidates = None
    else:
        ngram_candidates = None   # no restriction → scorer uses all loaded models

    for idx, rt in enumerate(latin_tokens):
        # ------------------------------------------------------------------
        # Step 1: lexicon lookup (fastest path, highest precision)
        # ------------------------------------------------------------------
        lex = lexicon_lookup(rt.text)
        if lex is not None:
            lang, conf = lex
            if lang == "amb":
                result.append(Token(
                    text=rt.text,
                    language="amb",
                    token_type="text",
                    confidence=0.0,
                    start=rt.start,
                    end=rt.end,
                    ambiguous_candidates=[],
                ))
                continue
            tok = Token(
                text=rt.text,
                language=lang,
                token_type="text",
                confidence=conf,
                start=rt.start,
                end=rt.end,
            )
            _maybe_mark_ne(tok, rt)
            result.append(tok)
            continue

        # ------------------------------------------------------------------
        # Step 2: n-gram model (covers ur-Latn, tl, sw)
        # ------------------------------------------------------------------
        ng = ngram_score(rt.text, ngram_candidates)
        if ng is not None:
            lang, conf = ng
            if conf >= min_confidence:
                tok = Token(
                    text=rt.text,
                    language=lang,
                    token_type="text",
                    confidence=conf,
                    start=rt.start,
                    end=rt.end,
                )
                _maybe_mark_ne(tok, rt)
                result.append(tok)
                continue

        # ------------------------------------------------------------------
        # Step 3: lingua (for all other Latin-script languages)
        # Skip lingua entirely for tokens whose only candidate n-gram
        # languages are in _LINGUA_SKIP — lingua will misclassify them.
        # ------------------------------------------------------------------
        skip_lingua = False
        if languages_hint is not None and languages_hint.issubset(_LINGUA_SKIP):
            skip_lingua = True

        if skip_lingua:
            result.append(Token(
                text=rt.text,
                language="und",
                token_type="text",
                confidence=0.0,
                start=rt.start,
                end=rt.end,
            ))
            continue

        window = _window_text(latin_tokens, idx)
        top2 = lingua_top2(window, languages_hint)
        lang, conf = (top2[0][0], top2[0][1]) if top2 else ("und", 0.0)

        if len(top2) >= 2:
            l1, c1 = top2[0]
            l2, c2 = top2[1]
            if _is_near_identical(l1, l2) and (c1 - c2) < _CONFIDENCE_GAP:
                result.append(Token(
                    text=rt.text,
                    language="und",
                    token_type="text",
                    confidence=0.0,
                    start=rt.start,
                    end=rt.end,
                    ambiguous_candidates=[l1, l2],
                ))
                continue

        if conf < min_confidence or lang == "und":
            result.append(Token(
                text=rt.text,
                language="und",
                token_type="text",
                confidence=conf,
                start=rt.start,
                end=rt.end,
            ))
            continue

        tok = Token(
            text=rt.text,
            language=lang,
            token_type="text",
            confidence=conf,
            start=rt.start,
            end=rt.end,
        )
        _maybe_mark_ne(tok, rt)
        result.append(tok)

    return result


def _maybe_mark_ne(tok: Token, rt: RawToken) -> None:
    if rt.is_ne_candidate and tok.language not in ("und", "amb"):
        tok.token_type = "ne-candidate"
