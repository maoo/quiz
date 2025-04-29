import os
import yaml
from pathlib import Path
import svgwrite
import argparse
from typing import Dict, List, Optional

class YAMLToSVG:
    def __init__(self, deck_name: str, output_dir: str = None):
        # If deck_name is a full path, use it as the deck path
        if os.path.isabs(deck_name) or deck_name.startswith('./'):
            self.deck_path = Path(deck_name)
        else:
            self.deck_path = Path("decks") / deck_name
            
        if not self.deck_path.exists():
            raise FileNotFoundError(f"Deck directory not found: {self.deck_path}")
            
        self.readme_path = self.deck_path / "README.yaml"
        if not self.readme_path.exists():
            raise FileNotFoundError(f"README.yaml not found in deck: {self.readme_path}")
            
        self.questions_path = self.deck_path / "questions"
        if not self.questions_path.exists():
            self.questions_path = self.deck_path / "cards"
            if not self.questions_path.exists():
                raise FileNotFoundError(f"Neither questions nor cards directory found in deck: {self.deck_path}")
        
        # If output_dir is specified, use it; otherwise use deck_path/cards
        if output_dir:
            self.output_path = Path(output_dir)
        else:
            self.output_path = self.deck_path / "cards"
            
        self.output_path.mkdir(parents=True, exist_ok=True)
        
    def load_question(self, card_id: str) -> Dict:
        """Load a question from its YAML file."""
        # Try both question.yaml and content.yaml
        for filename in ["question.yaml", "content.yaml"]:
            question_file = self.questions_path / card_id / filename
            if question_file.exists():
                with open(question_file, 'r') as f:
                    return yaml.safe_load(f)
        raise FileNotFoundError(f"No question file found for card {card_id}")
            
    def create_svg_card(self, question: Dict, card_id: str) -> None:
        """Create an SVG card for a question."""
        # Create SVG drawing
        output_file = self.output_path / f"{card_id}.svg"
        dwg = svgwrite.Drawing(
            filename=str(output_file),
            size=('210mm', '297mm'),  # A4 size
            viewBox=('0 0 210 297')
        )
        
        # Add background
        dwg.add(dwg.rect(insert=(0, 0), size=('210', '297'), fill='white'))
        
        # Add question text
        text = dwg.add(dwg.g(font_size='12', font_family='Arial'))
        text.add(dwg.text(
            question.get('question_content', question.get('question', 'No question content')),
            insert=('20', '40'),
            fill='black'
        ))
        
        # Add options if they exist
        if 'options' in question:
            y_pos = 60
            for i, option in enumerate(question['options'], 1):
                text.add(dwg.text(
                    f"{i}. {option}",
                    insert=('20', str(y_pos)),
                    fill='black'
                ))
                y_pos += 20
                
        # Save the SVG
        dwg.save()
        print(f"Saved SVG to {output_file}")
        
    def process_deck(self) -> None:
        """Process all questions in the deck."""
        # Load deck metadata
        with open(self.readme_path, 'r') as f:
            deck_meta = yaml.safe_load(f)
            
        # Check for either 'questions' or 'cards' in metadata
        if 'questions' in deck_meta:
            items = deck_meta['questions']
        elif 'cards' in deck_meta:
            items = deck_meta['cards']
        else:
            raise ValueError(f"No questions or cards found in deck metadata: {self.readme_path}")
            
        # Process each question/card
        for item in items:
            card_id = str(item['id']).zfill(3)
            try:
                question_data = self.load_question(card_id)
                self.create_svg_card(question_data, card_id)
                print(f"Created SVG for card {card_id}")
            except Exception as e:
                print(f"Error processing card {card_id}: {str(e)}")
            
def main():
    parser = argparse.ArgumentParser(description='Convert YAML questions to SVG cards')
    parser.add_argument('deck_name', help='Name of the deck to process')
    parser.add_argument('--output-dir', default=None,
                      help='Output directory for SVG files')
    
    args = parser.parse_args()
    
    try:
        converter = YAMLToSVG(args.deck_name, args.output_dir)
        converter.process_deck()
        print(f"Successfully processed deck: {args.deck_name}")
    except Exception as e:
        print(f"Error processing deck {args.deck_name}: {str(e)}")
        exit(1)
    
if __name__ == "__main__":
    main() 