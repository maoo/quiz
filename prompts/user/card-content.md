Generate one card content for the deck, in YAML format, following the schema defined in https://raw.githubusercontent.com/maoo/quiz/refs/heads/main/schemas/card.yaml

Questions must be generated so that the 8 answers related to the 8 options are pertinent to the question and diverse, but never null or empty.

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
  - Similar to the examples available in https://github.com/maoo/quiz/blob/main/decks/example/cards
  - Different from the bad examples listed below

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