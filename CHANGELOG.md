# Changelog

## [0.1.0] - 2026-06-13

Initial release.

### Detection capabilities
- Span-level language detection: each span of a mixed-language input is labelled independently, with character offsets into the original string
- 75 languages via [lingua](https://github.com/pemistahl/lingua-py), plus dedicated lexicons for Roman Urdu (`ur-Latn`), Tagalog (`tl`), Swahili (`sw`), French (`fr`), Spanish (`es`), Portuguese (`pt`), Italian (`it`), German (`de`), and Turkish (`tr`)
- Character n-gram models for Roman Urdu, Tagalog, and Swahili, enabling detection of content words not in the lexicon. Models are pre-bundled and loaded at import time
- Non-Latin scripts identified directly from Unicode block ranges (Arabic, Devanagari, CJK, Cyrillic, Thai, Hebrew, Georgian, Korean, Japanese, Bengali, and more) without calling the language model

### Robustness features
- URLs, @mentions, #hashtags, emoji, and numbers are extracted before detection and reinserted in the output, so they never corrupt the language signal
- Mid-sentence capitalised tokens inconsistent with surrounding context are tagged `ne` (named entity / proper noun) rather than assigned a spurious language
- Near-identical language pairs (Spanish/Portuguese, Norwegian/Danish/Swedish, Indonesian/Malay, Croatian/Serbian) are returned as `und` with `ambiguous_candidates` populated, rather than a confident wrong answer
- Context correction pass resolves undetermined tokens by majority vote over a +/- 3 token window, and absorbs single-token language islands into surrounding context

### API
- `analyze(text, *, languages, granularity, min_confidence, low_accuracy_mode, normalize, custom_lexicon)`
- `PolyStringResult`: `.spans`, `.languages`, `.dominant_language`, `.is_mixed`, `.confidence`, `.to_dict()`, `.to_dataframe()`, `.highlight()`, `.linguistic_spans()`
- `Span`: `text`, `language`, `token_type`, `confidence`, `start`, `end`, `is_foreign`, `ambiguous_candidates`
- `supported_languages()` returning the full list of detectable ISO codes
- `PolyStringError`, `UnsupportedLanguageError`, `InputTooShortError`
- Optional pandas integration: `pip install polystring[pandas]`
