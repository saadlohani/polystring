from __future__ import annotations

from typing import Literal

from polystring._exceptions import InputTooShortError, UnsupportedLanguageError
from polystring._models import PolyStringResult
from polystring._pipeline import (
    stage1_preprocess,
    stage2_script,
    stage3_classify,
    stage4_context,
    stage5_merge,
)
from polystring.lexicons import add_custom_lexicon

# Languages supported by lingua's ISO 639-1 codes (subset used for validation)
# We rely on lingua raising its own error if a code is truly unknown;
# this set is used only for fast pre-validation of the hint list.
_LINGUA_SUPPORTED: frozenset[str] = frozenset({
    "af", "sq", "ar", "hy", "az", "eu", "be", "bn", "bs", "bg", "ca", "zh",
    "hr", "cs", "da", "nl", "en", "eo", "et", "fi", "fr", "lg", "ka", "de",
    "el", "gu", "he", "hi", "hu", "is", "id", "ga", "it", "ja", "kn", "kk",
    "ko", "la", "lv", "lt", "mk", "ms", "mi", "mr", "mn", "ne", "nb", "nn",
    "fa", "pl", "pt", "pa", "ro", "ru", "sr", "sn", "sk", "sl", "so", "st",
    "es", "sw", "sv", "tl", "ta", "te", "th", "ts", "tn", "tr", "uk", "ur",
    "vi", "cy", "xh", "yo", "zu",
})


def analyze(
    text: str,
    *,
    languages: list[str] | None = None,
    granularity: Literal["span", "token"] = "span",
    min_confidence: float = 0.70,
    low_accuracy_mode: bool = False,
    normalize: bool = True,
    custom_lexicon: dict[str, list[str]] | None = None,
) -> PolyStringResult:
    """Detect languages of each span in mixed-language text.

    Parameters
    ----------
    text:
        Input text to analyse.
    languages:
        Restrict detection to these ISO 639-1 codes. Speeds up detection and
        reduces false positives on known language sets.
    granularity:
        "span" (default) merges adjacent same-language tokens into spans.
        "token" also populates result.tokens with per-token data.
    min_confidence:
        Tokens below this threshold are tagged "und". Default 0.70.
    low_accuracy_mode:
        Skip the lingua model entirely; use only lexicons and script detection.
        Much faster but lower recall.
    normalize:
        Run NFC normalisation before analysis. Set False to skip.
    custom_lexicon:
        Additional {lang_code: [word, ...]} entries merged into the lexicons
        before analysis.
    """
    if not isinstance(text, str):
        raise TypeError(f"text must be str, got {type(text).__name__}")

    if languages:
        for code in languages:
            if code not in _LINGUA_SUPPORTED:
                raise UnsupportedLanguageError(code)

    if custom_lexicon:
        add_custom_lexicon(custom_lexicon)

    languages_key = frozenset(languages) if languages else None

    stage1 = stage1_preprocess.run(
        text,
        normalize=normalize,
    )

    if len(stage1.linguistic_tokens) < 2:
        raise InputTooShortError(
            "Input has fewer than 2 tokens after special token removal. "
            "Cannot perform reliable language detection."
        )

    script_tokens, latin_tokens = stage2_script.run(stage1.linguistic_tokens)

    if low_accuracy_mode:
        from polystring._models import Token
        from polystring.lexicons import lexicon_lookup
        latin_classified: list[Token] = []
        for rt in latin_tokens:
            lex = lexicon_lookup(rt.text)
            if lex:
                lang, conf = lex
                latin_classified.append(Token(
                    text=rt.text,
                    language=lang if lang != "amb" else "und",
                    token_type="text",
                    confidence=conf if lang != "amb" else 0.0,
                    start=rt.start,
                    end=rt.end,
                ))
            else:
                latin_classified.append(Token(
                    text=rt.text,
                    language="und",
                    token_type="text",
                    confidence=0.0,
                    start=rt.start,
                    end=rt.end,
                ))
    else:
        latin_classified = stage3_classify.run(
            latin_tokens,
            languages_hint=languages_key,
            min_confidence=min_confidence,
        )

    all_tokens = sorted(
        script_tokens + latin_classified,
        key=lambda t: t.start,
    )

    all_tokens = stage4_context.run(all_tokens)

    return stage5_merge.run(
        all_tokens,
        stage1.special_tokens,
        stage1.normalized_text,
        granularity=granularity,
    )
