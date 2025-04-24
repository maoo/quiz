# 🏆 DevOps Quiz Generation Prompt

I am building a high-quality, professional, production-ready quiz designed primarily for physical use. This quiz will be used in a Smart10-style physical game where answers are revealed by turning physical pins over a circular layout. Because of this, the SVG output must be extremely precise and readable.

Each deck file (in `decks/<deck id>.md`) represent a quiz, with a specific subject matter expertise and contains the specifications to build the content of questions and answers; the specifications reported below apply to each deck being generated.

Each quiz should include 200 questions, each with 10 options and 10 answers; the quality of content, style (font style and size, layout and spacing) must be well thought and precise, in order to send the produced assets for printing.

## 🎯 Objective

- Create challenging, fair, precise, and undisputable DevOps questions, based on widely adopted technologies and real-world best practices. Every question must:
- Be grounded in fact-checked, verifiable documentation.
- Align with real certification content.
- Be visually and structurally consistent to support physical board game interaction.

## ⚖️ Design and Answer Rules

- Each question must have exactly 10 options.
- Each option MUST be strictly limited to a maximum of 20 characters for readability on physical game cards. ABSOLUTELY NO EXCEPTIONS to this limit. Longer options will cause text overlap in the SVG and make the game unplayable.
- Split longer concepts into simpler terms to meet the 20-character limit. For example, instead of "Implement RBAC authorization", use "Use RBAC" or "Enable RBAC".
- Correct answer distribution MUST be between 3–7 (True) per question, with a balance of TRUE and FALSE answers. This is a STRICT requirement.
- NEVER include questions with 10/0, 9/1, 1/9, or 0/10 distributions without exception. Having all TRUE or all FALSE answers is not acceptable for game play.
- Each option must be clear, stand-alone, and unambiguous.
- Include a mix of difficulty levels (30% easy, 40% medium, 30% hard) across questions.

## 📁 Output File Structure

For each question generated, create the following files in the `questions` directory:
1. `<deck id>/<question id>-question.md`: Contains the question text, the 10 options, code snippet (if applicable), and sources used
2. `<deck id>/<question id>-output.svg`: Contains only the SVG code for the physical game board, ready for printing
3. `<deck id>/<question id>-answers.md`: Contains the list of options with their answers

Where `<question id>` is a unique numeric identifier for each question (e.g., "001", "042", "123", etc.). Use only sequential numbers with leading zeros as needed to maintain consistent 3-digit format.

Each `<question id>-question.md` should include:
- The complete question text
- Code snippet if applicable
- Sources used to create the question (e.g., documentation URLs, certification guides)
- The URL to github.com/maoo/quiz/... that points to the `<question id>-question.md` file

## 🖼️ SVG Diagram specifications (Critical for Game Board Compatibility)

Each question must be accompanied by a square SVG graphic. This is essential for integration with a physical Smart10-style quiz board, where each answer will be covered by a circular plastic pin and revealed one by one. 

The SVG layout must match the Smart10 game board design with:
- Optimised for 1100x1100 pixels size (equivalent to 110mm)
- A central area for the question
- A "question ring", 330 pixels diameter, around the question; the question must be placed inside this ring
- An "option ring", 700 pixels diameter (not visible in final output)
- An "answer ring", 900 pixels diameter (not visible in final output)
- All option texts must be positioned on a regular decagon and placed between the question ring and the option ring (but closer to the question ring); this will ensure that all option texts are equidistant
- All answer texts must be positioned on a regular decagon and stay on top of the answer ring; this will ensure that all answer texts are equidistant
- The position of answer text boxes must be exact and consistent across all diagrams and decks.

### 🖼️ SVG Layout Requirements

- Each diagram has 21 elements: 1 question, 10 options and 10 answers.
- The question sits in the center of the diagram:
  - If text of the question is smaller than 200 chars, show the text in a box, with multi-line (3-4 lines), word-wrap, centered, with 24px font-size
  - If the text of the question is bigger than 200 chars OR there is a `code snippet` included in the question, then do the following:
    - First, generate a QR code using the qrencode command:
      ```
      qrencode -o questions/<deck id>/<question id>-qr.png "https://github.com/maoo/quiz/blob/main/questions/<deck id>/<question id>-question.md"
      ```
    - Then, embed the QR code file in the SVG by directly referencing the image file:
      ```xml
      <!-- Direct QR code image reference -->
      <image x="-100" y="-100" width="200" height="200" xlink:href="<question id>-qr.png" />
      ```
    - Last, hide the question ring
- All option texts should be broken into 3-4 lines where appropriate to keep text box width smaller (maximum 200px width)
- All option texts should use standard SVG text elements with 24px font-size, centered
- All answer texts should use standard SVG text elements with 18px font-size, centered
- All SVG elements should use standard SVG primitives (rect, text, etc.) instead of foreignObject for maximum compatibility
- Include a white background rectangle for the entire SVG
- Option texts in the SVG should NOT include the number prefix (e.g., use "Kubernetes" not "1. Kubernetes")
- Do not include difficulty level indicators (e.g., "Easy", "Medium", "Hard") in the SVG output
- All texts must be placed to ensure ABSOLUTELY NO OVERLAP with other text elements
- The layout must never shift or distort between SVGs, so that physical answer pins align with the printed answer areas
- All text elements should use dominant-baseline="middle" and text-anchor="middle" for proper centering

## ✅ Final Checklist per Question

- Does the question type (code vs knowledge) follow spec?
- Are there exactly 10 well-formed, independent options?
- Is each option STRICTLY 20 characters or less?
- Are there 3–7 correct (True) answers?
- Are answers undisputable, based on trusted sources?
- The option and answer rings should not be visible; only the question ring should be visible
- The question text box should be contained inside the question ring
- Is the SVG:
  - Square 1100x1100 pixels?
  - Using pixel dimensions instead of millimeters?
  - Using consistent layout with exact positions?
  - Options and answers perfectly aligned and equidistant?
  - Text positioned with ABSOLUTELY NO OVERLAP between any text elements?
  - For questions >200 characters (or with code snippet), has the QR code been generated with qrencode and properly referenced in the SVG?
  - Are option texts formatted to display in 3-4 lines where needed?

### ✅ Text layout validation

Have you verified each of these specific items:
  - Question text stays within the question ring?
  - All options are formatted to display on 3-4 lines where appropriate?
  - All text uses proper font sizes (24px for question/options, 18px for answers)?
  - All text uses standard SVG text elements (not foreignObject)?
  - All options have the same distance from the question box center?
  - All options have the same distance among each other?
  - All answers have the same distance from the question box center?
  - All answers have the same distance among each other?
  - All option text stays between the question and the option rings?
  - All answer text stays on top of the answer ring?
  - There is no text overlap?
  - Is the SVG clearly readable in standard viewers?
  - Does the SVG layout match the Smart10 game board design?
  - For code-based questions, has the QR code been generated and properly embedded in the SVG?