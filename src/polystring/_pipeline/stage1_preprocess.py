from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass

import regex as _regex

_SPECIAL_PATTERNS: list[tuple[str, re.Pattern]] = [
    ("url",     re.compile(r"https?://\S+|www\.\S+")),
    ("mention", re.compile(r"@\w+")),
    ("hashtag", re.compile(r"#\w+")),
    ("emoji",   _regex.compile(
        "[\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "\U00002702-\U000027B0"
        "\U0001F900-\U0001F9FF"
        "☀-⛿"
        "✀-➿]+"
    )),
    ("num",     re.compile(r"\b\d+[a-zA-Z]*\b|\b[a-zA-Z]*\d+\b")),
]


@dataclass
class SpecialToken:
    text: str
    token_type: str   # url | mention | hashtag | emoji | num
    start: int
    end: int
    hashtag_lang: str | None = None
    hashtag_confidence: float = 0.0


@dataclass
class RawToken:
    text: str
    start: int
    end: int
    is_ne_candidate: bool = False


@dataclass
class Stage1Result:
    linguistic_tokens: list[RawToken]
    special_tokens: list[SpecialToken]
    normalized_text: str    # NFC-normalized original (offsets valid against this)


def _nfc(text: str) -> str:
    return unicodedata.normalize("NFC", text)


def _extract_special_tokens(text: str) -> tuple[list[SpecialToken], str]:
    """Extract special tokens and replace them with whitespace-width placeholders.

    Returns (special_tokens, masked_text) where masked_text has the same byte
    offsets but non-linguistic tokens replaced with spaces so downstream
    tokenisation still splits correctly.
    """
    specials: list[SpecialToken] = []
    chars = list(text)

    for tok_type, pattern in _SPECIAL_PATTERNS:
        for m in pattern.finditer(text):
            already = any(s.start <= m.start() < s.end for s in specials)
            if already:
                continue
            specials.append(SpecialToken(
                text=m.group(),
                token_type=tok_type,
                start=m.start(),
                end=m.end(),
            ))
            for i in range(m.start(), m.end()):
                chars[i] = " "

    specials.sort(key=lambda s: s.start)
    masked = "".join(chars)
    return specials, masked


def _tokenize(masked_text: str) -> list[tuple[str, int, int]]:
    """Split masked text into (token, start, end) by whitespace and punctuation."""
    tokens: list[tuple[str, int, int]] = []
    for m in re.finditer(r"\S+", masked_text):
        token_text = m.group()
        stripped = token_text.strip(".,!?;:\"'()[]{}")
        if not stripped:
            continue
        offset = token_text.index(stripped[0]) if stripped else 0
        end = m.start() + offset + len(stripped)
        tokens.append((stripped, m.start() + offset, end))
    return tokens


def _is_ne_candidate(token: str, idx: int, tokens: list[tuple[str, int, int]]) -> bool:
    """True if a mid-sentence capitalised token that may be a named entity."""
    if idx == 0:
        return False
    if not token[0].isupper():
        return False
    if idx > 0:
        prev = tokens[idx - 1][0]
        if prev.endswith((".", "!", "?")):
            return False
    return True


def run(
    text: str,
    normalize: bool = True,
) -> Stage1Result:
    """Stage 1: extract special tokens, NFC normalise, tokenise, tag NE candidates."""
    normalized = _nfc(text) if normalize else text
    specials, masked = _extract_special_tokens(normalized)

    raw_tokens_raw = _tokenize(masked)
    linguistic_tokens: list[RawToken] = []
    for idx, (tok, start, end) in enumerate(raw_tokens_raw):
        if not tok.strip():
            continue
        is_ne = _is_ne_candidate(tok, idx, raw_tokens_raw)
        linguistic_tokens.append(
            RawToken(text=tok, start=start, end=end, is_ne_candidate=is_ne)
        )

    return Stage1Result(
        linguistic_tokens=linguistic_tokens,
        special_tokens=specials,
        normalized_text=normalized,
    )
