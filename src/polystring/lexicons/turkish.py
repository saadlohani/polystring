TURKISH: set[str] = {
    # Conjunctions — most diagnostic
    "ama", "fakat", "lakin", "ancak",
    "ve", "veya", "yahut",
    # "ya" omitted: in CONFLICT_WORDS (ES/UR/SW overlap)
    "ki", "ile", "hem",
    "cunku", "cunki",
    "eger", "yani", "oysa", "oysaki",
    "madem", "mademki",

    # High-frequency particles / postpositions
    "bir", "bu", "o",
    # "su" omitted: in CONFLICT_WORDS
    "var", "yok",
    "evet", "hayir",
    "iyi", "cok", "daha", "en",
    "sonra", "once", "simdi",
    "bugun", "yarin", "dun",
    "gibi", "kadar", "icin", "ile", "gore",
    "hep", "hic", "az",
    "zaten", "artik", "sadece", "bile",
    "yine", "tekrar", "gene",
    "hatta", "neyse", "belki",

    # Pronouns
    "ben", "sen", "biz", "siz", "onlar",
    "benim", "senin", "onun", "bizim", "sizin",
    "bana", "sana", "ona", "bize", "size", "onlara",
    "beni", "seni", "onu", "bizi", "sizi",
    "bende", "sende", "onda",
    "benimle", "seninle", "onunla",
    # "su" omitted: in CONFLICT_WORDS (ES/IT/PT pronoun/possessive overlap)

    # Interrogatives
    "neden", "niye", "nasil", "nerede", "ne",
    "kim", "hangi", "kac", "nereye", "nereden",
    "ne zaman",

    # Common verbs — present / past stems
    "istiyorum", "istiyorsun", "istiyor", "istiyoruz",
    "biliyorum", "biliyorsun", "biliyor", "biliyoruz",
    "gidiyorum", "gidiyorsun", "gidiyor",
    "geliyorum", "geliyorsun", "geliyor",
    "yapiyorum", "yapiyorsun", "yapiyor",
    "goruyorum", "goruyorsun", "goruyor",
    "diyorum", "diyorsun", "diyor",
    "veriyorum", "veriyorsun", "veriyor",
    "aliyorum", "aliyorsun", "aliyor",
    "gitti", "geldi", "yapti", "soyledi",
    "oldu", "olacak", "olabilir",
    "gidecek", "gelecek", "yapacak",
    "etmek", "yapmak", "gitmek", "gelmek",
    "istemek", "bilmek", "gormek", "vermek",

    # Negation / modal
    "degil", "degilim", "degilsin",
    "olmaz", "olur", "olabilir",
    "yapamam", "gidemem",

    # Common nouns
    "zaman", "gun", "yil", "ay", "hafta",
    "sabah", "aksam", "gece", "oglen",
    "yer", "ev", "okul", "is", "yol",
    "adam", "kadin", "cocuk", "arkadaslar",
    "insan", "insanlar", "herkes", "kimse",
    "sey", "seyler", "sorun", "durum",
    "hayat", "dunya", "ulke", "sehir",

    # Adjectives
    "buyuk", "kucuk", "guzel", "kotu",
    "yeni", "eski", "uzun", "kisa",
    "sicak", "soguk", "sert", "yumusak",
    "kolay", "zor", "dogru", "yanlis",
    "onemli", "gercek", "buyuk",

    # Greetings / social
    "tamam", "tabii", "tabi",
    "lutfen", "tesekkur", "merhaba",
    "elbette", "gercekten", "kesinlikle",
    "nasılsın", "naber",

    # Discourse / fillers
    "yani", "hani", "sanki", "mesela",
    "aslinda", "ayrıca", "onun", "icin",
    "boyle", "soyle", "boylece",
    "ne", "kadar", "gece",
}
