from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import pandas as pd


@dataclass
class Token:
    text: str
    language: str
    token_type: str
    confidence: float
    start: int
    end: int
    ambiguous_candidates: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "language": self.language,
            "token_type": self.token_type,
            "confidence": self.confidence,
            "start": self.start,
            "end": self.end,
            "ambiguous_candidates": self.ambiguous_candidates,
        }


@dataclass
class Span:
    text: str
    language: str
    token_type: str
    confidence: float
    start: int
    end: int
    is_foreign: bool = False
    ambiguous_candidates: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "language": self.language,
            "token_type": self.token_type,
            "confidence": self.confidence,
            "start": self.start,
            "end": self.end,
            "is_foreign": self.is_foreign,
            "ambiguous_candidates": self.ambiguous_candidates,
        }


@dataclass
class PolyStringResult:
    text: str
    spans: list[Span]
    tokens: list[Token] | None
    languages: set[str]
    dominant_language: str
    is_mixed: bool
    confidence: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "spans": [s.to_dict() for s in self.spans],
            "languages": list(self.languages),
            "dominant_language": self.dominant_language,
            "is_mixed": self.is_mixed,
            "confidence": self.confidence,
        }

    def to_dataframe(self) -> "pd.DataFrame":
        try:
            import pandas as pd
        except ImportError as e:
            raise ImportError(
                "pandas is required: pip install polystring[pandas]"
            ) from e
        return pd.DataFrame([s.to_dict() for s in self.spans])

    def highlight(self) -> str:
        # ANSI colour codes per language (cycles through a palette)
        _PALETTE = [
            "\033[91m", "\033[92m", "\033[93m", "\033[94m",
            "\033[95m", "\033[96m", "\033[97m",
        ]
        _RESET = "\033[0m"
        lang_colour: dict[str, str] = {}
        colour_idx = 0
        parts: list[str] = []
        for span in self.spans:
            if span.language not in lang_colour:
                lang_colour[span.language] = _PALETTE[colour_idx % len(_PALETTE)]
                colour_idx += 1
            parts.append(
                f"{lang_colour[span.language]}[{span.language}]{span.text}{_RESET}"
            )
        return " ".join(parts)

    def linguistic_spans(self) -> list[Span]:
        _NON_LINGUISTIC = {"url", "mention", "hashtag", "emoji", "num"}
        return [s for s in self.spans if s.token_type not in _NON_LINGUISTIC]
