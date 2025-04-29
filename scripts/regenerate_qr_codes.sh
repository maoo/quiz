#!/bin/bash

# Script to regenerate QR codes for all questions with the new URL format
# Usage: ./scripts/regenerate_qr_codes.sh [deck_name]

set -e  # Exit on error

# Function to print usage
print_usage() {
    echo "Usage: $0 [deck_name]"
    echo "  deck_name: Optional. If provided, only processes questions from this deck"
    echo "            If not provided, processes all questions in all decks"
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
if [ ! -d "decks" ]; then
    echo "Error: Must be run from project root directory"
    exit 1
fi

# Function to generate QR code for a question directory
generate_qr_code() {
    local question_dir="$1"
    local deck_name=$(echo "$question_dir" | cut -d'/' -f2)
    local card_id=$(basename "$question_dir")
    local qr_path="$question_dir/qr.png"
    local url="https://blog.session.it/quiz/decks/$deck_name/questions/$card_id/question"
    
    echo "Generating QR code for $url"
    qrencode -o "$qr_path" "$url"
    echo "Generated $qr_path"
}

# Get deck name from argument
deck_name="$1"

# Find all question directories
if [ -n "$deck_name" ]; then
    if [ ! -d "decks/$deck_name" ]; then
        echo "Error: Deck '$deck_name' not found"
        exit 1
    fi
    question_dirs=$(find "decks/$deck_name/questions" -type d -mindepth 1 -maxdepth 1)
else
    question_dirs=$(find decks/*/questions -type d -mindepth 1 -maxdepth 1)
fi

# Process each question directory
for dir in $question_dirs; do
    generate_qr_code "$dir"
done

echo "QR code regeneration complete!" 