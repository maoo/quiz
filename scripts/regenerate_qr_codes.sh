#!/bin/bash

# Usage: ./scripts/regenerate_qr_codes.sh <input_path1> [<input_path2> ...] [--url-prefix URL] [--output-prefix PATH]

set -e  # Exit on error

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <input_path1> [<input_path2> ...] [--url-prefix URL] [--output-prefix PATH]"
    exit 1
fi

# Get the script directory and project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Set up Python environment
cd "$PROJECT_ROOT"
poetry install

# Add src directory to PYTHONPATH
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"

# Call the Python CLI with all arguments
poetry run python -m src.qr_generator "$@"

echo "QR code regeneration complete!" 