#!/bin/bash

# Exit on error
set -e

echo "Starting integration test..."

# Find first valid deck
echo "Looking for valid decks..."

TEMP_DIR=$(mktemp -d)
echo "Using temporary directory: $TEMP_DIR"

# Set up Python path for src imports
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"

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

# Create output directory
mkdir -p ${TEMP_DIR}/output
cp -Rf $DECK_DIR/* ${TEMP_DIR}/output
echo "Created output directory: ${TEMP_DIR}/output"

# Generate QR codes if specified
echo "########################"
echo "Generating QR codes..."
./scripts/generate_qr_codes.sh ${TEMP_DIR}/output

# Convert YAML to SVG for all cards
echo "########################"
echo "Converting YAML to SVG..."
./scripts/yaml_to_svg.sh ${TEMP_DIR}/output

# List generated SVG files
echo "########################"
echo "Generated SVG files:"
find ${TEMP_DIR}/output -type f -name "*.svg" 2>/dev/null || echo "No SVG files found"

# Verify SVGs were created
echo "########################"
echo "Verifying SVGs..."
if [ ! "$(find ${TEMP_DIR}/output -type f -name "*.svg" 2>/dev/null)" ]; then
    echo "Warning: No SVG files were generated!"
else
    # Check SVG contents
    for svg_file in $(find ${TEMP_DIR}/output -type f -name "*.svg"); do
        echo "########################"
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
echo "########################"
echo "Converting YAML to Markdown..."
./scripts/yaml_to_markdown.sh "${TEMP_DIR}/output"

# Verify Markdown files were created
echo "Verifying Markdown files..."
if [ ! "$(ls -A ${TEMP_DIR}/output/*.md 2>/dev/null)" ]; then
    echo "No Markdown files were generated!"
    exit 1
fi

# Verify QR codes were created if specified
echo "Verifying QR codes..."
for card_dir in "${TEMP_DIR}/output"/*/; do
    if [ -f "${card_dir}content.yaml" ]; then
        card_id=$(basename "$card_dir")
        qr_path="${TEMP_DIR}/output/${DECK_NAME}/cards/${card_id}/qr.png"
        if [ ! -f "$qr_path" ]; then
            echo "QR code for ${card_id} was not generated at $qr_path!"
            exit 1
        fi
    fi
done

# Convert SVGs to PDFs
echo "########################"
echo "Converting SVGs to PDFs..."
./scripts/svg_to_pdf.sh ${TEMP_DIR}/output

# Verify PDFs were created
echo "Verifying PDFs..."
if ! find "${TEMP_DIR}/output" -type f -name '*.pdf' | grep -q .; then
    echo "No PDF files were generated!"
    exit 1
fi

# Install poppler-utils if not installed
if [[ "$OSTYPE" == "darwin"* && ! -f "/opt/homebrew/bin/brew" ]]; then
    echo "Installing poppler-utils..."
    brew install poppler
elif [[ "$OSTYPE" == "linux-gnu" && ! -f "/usr/bin/apt" ]]; then
    echo "Installing poppler-utils..."
    sudo apt-get update && sudo apt-get install -y poppler-utils
fi

# Check PDF sizes and contents, use find to avoid empty directories
for pdf_file in $(find "${TEMP_DIR}/output" -type f -name '*.pdf'); do
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
    fi
    if ! pdftotext "$pdf_file" - | grep -q "[a-zA-Z]"; then
        echo "PDF file $pdf_file does not contain readable text!"
        exit 1
    fi
done

echo "Integration test completed successfully!"
echo "Generated files are in ${TEMP_DIR}/output/" 

# rm -rf ${TEMP_DIR}