# Project Documentation 📚

## Prerequisites 🛠️

```sh
brew install qrencode
brew install librsvg
```

## Usage Guide 🚀

### Using Claude Code or ChatGPT

To generate new questions:
```sh
Follow instructions in quiz-prompt.md, to build a quiz deck of type devops-hero; only generate 2 questions, one of type code-block, one of type Knowledge-Based; only using the content of the prompt as context.
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