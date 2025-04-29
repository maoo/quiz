#!/bin/bash

# Exit on error
set -e

echo "Starting integration test..."

# Create output directory
mkdir -p /tmp/integration-test/output

# Generate SVGs and Markdown from YAML files
echo "Processing YAML files..."
for question_dir in decks/devops-hero/questions/*/; do
    if [ -f "${question_dir}question.yaml" ]; then
        question_id=$(basename "$question_dir")
        echo "Processing ${question_dir}question.yaml..."
        
        # Convert YAML to SVG
        poetry run python -m src.yaml_to_svg.generator "${question_dir}question.yaml" "/tmp/integration-test/output/${question_id}.svg"
        
        # Convert YAML to Markdown
        poetry run python -m src.yaml_to_markdown.generator "${question_dir}question.yaml" "/tmp/integration-test/output/${question_id}.md"
        
        # Generate QR code if specified in YAML
        if grep -q "qr:" "${question_dir}question.yaml"; then
            poetry run python -m src.qr_generator.generator "${question_dir}question.yaml" "/tmp/integration-test/output/${question_id}_qr.png"
        fi
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
    
    # Verify SVG contains QR code if present in original YAML
    question_id=$(basename "$svg_file" .svg)
    if grep -q "qr:" "decks/devops-hero/questions/${question_id}/question.yaml" && ! grep -q "image" "$svg_file"; then
        echo "SVG file $svg_file should contain QR code but doesn't!"
        exit 1
    fi
done

# Verify Markdown files were created
echo "Verifying Markdown files..."
if [ ! "$(ls -A /tmp/integration-test/output/*.md 2>/dev/null)" ]; then
    echo "No Markdown files were generated!"
    exit 1
fi

# Verify QR codes were created if specified
echo "Verifying QR codes..."
for question_dir in decks/devops-hero/questions/*/; do
    if [ -f "${question_dir}question.yaml" ] && grep -q "qr:" "${question_dir}question.yaml"; then
        question_id=$(basename "$question_dir")
        if [ ! -f "/tmp/integration-test/output/${question_id}_qr.png" ]; then
            echo "QR code for ${question_id} was not generated!"
            exit 1
        fi
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