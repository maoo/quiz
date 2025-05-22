# 🏆 Quiz Deck - Generation Prompt

Generate the contents for a quiz card deck, following exactly the same folder structure, file format and structure found in the https://github.com/maoo/quiz github repository (branch: main, folder: decks/example), but using the content described by a **content guidelines** YAML file (branch: main, folder: prompts) that is specified when invoking this prompt.

The best approach to access the github repository is to fetch the raw files using the web tools available.

There must be 10 cards in the generated deck, with all type of answer_type values, to keep it as balanced as possible (something like 3 binary, 2 order, 2 time, and 3 free_text).

Each card content must include exactly 1 question, 8 options and 8 answers; questions must be generated so that the 8 answers related to the 8 options are pertinent to the question and diverse; all card content is contained in the `cards/<card_id>` sub-folder , where `<card_id>` is a 3-digit sequential number, starting from `001`.

The output folder MUST contain:
- `index.yaml`
- for each card
  - `cards/<card_id>/content.yaml`
  - `cards/<card_id>/answers.yaml`

Card contents must be:
  - Always related to the introduction and subject matter found in the "content guidelines" file; use the web to find information related with the requested subject
  - Challenging
  - Fair, precise, and undisputable
  - Grounded in fact-checked, verifiable
  - Clear, stand-alone, and unambiguous
  - Concise, splitting longer concepts into simpler terms to meet the character limits:
    - Questions: mandatory; not empty; max 80 chars
    - Options: mandatory; not empty; all different from each other; max 35 chars
    - Answers: max 35 chars
  - Sometimes enhanced with emojis and other YAML-allowed graphical elements

If a card does not comply with the requirements above, it must be discarded and regenerated.

Follow these steps to generate the deck:
1. Checkout the https://github.com/maoo/quiz.git git repo (ignore certificates)
2. Fetch the **content guidelines** YAML file and parse it
3. Generate a proper deck name, based on the **content guidelines**
4. Copy the decks/example folder into the **output folder**, with the name of the generated deck
5. Based on the subject matter specified in **content guidelines**, search the web to find related news, info, data, facts, that can be used to generate the questions
6. Parse the "bad card examples" below
7. Generate the card contents as described before
8. Make sure that generated content is not similar to the bad examples parsed on step 6; if uncertain, discard the content and regenerate it
9. Update files in the **output folder** with the contents generated on step 6
10. Zip the **output folder** and return the URL to downaload it

## Bad examples

### Bad example 1

The following content.yaml contains emply options:
```
answer_type: "free_text"
question: "Nomina l'artista italiano noto come 'Sfera Ebbasta'"
options:
  - ""
  - ""
  - ""
  - ""
  - ""
  - ""
  - ""
  - ""
```

It is better to formulate the question this way:
```
answer_type: "free_text"
question: "Nomina gli artisti con questi nome d'arte"
options:
  - "Fred De Palma"
  - "Sfera Ebbasta"
  - "Ghali"
  - "Shiva"
  - "Marracash"
  - "Izi"
  - "Dark Polo Gang"
  - "Edo Fendy"
```
Each option will have a related answer with firstname and surname of the artist.

### Bad example 2

The following content.yaml contains only 2 valid options, "Si" or "No", instead of having 8 valid options; it also contains 6 options ("Opzione 3", "Opzione 4", ...) which have no meaning and are definitely not related to the question.

```
answer_type: "binary"
question: "La canzone 'Una volta ancora' di Fred De Palma è del 2019?"
options:
  - "Sì"
  - "No"
  - "Opzione 3"
  - "Opzione 4"
  - "Opzione 5"
  - "Opzione 6"
  - "Opzione 7"
  - "Opzione 8"
```

It is better to formulate the question this way:
```
answer_type: "binary"
question: "Quali canzoni sono di quale anno?"
options:
  - "Una volta ancora, Fred De Palma - 2019"
  - "Figli di papa, Sfera Ebbasta - 2022"
  - "Dende, Ghali - 2018"
  - "Ragnatele, Shiva - 2024"
  - "Notti, Sfera Ebbasta - 2021"
  - "Chic, Izi - 2025"
  - "Sportswear, Dark Polo Gang - 2021"
  - "BHMG, Sfera Ebbasta - 2020"
```
Each option will have a related True/False answer

### Bad example 3

The following content.yaml contains only 1 option that is true, all others will be false; also, considering that the answer is either true or false, the "answer_type" should be "binary".
```
answer_type: "time"
question: "In che anno è stata pubblicata 'Auto blu' di Eiffel 65 & The Ferragnez?"
options:
  - "2019"
  - "2020"
  - "2021"
  - "2022"
  - "2023"
  - "2018"
  - "2017"
  - "2016"
```

It is better to formulate the question this way:
```
answer_type: "time"
question: "In che anno sono state pubblicate queste canzoni?"
options:
  - "Una volta ancora, Fred De Palma"
  - "Figli di papa, Sfera Ebbasta"
  - "Dende, Ghali"
  - "Ragnatele, Shiva"
  - "Notti, Sfera Ebbasta"
  - "Chic, Izi"
  - "Sportswear, Dark Polo Gang"
  - "BHMG, Sfera Ebbasta"
```
Each option will have a related answer with the release year of the song.