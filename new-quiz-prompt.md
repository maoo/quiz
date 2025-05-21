# 🏆 Quiz Deck - Generation Prompt

Generate the contents for a quiz card deck, following exactly the same folder structure, file format and structure found in the https://github.com/maoo/quiz github repository (branch: main, folder: decks/example), but using the content described by a **content guidelines** YAML file (branch: main, folder: prompts) that is specified when invoking this prompt.

There must be 10 cards in the generated deck, with all type of answer_type values: binary, order, time, free_text; all equally distributed and shuffled across the deck.

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
    - Questions: max 80 chars
    - Options: max 35 chars
    - Answers: max 35 chars
  - Sometimes enhanced with emojis and other YAML-allowed graphical elements

If a card does not comply with the requirements above, it must be discarded and regenerated.

Follow these steps to generate the deck:
1. Checkout the https://github.com/maoo/quiz.git git repo (ignore certificates)
2. Fetch the **content guidelines** YAML file and parse it
3. Generate a proper deck name, based on the **content guidelines**
4. Copy the decks/example folder into the **output folder**, with the name of the generated deck
5. Based on the subject matter specified in **content guidelines**, search the web to find related news, info, data, facts, that can be used to generate the questions
6. Generate the card contents as described before
7. Update files in the **output folder** with the contents generated on step 6
8. Zip the **output folder** and return the URL to downaload it