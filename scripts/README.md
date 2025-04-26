# Scripts Documentation

## SVG Generation

The `generate_svgs.sh` script generates SVG files from markdown question files.

### Prerequisites

- Poetry must be installed and available in your PATH
- You must be in the project root directory when running the script

### Usage

```bash
# Generate SVGs for all questions in all decks
./scripts/generate_svgs.sh

# Generate SVGs for questions in a specific deck
./scripts/generate_svgs.sh devops-hero

# Show help
./scripts/generate_svgs.sh --help
```

### Testing Locally

1. Ensure you're in the project root directory
2. Make sure all dependencies are installed:
   ```bash
   poetry install
   ```
3. Run the script:
   ```bash
   # Test with devops-hero deck
   ./scripts/generate_svgs.sh devops-hero
   ```
4. Check the generated SVG files in the same directory as the markdown files

### Example

```bash
# Generate SVGs for the devops-hero deck
./scripts/generate_svgs.sh devops-hero

# This will process files like:
# - decks/devops-hero/questions/001-question.md
# - decks/devops-hero/questions/002-question.md
# etc.

# And generate corresponding SVG files:
# - decks/devops-hero/questions/001-output.svg
# - decks/devops-hero/questions/002-output.svg
# etc.
``` 