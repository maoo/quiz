# Quiz Tools

A collection of tools for generating and converting quiz content.

## Features

- **SVG Generator**: Create SVG images for quiz questions with QR codes and answers
- **SVG to PDF Converter**: Convert SVG files to PDF with proper image handling and scaling

## Installation

The project uses Poetry for dependency management. To install:

```bash
# Install Poetry if you haven't already
curl -sSL https://install.python-poetry.org | python3 -

# Clone the repository
git clone https://github.com/yourusername/quiz-tools.git
cd quiz-tools

# Install dependencies
poetry install
```

## Usage

### SVG Generator

```python
from svg_generator import QuizSVGGenerator

# Create a generator instance
generator = QuizSVGGenerator()

# Generate an SVG from a markdown file
generator.generate_svg("input.md", "output.svg")
```

### SVG to PDF Converter

```python
from svg_to_pdf import SVGToPDFConverter

# Create a converter instance
converter = SVGToPDFConverter()

# Convert an SVG to PDF
converter.convert_svg_to_pdf("input.svg", "output.pdf")
```

## Command Line Interface

### SVG Generator

```bash
python -m svg_generator.generator input.md output.svg
```

### SVG to PDF Converter

```bash
python -m svg_to_pdf.converter input.svg -o output.pdf
```

## Development

### Running Tests

```bash
poetry run pytest
```

### Type Checking

```bash
poetry run mypy src
```

### Linting

```bash
poetry run black src tests
poetry run isort src tests
poetry run flake8 src tests
```

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request