ITALIAN: set[str] = {
    # Pronouns — subject
    "io", "lui", "lei", "noi", "voi", "loro",
    # "tu" omitted: in CONFLICT_WORDS
    # Pronouns — clitic / possessive
    "mio", "mia", "miei", "mie",
    "tuo", "tua", "tuoi", "tue",
    "suo", "suoi",
    # "sua" "suo" omitted from CONFLICT_WORDS — but "suo" kept as PT/IT conflict
    # "mi" "la" "le" "lo" "li" "tu" "me" "te" omitted: in CONFLICT_WORDS
    "nostro", "nostra", "nostri", "nostre",
    "vostro", "vostra", "vostri", "vostre",
    "gli",

    # Articles — definite
    "il", "dello", "della", "degli", "delle",
    # Articles — indefinite
    "uno", "una", "degli",
    # Contracted
    "del", "dei", "dal", "dai", "sul", "sui",
    "nel", "nei", "col", "coi",
    # "de" "la" "le" "un" "al" "con" omitted: in CONFLICT_WORDS

    # Demonstratives
    "questo", "questa", "questi", "queste",
    "quello", "quella", "quelli", "quelle",

    # Prepositions
    "senza", "tra", "fra", "verso",
    "durante", "secondo", "fino",
    "dopo", "prima", "presso",
    # "con" "da" omitted: in CONFLICT_WORDS

    # Conjunctions
    "però", "pero", "eppure", "anzi",
    "perché", "perche", "poiché", "poiche",
    "mentre", "sebbene", "benché",
    "quando", "dove", "anche",
    "oppure",
    # "ma" "come" "si" omitted: in CONFLICT_WORDS

    # Adverbs
    "molto", "bene", "qui", "qua",
    "adesso", "prima", "dopo",
    "sempre", "mai", "spesso", "ancora",
    "anche", "solo", "solamente",
    "quasi", "forse", "così", "cosi",
    "tanto", "poco", "abbastanza",
    # "già" "gia" "so" "ora" "bene" "do" omitted: in CONFLICT_WORDS

    # Interrogatives
    "chi", "quale", "quali",
    "quanto", "quanta", "quando", "dove",
    # "che" "come" omitted: in CONFLICT_WORDS

    # High-frequency verbs — essere / avere / stare / fare
    "sono", "sei", "siamo", "siete",
    "era", "erano",
    "ho", "hai", "abbiamo", "avete", "hanno",
    "aveva", "avevano", "avrei",
    "sto", "stai", "stiamo", "state", "stanno",
    "facendo", "faccio", "fai", "facciamo",
    "fatto", "fece",
    # andare / venire
    "vado", "vai", "andiamo", "andate", "vanno",
    "vengo", "vieni", "veniamo", "venite",
    "andato", "andare",
    # potere / volere / sapere / dovere
    "posso", "puoi", "puo", "possiamo", "potete", "possono",
    "voglio", "vuoi", "vuole", "vogliamo", "volete", "vogliono",
    "sai", "sa", "sappiamo", "sapete", "sanno",
    "devo", "devi", "deve", "dobbiamo", "dovete", "devono",
    # dire / vedere / dare
    "dico", "dici", "dice", "diciamo",
    "disse", "dicevo",
    "vedo", "vedi", "vede", "vediamo",
    "diamo", "danno",
    # other common
    "credo", "credi", "crede",
    "penso", "pensi", "pensa",
    "capisco", "capisce",

    # Nouns — high-frequency
    "cosa", "cose", "giorno", "giorni", "volta", "volte",
    "gente", "vita", "tempo", "ora", "ore",
    "uomo", "donna", "bambino", "bambini",
    "famiglia", "casa", "paese", "lavoro",
    "problema", "anno", "anni",
    "amico", "amici", "parte", "mondo",
    "settimana", "mese",

    # Adjectives
    "grande", "grandi", "piccolo", "piccola",
    "buono", "buona", "buoni", "buone",
    "cattivo", "cattiva",
    "nuovo", "nuova", "nuovi", "nuove",
    "stesso", "stessa", "stessi", "stesse",
    "altro", "altra", "altri", "altre",
    "tutto", "tutta", "tutti", "tutte",
    "bello", "bella", "belli", "belle",

    # Greetings / social
    "ciao", "arrivederci", "grazie", "prego",
    "scusa", "scusi", "buongiorno", "buonasera",
    "buonanotte", "salve",

    # Discourse / fillers
    "allora", "quindi", "comunque", "insomma",
    "davvero", "ovviamente", "certo", "esatto",
    "dai", "figurati",
    "ecco", "appunto", "magari",
    # "vabbè" "bene" "come" "ma" "da" "do" "so" "ora" "qui" omitted: in CONFLICT_WORDS
}
