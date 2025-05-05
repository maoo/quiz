import os
import yaml
from pathlib import Path
import svgwrite
import argparse
import logging
from typing import Dict, List, Optional, Any, cast, Union

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class YAMLToSVG:
    """Convert YAML-based quiz questions to SVG cards.
    
    This class handles the conversion of YAML-based quiz questions into SVG cards
    that can be printed or displayed. It supports both relative and absolute paths
    for input decks and configurable output locations.
    """
    
    def __init__(
        self,
        deck_path: Union[str, Path],
        output_dir: Optional[Union[str, Path]] = None,
        card_size: tuple[float, float] = (210, 297),  # A4 size in mm
        font_size: int = 12,
        font_family: str = 'Arial'
    ) -> None:
        """Initialize the YAML to SVG converter.
        
        Args:
            deck_path: Path to the deck directory or name of the deck
            output_dir: Optional output directory for SVG files
            card_size: Size of the SVG card in millimeters (width, height)
            font_size: Font size for the card text
            font_family: Font family for the card text
        """
        self.card_size = card_size
        self.font_size = font_size
        self.font_family = font_family
        
        # Handle deck path
        if isinstance(deck_path, str):
            if os.path.isabs(deck_path) or deck_path.startswith('./'):
                self.deck_path = Path(deck_path)
            else:
                self.deck_path = Path("decks") / deck_path
        else:
            self.deck_path = deck_path
            
        if not self.deck_path.exists():
            raise FileNotFoundError(f"Deck directory not found: {self.deck_path}")
            
        # Set up paths
        self.readme_path = self.deck_path / "index.yaml"
        if not self.readme_path.exists():
            raise FileNotFoundError(f"index.yaml not found in deck: {self.readme_path}")
            
        # Try both questions and cards directories
        for dir_name in ["questions", "cards"]:
            self.questions_path = self.deck_path / dir_name
            if self.questions_path.exists():
                break
        else:
            raise FileNotFoundError(f"Neither questions nor cards directory found in deck: {self.deck_path}")
        
        # Set up output directory
        if output_dir:
            self.output_path = Path(output_dir)
        else:
            self.output_path = self.deck_path / "cards"
            
        self.output_path.mkdir(parents=True, exist_ok=True)
        
    def load_question(self, card_id: str) -> Dict[str, Any]:
        """Load a question from its YAML file.
        
        Args:
            card_id: The ID of the card to load
            
        Returns:
            Dict containing the question data
            
        Raises:
            FileNotFoundError: If no question file is found
        """
        for filename in ["question.yaml", "content.yaml"]:
            question_file = self.questions_path / card_id / filename
            if question_file.exists():
                with open(question_file, 'r') as f:
                    return cast(Dict[str, Any], yaml.safe_load(f))
        raise FileNotFoundError(f"No question file found for card {card_id}")
            
    def create_svg_card(self, question: Dict[str, Any], card_id: str) -> None:
        """Create an SVG card for a question.
        
        Args:
            question: Dictionary containing the question data
            card_id: The ID of the card to create
        """
        output_file = self.output_path / f"{card_id}.svg"
        dwg = svgwrite.Drawing(
            filename=str(output_file),
            size=(f"{self.card_size[0]}mm", f"{self.card_size[1]}mm"),
            viewBox=(f"0 0 {self.card_size[0]} {self.card_size[1]}")
        )
        
        # Add background
        dwg.add(dwg.rect(
            insert=(0, 0),
            size=(str(self.card_size[0]), str(self.card_size[1])),
            fill='white'
        ))
        
        # Add question text
        text = dwg.add(dwg.g(
            font_size=str(self.font_size),
            font_family=self.font_family
        ))
        
        question_text = question.get('question_content', question.get('question', 'No question content'))
        text.add(dwg.text(
            question_text,
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
        logger.info(f"Saved SVG to {output_file}")
        
    def process_deck(self) -> None:
        """Process all questions in the deck.
        
        Raises:
            ValueError: If no questions or cards are found in the deck metadata
        """
        # Load deck metadata
        with open(self.readme_path, 'r') as f:
            deck_meta = cast(Dict[str, Any], yaml.safe_load(f))
            
        # Get items from either 'questions' or 'cards' in metadata
        items = deck_meta.get('questions', deck_meta.get('cards', []))
        if not items:
            raise ValueError(f"No questions or cards found in deck metadata: {self.readme_path}")
            
        # Process each question/card
        for item in items:
            card_id = str(item['id']).zfill(3)
            try:
                question_data = self.load_question(card_id)
                self.create_svg_card(question_data, card_id)
                logger.info(f"Created SVG for card {card_id}")
            except Exception as e:
                logger.error(f"Error processing card {card_id}: {str(e)}")
            
def main() -> None:
    parser = argparse.ArgumentParser(description='Convert YAML questions to SVG cards')
    parser.add_argument('deck_name', help='Name of the deck to process')
    parser.add_argument('--output-dir', default=None,
                      help='Output directory for SVG files')
    parser.add_argument('--card-width', type=float, default=210,
                      help='Card width in millimeters (default: 210)')
    parser.add_argument('--card-height', type=float, default=297,
                      help='Card height in millimeters (default: 297)')
    parser.add_argument('--font-size', type=int, default=12,
                      help='Font size for card text (default: 12)')
    parser.add_argument('--font-family', default='Arial',
                      help='Font family for card text (default: Arial)')
    
    args = parser.parse_args()
    
    try:
        converter = YAMLToSVG(
            args.deck_name,
            args.output_dir,
            card_size=(args.card_width, args.card_height),
            font_size=args.font_size,
            font_family=args.font_family
        )
        converter.process_deck()
        logger.info(f"Successfully processed deck: {args.deck_name}")
    except Exception as e:
        logger.error(f"Error processing deck {args.deck_name}: {str(e)}")
        exit(1)
    
if __name__ == "__main__":
    main() 