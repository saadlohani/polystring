FRENCH: set[str] = {
    # Pronouns — subject
    "je", "il", "elle", "nous", "vous", "ils", "elles",
    # "tu" omitted: in CONFLICT_WORDS (FR/ES/PT/IT overlap)
    # Pronouns — stressed / object
    "moi", "toi", "lui", "soi", "eux",
    # "me" "te" "se" omitted: in CONFLICT_WORDS
    "y", "en",
    # Pronouns — relative / interrogative
    # "qui" omitted: in CONFLICT_WORDS (IT overlap)
    # "que" omitted: in CONFLICT_WORDS
    "quoi", "lequel", "laquelle", "lesquels", "lesquelles",
    "dont",

    # Articles — definite
    # "le" "les" "la" omitted: in CONFLICT_WORDS (multi-language overlap)

    # Articles — indefinite
    # "un" omitted: in CONFLICT_WORDS
    "une",
    # Partitive / contracted
    "du", "des", "au", "aux",
    # "de" omitted: in CONFLICT_WORDS

    # Demonstratives
    "ce", "cet", "cette", "ces",
    "celui", "celle", "ceux", "celles",
    "ceci", "cela",

    # Possessives
    "mon", "mes", "ton", "ta", "tes",
    "son", "sa", "ses", "notre", "votre", "vos", "leur", "leurs",
    # "nos" omitted: in CONFLICT_WORDS (FR/PT 2-lexicon overlap)
    # "ma" omitted: in CONFLICT_WORDS (IT/PT overlap)

    # Prepositions
    "avec", "dans", "par", "pour", "sur", "sous", "entre", "vers",
    "depuis", "pendant", "sans", "contre", "chez", "devant", "derriere",
    "avant", "apres", "selon", "parmi",

    # Conjunctions
    # "mais" omitted: in CONFLICT_WORDS (PT overlap)
    # "or" omitted: in CONFLICT_WORDS
    # "si" omitted: in CONFLICT_WORDS
    # "ni" omitted: in CONFLICT_WORDS
    "donc", "car", "puisque",
    # "que" "comme" "bien" omitted: in CONFLICT_WORDS or too ambiguous
    "quand", "parce", "lorsque", "afin",

    # Adverbs — frequency / degree
    "tres", "encore", "toujours", "jamais", "souvent", "parfois",
    "beaucoup", "peu", "plus", "moins", "assez", "trop", "tellement",
    "vraiment", "seulement", "enfin", "maintenant",
    # "aussi" "bien" omitted: in CONFLICT_WORDS

    # Adverbs — place
    "ici", "voila", "alors", "ailleurs", "partout",

    # Interrogatives
    "pourquoi", "comment", "combien", "quand",
    # "que" "qui" "ou" omitted: in CONFLICT_WORDS

    # High-frequency verbs (conjugated forms diagnostic to French)
    "est", "sont", "etait", "etaient", "sera", "serait",
    "avoir", "avez", "avons", "avaient", "aura",
    "faire", "fait", "fais", "faites", "faisait",
    "aller", "vais", "allons", "allez", "allait",
    "venir", "viens", "venons", "venez",
    "pouvoir", "peux", "peut", "pouvons", "pouvez", "peuvent",
    "vouloir", "veux", "veut", "voulons", "voulez", "veulent",
    "savoir", "sais", "sait", "savons",
    "prendre", "prend", "prends", "prenons",
    "voir", "vois", "voit", "voyons",
    "dire", "dis", "dit", "disons",
    "mettre", "mets", "met", "mettons",
    "penser", "pense", "penses", "pensons",
    "parler", "parle", "parles", "parlons", "parlez",
    "donner", "donne", "donnes",
    "trouver", "trouve", "trouves",
    "croire", "crois", "croit",
    "falloir", "faut",
    "rester", "reste", "restons",
    "passer", "passe",

    # Nouns — high-frequency
    "chose", "choses", "jour", "jours", "gens", "vie", "fois",
    "monde", "temps", "heure", "heures", "homme", "femme",
    "enfant", "enfants", "famille", "maison", "pays", "travail",
    "probleme", "question", "annee", "annees", "ami", "amis",
    "place", "partie", "point", "moment", "cas", "droits",
    "semaine", "mois",

    # Adjectives — common
    "grand", "grande", "grands", "grandes",
    "petit", "petite", "petits", "petites",
    "bon", "bonne", "bons", "bonnes",
    "nouveau", "nouvelle", "nouveaux",
    "premier", "premiere", "derniere", "dernier",
    "tout", "toute", "tous", "toutes",
    "autre", "autres", "meme", "memes",
    "seul", "seule", "seuls", "seules",
    "propre", "propres",

    # Greetings / social
    "merci", "bonjour", "bonsoir", "salut", "bonne",
    "aujourd",  # "aujourd'hui" always splits here

    # Discourse / fillers
    "oui", "non", "voila", "alors", "donc", "enfin",
    "hein", "ben", "nan",
    # "quoi" kept — diagnostic to French
    "quoi",
}
