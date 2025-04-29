#!/bin/bash

# test_generate_svgs.sh - Script to test SVG generation from YAML questions
# Usage: ./scripts/test_generate_svgs.sh [deck_name]
#   deck_name: Optional. If provided, only tests questions from this deck
#              If not provided, tests all questions in all decks

set -e  # Exit on error

# Function to print usage
print_usage() {
    echo "Usage: $0 [deck_name]"
    echo "  deck_name: Optional. If provided, only tests questions from this deck"
    echo "            If not provided, tests all questions in all decks"
    echo ""
    echo "Example: $0 devops-hero"
    echo "         $0"
}

# Check if help is requested
if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
    print_usage
    exit 0
fi

# Ensure we're in the project root
if [ ! -d "src" ] || [ ! -d "decks" ]; then
    echo "Error: Must be run from project root directory"
    exit 1
fi

# Ensure poetry is available
if ! command -v poetry &> /dev/null; then
    echo "Error: poetry is not installed or not in PATH"
    exit 1
fi

# Run the actual script
echo "Testing SVG generation..."
./scripts/yaml_to_svg.sh "$1"

# Verify SVG files were generated
echo "Verifying SVG files..."
if [ -n "$1" ]; then
    find "decks/$1/questions" -name 'card.svg' | while read -r svg_file; do
        if [ ! -s "$svg_file" ]; then
            echo "Error: Empty SVG file generated: $svg_file"
            exit 1
        fi
    done
else
    find decks -name 'card.svg' | while read -r svg_file; do
        if [ ! -s "$svg_file" ]; then
            echo "Error: Empty SVG file generated: $svg_file"
            exit 1
        fi
    done
fi

echo "SVG generation test completed successfully!" 