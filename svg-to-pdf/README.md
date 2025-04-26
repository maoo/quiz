# SVG to PDF Converter

A robust tool to convert SVG files to PDF format, preserving embedded images and ensuring proper sizing and rendering.

## Features

- Converts SVG files to PDF with a focus on maintaining visual fidelity
- Renders 1100x1100 pixel SVG canvas as 11x11cm in PDF
- Automatically embeds external images like QR codes
- Multiple conversion methods with automatic fallbacks:
  - CairoSVG (primary method)
  - WeasyPrint (HTML embedding method)
  - svglib/reportlab
  - Inkscape (if available)
  - rsvg-convert (if available)
  - Chrome/Chromium headless (if available)
  - ImageMagick (last resort)
- Handles malformed XML with automatic repair
- Command-line interface with configurable options

## Installation

```bash
# Install system dependencies (Ubuntu/Debian)
sudo apt-get install -y libcairo2-dev libpango1.0-dev libgdk-pixbuf2.0-dev librsvg2-dev

# Install the package
cd svg-to-pdf
poetry install
```

## Usage

```bash
# Using Poetry run
poetry run svg-to-pdf path/to/file.svg -o output.pdf

# After installation
svg-to-pdf path/to/file.svg -o output.pdf

# Set custom DPI (default is 254, which gives ~100px per cm)
poetry run svg-to-pdf input.svg -o output.pdf --dpi 300

# Enable verbose logging
poetry run svg-to-pdf input.svg -o output.pdf -v
```

### Options

- `-o, --output`: Specify output file path (default: same as input with .pdf extension)
- `--width`: Width in centimeters (default: 11)
- `--height`: Height in centimeters (default: 11)
- `-v, --verbose`: Enable verbose output
- `--dpi`: DPI for PDF generation (default: 254)

## Requirements

- Python 3.8+
- Primary dependencies:
  - CairoSVG
  - svglib/reportlab
  - lxml
  - Pillow
- Optional dependencies (used if available):
  - WeasyPrint
  - Inkscape
  - rsvg-convert
  - Chrome/Chromium
  - ImageMagick

## Development

### Running Tests

```bash
cd svg-to-pdf
poetry install
poetry run pytest
```

### Running Linting

```bash
cd svg-to-pdf
poetry run flake8 svg_to_pdf tests
poetry run black svg_to_pdf tests
```

### Architecture

The converter uses a chain of responsibility pattern with multiple converter implementations:

1. `CairoConverter`: Uses CairoSVG with XML validation via lxml
2. `WeasyPrintConverter`: Embeds SVG in HTML for better rendering
3. `SvglibConverter`: Uses svglib/reportlab
4. `InkscapeConverter`: Uses Inkscape CLI if available
5. `RsvgConverter`: Uses rsvg-convert if available
6. `ChromeConverter`: Uses Chrome/Chromium headless if available
7. `ImageMagickConverter`: Uses ImageMagick as a last resort

The converters are tried in order until one succeeds.

## Docker Usage

```bash
docker build -t svg-to-pdf .
docker run --rm -v $(pwd):/work svg-to-pdf svg-to-pdf input.svg -o output.pdf
```