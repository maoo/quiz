#!/bin/bash

# Test script for generate_svgs.sh
# This script tests the functionality of generate_svgs.sh

set -e  # Exit on error

# Create a temporary directory for test files
TEST_DIR=$(mktemp -d)
trap 'rm -rf "$TEST_DIR"' EXIT

# Create a test deck structure
mkdir -p "$TEST_DIR/decks/test-deck/questions"
mkdir -p "$TEST_DIR/decks/test-deck2/questions"

# Create test markdown files
cat > "$TEST_DIR/decks/test-deck/questions/001-question.md" << EOF
# Test Question 1
This is a test question with some text.
EOF

cat > "$TEST_DIR/decks/test-deck/questions/002-question.md" << EOF
# Test Question 2
This is another test question with a QR code.
qr: https://example.com
EOF

cat > "$TEST_DIR/decks/test-deck2/questions/003-question.md" << EOF
# Test Question 3
This is a question from a different deck.
EOF

# Function to test with a specific deck
test_specific_deck() {
    echo "Testing with specific deck..."
    cd "$TEST_DIR"
    MARKDOWN_FILES="" ./scripts/generate_svgs.sh test-deck
    
    # Verify SVGs were created for the specific deck
    if [ ! -f "$TEST_DIR/decks/test-deck/questions/001-output.svg" ]; then
        echo "Error: SVG not generated for 001-question.md"
        exit 1
    fi
    if [ ! -f "$TEST_DIR/decks/test-deck/questions/002-output.svg" ]; then
        echo "Error: SVG not generated for 002-question.md"
        exit 1
    fi
    if [ -f "$TEST_DIR/decks/test-deck2/questions/003-output.svg" ]; then
        echo "Error: SVG generated for wrong deck"
        exit 1
    fi
}

# Function to test with MARKDOWN_FILES environment variable
test_markdown_files_env() {
    echo "Testing with MARKDOWN_FILES environment variable..."
    cd "$TEST_DIR"
    MARKDOWN_FILES="decks/test-deck2/questions/003-question.md" ./scripts/generate_svgs.sh
    
    # Verify only the specified file was processed
    if [ -f "$TEST_DIR/decks/test-deck/questions/001-output.svg" ]; then
        echo "Error: SVG generated for unspecified file"
        exit 1
    fi
    if [ -f "$TEST_DIR/decks/test-deck/questions/002-output.svg" ]; then
        echo "Error: SVG generated for unspecified file"
        exit 1
    fi
    if [ ! -f "$TEST_DIR/decks/test-deck2/questions/003-output.svg" ]; then
        echo "Error: SVG not generated for specified file"
        exit 1
    fi
}

# Function to test with no arguments (all decks)
test_all_decks() {
    echo "Testing with no arguments (all decks)..."
    cd "$TEST_DIR"
    MARKDOWN_FILES="" ./scripts/generate_svgs.sh
    
    # Verify SVGs were created for all decks
    if [ ! -f "$TEST_DIR/decks/test-deck/questions/001-output.svg" ]; then
        echo "Error: SVG not generated for 001-question.md"
        exit 1
    fi
    if [ ! -f "$TEST_DIR/decks/test-deck/questions/002-output.svg" ]; then
        echo "Error: SVG not generated for 002-question.md"
        exit 1
    fi
    if [ ! -f "$TEST_DIR/decks/test-deck2/questions/003-output.svg" ]; then
        echo "Error: SVG not generated for 003-question.md"
        exit 1
    fi
}

# Copy the script to the test directory
mkdir -p "$TEST_DIR/scripts"
cp scripts/generate_svgs.sh "$TEST_DIR/scripts/"

# Run tests
test_specific_deck
test_markdown_files_env
test_all_decks

echo "All tests passed successfully!" 