SWAHILI: set[str] = {
    # Core function words / agreement markers
    "wa", "kwa", "za",
    # "la" omitted: in CONFLICT_WORDS (FR/SW 2-lexicon overlap)
    # "ya" omitted: in CONFLICT_WORDS (ES/UR/TR overlap)
    # "na" omitted: in CONFLICT_WORDS (TL/UR/DE overlap)
    # "ni" omitted: in CONFLICT_WORDS (IT/TL/Slavic overlap)
    "katika", "kuwa",

    # Demonstratives
    "hii", "hizi", "hiyo", "hayo", "hao",
    "ile", "zile", "lile", "yule", "wale",
    "hapa", "huko", "hapo", "pale",

    # Pronouns
    "mimi", "wewe", "yeye", "sisi", "nyinyi", "wao",
    "mimi", "mwenyewe", "wenyewe",
    "yangu", "yako", "yake", "yetu", "yenu", "yao",
    "wangu", "wako", "wake", "wetu", "wenu", "wao",

    # Interrogatives
    "nini", "wapi", "lini", "jinsi", "kwa", "vipi", "ngapi",

    # Conjunctions
    "kama", "lakini", "ingawa", "ijapokuwa", "au",
    "pia", "ama", "bali", "wala",

    # Prepositions / postpositions
    "kabla", "baada", "juu", "chini", "mbele", "nyuma",
    "ndani", "nje", "karibu", "mbali", "pamoja",

    # Adverbs / time
    "sasa", "leo", "kesho", "jana", "juzi", "kesho",
    "bado", "tayari", "pia", "zaidi", "kidogo",
    "sana", "haraka", "polepole", "mara", "kila",
    "daima", "wakati",

    # Affirmation / negation
    "ndiyo", "ndio", "hapana", "sivyo",
    # "la" omitted: in CONFLICT_WORDS (FR/SW 2-lexicon overlap)
    "kweli", "kweli",

    # Subject / object prefixes (appear as standalone tokens in informal text)
    "ninataka", "unataka", "anataka", "tunataka", "mnataka", "wanataka",
    "ninajua", "unajua", "anajua", "hatujui",
    "ninaenda", "unaenda", "anaenda", "tunaenda",
    "ninapenda", "unapenda", "anapenda",
    "nilisema", "alisema", "walisema",
    "ninafanya", "unafanya", "anafanya",
    "nilikuwa", "ulikuwa", "alikuwa", "tulikuwa",
    "nitakwenda", "utakwenda", "atakwenda",
    "ninaweza", "unaweza", "anaweza",

    # Common infinitives / verb stems
    "kusema", "kwenda", "kuja", "kuona", "kusikia",
    "kupenda", "kufanya", "kupata", "kutaka", "kujua",
    "kusaidia", "kulala", "kula", "kunywa", "kucheza",
    "kusoma", "kuandika", "kufungua", "kufunga",
    "kuweza", "kulazimika",

    # Nouns — people & social
    "mtu", "watu", "mtoto", "watoto", "mwanaume", "mwanamke",
    "familia", "ndugu", "kaka", "dada", "mama", "baba",
    "mwalimu", "daktari", "askari", "dereva",
    "marafiki", "adui",

    # Nouns — time / abstract
    "siku", "wiki", "mwezi", "mwaka", "usiku", "asubuhi",
    "mchana", "jioni", "dakika", "saa",

    # Nouns — everyday
    "nyumba", "mji", "nchi", "barabara", "shule", "hospitali",
    "chakula", "maji", "fedha", "pesa", "kazi", "biashara",
    "habari", "jambo", "shida", "tatizo", "jibu",

    # Adjectives
    "nzuri", "mbaya", "kubwa", "ndogo", "mzuri",
    "mpya", "wa", "mrefu", "mfupi", "mzee",

    # Greetings / social
    "asante", "habari", "jambo", "karibu", "rafiki",
    "pamoja", "tafadhali", "samahani", "hongera",
    "kwaheri", "hujambo", "sijambo", "mambo",
    "salama", "poa", "safi",

    # Discourse / fillers
    "lakini", "basi", "sawa", "haya", "naam",
    "yaani", "kwa", "hivyo", "hata",
}
