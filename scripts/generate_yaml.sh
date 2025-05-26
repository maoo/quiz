#!/bin/bash

# generate_yaml.sh - Generate YAML content for a given deck
# Usage: ./scripts/generate_yaml.sh <deck_name>

if [ "$#" -eq 0 ]; then
    echo "Usage: $0 <deck_name>"
    exit 1
fi

# Check for OpenAI API key
if [ -z "$OPENAI_API_KEY" ]; then
    echo "Error: OPENAI_API_KEY environment variable is not set"
    echo "Please set your OpenAI API key using:"
    echo "export OPENAI_API_KEY='your-api-key-here'"
    exit 1
fi

# Set up Python environment
cd "$PROJECT_ROOT"
poetry install

# Add src directory to PYTHONPATH
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"

# Generate YAML content
if ! poetry run python -c "from src.yaml_generator import generate_deck_content; generate_deck_content('$1')"; then
    echo "Error: Failed to generate YAML content for deck: $1"
    echo "Please check your OpenAI API key and try again"
    exit 1
fi

echo "Successfully generated YAML content for deck: $1" 