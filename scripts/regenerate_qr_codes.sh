#!/bin/bash

# Script to regenerate QR codes for all questions with the new URL format
# Usage: ./scripts/regenerate_qr_codes.sh [deck_name] [input_path] [output_path] [url_prefix]

set -e  # Exit on error

# Default paths and URL
DEFAULT_INPUT_PATH="decks"
DEFAULT_OUTPUT_PATH="/tmp/decks-qr-codes"
DEFAULT_URL_PREFIX="https://blog.session.it/quiz/decks"

# Function to print usage
print_usage() {
    echo "Usage: $0 [deck_name] [input_path] [output_path] [url_prefix]"
    echo "  deck_name: Optional. If provided, only processes questions from this deck"
    echo "            If not provided, processes all questions in all decks"
    echo "  input_path: Optional. Path to the decks directory (default: $DEFAULT_INPUT_PATH)"
    echo "  output_path: Optional. Path where QR codes will be written (default: $DEFAULT_OUTPUT_PATH)"
    echo "  url_prefix: Optional. Base URL for the QR codes (default: $DEFAULT_URL_PREFIX)"
    echo ""
    echo "Example: $0 devops-hero"
    echo "         $0 devops-hero /path/to/decks /path/to/output"
    echo "         $0 devops-hero /path/to/decks /path/to/output https://example.com/quiz/decks"
    echo "         $0"
}

# Check if help is requested
if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
    print_usage
    exit 0
fi

# Get parameters
deck_name="$1"
input_path="${2:-$DEFAULT_INPUT_PATH}"
output_path="${3:-$DEFAULT_OUTPUT_PATH}"
url_prefix="${4:-$DEFAULT_URL_PREFIX}"

# Ensure input path exists
if [ ! -d "$input_path" ]; then
    echo "Error: Input path '$input_path' does not exist"
    exit 1
fi

# Create output path if it doesn't exist
if [ ! -d "$output_path" ]; then
    echo "Creating output directory: $output_path"
    mkdir -p "$output_path"
fi

# Function to generate QR code for a question directory
generate_qr_code() {
    local question_dir="$1"
    local deck_name=$(echo "$question_dir" | cut -d'/' -f2)
    local card_id=$(basename "$question_dir")
    local qr_path="$output_path/$deck_name/cards/$card_id/qr.png"
    local url="$url_prefix/$deck_name/$card_id"
    
    # Create output directory if it doesn't exist
    mkdir -p "$(dirname "$qr_path")"
    
    echo "Generating QR code for $url"
    poetry run python -m src.qr_generator "$deck_name" "$card_id" "$url" "$qr_path"
    echo "Generated $qr_path"
}

# Find all question directories
if [ -n "$deck_name" ]; then
    if [ ! -d "$input_path/$deck_name" ]; then
        echo "Error: Deck '$deck_name' not found in $input_path"
        exit 1
    fi
    question_dirs=$(find "$input_path/$deck_name/cards" -type d -mindepth 1 -maxdepth 1)
else
    question_dirs=$(find "$input_path"/*/cards -type d -mindepth 1 -maxdepth 1)
fi

# Process each question directory
for dir in $question_dirs; do
    generate_qr_code "$dir"
done

echo "QR code regeneration complete!" 