#!/bin/bash

# generate_svgs.sh - Script to generate SVG files from markdown questions
# Usage: ./scripts/generate_svgs.sh [deck_name]
#   deck_name: Optional. If provided, only processes questions from this deck
#              If not provided, processes all questions in all decks
# Environment variables:
#   MARKDOWN_FILES: Optional. Space-separated list of markdown files to process.
#                   If provided, this takes precedence over deck_name.

set -e  # Exit on error

# Function to get markdown files based on deck name
get_markdown_files() {
    local deck_name="$1"
    if [ -n "$MARKDOWN_FILES" ]; then
        echo "$MARKDOWN_FILES"
    elif [ -n "$deck_name" ]; then
        find "decks/$deck_name/questions" -name 'question.md'
    else
        find decks -name 'question.md'
    fi
}

# Function to print usage
print_usage() {
    echo "Usage: $0 [deck_name]"
    echo "  deck_name: Optional. If provided, only processes questions from this deck"
    echo "            If not provided, processes all questions in all decks"
    echo ""
    echo "Environment variables:"
    echo "  MARKDOWN_FILES: Optional. Space-separated list of markdown files to process."
    echo "                  If provided, this takes precedence over deck_name."
    echo ""
    echo "Example: $0 devops-hero"
    echo "         $0"
    echo "         MARKDOWN_FILES='decks/deck1/questions/001/question.md decks/deck2/questions/002/question.md' $0"
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

# Process each markdown file
echo "Generating SVGs..."
for file in $(get_markdown_files "$1"); do
    if [ -f "$file" ]; then
        output_file="$(dirname "$file")/card.svg"
        echo "Processing $file -> $output_file"
        poetry run python -m src.svg_generator.generator "$file" "$output_file"
    fi
done

echo "SVG generation complete!" 