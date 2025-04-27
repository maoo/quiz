# 🏆 DevOps Quiz Generation Prompt

I am building a high-quality, professional, production-ready quiz designed primarily for physical use. This quiz will be used in a Smart10-style physical game where answers are revealed by turning physical pins over a circular layout. Because of this, the SVG output must be extremely precise and readable.

Each deck file (in `decks/<deck id>/prompts/<deck id>.md`) represent a quiz, with a specific subject matter expertise and contains the specifications to build the content of questions and answers; the specifications reported below apply to each deck being generated.

Each quiz should include 200 questions, each with 10 options and 10 answers; the quality of content, style (font style and size, layout and spacing) must be well thought and precise, in order to send the produced assets for printing.

Each deck must have a homepage on https://blog.session.it/quiz/decks/<deck id>, that shows decks and questions; each deck must have a homepage (in `decks/<deck id>/README.md`) with:
- The title of the deck
- 3 Paragraphs description of the game, mostly around the questions, topics, sources, etc
- The list of questions, with a link to `https://blog.session.it/quiz/decks/<deck id>/questions/<question id>-question` for each of them ; also add a link to the SVG and PDF version of the question.

IMPORTANT! When new questions are added to an existing deck, make sure that:
  - The deck homepage is updated to report all questions
  - The types of questions and answers are properly balanced, following the "Design and Answer Rules" described below
  - CRITICAL: Answer types MUST strictly adhere to the percentage distribution defined in the "Answer Types" section below. Check ALL existing questions in the deck before adding new ones to maintain these ratios.
  - The types of questions and answers must be shuffled (randomly ordered) across the deck, using a random order, but trying to avoid having 2 questions or answers of the same type sequentially in the deck; if needed, change the number of an existing question, and update the deck homepage.

## 🎯 Objective

Create the content of the game following the "Output File Structure" described below; content must be:
  - Challenging, fair, precise, and undisputable DevOps questions, based on widely adopted technologies and real-world best practices. Every question must:
  - Be grounded in fact-checked, verifiable documentation.

All conent must be nicely and clearly visualized, taking advantage of emojis, clickable links, styling, layout and any other tool in Markdown format that can make the web rendering pleasant, cool and clear.

## ⚖️ Design and Answer Rules
- Each deck contains 200 designs.
- Each design has one question.
- Each question must have exactly 10 options.
- Each option (10 in total) has an answer (10 in total)
- Each option MUST be strictly limited to a maximum of 20 characters for readability on physical game cards. ABSOLUTELY NO EXCEPTIONS to this limit. Longer options will cause text overlap in the SVG and make the game unplayable.
- Questions can be of different types:
  - Text (50% of the deck): This type is used for text questions, for example, "what is the color of these logos"; the text must be maximum 80 characters, so be dry and succint
  - QR (50% of the deck): A QR is generated and visualized in the design, pointing to `https://blog.session.it/quiz/decks/<deck id>/questions/<question id>-question` , which will visualize the contents of `decks/<deck id>/questions/<question id>-question`; in this file, we can embed any content, of any type or length, to define our questions and options; the following distribution of content types must be respected:
    - YouTube embedded video (15% of the deck)
    - Embedded images (15% of the deck)
    - Embedded content (20% of the deck), for example links to external pages (make sure it opens in a new tab), tables, snippets
- Options are only of one type: a text string of maximum 80 characters
- Answers can be of different types, depending on the question (these percentages define the required Answer Type Distribution):
    - Binary answer (30% of the deck, STRICT MAXIMUM): True/False, On/Off, Black/White
    - Free answer (70% of the deck combined, MUST INCLUDE ALL THREE TYPES):
      - (20% of the deck) ordering number (for example, order options from youngest to oldest)
      - (20% of the deck) Decade (1980-1990-2000-2010-2020) or other type of dates (month, day, century, etc)
      - (30% of the deck) names, labels, colors and other type of words
- The type of questions and answers MUST be more varied and shuffled within the deck
- CRUCIAL: When adding to an existing deck, analyze ALL existing questions to ensure the deck maintains proper answer type balance. If a deck already has many binary (True/False) questions, subsequent additions MUST focus on the other answer types.
- Answers must be maximum 15 characters
- Split longer concepts into simpler terms to meet the 20-character limit. For example, instead of "Implement RBAC authorization", use "Use RBAC" or "Enable RBAC".
- Correct answer distribution for binary answers MUST be between 3–7 (True) per question, with a balance of TRUE and FALSE answers. This is a STRICT requirement.
- NEVER include questions with 10/0, 9/1, 1/9, or 0/10 binary answer distributions without exception. Having all TRUE or all FALSE answers is not acceptable for game play.
- Each option must be clear, stand-alone, and unambiguous.
- Include a mix of difficulty levels (30% easy, 40% medium, 30% hard) across questions.

## 📁 Output File Structure

For each question generated, create the following files in the `decks/<deck_name>/questions/<question_id>` directory:
1. `question.md`: Contains the question text, the 10 options, code snippet (if applicable); at the bottom, with a smaller font, add question type, answers type, sources used and URL to the question (using the template `https://blog.session.it/quiz/decks/<deck_name>/questions/<question_id>/question`).
2. `card.svg`: Contains only the SVG code for the physical game board, generated by GitHub Actions.
3. `card.pdf`: Contains only the PDF version of the SVG image, generated by GitHub Actions.
4. `answers.md`: Contains the list of options with their answers.
5. (for questions of type QR only) `qr.png`: Contains the QR code encoding `https://blog.session.it/quiz/decks/<deck_name>/questions/<question_id>/question` which is visualized in the diagram; this file must be generated using `qrencode -o decks/<deck_name>/questions/<question_id>/qr.png "https://blog.session.it/quiz/decks/<deck_name>/questions/<question_id>/question"` as soon as the `question.md` file is created.

Where `<question_id>` is a unique, sequential numeric identifier for each question (e.g., "001", "042", "123", etc.). Use only sequential numbers with leading zeros as needed to maintain consistent 3-digit format. Always create 001 first, unless the question already exists in the current deck folder.

Each `<question_id>-question.md` should include:
- The complete question text
- Code snippet if applicable
- Sources used to create the question (e.g., documentation URLs, certification guides)
- The URL to github.com/maoo/quiz/... that points to the `<question id>-question.md` file

## ✅ Final Checklist per Question

- Does the question type (code vs knowledge) follow spec?
- Are there exactly 10 well-formed, independent options?
- Is each option STRICTLY 20 characters or less?
- For binary questions: Are there 3–7 correct (True) answers?
- Are answers undisputable, based on trusted sources?
- For code-based questions, has the QR code been generated and properly embedded in the SVG?
- Is the deck homepage up to date with all questions and with links to SVG and PDF versions of the question?
- CRITICAL: Are answer types properly balanced across the ENTIRE deck according to the percentages defined in the "Answer Types" section?
- Are all types of questions and answers are properly balanced and shuffled across the deck?
- Does this question contribute to proper answer type distribution? If a deck is already heavy on one answer type, avoid adding more of that same type.

## 📊 Answer Type Distribution Tracking

When adding new questions:
1. Count the current number of each answer type in the deck
2. Calculate the current percentages
3. Determine which answer types are underrepresented
4. Prioritize those underrepresented answer types for new questions
5. Document your answer type analysis before adding new questions

Remember to refer to the percentages defined in the "Answer Types" section for the target distribution.