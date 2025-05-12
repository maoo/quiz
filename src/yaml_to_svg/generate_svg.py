import os
import yaml
from pathlib import Path
import svgwrite
import argparse
import logging
from typing import Dict, List, Optional, Any, cast, Union
from src.file_utils import get_question_folders, get_deck_folders

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class YAMLToSVG:
    """Convert YAML-based quiz questions to SVG cards.
    
    This class handles the conversion of YAML-based quiz questions into SVG cards
    that can be printed or displayed. It supports both relative and absolute paths
    for input decks.
    """
    
    def __init__(
        self,
        input_paths: Optional[List[str]] = None,
        card_size: Optional[tuple] = None,
        font_size: Optional[int] = None,
        font_family: Optional[str] = None
    ) -> None:
        if input_paths is not None:
            self.input_paths = input_paths
            self.card_size = card_size if card_size is not None else (210, 297)
            self.font_size = font_size if font_size is not None else 12
            self.font_family = font_family if font_family is not None else 'Arial'
            # Deck path logic
            self.deck_path = Path(input_paths[0])
            if not self.deck_path.exists():
                raise FileNotFoundError(f"Deck path {self.deck_path} does not exist")
            if not (self.deck_path / "index.yaml").exists():
                raise FileNotFoundError(f"index.yaml not found in {self.deck_path}")
            self.output_dir = getattr(self, 'output_dir', self.deck_path)
        else:
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
            # Deck path logic
            self.deck_path = Path(self.input_paths[0])
            if not self.deck_path.exists():
                raise FileNotFoundError(f"Deck path {self.deck_path} does not exist")
            if not (self.deck_path / "index.yaml").exists():
                raise FileNotFoundError(f"index.yaml not found in {self.deck_path}")
            self.output_dir = getattr(self, 'output_dir', self.deck_path)

    @property
    def output_path(self) -> Path:
        return Path(self.output_dir)

    def load_question(self, question_folder: str) -> dict[str, Any]:
        folder = Path(question_folder)
        if not folder.is_dir():
            for subdir in ["questions", "cards"]:
                candidate = self.deck_path / subdir / question_folder
                if candidate.is_dir():
                    folder = candidate
                    break
        for filename in ["question.yaml", "content.yaml"]:
            question_file = folder / filename
            if question_file.exists():
                with open(question_file, 'r') as f:
                    data = yaml.safe_load(f)
                    if not isinstance(data, dict):
                        raise ValueError(f"YAML file {question_file} did not return a dict")
                    data['question_folder'] = str(folder)
                    return data
        raise FileNotFoundError(f"No question file found in folder {folder}")
            
    def create_svg_card(self, question: dict, card_id: str) -> None:
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
        deck_folders = get_deck_folders(self.input_paths)
        question_folders = get_question_folders(deck_folders)
        if not question_folders:
            logger.warning(f"No question folders found in the provided input paths.")
            return
        with open(self.deck_path / "index.yaml", 'r') as f:
            meta = yaml.safe_load(f)
        for question_folder in question_folders:
            try:
                card_id = Path(question_folder).name
                question = self.load_question(question_folder)
                self.create_svg_card(question, card_id)
            except Exception as e:
                logger.error(f"Failed to process question {question_folder}: {e}")
            
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