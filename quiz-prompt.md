# 🏆 Quiz Deck - Generation Prompt

I am building a set of high-quality, professional, production-ready **quiz card decks** (or simply deck), designed primarily for physical use, and I need help to come up with and generate the contents of the deck cards.

Each deck contains 200 **quiz cards**, each containing a quiz, that are related to the same subject; the deck is described by `decks/<deck id>/prompts/<deck id>.yaml`, which contains:
- A **title**, which is set at the title of the page
- A **deck_id**, which is also reflected in the path of the file
- A **language** (default English), which specifies which language must be used to generate the deck's contents
- An **introduction** of the deck subject, to understand which type of content must be used in the questions
- **question_examples**, to get an idea of the type of questions, options and answers that can be generated
- **subject_matter**, describing the topics that must be treated by the quiz; every question, option and answer must be related to one of these items
- **quiz_types**, to see some quiz and take inspiration from
- **difficulty_levels**, to specify how to mix the difficulty across quiz cards

## ⚖️ Quiz card specifications

Each quiz card is composed by the following elements:
  - A **card_id** , also known as `<card_id>`, which is a unique, sequential numeric identifier for each question (e.g., "001", "042", "123", etc.).
  - A **question_type**, which can be either `short` or `extended`.
  - **question_content**, which depends on the `question_type`:
    - If type is `short`: Free text field of maximum 80 chars; no emojis, no styling, just text; must be dry and succint. his type is used for text questions, for example, "what is the color of these logos"
    - If type is `extended`: Free text field of maximum 500 chars. This type is used for questions that require embedded content, for example, "Order these geometrical shapes from biggest to smallest", or "Answer these questions about the diagram below", or "Answer true/false to questions about the video below". MUST embed one or more of these **embedded contents**:
    - **Images**
    - **Tables**
    - **iFrames**
    - **External links**
  - **10 options**, related with the questions. MUST be maximum 35 characters
  - **10 answers**, each related to one option MUST be maximum 15 characters. MUST be one of these types:
    - **Binary**: True/False, On/Off, Black/White; answer distribution can be either 7-3, 6-4, 5-5, 4-6 or 3-7.
    - **Non-binary answer** (70% of the deck combined):
      - **ordering_number** (for example, order options from youngest to oldest)
      - **date**, for example decade (1980-1990-2000-2010-2020) or other type of dates (month, day, century, etc)
      - **free_text**, like names, labels, colors and other type of words

## ⚖️ Deck specifications

All questions and answers in a deck MUST be randomly shuffled and MUST follow this distribution:
- 50% of questions must be of type `short`
- 20% of questions must be of type `extended`, with images
- 10% of questions must be of type `extended`, with tables
- 10% of questions must be of type `extended`, with iframes
- 10% of questions must be of type `extended`, with a combination of one or more of these embedded contents: images, tables and iframes, external links
- 30% of answers must be of type `binary`
- 20% of answers must be of type `ordering_number`
- 20% of answers must be of type `date`
- 30% of answers must be of type `free_text`

The order of the quiz cards across the deck MUST be random.
## 📁 Output File Structure

The folder `decks/<deck_name>` MUST contain:
1. `index.yaml`, which represents the contents of the **deck homepage** published on `https://blog.session.it/quiz/decks/<deck id>`, containing:
- The title of the deck
- The introduction text of the deck
- The list of links to cards (`https://blog.session.it/quiz/decks/<deck id>/cards/<card id>`), with the link to SVG (`https://blog.session.it/quiz/decks/<deck id>/cards/<card id>/content.svg`) and PDF (`https://blog.session.it/quiz/decks/<deck id>/cards/<card id>/content.pdf`) versions too.

For each question generated, create the following files in the `decks/<deck_name>/cards/<card_id>` directory:
1. `content.yaml`: Contains all content related to a quiz card, listed in "Quiz card specifications", except for the 10 answers:
  - The **Question**
  - The **Embedded Contents**
  - The **10 Options**
  - **Sources** , list of links to sources to certify the answer
  - The **URL** to the current card - `https://blog.session.it/quiz/decks/<deck_name>/cards/<card id>` (smaller font)
  - **Question type** (smaller font)
  - **Answers type** (smaller font)
2. `answers.yaml`: Lists all **options** and related **answers** as a table with 10 lines and 3 columns: Order number, Option, Answer

All YAML files must comply with the schemas defined in the `schemas/` folder.

## ✅ Content Quality

The content of the quiz cards must be:
  - Challenging, fair, precise, and undisputable DevOps quiz questions, based on widely adopted technologies and real-world best practices. Every card must:
  - Grounded in fact-checked, verifiable documentation.
  - Clear, stand-alone, and unambiguous.
  - Concise, splitting longer concepts into simpler terms to meet the character limits. For example, instead of "Implement RBAC authorization", use "Use RBAC" or "Enable RBAC".

## 🔍 Content Validation

All external content must be validated and follow these guidelines:

### Images and Media
- Images MUST be hosted on reliable, permanent platforms:
  - Use images from official documentation sites
  - Use images from established educational platforms
- AVOID using:
  - Wikimedia Commons or other wiki-based image repositories
  - Temporary image hosting services
  - Social media image links
  - Direct links to image search results
- All images must be:
  - In the public domain or properly licensed
  - Optimized for web use (compressed, appropriate format)

### Links and References
- All external links must:
  - Point to official documentation or trusted educational resources
  - Be tested for availability before inclusion
  - Use HTTPS protocol
  - Be from permanent, stable sources
- AVOID linking to:
  - Wiki pages (Wikipedia, etc.)
  - Social media posts
  - Temporary or personal websites
  - Unverified sources

### Content Testing
- Before finalizing any card:
  - Test all links for availability
  - Verify image accessibility
  - Check content licensing
  - Validate source reliability
  - Ensure content permanence

All output content (all card.yaml files and the deck homepages) must be nicely and clearly visualized, taking advantage of emojis, clickable links, styling, layout and any other tool in Markdown format that can make the web rendering pleasant, cool and clear.

## ✅ Content Checklist

- Are there exactly 10 well-formed, independent options?
- For binary questions: Are there 3–7 correct (True) answers?
- Is each option STRICTLY 20 characters or less?
- Are answers undisputable, based on trusted sources?
- Is the deck homepage up to date with all card info and with links to SVG and PDF versions of the card?
- Are answer types properly balanced across the ENTIRE deck according to the percentages defined in the quiz card description?
- Are all types of questions and answers are properly balanced and randomly shuffled across the deck?