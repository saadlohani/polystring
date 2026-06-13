from __future__ import annotations

from polystring._models import Token
from polystring._pipeline.stage1_preprocess import RawToken

# Unicode block -> language code (or comma-separated candidates)
# Ordered by frequency in social-media mixed text
_BLOCK_MAP: list[tuple[range, str]] = [
    # Perso-Arabic
    (range(0x0600, 0x06FF + 1), "ar"),   # will be refined later if needed
    (range(0x0750, 0x077F + 1), "ar"),
    (range(0xFB50, 0xFDFF + 1), "ar"),
    (range(0xFE70, 0xFEFF + 1), "ar"),
    # Devanagari
    (range(0x0900, 0x097F + 1), "hi"),
    # Bengali
    (range(0x0980, 0x09FF + 1), "bn"),
    # Gurmukhi (Punjabi)
    (range(0x0A00, 0x0A7F + 1), "pa"),
    # Gujarati
    (range(0x0A80, 0x0AFF + 1), "gu"),
    # Tamil
    (range(0x0B80, 0x0BFF + 1), "ta"),
    # Telugu
    (range(0x0C00, 0x0C7F + 1), "te"),
    # Kannada
    (range(0x0C80, 0x0CFF + 1), "kn"),
    # Malayalam
    (range(0x0D00, 0x0D7F + 1), "ml"),
    # Sinhala
    (range(0x0D80, 0x0DFF + 1), "si"),
    # Thai
    (range(0x0E00, 0x0E7F + 1), "th"),
    # Georgian
    (range(0x10A0, 0x10FF + 1), "ka"),
    # Hangul (Korean)
    (range(0xAC00, 0xD7AF + 1), "ko"),
    (range(0x1100, 0x11FF + 1), "ko"),
    # CJK Unified
    (range(0x4E00, 0x9FFF + 1), "zh"),
    (range(0x3400, 0x4DBF + 1), "zh"),
    (range(0x20000, 0x2A6DF + 1), "zh"),
    # Hiragana / Katakana -> Japanese
    (range(0x3040, 0x309F + 1), "ja"),
    (range(0x30A0, 0x30FF + 1), "ja"),
    # Cyrillic
    (range(0x0400, 0x04FF + 1), "ru"),
    (range(0x0500, 0x052F + 1), "ru"),
    # Greek
    (range(0x0370, 0x03FF + 1), "el"),
    # Hebrew
    (range(0x0590, 0x05FF + 1), "he"),
    # Armenian
    (range(0x0530, 0x058F + 1), "hy"),
    # Ethiopic
    (range(0x1200, 0x137F + 1), "am"),
]


def _script_of(char: str) -> str | None:
    """Return language hint if char is in a non-Latin, non-ASCII block."""
    cp = ord(char)
    for block, lang in _BLOCK_MAP:
        if cp in block:
            return lang
    return None


def _dominant_script(text: str) -> str | None:
    """Return the dominant non-Latin script language for a token, or None."""
    counts: dict[str, int] = {}
    for ch in text:
        lang = _script_of(ch)
        if lang:
            counts[lang] = counts.get(lang, 0) + 1
    if not counts:
        return None
    return max(counts, key=lambda k: counts[k])


def run(tokens: list[RawToken]) -> tuple[list[Token], list[RawToken]]:
    """Stage 2: classify non-Latin tokens immediately; pass Latin ones forward.

    Returns (classified_tokens, latin_tokens).
    Classified tokens have language set to the script-inferred code.
    """
    classified: list[Token] = []
    latin: list[RawToken] = []

    for rt in tokens:
        lang = _dominant_script(rt.text)
        if lang is not None:
            classified.append(Token(
                text=rt.text,
                language=lang,
                token_type="text",
                confidence=0.99,
                start=rt.start,
                end=rt.end,
            ))
        else:
            latin.append(rt)

    return classified, latin
