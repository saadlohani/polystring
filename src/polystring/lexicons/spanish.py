SPANISH: set[str] = {
    # Pronouns — subject
    "yo", "usted", "nosotros", "nosotras",
    "vosotros", "vosotras", "ustedes", "ellos", "ellas",
    # "tu" omitted: in CONFLICT_WORDS
    # Pronouns — object / reflexive
    # "me" "te" "se" "nos" omitted: in CONFLICT_WORDS
    "lo", "los", "li",

    # Articles
    # "la" "le" "les" "un" "el" omitted: in CONFLICT_WORDS
    "unas", "unos",

    # Demonstratives
    # "este" "esta" "ese" "esa" omitted: in CONFLICT_WORDS
    "estos", "estas", "esos", "esas",
    "aquel", "aquella", "aquellos", "aquellas",
    "esto", "eso", "aquello",

    # Possessives
    # "mi" "su" "tu" omitted: in CONFLICT_WORDS
    "mis", "tus", "sus",
    "nuestro", "nuestra", "nuestros", "nuestras",
    "vuestro", "vuestra", "vuestros", "vuestras",
    "mio", "mia", "mios", "mias",
    "tuyo", "tuya", "tuyos", "tuyas",

    # Prepositions
    # "con" "por" omitted: in CONFLICT_WORDS
    "sin", "bajo", "entre", "hacia", "hasta",
    "desde", "durante", "mediante", "segun",
    "ante", "tras",
    # "de" omitted: in CONFLICT_WORDS

    # Conjunctions
    "pero", "sino", "aunque", "mientras",
    "porque", "pues", "cuando",
    "donde", "ademas", "tampoco",
    # "como" "que" omitted: in CONFLICT_WORDS

    # Adverbs
    "muy", "aqui", "ahi", "alla",
    "ahora", "antes", "despues", "siempre", "nunca",
    "todavia", "tambien",
    "casi", "solo", "solamente", "quizas", "acaso",
    "asi", "tan", "tanto", "cuanto",
    # "ya" "bien" "mal" omitted: in CONFLICT_WORDS

    # Interrogatives
    "quien", "quienes", "cual", "cuales",
    "cuanto", "cuanta", "donde", "cuando",
    # "que" "como" "por" omitted: in CONFLICT_WORDS

    # High-frequency verbs — ser / estar / haber / tener
    "soy", "eres", "somos", "sois",
    "estoy", "estamos", "estais", "estan",
    "hay", "hubo", "habia",
    "tengo", "tienes", "tenemos", "teneis", "tienen",
    "tenia", "tuvo", "tuve",
    # ir / venir
    "voy", "vas", "vamos", "vais", "van",
    "vengo", "vienes", "venimos", "vienen",
    "fui", "fue", "fueron",
    # poder / querer / saber / hacer
    "puedo", "puedes", "puede", "podemos", "pueden",
    "quiero", "quieres", "quiere", "queremos", "quieren",
    "queria", "quiso",
    "sabe", "sabemos", "saben",
    "hago", "haces", "hace", "hacemos", "hacen",
    "hizo", "hice",
    # decir / ver / dar
    "digo", "dices", "dice", "decimos", "dicen",
    "dijo", "dije",
    "veo", "ves", "vemos", "ven",
    "doy", "das", "damos", "dan",
    # other common
    "creo", "crees", "cree", "creemos",
    "pienso", "piensas", "piensa",
    "necesito", "necesitas", "necesita",
    "gustaria", "gusta", "gusto",

    # Nouns — high-frequency
    "cosa", "cosas", "dia", "dias", "vez", "veces",
    "gente", "vida", "tiempo", "hora", "horas",
    "hombre", "mujer", "nino", "ninos",
    "familia", "casa", "pais", "trabajo",
    "problema", "pregunta", "ano", "anos",
    "amigo", "amigos", "parte", "mundo",
    "semana", "mes",

    # Adjectives — common
    "grande", "grandes", "pequeno", "pequena",
    "bueno", "buena", "buenos", "buenas",
    "malo", "mala", "malos", "malas",
    "nuevo", "nueva", "nuevos", "nuevas",
    "mismo", "misma",
    "otro", "otra", "otros", "otras",
    "todo", "toda", "todos", "todas",
    "mucho", "mucha", "muchos", "muchas",
    "poco", "poca", "pocos", "pocas",

    # Greetings / social
    "hola", "adios", "gracias", "favor",
    "perdon", "disculpe", "bienvenido",

    # Discourse / fillers
    "pues", "bueno", "claro", "entonces",
    "verdad", "vale", "oye", "mira", "vaya",
    "oiga", "venga",
    # "bien" "mal" "no" "al" "es" "el" "la" omitted: in CONFLICT_WORDS
}
