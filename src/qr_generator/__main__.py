#!/usr/bin/env python3

import argparse
from .generator import generate_question_qr_code
from src.file_utils import get_question_folders, extract_deck_and_card_id
import os

def process_questions(questionFolders, generate_question_qr_code, url_prefix):
    generated = []
    errors = []
    for questionFolder in questionFolders:
        deck_name, card_id = extract_deck_and_card_id(questionFolder)
        print(f"Processing {questionFolder} for deck {deck_name} and card {card_id}")
        if not deck_name or not card_id:
            print(f"Skipping {questionFolder}: could not extract deck_name/card_id")
            errors.append(questionFolder)
            continue
        result = generate_question_qr_code(
            deck_name,
            card_id,
            output_dir=questionFolder,
            url_prefix=url_prefix
        )
        if result:
            print(f"Generated QR code at: {result}")
            generated.append(result)
        else:
            print(f"Failed to generate QR code for {questionFolder}")
            errors.append(questionFolder)
    print(f"\nSummary: {len(generated)} QR codes generated, {len(errors)} errors.")
    if errors:
        print("Errors for files:")
        for e in errors:
            print(f"  {e}")
    return generated, errors 

def main() -> None:
    parser = argparse.ArgumentParser(description='Generate QR codes for quiz questions')
    parser.add_argument('input_paths', nargs='+', help='List of folders or content.yaml files to process')
    parser.add_argument('--url-prefix', default='https://blog.session.it/quiz/decks',
                      help='Prefix for the URL (default: https://blog.session.it/quiz/decks)')
    args = parser.parse_args()

    questions = get_question_folders(args.input_paths)
    if not questions:
        print("No question folders found in the provided input paths.")
        return

    process_questions(
        questions,
        generate_question_qr_code,
        url_prefix=args.url_prefix)

if __name__ == '__main__':
    main() 