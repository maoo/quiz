#!/usr/bin/env python3

import argparse
from .generator import generate_question_qr_code
from src.file_utils import get_question_folders, get_deck_folders, extract_deck_and_card_id
from typing import Callable, List, Tuple, Optional
from pathlib import Path

def process_questions(
    questionFolders: List[str],
    generate_question_qr_code: Callable[[str, str, str, str], Optional[str]],
    url_prefix: str
) -> Tuple[List[str], List[str]]:
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
            questionFolder,
            url_prefix
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
    parser = argparse.ArgumentParser(description="Generate QR codes for quiz questions.")
    parser.add_argument("input_paths", nargs="+", help="Paths to deck folders or content.yaml files")
    parser.add_argument("--url-prefix", default="https://blog.session.it/quiz/decks", help="URL prefix for QR codes")
    args = parser.parse_args()

    # If input is a content.yaml file, extract deck_name and card_id from the path
    if len(args.input_paths) == 1 and args.input_paths[0].endswith("content.yaml"):
        content_path = Path(args.input_paths[0])
        deck_name = content_path.parents[2].name
        card_id = content_path.parents[0].name
        output_dir = str(content_path.parent)
        generate_question_qr_code(deck_name, card_id, output_dir, args.url_prefix)
        return

    # Otherwise, treat as batch deck processing
    decks = get_deck_folders(args.input_paths)
    questions = get_question_folders(decks)
    if not questions:
        print("No question folders found in the provided input paths.")
        return
    process_questions(
        questions,
        generate_question_qr_code,
        url_prefix=args.url_prefix)

if __name__ == '__main__':
    main() 