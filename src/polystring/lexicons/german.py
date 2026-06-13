GERMAN: set[str] = {
    # Pronouns — subject
    "ich", "du", "er", "sie", "wir", "ihr",
    # Pronouns — object / dative
    "mich", "dich", "ihn", "uns", "euch",
    "mir", "dir", "ihm", "ihnen",
    # Possessives
    "mein", "meine", "meinen", "meiner", "meinem",
    "dein", "deine", "deinen", "deiner", "deinem",
    "sein", "seine", "seinen", "seiner", "seinem",
    "unser", "unsere", "unseren", "unserer",
    "euer", "eure", "euren", "eurer",
    "ihre", "ihren", "ihrer", "ihrem",

    # Articles — definite (highly diagnostic)
    "der", "die", "das", "dem", "den", "des",
    # Articles — indefinite
    "ein", "eine", "einen", "einem", "einer", "eines",
    # Negation article
    "kein", "keine", "keinen", "keinem",

    # Prepositions
    "mit", "ohne", "durch", "gegen", "um",
    "seit", "von", "nach",
    "vor", "hinter", "zwischen", "uber", "unter",
    "neben", "auf", "zu",
    "bis", "wahrend", "wegen",
    # "an" "in" "am" "bei" "aus" omitted: in CONFLICT_WORDS

    # Conjunctions
    "und", "aber", "oder", "denn", "sondern",
    "weil", "dass", "wenn", "ob", "als",
    "obwohl", "damit", "sodass", "wahrend",
    "nachdem", "bevor",

    # Adverbs
    "sehr", "auch", "noch", "schon", "nur",
    "jetzt", "dann", "dort", "hier", "nie",
    "immer", "oft", "manchmal", "wieder",
    "gerne", "leider", "eigentlich", "vielleicht",
    "wahrscheinlich", "sicher", "genau", "fast",
    "eben", "halt", "doch",
    # "also" "so" "mal" "ja" "na" "an" "aus" omitted: in CONFLICT_WORDS

    # Interrogatives
    "wer", "welcher", "welche", "welches",
    "wie", "wo", "wann", "warum", "woher", "wohin",
    # "was" omitted: in CONFLICT_WORDS

    # High-frequency verbs — sein / haben / werden / machen
    "bin", "bist", "sind", "seid", "war", "waren",
    "habe", "hast", "hat", "haben", "habt", "hatte",
    "werde", "wirst", "wird", "werden", "werdet",
    "mache", "machst", "macht", "machen",
    "gemacht",
    # gehen / kommen
    "gehe", "gehst", "geht", "gehen",
    "komme", "kommst", "kommt", "kommen",
    "gegangen", "gekommen",
    # wissen / konnen / mussen / wollen / sollen
    "weis", "wissen",
    "kann", "kannst", "konnen", "konnt",
    "muss", "musst", "mussen",
    "will", "willst", "wollen", "wollt",
    "soll", "sollst", "sollen", "sollt",
    # sagen / sehen / geben / nehmen
    "sage", "sagst", "sagt", "sagen", "sagte",
    "sehe", "siehst", "sieht", "sehen", "sah",
    "gebe", "gibst", "gibt", "geben", "gab",
    "nehme", "nimmst", "nimmt", "nehmen",
    # other common
    "denke", "denkst", "denkt",
    "glaube", "glaubst", "glaubt",
    "finde", "findest", "findet",
    "brauche", "brauchst", "braucht",

    # Nouns — high-frequency (lowercase in mixed text)
    "ding", "dinge", "tag", "tage", "leute",
    "leben", "zeit", "stunde", "stunden",
    "mann", "frau", "kind", "kinder",
    "familie", "haus", "land", "arbeit",
    "problem", "frage", "jahr", "jahre",
    "freund", "freunde", "teil", "welt",
    "woche", "monat",
    # "mal" omitted: in CONFLICT_WORDS

    # Adjectives
    "gross", "kleine", "klein",
    "gute", "guten", "gutem",
    "schlecht", "schlechte",
    "neu", "neue", "neuen",
    "gleich", "gleiche",
    "andere", "anderen",
    "alle", "allen",
    "viele", "vielen",
    "wenige", "wenigen",
    "schone",
    # "gut" "gut" "so" "an" "aus" "was" omitted: in CONFLICT_WORDS

    # Greetings / social
    "hallo", "tschuss", "danke", "bitte",
    "entschuldigung", "guten", "morgen",
    "abend", "nacht",

    # Discourse / fillers
    "naja", "okay",
    "ne", "nein",
    "stimmt", "klar", "super",
    "ach", "hmm",
    # "also" "ja" "na" "jo" "genau" "an" omitted: in CONFLICT_WORDS
}
