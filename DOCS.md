# Project Documentation 📚

## Project Overview 🎯

This project is an AI-powered quiz generation system that creates high-quality, visually appealing quiz cards for various learning and assessment purposes. The system combines the power of AI language models (Claude and ChatGPT) with automated image generation to create engaging educational content.

### Use Cases 🎓
- **Professional Certification Preparation**: Create study materials for technical certifications (DevOps, Cloud, Security, etc.)
- **Educational Gaming**: Generate interactive quiz cards for classroom activities or educational games
- **Corporate Training**: Develop assessment materials for employee training programs
- **Personal Learning**: Create custom study decks for self-paced learning
- **Social Learning**: Generate quiz cards for group study sessions or family game nights

### Technical Approach 🛠️

The system follows a modular approach:

1. **Content Generation**
   - Uses AI prompts to generate questions, answers, and explanations
   - Supports multiple question types (code blocks, knowledge-based, etc.)
   - Maintains consistency through structured prompt engineering

2. **Visual Generation**
   - Converts text content into visually appealing SVG cards
   - Uses QR codes for easy access to digital content
   - Implements consistent styling and formatting

3. **Automation Pipeline**
   - Automated question generation and iteration
   - Batch processing of quiz decks
   - Version control for content management

4. **Output Formats**
   - Markdown files for content storage
   - SVG files for visual representation
   - Printable format for physical cards

### Key Components 🔑

- **Prompt Engineering**: Structured prompts in `quiz-prompt.md` guide AI generation
- **Content Management**: Organized storage of questions and assets
- **Visual Design**: Automated SVG generation with consistent styling
- **Printing System**: Optimized for high-quality physical output

## Prerequisites 🛠️

```sh
brew install qrencode
brew install librsvg
```

## Usage Guide 🚀

### Using Claude Code or ChatGPT

To generate new questions:
```sh
Follow instructions in quiz-prompt.md, to build a quiz deck of type devops-hero; generate 4 additional questions, only using the content of the prompt as context.
```

To reiterate on existing questions:
```sh
Follow instructions in quiz-prompt.md, to build a quiz deck of type devops-hero; only generate 2 questions, one of type code-block, one of type Knowledge-Based; you can reuse the .md files that were previously generated, but svg files must be recreated from scratch, only using the content of the prompt as context.
```

## Hardware Requirements 🖨️

### Recommended Printer Setup
- [Canon Pixma G650 Megatank](https://www.amazon.es/Canon-4620C006-PIXMA-G650/dp/B093QG1Y8C) - Impresora Fotográfica 3 en 1 (233€)
- [Papel Fotográfico Láser Brillante](https://www.amazon.es/Fotogr%C3%A1fico-Brillante-impresoras-Certificados-Calendarios/dp/B07VVDM9FJ) - Doble cara, A4, 250 g/m², 100 hojas
- [Laser Printer Discussion](https://www.reddit.com/r/Printing/comments/10un1q5/a_decent_laser_printer_for_heavyweight_paper/?tl=es-es) - Reddit thread about suitable printers

## Future Development Ideas 💡

### Planned Improvements
1. **Split quiz-prompt.md into sequential steps:**
   - Read and understand content requirements (from deck md file)
   - Generate questions, options, and answers in .md format under `questions/<deck id>`
   - Iterate on questions, parse contents from .md files and generate SVG files
   - Implement deterministic SVG generation using software instead of AI prompts

2. **Website Enhancements:**
   - Create a cleaner URI structure
   - Use a professional domain name (quiz.session.it or purchased domain)
   - Improve markdown file visualization
   - Enhance SVG visualization with better colors and fonts