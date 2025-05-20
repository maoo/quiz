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

The folder `decks/<deck_name>` MUST contain:
1. `index.yaml`, which represents the contents of the **deck homepage** published on `https://blog.session.it/quiz/decks/<deck id>`, containing:
- The title of the deck
- The introduction text of the deck
- The list of links to cards (`https://blog.session.it/quiz/decks/<deck id>/cards/<card id>`), with the link to SVG (`https://blog.session.it/quiz/decks/<deck id>/cards/<card id>/content.svg`) and PDF (`https://blog.session.it/quiz/decks/<deck id>/cards/<card id>/content.pdf`) versions too.

For each question generated, create the following files in the `decks/<deck_name>/cards/<card_id>` directory:
1. `content.yaml`: Contains all content related to a quiz card, listed in "Quiz card specifications", except for the 10 answers:
  - The **Question**
  - The **Embedded Contents**
  - The **10 Options**, in a random order
  - **Sources** , list of links to sources to certify the answer
  - The **URL** to the current card - `https://blog.session.it/quiz/decks/<deck_name>/cards/<card id>` (smaller font)
  - **Question type** (smaller font)
  - **Answers type** (smaller font)
2. `answers.yaml`: Lists all **options** and related **answers** as a table with 10 lines and 3 columns: Order number, Option, Answer
