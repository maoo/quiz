#!/bin/bash

# yaml_to_markdown.sh - Convert YAML cards to Markdown for a given deck
# Usage: ./scripts/yaml_to_markdown.sh <deck_dir>

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <input_path> [<input_path> ...]"
    exit 1
fi

INPUT_PATHS="$1"

# Set up Python environment
cd "$PROJECT_ROOT"
poetry install

# Add src directory to PYTHONPATH
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"

poetry run python -m src.yaml_to_markdown.generate_markdown "$INPUT_PATHS"

echo "YAML to Markdown conversion completed" 