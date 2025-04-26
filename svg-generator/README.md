# SVG Generator for Quiz Questions 🎨

This tool generates beautiful SVG visualizations from markdown-formatted quiz questions.

## Installation 🛠️

```bash
cd svg-generator
poetry install
```

## Usage 🚀

```bash
poetry run python generator.py <input_markdown> <output_svg>
```

### Example

```bash
poetry run python generator.py questions/001-question.md questions/001-output.svg
```

## Features ✨

- Converts markdown questions to SVG format
- Generates visualizations with:
  - Question title
  - Multiple choice options
  - Answer indicators (TRUE/FALSE)
  - Integration with QR codes
  - Clean, professional layout
- Optimized for conversion to PDF with the svg-to-pdf tool

## Input Format 📝

The input markdown should follow this format:

```markdown
# Quiz Questions

## Question Title Here

1. Option One
2. Option Two (this will be FALSE)
3. Option Three (TRUE) - will be marked as TRUE
4. Option Four
...
```

Special words in options like "Use minimal base images" will be automatically marked as TRUE.

## QR Code Integration 📲

If a QR code image file exists with the same base name as your question file but with `-qr.png` suffix, it will be automatically included in the generated SVG.

For example:
- `001-question.md` → Question file
- `001-qr.png` → QR code image file that will be embedded

## Development 👩‍💻👨‍💻

### Running Tests

```bash
cd svg-generator
poetry install
poetry run pytest
```

### Running Linting

```bash
cd svg-generator
poetry run flake8 *.py tests
poetry run black *.py tests
```

## Output Preview 🖼️

The generated SVG will be a professional-looking visualization of your quiz question, ready for printing or web display. After generation, you can convert the SVG to PDF using the svg-to-pdf tool.