# 🏆 Quiz Deck - Generation Prompt

Generate the contents for a quiz card deck, following exactly the same folder structure, file format and structure found in the https://github.com/maoo/quiz github repository (branch: main, folder: decks/example), but using different content, following the provided **content guidelines**.

There must be 10 cards in the generated deck, with all type of answer_type values: binary, order, time, free_text, color; all equally distributed and shuffled across the deck.

Each card content must include exactly 1 question, 8 options and 8 answers; questions must be generated so that the 8 answers related to the 8 options are pertinent to the question and diverse

The output folder MUST contain:
- `index.yaml`
- for each card
  - `cards/<card_id>/content.yaml`
  - `cards/<card_id>/answers.yaml`

Card contents must be:
  - Challenging
  - Fair, precise, and undisputable
  - Grounded in fact-checked, verifiable
  - Clear, stand-alone, and unambiguous
  - Concise, splitting longer concepts into simpler terms to meet the character limits:
    - Questions: max 80 chars
    - Options: max 35 chars
    - Answers: max 35 chars
  - Sometimes enhanced with emojis and other YAML-allowed graphical elements

If a card does not comply with the requirements above, it must be discarded and regenerated.