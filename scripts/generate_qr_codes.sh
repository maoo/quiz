#!/bin/bash

# Function to process a single question file
process_question_file() {
    local file="$1"
    local DECK_NAME=$(echo "$file" | cut -d'/' -f2)
    local card_id=$(echo "$file" | cut -d'/' -f4)
    
    poetry run python -c "
from src.qr_generator import generate_question_qr_code
generate_question_qr_code('$DECK_NAME', '$card_id')
"
}

# Main script
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <event_type> [before_commit] [current_commit]"
    echo "event_type: manual or push"
    echo "before_commit: commit hash before changes (required for push)"
    echo "current_commit: current commit hash (required for push)"
    exit 1
fi

EVENT_TYPE="$1"
BEFORE_COMMIT="$2"
CURRENT_COMMIT="$3"

# Get the script directory and project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Set up Python environment
cd "$PROJECT_ROOT"
poetry install

# Add src directory to PYTHONPATH
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"

if [ "$EVENT_TYPE" = "manual" ]; then
    # For manual triggers, process all question files
    find decks -name "content.yaml" | while read -r file; do
        process_question_file "$file"
    done
else
    # For push events, only process changed files
    if [ -z "$BEFORE_COMMIT" ] || [ -z "$CURRENT_COMMIT" ]; then
        echo "Error: before_commit and current_commit are required for push events"
        exit 1
    fi
    
    # Check if we have a valid before commit
    if git rev-parse --verify --quiet "$BEFORE_COMMIT" >/dev/null; then
        CHANGED_FILES=$(git diff --name-only "$BEFORE_COMMIT" "$CURRENT_COMMIT" | grep "decks/.*/cards/.*/content.yaml")
    else
        # If no before commit, get all files in the current commit
        CHANGED_FILES=$(git ls-tree -r --name-only "$CURRENT_COMMIT" | grep "decks/.*/cards/.*/content.yaml")
    fi
    
    if [ -n "$CHANGED_FILES" ]; then
        for file in $CHANGED_FILES; do
            process_question_file "$file"
        done
    else
        echo "No question files to process"
    fi
fi

echo "QR code generation completed" 