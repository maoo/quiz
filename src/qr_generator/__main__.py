#!/usr/bin/env python3

import argparse
from .generator import generate_question_qr_code

def main() -> None:
    parser = argparse.ArgumentParser(description='Generate QR codes for quiz questions')
    parser.add_argument('deck_name', help='Name of the deck')
    parser.add_argument('card_id', help='ID of the card')
    parser.add_argument('--url-prefix', default='https://blog.session.it/quiz/decks',
                      help='Prefix for the URL (default: https://blog.session.it/quiz/decks)')
    parser.add_argument('--output-prefix', default='gh-pages/decks',
                      help='Prefix for the output path (default: gh-pages/decks)')
    
    args = parser.parse_args()
    
    result = generate_question_qr_code(
        args.deck_name,
        args.card_id,
        url_prefix=args.url_prefix,
        output_prefix=args.output_prefix
    )
    
    if result:
        print(f"Generated QR code at: {result}")
    else:
        print("Failed to generate QR code")
        exit(1)

if __name__ == '__main__':
    main() 