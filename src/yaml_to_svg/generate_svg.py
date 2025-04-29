import os
import yaml
from pathlib import Path
import svgwrite
from typing import Dict, List, Optional

class YAMLToSVG:
    def __init__(self, deck_path: str):
        self.deck_path = Path(deck_path)
        self.questions_path = self.deck_path / "questions"
        self.output_path = self.deck_path / "cards"
        self.output_path.mkdir(exist_ok=True)
        
    def load_question(self, question_id: str) -> Dict:
        """Load a question from its YAML file."""
        question_file = self.questions_path / question_id / "question.yaml"
        with open(question_file, 'r') as f:
            return yaml.safe_load(f)
            
    def create_svg_card(self, question: Dict, question_id: str) -> None:
        """Create an SVG card for a question."""
        # Create SVG drawing
        dwg = svgwrite.Drawing(
            filename=str(self.output_path / f"{question_id}.svg"),
            size=('210mm', '297mm'),  # A4 size
            viewBox=('0 0 210 297')
        )
        
        # Add background
        dwg.add(dwg.rect(insert=(0, 0), size=('210', '297'), fill='white'))
        
        # Add question text
        text = dwg.add(dwg.g(font_size='12', font_family='Arial'))
        text.add(dwg.text(
            question['question'],
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
        
    def process_deck(self) -> None:
        """Process all questions in the deck."""
        # Load deck metadata
        with open(self.deck_path / "README.yaml", 'r') as f:
            deck_meta = yaml.safe_load(f)
            
        # Process each question
        for question in deck_meta['questions']:
            question_id = str(question['id']).zfill(3)
            question_data = self.load_question(question_id)
            self.create_svg_card(question_data, question_id)
            
def main():
    # Process the fun-math deck
    converter = YAMLToSVG("decks/fun-math/questions/decks/fun-math")
    converter.process_deck()
    
if __name__ == "__main__":
    main() 