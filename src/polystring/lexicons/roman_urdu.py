ROMAN_URDU: set[str] = {
    # Copulas & auxiliaries
    "hai", "hain", "tha", "thi", "the", "hy",
    "hona", "hoon", "hoga", "hogi", "honge",
    # "ho" omitted: overlaps Tagalog lexicon
    "hua", "hui", "hue",

    # Negation
    "nahi", "nhi", "nahin", "naheen", "nai", "mat",
    # "na" omitted: in CONFLICT_WORDS

    # Question words
    "kya", "kia", "keeya", "kyun", "kyunke", "kyunki",
    "kahan", "kab", "kaun", "kitna", "kitni", "kitne",
    "kaisa", "kaisi", "kaise",

    # Conjunctions
    "aur", "aor", "lekin", "lkn", "magar", "phir", "phr",
    "bhi", "bi", "toh", "tou", "ab", "abhi", "agar", "jab", "tab",
    "jabke", "jaise", "taake", "warna", "balke", "halanke",

    # Pronouns
    "main", "mein", "mai", "hum", "ham", "tum", "ap", "aap",
    "woh", "wo", "unn", "unka", "unki", "unke",
    "mera", "meri", "mere", "tera", "teri", "tere",
    "uska", "uski", "uske", "humara", "humari", "humare",
    "tumhara", "tumhari", "tumhare", "apna", "apni", "apne",
    "mujhe", "tujhe", "usse", "hume", "humko", "tumhe", "tumko",
    "inhe", "unhe", "yeh", "inn", "unhone",
    "humein", "mujhko",

    # Demonstratives
    "yahan", "vahan", "wahan", "idhar", "udhar",
    "iss", "uss", "is", "us",
    # "un" omitted: overlaps French lexicon
    # "in" omitted: in CONFLICT_WORDS

    # Common verbs (infinitive & conjugated forms)
    "karo", "karna", "karta", "karti", "karte", "kiya", "kar",
    # "ki" omitted: overlaps Turkish lexicon
    "raha", "rahi", "rahe", "rehna", "rehta", "rehti", "rehte",
    "aana", "aata", "aati", "aate", "aaya", "aayi", "aaye", "aa",
    "jaana", "jaata", "jaati", "jaate", "gaya", "gayi", "gaye", "jao",
    "lena", "leta", "leti", "lete", "liya", "liye",
    # "le" omitted: overlaps French lexicon
    "dena", "deta", "deti", "dete", "diya", "diye",
    # "do" omitted: in CONFLICT_WORDS (EN + PT overlap)
    # "de" omitted: in CONFLICT_WORDS (FR/ES/PT/IT preposition overlap)
    "bolna", "bolta", "bolti", "bolte", "bola", "boli", "bolo",
    "sunna", "sunta", "sunti", "sunte", "suna", "suni", "suno",
    "dekhna", "dekhta", "dekhti", "dekhte", "dekha", "dekhi", "dekho",
    "padhna", "padhta", "padhti", "padhte", "padha", "padhi", "padho",
    "likhna", "likhta", "likhti", "likhte", "likha", "likhi",
    "khana", "khaana", "khata", "khati", "khate", "khaya", "khayi",
    "peena", "peeta", "peeti", "peete", "piya", "piyi",
    "sona", "sota", "soti", "sote", "soya", "soyi",
    "uthna", "uthta", "uthti", "uthte", "utha", "uthi", "utho",
    "baithna", "baitha", "baithi", "baitho",
    "chalna", "chalta", "chalti", "chalte", "chala", "chali", "chalo",
    "daurna", "daurta", "daurti", "daurte",
    "hasna", "hasta", "hasti", "haste", "hansa", "hansi",
    "rona", "rota", "roti", "rote", "roya", "royi",
    "samajh", "samjha", "samjhi", "samjho", "samajhna",
    "poochna", "poocha", "poocho",
    "batana", "batao", "bata", "bataya",
    "milna", "milta", "milti", "milte", "mila", "mili",
    "banana", "banata", "banati", "banate", "bana", "bani",
    "todna", "toda", "todi",
    "chhodna", "chhoda", "chhodi", "chhodo",
    "pakadna", "pakda", "pakdo",
    "chalana", "chalao",
    "bhoolna", "bhoola", "bhooli",
    "yaad", "yaadein",

    # Nouns — people & relationships
    "yaar", "yar", "bhai", "bhaiya", "behan", "amma", "ammi", "abba",
    "abbu", "dost", "ladki", "ladka", "aurat", "mard", "bachcha",
    "bacche", "bacchi", "beta", "beti", "baap", "maa", "dada", "dadi",
    "nana", "nani", "chacha", "chachi", "mama", "mami", "phupho",
    "insaan",
    # "log" omitted: in CONFLICT_WORDS

    # Nouns — time
    "aaj", "aj", "kal", "parso", "raat", "subah", "subha", "dopahar",
    "shaam", "waqt", "wakt", "hafte", "mahina", "saal",
    "zamana", "daur", "abhi", "pehle", "baad",
    # "din" omitted: in CONFLICT_WORDS

    # Nouns — place & direction
    "ghar", "daftar", "school", "jagah", "taraf", "darmiyan",
    "upar", "neeche", "andar", "paas", "door", "seedha", "ulta",
    "aage", "peeche", "daayen", "baayen",

    # Nouns — everyday life
    "kaam", "khatam", "cheez", "cheezon", "paise", "paisa", "khaana",
    "pani", "paani", "mausam", "baarish", "dhoop", "roshni",
    "awaaz", "baat", "baatein", "khabar", "khwaab", "sapna", "sapne",
    "umeed", "dua", "rishta", "maafi", "shukr", "tauba",
    "namaaz", "ibadat", "deen",

    # Nouns — emotions & states
    "dil", "pyaar", "mohabbat", "ishq", "nafrat", "khushi", "gham",
    "dard", "takleef", "aaraam", "neend", "thakan", "zindagi",
    "mushkil", "mushkilat", "mushkilein", "azaadi", "duniya",

    # Adjectives
    "acha", "accha", "thik", "theek", "bura", "sahi", "galat",
    "naya", "purana", "bara", "bada", "chota", "tez", "dheere",
    "garam", "thanda", "mehngi", "sasta", "mushkil", "aasaan",
    "thaka", "thaki", "akela", "akeli", "khush", "udaas",
    "majbooran", "zaroor", "zarur",

    # Adverbs & particles
    "bahut", "bohat", "bohot", "zyada", "ziada", "thoda", "thora",
    "kuch", "sab", "bilkul", "matlab", "ekdum", "haan",
    "han", "haa", "jaldi", "dheere", "phirse", "dobara",
    "sirf", "bas", "hi", "bhi",

    # Postpositions
    "mein", "pe", "ke", "tak", "liye", "saath", "bina", "jaise", "jaisa",
    # "ko" "ka" omitted: in CONFLICT_WORDS
    # "ki" omitted: overlaps Turkish lexicon
    # "par" "un" "le" omitted: overlap French lexicon

    # Hinglish social / filler words
    "arey", "arre", "oye", "arrey",
    "wali", "wale",
    # "wala" omitted: overlaps Tagalog lexicon
    # "ho" omitted: overlaps Tagalog lexicon
}
