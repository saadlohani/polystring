"""polystring — span-level language detection for mixed-language text."""
from __future__ import annotations

from polystring._analyzer import analyze
from polystring._exceptions import InputTooShortError, PolyStringError, UnsupportedLanguageError
from polystring._models import PolyStringResult, Span, Token

__version__ = "0.1.0"
__all__ = [
    "__version__",
    "analyze",
    "supported_languages",
    "Span",
    "Token",
    "PolyStringResult",
    "PolyStringError",
    "UnsupportedLanguageError",
    "InputTooShortError",
]


def supported_languages() -> list[str]:
    """Return sorted list of ISO 639-1 codes supported for detection."""
    from polystring._analyzer import _LINGUA_SUPPORTED
    return sorted(_LINGUA_SUPPORTED)
