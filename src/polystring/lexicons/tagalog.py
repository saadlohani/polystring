TAGALOG: set[str] = {
    # Core markers — extremely diagnostic, unique to Tagalog
    "mga", "ang", "ng", "ay", "nang",
    "nina", "sina",

    # Pronouns — nominative
    "siya", "sila", "kami", "tayo", "kayo", "ikaw", "ako",
    # Pronouns — genitive / oblique
    "niya", "nila", "namin", "natin", "ninyo", "nyo", "niya",
    "akin", "iyo", "kanya", "amin", "atin", "inyo",
    "kanila", "kanilang", "aking", "iyong", "kaniyang",

    # Demonstratives
    "ito", "iyon", "iyan", "dito", "doon", "diyan",
    "nito", "noon", "niyan", "rito", "roon",
    "ngayon", "kahapon", "bukas",

    # Negation / affirmation
    "hindi", "huwag", "wag", "oo", "opo", "oho",
    "hindi", "di",

    # Particles (most diagnostic to Tagalog)
    "po", "ho", "kasi", "naman", "talaga", "daw", "raw",
    "ba", "rin", "pa", "lamang",
    # "din"  omitted: in CONFLICT_WORDS (UR time word overlap)
    # "na"   omitted: in CONFLICT_WORDS (UR + SW + DE overlap)
    # "lang" omitted: in CONFLICT_WORDS (EN word overlap)
    # "man"  omitted: in CONFLICT_WORDS (TL + EN overlap)
    # "para" omitted: in CONFLICT_WORDS (TL + ES/PT overlap)
    "pala", "nga", "muna", "yata", "sana",
    # "man" omitted: in CONFLICT_WORDS

    # Existential
    "may", "mayroon", "wala", "meron",

    # Conjunctions / linkers
    "at", "pero", "ngunit", "o", "kahit", "kaya", "kung",
    "dahil", "habang", "kapag", "pagka", "bago", "matapos",
    # "para" omitted: in CONFLICT_WORDS (ES/PT "for" overlap)
    "upang", "sapagkat",

    # Prepositions / focus markers
    "sa", "kay", "nina", "mula", "hanggang",
    # "para" omitted: in CONFLICT_WORDS
    "tungkol", "patungkol", "ukol",

    # High-frequency verbs (mag- / -um- / ma- forms)
    "kumain", "kakain", "kumakain",
    "pumunta", "pupunta", "pumupunta",
    "umalis", "aalis", "umaalis",
    "bumalik", "babalik", "bumabalik",
    "magluto", "magluluto", "nagluluto",
    "matulog", "matutulog", "natutulog",
    "gumawa", "gagawa", "gumagawa",
    "magsalita", "magsasalita",
    "umiyak", "iiyak",
    "tumawa", "tatawa",
    "magbasa", "magbabasa",
    "magsulat", "magsusulat",
    "magbayad", "magbabayad",
    "makita", "makikita",
    "marinig", "maririnig",
    "malaman", "malalaman",

    # Adjectives / descriptors — common
    "maganda", "magandang", "masaya", "malungkot",
    "malaki", "maliit", "mahirap", "madali",
    "mahal", "mura", "bago", "luma", "mabilis",
    "mabagal", "mainit", "malamig", "masarap",
    "maayos", "matagal", "maikli",

    # Adverbs / degree words
    "medyo", "sobra", "talagang", "halos",
    "lagi", "palagi", "minsan", "madalas",
    "maagang", "agad", "kaagad",

    # Nouns — common
    "bahay", "trabaho", "pamilya", "bata", "buhay",
    "tao", "oras", "araw", "gabi", "umaga", "tanghali",
    "hapon", "linggo", "buwan", "taon", "lugar",
    "pagkain", "tubig", "kuya", "ate", "lola", "lolo",
    "nanay", "tatay", "kaibigan", "kapitbahay",
    "puso", "isip", "katawan", "kamay", "mata",
    "daan", "kalsada", "eskwela", "opisina",
    "pelikula", "musika", "laro",

    # Greetings / social
    "salamat", "kamusta", "kumusta", "paalam", "ingat",
    "mabuhay", "maligayang", "pasensya",

    # Numbers (written forms common in mixed text)
    "isa", "dalawa", "tatlo", "apat", "lima",
    "anim", "pito", "walo", "siyam", "sampu",

    # Discourse fillers
    "kaya", "tapos", "tsaka", "saka", "parang",
    "ganon", "ganun", "gano", "ganito",
    "ayun", "ayan", "yun", "yung", "yung", "yong",
    "diba", "di", "ano", "eh",
}
