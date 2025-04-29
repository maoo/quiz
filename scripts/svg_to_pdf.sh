#!/bin/bash

# Function to get SVG files based on event type
get_svg_files() {
    if [ "$1" == "manual" ]; then
        if [ -n "$2" ]; then
            find gh-pages/decks/$2/cards -name '*.svg'
        else
            find gh-pages/decks -name '*.svg'
        fi
    else
        echo "$3"
    fi
}

# Main script
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <event_type> <deck_name> [changed_files]"
    echo "event_type: manual or workflow"
    echo "deck_name: name of the deck to process (optional for manual)"
    echo "changed_files: list of changed files (required for workflow)"
    exit 1
fi

EVENT_TYPE="$1"
DECK_NAME="$2"
CHANGED_FILES="$3"

# Get the script directory and project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Set up Python environment
cd "$PROJECT_ROOT"
poetry install

# Add src directory to PYTHONPATH
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"

# Process each SVG file
failed_files=()
for svg_file in $(get_svg_files "$EVENT_TYPE" "$DECK_NAME" "$CHANGED_FILES"); do
    if [ -f "$svg_file" ] && [[ "$svg_file" == *.svg ]]; then
        output_file="${svg_file%.svg}.pdf"
        if ! poetry run python -m src.svg_to_pdf.converter "$svg_file" -o "$output_file" --width 11 --height 11; then
            failed_files+=("$svg_file")
        fi
    else
        echo "Warning: $svg_file not found or not an SVG file"
    fi
done

# Fail the script if any conversions failed
if [ ${#failed_files[@]} -ne 0 ]; then
    echo "Error: Failed to convert the following files:"
    printf '%s\n' "${failed_files[@]}"
    exit 1
fi

echo "All SVG files converted successfully" 