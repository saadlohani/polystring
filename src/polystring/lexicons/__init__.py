from __future__ import annotations

from polystring.lexicons.french import FRENCH
from polystring.lexicons.german import GERMAN
from polystring.lexicons.italian import ITALIAN
from polystring.lexicons.portuguese import PORTUGUESE
from polystring.lexicons.roman_urdu import ROMAN_URDU
from polystring.lexicons.spanish import SPANISH
from polystring.lexicons.swahili import SWAHILI
from polystring.lexicons.tagalog import TAGALOG
from polystring.lexicons.turkish import TURKISH

# Words that are genuinely ambiguous across multiple lexicon languages.
# Matching a conflict word returns ("amb", 0.0), which stage 4 resolves by
# context instead of making a wrong early commitment.
#
# Rule: only list a word here if it appears in TWO OR MORE of the lexicons
# above AND no single language strongly dominates its usage. Words that belong
# clearly to one language should stay in that lexicon only.
CONFLICT_WORDS: frozenset[str] = frozenset({
    # English prepositions / conjunctions that bleed into Romance / other
    "to", "or", "are", "so", "no",
    # Cross-lexicon ambiguities — only words appearing in 2+ lexicons OR
    # genuinely ambiguous with English/other common tokens are listed here.
    "se",       # ES reflexive + UR postposition
    "din",      # TL particle + UR time word
    "bad",      # EN adjective + UR postposition
    "bed",      # EN noun
    "on",       # EN + various
    "na",       # TL particle + SW + UR + DE filler (4 languages)
    "ka",       # UR genitive + TL
    "ko",       # UR oblique + TL
    "lang",     # TL "only" + EN word
    "nah",      # EN filler + various
    "do",       # EN + UR verb
    "log",      # UR plural + EN word
    "ya",       # TR + UR + SW (3 lexicons)
    "me",       # ES/IT/PT/FR clitic (4 lexicons)
    "te",       # ES/IT/PT/FR clitic (4 lexicons)
    "tu",       # FR/ES/PT/IT (4 lexicons)
    "mi",       # ES/IT/PT pronoun (3 lexicons)
    "ma",       # IT conjunction + PT (2 lexicons)
    "que",      # ES/PT/FR interrogative / conjunction (3 lexicons)
    "como",     # ES/PT "how/as" (2 lexicons)
    "si",       # ES/IT/PT "if/yes" (3 lexicons)
    "su",       # ES/IT/PT possessive/pronoun (3 lexicons)
    "sua",      # PT/IT possessive (2 lexicons)
    "de",       # FR/ES/PT/IT preposition (4 lexicons)
    "le",       # FR/IT/ES clitic (3 lexicons)
    "les",      # FR article + ES (2 lexicons)
    "mal",      # ES/DE adjective/adverb (2 lexicons)
    "bien",     # FR/ES adverb (2 lexicons)
    "por",      # ES/PT preposition (2 lexicons)
    "da",       # IT/PT particle (2 lexicons)
    "mais",     # FR conjunction + PT "more" (2 lexicons)
    "so",       # DE/EN (DE lexicon + EN)
    "ja",       # DE "yes" + PT "already" (2 lexicons)
    "an",       # DE preposition + EN article
    "in",       # EN + IT/DE preposition
    "al",       # ES/IT contraction (2 lexicons)
    "also",     # DE "so" + EN "also"
    "con",      # ES/IT/PT preposition (3 lexicons)
    "un",       # FR/ES/IT/PT article (4 lexicons)
    "el",       # ES article (ambiguous in EN context)
    "es",       # ES verb "is" + ambiguous with EN
    "ni",       # IT/TL overlap (2 lexicons)
    "este",     # ES/PT demonstrative (2 lexicons)
    "esta",     # ES/PT demonstrative (2 lexicons)
    "dos",      # ES/PT (2 lexicons)
    "nos",      # FR/PT pronoun (2 lexicons)
    "la",       # FR/SW overlap (2 lexicons)
    "para",     # TL conjunction + ES/PT "for" (3 lexicons)
    "man",      # TL "naman" short form + EN word (TL + EN)
    "gut",      # DE + resembles EN "gut"
    "was",      # DE interrogative + EN past tense
    "bei",      # DE preposition
    "aus",      # DE preposition
})

# ISO 639-1 (or BCP-47 variant) code -> word set
LANGUAGE_LEXICONS: dict[str, set[str]] = {
    "ur-Latn": ROMAN_URDU,
    "tr":      TURKISH,
    "tl":      TAGALOG,
    "sw":      SWAHILI,
    "fr":      FRENCH,
    "es":      SPANISH,
    "pt":      PORTUGUESE,
    "it":      ITALIAN,
    "de":      GERMAN,
}


def lexicon_lookup(token: str) -> tuple[str, float] | None:
    """Return (language_code, confidence) or None if not found.

    Conflict words return ("amb", 0.0) so stage 4 can resolve by context.
    """
    t = token.lower().strip(".,!?;:\"'()[]{}")
    if not t:
        return None
    if t in CONFLICT_WORDS:
        return ("amb", 0.0)
    for lang, words in LANGUAGE_LEXICONS.items():
        if t in words:
            return (lang, 0.90)
    return None


def add_custom_lexicon(custom: dict[str, list[str]]) -> None:
    """Merge caller-supplied words into LANGUAGE_LEXICONS in-place."""
    for lang, words in custom.items():
        if lang in LANGUAGE_LEXICONS:
            LANGUAGE_LEXICONS[lang].update(words)
        else:
            LANGUAGE_LEXICONS[lang] = set(words)
