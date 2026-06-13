PORTUGUESE: set[str] = {
    # Pronouns — subject
    "eu", "voce", "ele", "ela", "eles", "elas",
    # "nos" omitted: in CONFLICT_WORDS (FR/PT 2-lexicon overlap)
    "vos",
    # Pronouns — object / clitic
    "lhe", "lhes",
    "mim", "ti",
    # "me" "te" "nos" omitted: in CONFLICT_WORDS (multi-language overlap)

    # Articles — definite
    "os", "as",
    # "de" "do" "dos" "da" omitted: in CONFLICT_WORDS
    "das", "ao", "aos", "pelo", "pela",
    "pelos", "pelas", "num", "numa", "nuns", "numas",
    "nele", "nela", "neles", "nelas", "nisto", "nisso",
    # "un" "la" "le" "les" omitted: in CONFLICT_WORDS

    # Demonstratives
    # "este" "esta" omitted: in CONFLICT_WORDS
    "estes", "estas",
    "esse", "essa", "esses", "essas",
    "aquele", "aquela", "aqueles", "aquelas",
    "isto", "isso", "aquilo",

    # Possessives
    "meu", "minha", "meus", "minhas",
    "teu", "tua", "teus", "tuas",
    "seu", "seus",
    # "sua" omitted: in CONFLICT_WORDS (IT overlap)
    "nosso", "nossa", "nossos", "nossas",

    # Prepositions
    "com", "sem", "entre", "sob", "sobre", "desde",
    "durante", "segundo", "ate", "apos",
    "perante", "mediante",
    # "por" "de" omitted: in CONFLICT_WORDS

    # Conjunctions
    "mas", "porem", "todavia", "contudo",
    "porque", "pois", "quando",
    "onde", "embora", "ainda",
    # "como" "que" "si" "ma" omitted: in CONFLICT_WORDS

    # Adverbs
    "muito", "aqui", "ali",
    "agora", "antes", "depois", "sempre", "nunca",
    "tambem", "somente", "apenas",
    "quase", "talvez", "assim",
    "tao", "tanto", "quanto",
    # "ja" "so" "mal" "bem" "ora" "es" omitted: in CONFLICT_WORDS

    # Interrogatives
    "quem", "qual", "quais",
    "quanto", "quando", "onde",
    # "que" "como" omitted: in CONFLICT_WORDS

    # High-frequency verbs — ser / estar / ter / haver
    "sou", "somos", "sao",
    "estou", "estamos", "estao",
    "tenho", "tens", "temos", "tem",
    "tinha", "teve",
    "havia", "houve",
    # "ha" "es" omitted: in CONFLICT_WORDS
    # ir / vir
    "vou", "vai", "vamos", "vao",
    "venho", "vens", "vem", "vimos",
    "fui", "foi", "fomos", "foram",
    # poder / querer / saber / fazer
    "posso", "podes", "pode", "podemos", "podem",
    "quero", "queres", "quer", "queremos", "querem",
    "sei", "sabe", "sabemos", "sabem",
    "faco", "faz", "fazemos", "fazem",
    "fez", "fiz",
    # dizer / ver / dar
    "digo", "diz", "dizemos", "dizem",
    "disse", "dizia",
    "vejo", "vemos", "veem",
    "dou", "damos", "dao",
    # other common
    "acho", "acha", "achamos",
    "penso", "pensa", "pensamos",
    "preciso", "precisa",
    "gosto", "gosta",

    # Nouns — high-frequency
    "coisa", "coisas", "dia", "dias", "vez",
    "gente", "vida", "tempo", "hora", "horas",
    "homem", "mulher", "crianca", "criancas",
    "familia", "casa", "pais", "trabalho",
    "problema", "pergunta", "ano", "anos",
    "amigo", "amigos", "parte", "mundo",
    "semana", "mes",

    # Adjectives
    "grande", "grandes", "pequeno", "pequena",
    "bom", "boa", "bons", "boas",
    "mau", "maus",
    "novo", "nova", "novos", "novas",
    "mesmo", "mesma", "mesmos", "mesmas",
    "outro", "outra", "outros", "outras",
    "todo", "toda", "todos", "todas",
    "muito", "muita", "muitos", "muitas",
    "pouco", "pouca", "poucos", "poucas",
    # "ma" omitted: in CONFLICT_WORDS

    # Greetings / social
    "ola", "obrigado", "obrigada",
    "desculpe", "perdao", "favor",
    "tchau", "boas", "boa", "oi",

    # Discourse / fillers
    "entao", "pois", "bom", "claro",
    "verdade", "certo", "enfim",
    "veja", "olha", "cara", "mano",
    # "ora" "dos" "do" "da" "es" "ma" "si" "so" omitted: in CONFLICT_WORDS
}
