from __future__ import annotations

from collections import Counter
from typing import Literal

from polystring._models import PolyStringResult, Span, Token
from polystring._pipeline.stage1_preprocess import SpecialToken

_NON_LINGUISTIC = {"url", "mention", "hashtag", "emoji", "num"}


def _tokens_to_spans(tokens: list[Token]) -> list[Span]:
    if not tokens:
        return []

    spans: list[Span] = []
    cur = tokens[0]
    merged_text = cur.text
    merged_start = cur.start
    merged_end = cur.end
    conf_sum = cur.confidence
    conf_count = 1
    merged_cands = list(cur.ambiguous_candidates)

    for tok in tokens[1:]:
        same_lang = tok.language == cur.language
        same_type = tok.token_type == cur.token_type
        contiguous = tok.start <= merged_end + 1

        if same_lang and same_type and contiguous:
            merged_text = merged_text + " " + tok.text
            merged_end = tok.end
            conf_sum += tok.confidence
            conf_count += 1
        else:
            spans.append(Span(
                text=merged_text,
                language=cur.language,
                token_type=cur.token_type,
                confidence=conf_sum / conf_count,
                start=merged_start,
                end=merged_end,
                ambiguous_candidates=merged_cands,
            ))
            cur = tok
            merged_text = tok.text
            merged_start = tok.start
            merged_end = tok.end
            conf_sum = tok.confidence
            conf_count = 1
            merged_cands = list(tok.ambiguous_candidates)

    spans.append(Span(
        text=merged_text,
        language=cur.language,
        token_type=cur.token_type,
        confidence=conf_sum / conf_count,
        start=merged_start,
        end=merged_end,
        ambiguous_candidates=merged_cands,
    ))
    return spans


def _insert_special_tokens(spans: list[Span], specials: list[SpecialToken]) -> list[Span]:
    special_spans = [
        Span(
            text=st.text,
            language=st.token_type,
            token_type=st.token_type,
            confidence=0.0,
            start=st.start,
            end=st.end,
        )
        for st in specials
    ]
    all_spans = spans + special_spans
    all_spans.sort(key=lambda s: s.start)
    return all_spans


def _compute_dominant(spans: list[Span]) -> str:
    coverage: Counter[str] = Counter()
    for span in spans:
        if span.token_type in _NON_LINGUISTIC or span.language in ("und", "ne"):
            continue
        coverage[span.language] += span.end - span.start
    if not coverage:
        return "und"
    return coverage.most_common(1)[0][0]


def _mark_foreign(spans: list[Span], dominant: str) -> None:
    for span in spans:
        if span.token_type not in _NON_LINGUISTIC and span.language not in ("und", "ne"):
            span.is_foreign = span.language != dominant


def _overall_confidence(spans: list[Span]) -> float:
    linguistic = [s for s in spans if s.token_type == "text" and s.language not in ("und", "ne")]
    if not linguistic:
        return 0.0
    return sum(s.confidence for s in linguistic) / len(linguistic)


def run(
    tokens: list[Token],
    specials: list[SpecialToken],
    original_text: str,
    granularity: Literal["span", "token"] = "span",
) -> PolyStringResult:
    spans = _tokens_to_spans(tokens)
    spans = _insert_special_tokens(spans, specials)

    dominant = _compute_dominant(spans)
    _mark_foreign(spans, dominant)

    languages: set[str] = {
        s.language for s in spans
        if s.token_type == "text" and s.language not in ("und", "ne", "amb")
    }
    is_mixed = len(languages) > 1
    confidence = _overall_confidence(spans)

    return PolyStringResult(
        text=original_text,
        spans=spans,
        tokens=tokens if granularity == "token" else None,
        languages=languages,
        dominant_language=dominant,
        is_mixed=is_mixed,
        confidence=confidence,
    )
