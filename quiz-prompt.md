🏆 DevOps Quiz Generation Prompt (Production-Ready Edition)

I am building a high-quality, professional quiz designed for both digital and physical use. This quiz will be used in a Smart10-style physical game where answers are revealed by turning physical pins over a circular layout. Because of this, the SVG output must be extremely precise and readable.

Each deck file (in "decks/<deck id>.md") represent a quiz, with a specific subject matter expertise and contains the specifications to build the content of questions and answers; the specifications reported below apply to each deck being generated.

Each quiz should include 200 questions, each with 10 options and 10 answers.

📁 Output File Structure

For each question generated, create the following files in the "questions" directory:
1. <deck id>/<question id>-question.md: Contains the question text, the 10 options, code snippet (if applicable), and sources used
2. <deck id>/<question id>-output.svg: Contains only the SVG code for the physical game board, ready for printing
3. <deck id>/<question id>-answers.md: Contains the list of options with their answers

Where <id> is a unique numeric identifier for each question (e.g., "001", "042", "123", etc.). Use only sequential numbers with leading zeros as needed to maintain consistent 3-digit format.

Each <id>-question.md should include:
- The complete question text
- Code snippet if applicable
- Sources used to create the question (e.g., documentation URLs, certification guides)
- The URL to github.com/maoo/quiz/... that points to the <id>-question.md file

🎯 Objective

- Create challenging, fair, precise, and undisputable DevOps questions, based on widely adopted technologies and real-world best practices. Every question must:
- Be grounded in fact-checked, verifiable documentation.
- Align with real certification content.
- Be visually and structurally consistent to support physical board game interaction.

⚖️ Design and Answer Rules

- Each question must have exactly 10 options.
- Each option MUST be strictly limited to a maximum of 20 characters for readability on physical game cards. ABSOLUTELY NO EXCEPTIONS to this limit. Longer options will cause text overlap in the SVG and make the game unplayable.
- Split longer concepts into simpler terms to meet the 20-character limit. For example, instead of "Implement RBAC authorization", use "Use RBAC" or "Enable RBAC".
- Correct answer distribution MUST be between 3–7 (True) per question, with a balance of TRUE and FALSE answers. This is a STRICT requirement.
- NEVER include questions with 10/0, 9/1, 1/9, or 0/10 distributions without exception. Having all TRUE or all FALSE answers is not acceptable for game play.
- Each option must be clear, stand-alone, and unambiguous.
- Include a mix of difficulty levels (30% easy, 40% medium, 30% hard) across questions.


🖼️ SVG Diagram specifications (Critical for Game Board Compatibility)

Each question must be accompanied by a square SVG graphic. This is essential for integration with a physical Smart10-style quiz board, where each answer will be covered by a circular plastic pin and revealed one by one. 

The SVG layout must match the Smart10 game board design with:
- Optimised for 11x11 cm size
- A central area for the question
- A "question ring", 33mm diameter, around the question; the question must be place inside this ring
- An "option ring", 70mm diameter
- An "answer ring", 90mm diameter; this circle does not need to be shown
- All option texts must overlap with a regular decagon and placed between the question ring and the option ring (But closer to the question ring, than the option ring); this will ensure that all option texts are equidistant
- All answer texts must overlap with a regular decagon and stay on top of the answer ring; this will ensure that all answer texts are equidistant
- The position of answer text boxes must be exact and consistent across all diagrams and decks.

🖼️ SVG Layout Requirements

- Each diagram has 21 elements: 1 question, 10 options and 10 answers.
- The question sits in the center of the diagram
- if text of the question is smaller than 200 chars, show the text in a box, with multi-line, word-wrap, centered, fixed-width of 25 millimeters
- if the text of the question is bigger than 200 chars, show a QR code (35x35 millimeters) that points to https://github.com/maoo/quiz/blob/main/questions/<id>-question.md where <id> is the unique numeric identifier (e.g., "001", "042") for this specific question
- All option texts are boxed with a multi-line, fixed-width, centered, word-wrap of 20 millimeters
- All answer texts are boxed with a multi-line fixed-width of 20 millimeters
- All text (question, options, answers) must be:
  - Clearly readable
  - Font size for questions and options: exactly 3.5 millimeters
  - Font size for answers: exactly 2.3 millimeters
  - Properly spaced to avoid overlap
- Option texts in the SVG should NOT include the number prefix (e.g., use "Kubernetes" not "1. Kubernetes").
- Do not include difficulty level indicators (e.g., "Easy", "Medium", "Hard") in the SVG output.
- All texts must be placed to ensure ABSOLUTELY NO OVERLAP with texts. Text overlap makes the game unplayable and is an immediate rejection criteria.
- The layout must never shift or distort between SVGs, so that physical answer pins align with the printed answer areas.

✅ Final Checklist per Question

- Does the question type (code vs knowledge) follow spec?
- Are there exactly 10 well-formed, independent options?
- Is each option STRICTLY 30 characters or less?
- Are there 3–7 correct (True) answers?
- Are answers undisputable, based on trusted sources?
- Is the SVG:
  - Square (1000x1000)?
  - Using consistent layout with exact positions?
  - Using right font size?
  - Options and answers perfectly aligned and equidistant?
  - Text positioned with ABSOLUTELY NO OVERLAP between any text elements?
  - For questions >200 characters, is ONLY a QR code shown (no question text)?

✅ Text layout validation

Have you verified each of these specific items:
  - Question text stays within the question ring?
  - All options have the same distance from the question box center?
  - All options have the same distance among each other?
  - All answers have the same distance from the question box center?
  - All answers have the same distance among each other?
  - All option text stays on top of the option ring?
  - All answer text stays on top of the answer ring?
  - There is no text overlap?
  - Would the SVG be clearly readable when printed?
  - Does the SVG layout match the Smart10 game board design?
