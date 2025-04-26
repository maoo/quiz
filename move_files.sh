#!/bin/bash

# Move files for each question
for i in {001..018}; do
    # Create directory if it doesn't exist
    mkdir -p "$i"
    
    # Move question files
    mv "${i}-question.md" "$i/question.md" 2>/dev/null
    mv "${i}-answers.md" "$i/answers.md" 2>/dev/null
    mv "${i}-qr.png" "$i/qr.png" 2>/dev/null
    mv "${i}-output.svg" "$i/card.svg" 2>/dev/null
    mv "${i}-output.pdf" "$i/card.pdf" 2>/dev/null
done 