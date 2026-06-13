# polystring

**Span-level language detection for mixed-language text.**

Most language detection libraries return a single label for the whole string. polystring returns a labelled span for _every part_ of the sentence, with character offsets, confidence scores, and special-token extraction baked in.

```python
from polystring import analyze

result = analyze("je suis tellement tired, this week has been rough")

for span in result.spans:
    print(f"[{span.language}] {span.text!r}")

# [fr] 'je suis tellement tired'
# [en] 'this week has been rough'
```

## Why span-level detection matters

| Tool           | What it returns for `"hola I love this city, en serio"`       |
| -------------- | ------------------------------------------------------------- |
| `langdetect`   | `"es"` (labels the whole string)                              |
| `lingua`       | `"es"` (labels the whole string)                              |
| `langid`       | `"es"` (labels the whole string)                              |
| **polystring** | `[es] "hola"` · `[en] "I love this city"` · `[es] "en serio"` |

Code-switching (mixing languages within a single sentence) is normal on social media, in diaspora communities, in customer support chats, and in any multilingual context. A single label for the whole input misses the structure entirely. polystring is built specifically for this problem.

## Installation

```bash
pip install polystring
```

Optional extras:

```bash
pip install polystring[pandas]     # enables result.to_dataframe()
```

---

## Examples

### Spanish / English (Spanglish)

```python
result = analyze("no puedo creer how good this restaurant is, en serio")

for span in result.spans:
    print(f"[{span.language}] {span.text!r}")

# [es] 'no puedo creer'
# [en] 'how good this restaurant is'
# [es] 'en serio'
```

### French / English

```python
result = analyze("je suis tellement tired lately, I need des vacances")

for span in result.spans:
    print(f"[{span.language}] {span.text!r}")

# [fr] 'je suis tellement tired lately'
# [en] 'I need'
# [fr] 'des vacances'
```

### Mixed with non-Latin scripts

```python
result = analyze("this is great هذا رائع جداً I am very impressed")

for span in result.spans:
    print(f"[{span.language}] {span.text!r}")

# [en] 'this is great'
# [ar] 'هذا رائع جداً'
# [en] 'I am very impressed'
```

## Working with results

```python
result = analyze("je suis tellement tired, this week has been rough")

result.dominant_language   # 'fr'
result.is_mixed            # True
result.languages           # {'fr', 'en'}
result.confidence          # 0.87  (mean confidence across linguistic spans)
```

### Serialise to dict

```python
result.to_dict()
# {
#   'text': 'je suis tellement tired, this week has been rough',
#   'spans': [{'text': 'je suis tellement tired', 'language': 'fr', ...}, ...],
#   'dominant_language': 'fr',
#   'is_mixed': True,
#   'confidence': 0.87,
#   ...
# }
```

### Serialise to DataFrame

```python
# pip install polystring[pandas]
df = result.to_dataframe()
#                      text language token_type  confidence  start  end  is_foreign
# 0  je suis tellement tired       fr       text        0.91      0   23       False
# 1  this week has been rough      en       text        0.84     25   49        True
```

### ANSI-coloured terminal output

```python
print(result.highlight())
# [fr]je suis tellement tired [en]this week has been rough
# (each language rendered in a distinct colour)
```

### Filter to linguistic spans only

```python
result.linguistic_spans()
# Returns spans with token_type == "text" only (no URLs, emoji, mentions, etc.)
```

## Span fields

| Field                  | Type        | Description                                                                                   |
| ---------------------- | ----------- | --------------------------------------------------------------------------------------------- |
| `text`                 | `str`       | Text as it appears in the input                                                               |
| `language`             | `str`       | ISO 639-1 code. `"ur-Latn"` for Roman Urdu, `"und"` for undetermined, `"ne"` for proper nouns |
| `token_type`           | `str`       | `"text"`, `"url"`, `"mention"`, `"hashtag"`, `"emoji"`, `"num"`, or `"ne"`                    |
| `confidence`           | `float`     | 0.0 to 1.0. Non-text tokens are always 0.0                                                    |
| `start` / `end`        | `int`       | Character offsets into the original string                                                    |
| `is_foreign`           | `bool`      | `True` if this span is not the dominant language                                              |
| `ambiguous_candidates` | `list[str]` | Populated when `language == "und"` due to a near-identical pair (e.g. `["es", "pt"]`)         |

## Language coverage

polystring detects **75 languages** via [lingua](https://github.com/pemistahl/lingua-py). Non-Latin scripts (Arabic, Devanagari, CJK, Cyrillic, Thai, Hebrew, Korean, and more) are identified directly from Unicode ranges, no model call needed.

Nine languages have dedicated lexicons on top of the model, which significantly improves accuracy on short spans and code-switched text: Roman Urdu / Hinglish, Spanish, Portuguese, Italian, German, Turkish, Tagalog, Swahili

```python
import polystring
print(polystring.supported_languages())  # full list of 75 ISO 639-1 codes
```

## Options

```python
analyze(
    text,
    languages=["es", "en"],      # restrict to known language set (faster, fewer false positives)
    granularity="token",          # "span" (default) or "token" to get per-word data
    min_confidence=0.70,          # tokens below this threshold become "und"
    low_accuracy_mode=False,      # lexicon + script detection only, no model (very fast)
    normalize=True,               # NFC normalisation
    custom_lexicon={"sw": ["mambo", "vipi"]},   # inject domain-specific words
)
```

### `granularity="token"` gives per-word data

```python
result = analyze("bonjour how are you doing", granularity="token")

for tok in result.tokens:
    print(f"[{tok.language}] {tok.text!r}  ({tok.confidence:.2f})")

# [fr] 'bonjour'  (0.92)
# [en] 'how'      (0.83)
# [en] 'are'      (0.81)
# [en] 'you'      (0.85)
# [en] 'doing'    (0.88)
```

## Contributing

```bash
git clone https://github.com/saadlohani/polystring
cd polystring
pip install -e ".[dev]"
pytest
```

## License

MIT
