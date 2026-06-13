from __future__ import annotations

from collections import Counter

from polystring._models import Token

_CONTEXT_WINDOW = 3
_UND_MAX_CONFIDENCE = 0.75

_NON_LINGUISTIC = {"url", "mention", "hashtag", "emoji", "num"}


def _confirmed_lang(tok: Token) -> str | None:
    """Return the token's language if it is a definite linguistic assignment."""
    if tok.token_type in _NON_LINGUISTIC:
        return None
    if tok.language in ("und", "amb", "ne"):
        return None
    return tok.language


def _context_majority(tokens: list[Token], idx: int) -> str | None:
    """Return the majority confirmed language in a +-CONTEXT_WINDOW radius."""
    start = max(0, idx - _CONTEXT_WINDOW)
    end = min(len(tokens), idx + _CONTEXT_WINDOW + 1)
    langs: list[str] = []
    for i in range(start, end):
        if i == idx:
            continue
        lang = _confirmed_lang(tokens[i])
        if lang:
            langs.append(lang)
    if not langs:
        return None
    counts = Counter(langs)
    top = counts.most_common(1)[0]
    return top[0]


def run(tokens: list[Token]) -> list[Token]:
    """Stage 4: context-driven correction pass. Mutates tokens in-place."""

    # 4a. "und" inherits from confident neighbours
    for idx, tok in enumerate(tokens):
        if tok.language == "und" and not tok.ambiguous_candidates:
            majority = _context_majority(tokens, idx)
            if majority:
                tok.language = majority
                tok.confidence = min(_UND_MAX_CONFIDENCE, tok.confidence or _UND_MAX_CONFIDENCE)

    # 4b. Single-token language islands absorbed (skip NE candidates — handled in 4e)
    for idx, tok in enumerate(tokens):
        if tok.token_type in _NON_LINGUISTIC or tok.token_type == "ne-candidate":
            continue
        lang = _confirmed_lang(tok)
        if lang is None:
            continue
        left = _confirmed_lang(tokens[idx - 1]) if idx > 0 else None
        right = _confirmed_lang(tokens[idx + 1]) if idx < len(tokens) - 1 else None
        if left and right and left == right and left != lang:
            tok.language = left
            tok.confidence = min(_UND_MAX_CONFIDENCE, tok.confidence)

    # 4c. Near-identical pair resolution via sentence-level prior
    from polystring._pipeline.stage3_classify import _is_near_identical
    sentence_langs = [_confirmed_lang(t) for t in tokens if _confirmed_lang(t)]
    sentence_prior: str | None = None
    if sentence_langs:
        sentence_prior = Counter(sentence_langs).most_common(1)[0][0]

    for tok in tokens:
        if tok.language == "und" and len(tok.ambiguous_candidates) == 2:
            l1, l2 = tok.ambiguous_candidates
            if _is_near_identical(l1, l2) and sentence_prior in (l1, l2):
                tok.language = sentence_prior  # type: ignore[assignment]
                tok.confidence = _UND_MAX_CONFIDENCE
                tok.ambiguous_candidates = []

    # 4d. "amb" conflict word resolution
    for idx, tok in enumerate(tokens):
        if tok.language != "amb":
            continue
        majority = _context_majority(tokens, idx)
        if majority:
            tok.language = majority
            tok.confidence = _UND_MAX_CONFIDENCE
        else:
            tok.language = "und"

    # 4e. NE candidate resolution
    for idx, tok in enumerate(tokens):
        if tok.token_type != "ne-candidate":
            continue
        majority = _context_majority(tokens, idx)
        if majority and majority != tok.language:
            # Lingua's assignment conflicts with surrounding context -> proper noun
            tok.language = "ne"
            tok.token_type = "ne"
            tok.confidence = 0.0
        else:
            # Consistent with context — keep as text token
            tok.token_type = "text"

    # 4f. Remaining "und" kept as-is (honest output)

    return tokens
