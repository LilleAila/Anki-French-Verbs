import genanki
from pathlib import Path

vowels = ["a", "e", "i", "o", "y"]
subjects = {
    "je": 0,
    "j'": 0,
    "tu": 1,
    "il": 2,
    "elle": 2,
    "on": 2,
    "nous": 3,
    "vous": 4,
    "ils": 5,
    "elles": 5
}
otherSubjects = ["tu", "il", "elle", "on", "nous", "vous", "ils", "elles"]

avoir = {
    "je": "ai",
    "j'": "ai",
    "tu": "as",
    "il": "a",
    "elle": "a",
    "on": "a",
    "nous": "avons",
    "vous": "avez",
    "ils": "ont",
    "elles": "ont"
}

aller = {
    "je": "vais",
    "j'": "vais",
    "tu": "vas",
    "il": "va",
    "elle": "va",
    "on": "va",
    "nous": "allons",
    "vous": "allez",
    "ils": "vont",
    "elles": "vont"
}

etre = {
    "je": "suis",
    "j'": "suis",
    "tu": "es",
    "il": "est",
    "elle": "est",
    "on": "est",
    "nous": "sommes",
    "vous": "êtes",
    "ils": "sont",
    "elles": "sont"
}

se = {
    "je": "me",
    "j'": "me",
    "tu": "te",
    "il": "se",
    "elle": "se",
    "on": "se",
    "nous": "nous",
    "vous": "vous",
    "ils": "se",
    "elles": "se"
}

seEtre = {
    "je": "me suis",
    "j'": "me suis",
    "tu": "t'es",
    "il": "s'est",
    "elle": "s'est",
    "on": "s'est",
    "nous": "nous sommes",
    "vous": "vous êtes",
    "ils": "se sont",
    "elles": "se sont"
}

seIndexes = {
    "je": 0,
    "j'": 0,
    "tu": 0,
    "il": 0,
    "elle": 0,
    "on": 0,
    "nous": 1,
    "vous": 1,
    "ils": 1,
    "elles": 1
}

# regularVerbs = [
#   "parler", "aimer", "dormir", "choisir", "attendre"
# ]

regularVerbs = [
    # {
    #     "value": "parler",
    #     "translated": "å snakke"
    # }
]
    
regularVerbs = Path("regelrett.txt").read_text().split("\n")
regularVerbs = list(map(lambda a: {
    "value": a.lower().split(" å ")[0],
    "translated": "å " + " å ".join(a.lower().split(" å ")[1:])
}, regularVerbs))

# print(len(regularVerbs))
# print(regularVerbs[0], regularVerbs[1])

# cards = []

cards = {
    "e": [],
    "i": [],
    "r": [],
    "s": [],
    "u": []
}

for i in regularVerbs:
    verb = i["value"]
    translated = i["translated"]
    jeorj = "j'" if verb[0] in vowels else "je"
    present = []
    past = ""
    future = verb
    currentSubjects = [jeorj] + otherSubjects

    verbtype = verb[len(verb) - 2] if verb[:3] != "se " else "s"

    cards[verbtype].append(verb.capitalize() + " - {{c1::" + translated + "}}")
    match verbtype:
        case "e":  # ER-verb
            # print("ER")
            present = [
                verb[:-1],
                verb[:-1] + "s",
                verb[:-1],
                verb[:-2] + "ons",
                verb[:-2] + "ez",
                verb[:-2] + "ent"
            ]
            past = verb[:-2] + "é"
        case "i":  # IR-verb
            # print("IR")
            present = [
                verb[:-3] + "s",
                verb[:-3] + "s",
                verb[:-3] + "t",
                verb[:-2] + "ons",
                verb[:-2] + "ez",
                verb[:-2] + "ent"
            ]
            past = verb[:-1]
        case "r":  # RE-verb
            # print("RE")
            present = [
                verb[:-2] + "s",
                verb[:-2] + "s",
                verb[:-2],
                verb[:-2] + "ons",
                verb[:-2] + "ez",
                verb[:-2] + "ent"
            ]
            past = verb[:-2] + "u"
        case "s":  # Refleksivt verb
            # print("Refleksivt")
            verb = verb[3:]
            future = verb
            present = [
                verb[:-1],
                verb[:-1],
                verb[:-1],
                verb[:-2] + "ons",
                verb[:-2] + "ez",
                verb[:-2] + "ent"
            ]
            past = [
                verb[:-2] + "é(e)",
                verb[:-2] + "é(e)s"
            ]

    if verbtype != "s":
        for subj in currentSubjects:
            cards[verbtype].append(verb.capitalize() +
                         " (présent) - " +
                         subj +
                         (" " if subj != "j'" else "") +
                         "{{c1::" + present[subjects[subj]] + "}}")
            cards[verbtype].append(verb.capitalize() +
                         " (passé composé) - " +
                         (subj if subj != "je" else "j'") +
                         (" " if subj != "je" else "") +
                         "{{c1::" + avoir[subj] + " " + past + "}}")
            cards[verbtype].append(verb.capitalize() +
                         " (futur proche) - " +
                         ((subj + " ") if subj != "j'" else "je ") +
                         "{{c1::" + aller[subj] + " " + future + "}}")
    else:
        # lage det samme som over men at det virker med refleksive verb
        for subj in currentSubjects:
            cards[verbtype].append("Se " + verb +
                         " (présent) - " +
                         (subj if subj != "j'" else "je") +
                         " {{c1::" + se[subj] + " " + present[subjects[subj]] + "}}")
            cards[verbtype].append("Se " + verb +
                         " (passé composé) - " +
                         (subj if subj != "j'" else "je") +
                         " {{c1::" + seEtre[subj] + " " + past[seIndexes[subj]] + "}}")
            cards[verbtype].append("Se " + verb +
                         " (futur proche) " +
                         (subj if subj != "j'" else "je") +
                         " {{c1::" + aller[subj] + " " + se[subj] + " " + future + "}}")
    # Legge til en kode som leser uregelrette verb fra csv

uregelrett = Path("uregelrett.csv").read_text().split("\n")
uregelrett = list(map(lambda a: a.split(","), uregelrett))

uregelrette = []

step = 8
for i in range(0, len(uregelrett), step):
    uregelrette.append(uregelrett[i:i+step])

times = ["présent", "passé composé", "futur proche"]

for verb in uregelrette:
    infinitive = verb[0][1].lower().replace("*", "")
    translated = verb[0][2].lower()

    cards["u"].append(infinitive.capitalize() + " - {{c1::" + translated + "}}")

    verbForms = verb[2:]

    # print(verbForms)

    for currentForm in verbForms:
        forms = currentForm[-3:]
        currentSubjects = currentForm[:-3]
        currentSubjects = list(map(lambda a: a.replace('"', "").split("/")[0].strip(), currentSubjects))
        # print(currentSubjects, forms)
        for time in range(1, 3+1):
            # print(form)
            for subj in currentSubjects:
                # for time in range(1, 3):
                havespace = " "
                if subj == "je" and forms[time-1][:1] in vowels:
                    subj = "j'"
                    havespace = ""
                # print(form, time, subj)
                cards["u"].append(infinitive.capitalize() +
                                    " (" + times[time-1] + ") - " +
                                    subj + havespace +
                                    "{{c1::" + forms[time-1] + "}}")

[print(i) for i in cards["u"]]

# print(cards, len(cards))
# print(len(cards))

decks = {
    "e": genanki.Deck(
        1677740668561,  # INsert id here
        "Franske Verb::ER-Verb"
    ),
    "i": genanki.Deck(
        1677740668562,
        "Franske Verb::IR-Verb"
    ),
    "r": genanki.Deck(
        1677740668563,
        "Franske Verb::RE-Verb"
    ),
    "s": genanki.Deck(
        1677740668564,
        "Franske Verb::Refleksive Verb"
    ),
    "u": genanki.Deck(
        1677740668565,
        "Franske Verb::Uregelrette Verb"
    )
}

# for card in cards:
#     note = genanki.Note(model=genanki.CLOZE_MODEL, fields=[card, ""])
#     deck.add_note(note)

for key in cards.keys():
    # print(key)
    for card in cards[key]:
        # print(card, decks[key])
        note = genanki.Note(model=genanki.CLOZE_MODEL, fields=[card, ""])
        decks[key].add_note(note)

# [print(i) for i in cards.values()]

genanki.Package([*decks.values()]).write_to_file('decks.apkg')
