# 🏆 Quiz Deck - Generation Prompt

Generate the contents for a quiz card deck, following exactly the same folder structure, file format and structure found in the https://github.com/maoo/quiz github repository (branch: main, folder: decks/example), but using different content, following the provided **content guidelines**.

There must be 10 cards in the generated deck, with all type of answer_type values: binary, order, time, free_text, color; all equally distributed and shuffled across the deck.

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
