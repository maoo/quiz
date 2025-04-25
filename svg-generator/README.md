# SVG Generator for Quiz Questions

This tool generates SVG visualizations from markdown-formatted quiz questions.

## Installation

```bash
poetry install
```

## Usage

```bash
poetry run python generator.py <input_markdown> <output_svg>
```

## Example

```bash
poetry run python generator.py questions/001-question.md questions/001-output.svg
```

The tool will read the markdown file and generate an SVG visualization with the question title, options, and answers. 