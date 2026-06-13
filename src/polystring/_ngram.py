"""Character n-gram language scorer for low-resource romanised languages.

Loaded once at import time from pre-built JSON profiles in polystring/data/.
Used in stage 3 between lexicon lookup and lingua for languages where lingua
has insufficient training data (ur-Latn, tl, sw).

Architecture: discriminative hit-count scoring.

Each profile contains only *discriminative* n-grams: n-grams that appear
significantly more often in that language than in all competitor languages
(other target languages + English background), as determined at build time
by a log-prob margin threshold.

At inference time we count how many of a token's n-grams match each
language's discriminative profile.  The language with the most hits wins,
provided it leads the runner-up by at least _MIN_GAP_HITS and has at least
_MIN_HITS total.  Ties are broken by the average log-prob of matched n-grams.

This avoids the cross-contamination problem that affects plain LLR scoring:
because the profiles are pre-filtered to exclude n-grams shared across
ur-Latn/tl/sw, an Urdu word cannot "accidentally" accumulate Tagalog hits.
"""
from __future__ import annotations

import json
import math
import re
from pathlib import Path

_DATA_DIR = Path(__file__).parent / "data"

NGRAM_LANGUAGES: frozenset[str] = frozenset({"ur-Latn", "tl", "sw"})

# Scoring thresholds (tuned empirically on build corpora test words)
_MIN_HITS = 2           # winner must have at least this many discriminative n-gram hits
_MIN_GAP_HITS = 1       # winner must lead runner-up by at least this many hits
_MIN_TOKEN_LEN = 4      # tokens shorter than this are not scored (too noisy)

_CLEAN = re.compile(r"[^a-z'\-]")

_MODELS: dict[str, dict[str, dict[str, float]]] = {}
_NGRAM_SIZES: dict[str, list[int]] = {}
_LOADED = False


def _load() -> None:
    global _LOADED
    if _LOADED:
        return

    for lang in NGRAM_LANGUAGES:
        fname = _DATA_DIR / f"{lang.replace('-', '_')}_ngram.json"
        if not fname.exists():
            continue
        payload = json.loads(fname.read_text(encoding="utf-8"))
        _MODELS[lang] = payload["profile"]
        _NGRAM_SIZES[lang] = payload["ngram_sizes"]

    _LOADED = True


def _hit_score(cleaned: str, profile: dict[str, dict[str, float]], sizes: list[int]) -> tuple[int, float]:
    """Count discriminative n-gram hits and sum their log-probs.

    Returns (hit_count, avg_log_prob_of_hits) where avg is 0 when hit_count=0.
    """
    hit_count = 0
    lp_sum = 0.0

    for n in sizes:
        table = profile[str(n)]
        padded = f"{'_' * (n - 1)}{cleaned}{'_' * (n - 1)}"
        for i in range(len(padded) - n + 1):
            ng = padded[i:i + n]
            v = table.get(ng)
            if v is not None:
                hit_count += 1
                lp_sum += v

    avg_lp = lp_sum / hit_count if hit_count > 0 else 0.0
    return hit_count, avg_lp


def score(token: str, candidates: frozenset[str] | None = None) -> tuple[str, float] | None:
    """Score token using discriminative character n-gram hit counts.

    Each language's profile contains only n-grams exclusive to that language
    (built with a log-prob margin vs. all competitor languages + English).
    The winner is the language that matches the most of the token's n-grams.

    Parameters
    ----------
    token:
        Raw token text; cleaned internally.
    candidates:
        Restrict scoring to languages in this set that also have n-gram models.

    Returns
    -------
    (lang, confidence) with confidence ∈ [0.60, 0.95], or None if no model
    wins convincingly.
    """
    _load()

    if not _MODELS:
        return None

    cleaned = _CLEAN.sub("", token.lower()).strip("-'")
    if len(cleaned) < _MIN_TOKEN_LEN:
        return None

    langs_to_score = set(_MODELS.keys())
    if candidates is not None:
        langs_to_score &= candidates
    if not langs_to_score:
        return None

    results: list[tuple[int, float, str]] = []
    for lang in langs_to_score:
        hits, avg_lp = _hit_score(cleaned, _MODELS[lang], _NGRAM_SIZES[lang])
        results.append((hits, avg_lp, lang))

    # Sort: primary by hit count (desc), secondary by avg log-prob (desc)
    results.sort(key=lambda x: (x[0], x[1]), reverse=True)
    best_hits, best_avg, best_lang = results[0]

    if best_hits < _MIN_HITS:
        return None

    if len(results) > 1 and (best_hits - results[1][0]) < _MIN_GAP_HITS:
        return None

    # Map hit count to confidence: 2 hits → 0.65, 10+ hits → 0.90
    confidence = max(0.60, min(0.95, 0.60 + best_hits * 0.03))
    return best_lang, confidence


def available_languages() -> frozenset[str]:
    """Return languages for which a model file is present."""
    _load()
    return frozenset(_MODELS.keys())
