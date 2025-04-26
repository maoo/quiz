#!/bin/bash

# Test script for generate_svgs.sh
# This script tests the functionality of generate_svgs.sh

set -e  # Exit on error

# Function to test with a specific deck
test_specific_deck() {
    echo "Testing with specific deck..."
    MARKDOWN_FILES="" ./scripts/generate_svgs.sh devops-hero
    
    # Verify SVGs were created for the specific deck
    if [ ! -f "decks/devops-hero/questions/001/card.svg" ]; then
        echo "Error: SVG not generated for devops-hero deck"
        exit 1
    fi
}

# Function to test with MARKDOWN_FILES environment variable
test_markdown_files_env() {
    echo "Testing with MARKDOWN_FILES environment variable..."
    MARKDOWN_FILES="decks/devops-hero/questions/001/question.md" ./scripts/generate_svgs.sh
    
    # Verify only the specified file was processed
    if [ ! -f "decks/devops-hero/questions/001/card.svg" ]; then
        echo "Error: SVG not generated for specified file"
        exit 1
    fi
}

# Function to test with no arguments (all decks)
test_all_decks() {
    echo "Testing with no arguments (all decks)..."
    MARKDOWN_FILES="" ./scripts/generate_svgs.sh
    
    # Verify SVGs were created for all decks
    if [ ! -f "decks/devops-hero/questions/001/card.svg" ]; then
        echo "Error: SVG not generated for devops-hero deck"
        exit 1
    fi
}

# Run tests
test_specific_deck
test_markdown_files_env
test_all_decks

echo "All tests passed successfully!" 