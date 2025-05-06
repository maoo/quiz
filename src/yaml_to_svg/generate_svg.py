import os
import yaml
from pathlib import Path
import svgwrite
import argparse
import logging
from typing import Dict, List, Optional, Any, cast, Union
from src.file_processor import get_question_folders

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class YAMLToSVG:
    """Convert YAML-based quiz questions to SVG cards.
    
    This class handles the conversion of YAML-based quiz questions into SVG cards
    that can be printed or displayed. It supports both relative and absolute paths
    for input decks.
    """
    
    def __init__(self):
        parser = argparse.ArgumentParser(description='Convert YAML questions to SVG cards')
        parser.add_argument('input_paths', nargs='+', help='List of folders or content.yaml files to process')
        parser.add_argument('--card-width', type=float, default=210,
                          help='Card width in millimeters (default: 210)')
        parser.add_argument('--card-height', type=float, default=297,
                          help='Card height in millimeters (default: 297)')
        parser.add_argument('--font-size', type=int, default=12,
                          help='Font size for card text (default: 12)')
        parser.add_argument('--font-family', default='Arial',
                          help='Font family for card text (default: Arial)')
        args = parser.parse_args()

        self.input_paths = args.input_paths
        self.card_size = (args.card_width, args.card_height)
        self.font_size = args.font_size
        self.font_family = args.font_family

    def load_question(self, question_folder: str) -> Dict[str, Any]:
        """Load a question from its YAML file.
        
        Args:
            question_folder: The folder containing the question files
            
        Returns:
            Dict containing the question data, with an added 'question_folder' key
            
        Raises:
            FileNotFoundError: If no question file is found
        """
        folder = Path(question_folder)
        for filename in ["question.yaml", "content.yaml"]:
            question_file = folder / filename
            if question_file.exists():
                with open(question_file, 'r') as f:
                    data = cast(Dict[str, Any], yaml.safe_load(f))
                    data['question_folder'] = str(folder)
                    return data
        raise FileNotFoundError(f"No question file found in folder {question_folder}")
            
    def create_svg_card(self, question: Dict[str, Any], card_id: str) -> None:
        """Create an SVG card for a question.
        
        Args:
            question: Dictionary containing the question data
            card_id: The ID of the card to create
        """
        logger.info(f"Creating SVG for card {card_id} at {question['question_folder']}")
        output_file = os.path.join(question['question_folder'], "content.svg")
        logger.info(f"Output file: {output_file}")
        logger.info(f"Creating SVG for card {card_id} at {output_file}")
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
        question_folders = get_question_folders(self.input_paths)
        if not question_folders:
            logger.warning(f"No question folders found in the provided input paths.")
            return
        for question_folder in question_folders:
            try:
                question_data = self.load_question(question_folder)
                card_id = str(Path(question_folder).name)
                self.create_svg_card(question_data, card_id)
                logger.info(f"Created SVG for card {card_id}")
            except Exception as e:
                logger.error(f"Error processing card in {question_folder}: {str(e)}")
            
def main() -> None:
    try:
        converter = YAMLToSVG()
        converter.process_deck()
        logger.info(f"Successfully processed deck: {converter.input_paths}")
    except Exception as e:
        logger.error(f"Error processing deck: {str(e)}")
        exit(1)
    
if __name__ == "__main__":
    main() 