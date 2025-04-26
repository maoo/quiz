#!/bin/bash

# Exit on error
set -e

echo "Starting integration test..."

# Create output directory
mkdir -p /tmp/integration-test/output

# Generate SVGs for all questions
echo "Generating SVGs..."
for question_file in decks/devops-hero/questions/*-question.md; do
    if [ -f "$question_file" ]; then
        filename=$(basename "$question_file" -question.md)
        echo "Processing $question_file..."
        poetry run python -m src.svg_generator.generator "$question_file" "/tmp/integration-test/output/${filename}.svg"
    fi
done

# Verify SVGs were created
echo "Verifying SVGs..."
if [ ! "$(ls -A /tmp/integration-test/output/*.svg 2>/dev/null)" ]; then
    echo "No SVG files were generated!"
    exit 1
fi

# Check SVG contents
for svg_file in /tmp/integration-test/output/*.svg; do
    echo "Checking $svg_file..."
    # Verify SVG contains question text
    if ! grep -q "text" "$svg_file"; then
        echo "SVG file $svg_file does not contain text elements!"
        exit 1
    fi
    
    # Verify SVG contains QR code if present in original markdown
    original_md=$(basename "$svg_file" .svg)-question.md
    if grep -q "qr:" "decks/devops-hero/questions/$original_md" && ! grep -q "image" "$svg_file"; then
        echo "SVG file $svg_file should contain QR code but doesn't!"
        exit 1
    fi
done

# Convert SVGs to PDFs
echo "Converting SVGs to PDFs..."
for svg_file in /tmp/integration-test/output/*.svg; do
    filename=$(basename "$svg_file" .svg)
    echo "Converting $svg_file..."
    poetry run python -m src.svg_to_pdf.converter "$svg_file" -o "/tmp/integration-test/output/${filename}.pdf"
done

# Verify PDFs were created
echo "Verifying PDFs..."
if [ ! "$(ls -A /tmp/integration-test/output/*.pdf 2>/dev/null)" ]; then
    echo "No PDF files were generated!"
    exit 1
fi

# Check PDF sizes and contents
for pdf_file in /tmp/integration-test/output/*.pdf; do
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
echo "Generated files are in /tmp/integration-test/output/" 