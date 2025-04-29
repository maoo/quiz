#!/bin/bash

# Function to get changed files for push event
get_changed_files() {
    local before_commit="$1"
    local current_commit="$2"
    
    if git rev-parse --verify --quiet "$before_commit" >/dev/null; then
        git diff --name-only "$before_commit" "$current_commit" | grep "decks/.*/cards/.*/content.yaml"
    else
        git ls-tree -r --name-only "$current_commit" | grep "decks/.*/cards/.*/content.yaml"
    fi
}

# Main script
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <event_type> <deck_name> [before_commit] [current_commit]"
    echo "event_type: manual or push"
    echo "deck_name: name of the deck to process (optional for manual)"
    echo "before_commit: commit hash before changes (required for push)"
    echo "current_commit: current commit hash (required for push)"
    exit 1
fi

EVENT_TYPE="$1"
DECK_NAME="$2"
BEFORE_COMMIT="$3"
CURRENT_COMMIT="$4"

# Create output directory if it doesn't exist
mkdir -p gh-pages/decks

# Get the script directory and project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Set up Python environment
cd "$PROJECT_ROOT"
poetry install

# Add src directory to PYTHONPATH
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"

# Generate SVGs based on event type
if [ "$EVENT_TYPE" = "manual" ]; then
    # For manual triggers, process specified deck or all decks
    poetry run python -m src.yaml_to_svg.generate_svg "${DECK_NAME}" --output-dir gh-pages/decks
else
    # For push events, process changed files
    if [ -z "$BEFORE_COMMIT" ] || [ -z "$CURRENT_COMMIT" ]; then
        echo "Error: before_commit and current_commit are required for push events"
        exit 1
    fi
    
    CHANGED_FILES=$(get_changed_files "$BEFORE_COMMIT" "$CURRENT_COMMIT")
    if [ -n "$CHANGED_FILES" ]; then
        # Process each changed file
        for file in $CHANGED_FILES; do
            DECK_NAME=$(echo "$file" | cut -d'/' -f2)
            poetry run python -m src.yaml_to_svg.generate_svg "$DECK_NAME" --output-dir gh-pages/decks
        done
    else
        echo "No YAML files to process"
    fi
fi

# List generated files
ls -lRt gh-pages/decks

echo "YAML to SVG conversion completed" 