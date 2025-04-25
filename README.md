## Prerequisites

```sh
brew install qrencode
brew install librsvg
```

## Usage

Using Claude Code (or ChatGPT), it should be possible to ask:
```
Follow instructions in quiz-prompt.md, to build a quiz deck of type devops-hero; only generate 2 questions, one of type code-block, one of type Knowledge-Based; only using the content of the prompt as context. 
```

To reiterate on existing questions:
```
Follow instructions in quiz-prompt.md, to build a quiz deck of type devops-hero; only generate 2 questions, one of type code-block, one of type Knowledge-Based; you can reuse the .md files that were previously generated, but svg files must be recreated from scratch, only using the content of the prompt as context. 
```

## Printers, ink and paper
- Canon Pixma G650 Megatank, Impresora Fotográfica 3 en 1 (233€) - https://www.amazon.es/Canon-4620C006-PIXMA-G650/dp/B093QG1Y8C
- Papel Fotográfico Láser Brillante de Doble cara, A4, 250 g/m², 100 hojas, para impresoras LASER (14€)- https://www.amazon.es/Fotogr%C3%A1fico-Brillante-impresoras-Certificados-Calendarios/dp/B07VVDM9FJ
- https://www.reddit.com/r/Printing/comments/10un1q5/a_decent_laser_printer_for_heavyweight_paper/?tl=es-es

## Future ideas
- Split quiz-prompt.md into sequential steps:
  - Read and unsterstand content requirements (coming from the deck md file)
  - Generate questions, options and answers and store them into .md format, under the `questions/<deck id>` folder
  - Iterate on each question, parse contents from .md files and generate the SVG file
  - SVG generation should be done using a software, not an AI prompt (to make it fully deterministic)
- Build a nicer website
  - Build a shorter, cleaner URI space
  - Use a nice host name (either buy, or use quiz.session.it)
  - Improve md file visualization
  - Improve SVG visualization (color and fonts mostly)