#!/bin/bash

# yaml_to_markdown.sh - Convert YAML cards to Markdown for a given deck
# Usage: ./scripts/yaml_to_markdown.sh <deck_dir> <output_dir>

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <deck_dir> <output_dir>"
    exit 1
fi

DECK_DIR="$1"
OUTPUT_DIR="$2"

# Get the script directory and project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Set up Python environment
cd "$PROJECT_ROOT"
poetry install

# Add src directory to PYTHONPATH
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"

poetry run python -m src.yaml_to_markdown.generate_markdown "$DECK_DIR" "$OUTPUT_DIR"

echo "YAML to Markdown conversion completed" 