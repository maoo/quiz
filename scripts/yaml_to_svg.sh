#!/bin/bash

INPUT_PATHS="$@"

# Get the script directory and project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Set up Python environment
cd "$PROJECT_ROOT"
poetry install

# Add src directory to PYTHONPATH
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"

poetry run python -m src.yaml_to_svg.generate_svg "${INPUT_PATHS}"

echo "YAML to SVG conversion completed" 