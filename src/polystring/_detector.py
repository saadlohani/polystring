from __future__ import annotations

import functools
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lingua import LanguageDetector

_detector: LanguageDetector | None = None
_detector_languages: frozenset[str] | None = None


def _build_detector(languages: list[str] | None = None) -> LanguageDetector:
    from lingua import Language, LanguageDetectorBuilder

    if languages:
        from lingua import IsoCode639_1
        lang_objs = []
        for code in languages:
            try:
                iso = IsoCode639_1[code.upper()]
                lang = Language.from_iso_code_639_1(iso)
                lang_objs.append(lang)
            except (KeyError, Exception):
                pass
        if not lang_objs:
            builder = LanguageDetectorBuilder.from_all_languages()
        else:
            builder = LanguageDetectorBuilder.from_languages(*lang_objs)
    else:
        builder = LanguageDetectorBuilder.from_all_languages()

    return builder.with_preloaded_language_models().build()


def get_detector(languages: list[str] | None = None) -> LanguageDetector:
    global _detector, _detector_languages

    key = frozenset(languages) if languages else None
    if _detector is None or _detector_languages != key:
        _detector = _build_detector(languages)
        _detector_languages = key
        lingua_top2.cache_clear()
    return _detector


@functools.lru_cache(maxsize=4096)
def lingua_top2(
    text: str, languages_key: frozenset[str] | None = None
) -> list[tuple[str, float]]:
    detector = get_detector(list(languages_key) if languages_key else None)
    confidence_values = detector.compute_language_confidence_values(text)
    out: list[tuple[str, float]] = []
    for cv in confidence_values[:2]:
        code = cv.language.iso_code_639_1.name.lower()
        out.append((code, cv.value))
    return out


def lingua_confidence_for(text: str, lang_code: str) -> float:
    """Return lingua's confidence that `text` is in `lang_code`."""
    from lingua import IsoCode639_1, Language

    detector = get_detector()
    try:
        iso = IsoCode639_1[lang_code.upper()]
        lang = Language.from_iso_code_639_1(iso)
    except (KeyError, Exception):
        return 0.0

    for cv in detector.compute_language_confidence_values(text):
        if cv.language == lang:
            return cv.value
    return 0.0
