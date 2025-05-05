#!/bin/bash

# Exit on error
set -e

echo "Starting integration test..."

# Find first valid deck
echo "Looking for valid decks..."

TEMP_DIR=$(mktemp -d)
echo "Using temporary directory: $TEMP_DIR"

DECK_DIR=""
for deck in decks/*/; do
    if [ -f "${deck}index.yaml" ] && [ -d "${deck}cards" ]; then
        DECK_DIR="$deck"
        echo "Found valid deck: $deck"
        break
    fi
done

if [ -z "$DECK_DIR" ]; then
    echo "No valid deck found! A valid deck must have a index.yaml and a cards/ directory."
    exit 1
fi

# Extract deck name from path
DECK_NAME=$(basename "$DECK_DIR")
echo "Processing deck: $DECK_NAME"

# Create output directory
mkdir -p ${TEMP_DIR}/output
echo "Created output directory: ${TEMP_DIR}/output"

# Generate SVGs and Markdown from YAML files
echo "Processing YAML files..."

# Generate QR codes if specified
echo "Generating QR codes..."
for card_dir in "${DECK_DIR}cards"/*/; do
    if [ -f "${card_dir}content.yaml" ] && grep -q "qr:" "${card_dir}content.yaml"; then
        card_id=$(basename "$card_dir")
        poetry run python -m src.qr_generator.generate_qr "$DECK_NAME" --output-dir ${TEMP_DIR}/output
    fi
done

# Convert YAML to SVG for all cards
echo "Converting YAML to SVG..."
echo "Running command: poetry run python -m src.yaml_to_svg.generate_svg \"$DECK_NAME\" --output-dir ${TEMP_DIR}/output"
poetry run python -m src.yaml_to_svg.generate_svg "$DECK_NAME" --output-dir ${TEMP_DIR}/output

# List generated SVG files
echo "Generated SVG files:"
ls -la ${TEMP_DIR}/output/*.svg 2>/dev/null || echo "No SVG files found"

# Verify SVGs were created
echo "Verifying SVGs..."
if [ ! "$(ls -A ${TEMP_DIR}/output/*.svg 2>/dev/null)" ]; then
    echo "Warning: No SVG files were generated!"
else
    # Check SVG contents
    for svg_file in ${TEMP_DIR}/output/*.svg; do
        echo "Checking $svg_file..."
        # Verify SVG contains question text
        if ! grep -q "text" "$svg_file"; then
            echo "SVG file $svg_file does not contain text elements!"
            exit 1
        fi
        
        # Verify SVG contains QR code if present in original YAML
        card_id=$(basename "$svg_file" .svg)
        if [ -f "${DECK_DIR}cards/${card_id}/content.yaml" ] && \
           grep -q "qr:" "${DECK_DIR}cards/${card_id}/content.yaml" && \
           ! grep -q "image" "$svg_file"; then
            echo "SVG file $svg_file should contain QR code but doesn't!"
            exit 1
        fi
    done
fi

# Convert YAML to Markdown for all cards
echo "Converting YAML to Markdown..."
echo "poetry run python -m src.yaml_to_markdown.generate_markdown ${DECK_DIR} ${TEMP_DIR}/output"
poetry run python -m src.yaml_to_markdown.generate_markdown "${DECK_DIR}" "${TEMP_DIR}/output"

# Verify Markdown files were created
echo "Verifying Markdown files..."
if [ ! "$(ls -A ${TEMP_DIR}/output/*.md 2>/dev/null)" ]; then
    echo "No Markdown files were generated!"
    exit 1
fi

# Verify QR codes were created if specified
echo "Verifying QR codes..."
for card_dir in "${DECK_DIR}cards"/*/; do
    if [ -f "${card_dir}content.yaml" ] && grep -q "qr:" "${card_dir}content.yaml"; then
        card_id=$(basename "$card_dir")
        if [ ! -f "${TEMP_DIR}/output/${card_id}_qr.png" ]; then
            echo "QR code for ${card_id} was not generated!"
            exit 1
        fi
    fi
done

# Convert SVGs to PDFs
echo "Converting SVGs to PDFs..."
for svg_file in ${TEMP_DIR}/output/*.svg; do
    if [ -f "$svg_file" ]; then
        filename=$(basename "$svg_file" .svg)
        echo "Converting $svg_file..."
        poetry run python -m src.svg_to_pdf.converter "$svg_file" -o "${TEMP_DIR}/output/${filename}.pdf"
    fi
done

# Verify PDFs were created
echo "Verifying PDFs..."
if [ ! "$(ls -A ${TEMP_DIR}/output/*.pdf 2>/dev/null)" ]; then
    echo "No PDF files were generated!"
    exit 1
fi

# Check PDF sizes and contents
for pdf_file in ${TEMP_DIR}/output/*.pdf; do
    echo "Checking $pdf_file..."
    # Check PDF size is reasonable (more than 1KB)
    FILE_SIZE=$(du -k "$pdf_file" | cut -f1)
    if [ "$FILE_SIZE" -lt 1 ]; then
        echo "PDF file $pdf_file is too small (likely empty)"
        exit 1
    fi
    
    # Verify PDF contains text (using pdftotext)
    if ! command -v pdftotext &> /dev/null; then
        echo "Installing poppler-utils..."
        if [[ "$OSTYPE" == "darwin"* ]]; then
            brew install poppler
        else
            sudo apt-get update && sudo apt-get install -y poppler-utils
        fi
    fi
    if ! pdftotext "$pdf_file" - | grep -q "[a-zA-Z]"; then
        echo "PDF file $pdf_file does not contain readable text!"
        exit 1
    fi
done

echo "Integration test completed successfully!"
echo "Generated files are in ${TEMP_DIR}/output/" 