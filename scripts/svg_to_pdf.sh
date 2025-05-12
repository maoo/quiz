#!/bin/bash

# TODO
# - All bash scripts in the scripts/ directory must accept an input_path as parameter, not an output_path
# - Go case by case and update the script to make sure the folder structure is unique
# - Create a common bash script to handle manual and workflow events

# Function to get SVG files based on event type
get_svg_files() {
    find $1 -name '*.svg'
}

# Main script
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <input_paths>"
    exit 1
fi

INPUT_PATHS="$@"

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
for svg_file in $(get_svg_files "$INPUT_PATHS"); do
    echo "Processing $svg_file"
    if [ -f "$svg_file" ] && [[ "$svg_file" == *.svg ]]; then
        echo "Converting $svg_file to PDF"
        output_file="${svg_file%.svg}.pdf"
        # if ! poetry run python -m src.svg_to_pdf.converter "$svg_file" --width 11 --height 11; then
        if ! poetry run python -m src.svg_to_pdf.converter "$svg_file"; then
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