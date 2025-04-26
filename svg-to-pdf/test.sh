#!/bin/bash
# Test script to verify the SVG to PDF conversion

set -e  # Exit on any error

# Install dependencies
echo "Installing dependencies..."
poetry install

# Define test files
TEST_SVGS=(
  "../decks/devops-hero/questions/002-output.svg"
  "../decks/devops-hero/questions/004-output.svg"
)

echo "Running converter tests..."

for TEST_SVG in "${TEST_SVGS[@]}"; do
  echo "------------------------------"
  echo "Testing conversion of: $TEST_SVG"
  echo "------------------------------"
  
  TEST_PDF="/tmp/test-$(basename "$TEST_SVG" .svg).pdf"
  
  # Verify input SVG exists
  if [ ! -f "$TEST_SVG" ]; then
    echo "Error: SVG file not found at $TEST_SVG"
    exit 1
  fi
  
  # Check for QR code
  QR_FILE="${TEST_SVG/-output.svg/-qr.png}"
  if [ -f "$QR_FILE" ]; then
    echo "QR code file exists: $QR_FILE"
    echo "QR file size: $(du -h "$QR_FILE" | cut -f1)"
  else
    echo "Warning: QR code file not found at $QR_FILE"
  fi
  
  # Show SVG content
  echo "Checking SVG content..."
  grep -A 1 "image" "$TEST_SVG" || echo "No image tag found in SVG"
  echo "Total lines in SVG: $(wc -l < "$TEST_SVG")"
  echo "SVG file validation:"
  if command -v xmllint > /dev/null; then
    if xmllint --noout "$TEST_SVG" 2>/dev/null; then
      echo "  XML is valid"
    else
      echo "  XML has errors"
    fi
  else
    echo "  xmllint not available for validation"
  fi
  
  # Run the conversion
  echo "Converting SVG to PDF..."
  poetry run svg-to-pdf "$TEST_SVG" -o "$TEST_PDF" --verbose
  
  # Check the result
  if [ -f "$TEST_PDF" ]; then
    echo "Success! PDF created at $TEST_PDF"
    echo "PDF file size: $(du -h "$TEST_PDF" | cut -f1)"
    
    # Verify PDF content using pdfinfo if available
    if command -v pdfinfo > /dev/null; then
      echo "PDF Info:"
      pdfinfo "$TEST_PDF" | grep -E "Pages|Page size|File size"
    fi
    
    # Check if PDF has content (file size > 1KB)
    FILE_SIZE=$(du -k "$TEST_PDF" | cut -f1)
    if [ "$FILE_SIZE" -lt 1 ]; then
      echo "Error: PDF file is too small (likely empty)"
      exit 1
    fi
    
    # Open the PDF if on macOS (optional)
    if [[ "$OSTYPE" == "darwin"* ]]; then
      echo "Opening PDF for inspection..."
      open "$TEST_PDF"
    fi
  else
    echo "Error: PDF file not created"
    exit 1
  fi
  
  echo "Test successful for $TEST_SVG"
  echo ""
done

echo "All tests completed successfully!"