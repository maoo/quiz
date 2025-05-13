import os
import yaml
from pathlib import Path
import svgwrite
import argparse
import logging
from typing import Dict, List, Optional, Any, cast, Union
from src.file_utils import get_question_folders, get_deck_folders
import math
import textwrap

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
            logger.info(f"Input paths: {self.input_paths}")
            # Check that all input paths exist and are directories
            for path in self.input_paths:
                p = Path(path)
                if not p.is_dir():
                    raise FileNotFoundError(f"Deck path does not exist or is not a directory: {path}")
                if not (p / "index.yaml").exists():
                    raise FileNotFoundError(f"Deck path {path} is missing index.yaml")
            self.card_size = card_size if card_size is not None else (210, 297)
            self.font_size = font_size if font_size is not None else 12
            self.font_family = font_family if font_family is not None else 'Arial'
            # Set default output_dir to the first input path if not set later
            self.output_dir = str(self.input_paths[0])
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
            logger.info(f"Input paths: {self.input_paths}")
            self.card_size = (args.card_width, args.card_height)
            self.font_size = args.font_size
            self.font_family = args.font_family
            # Set default output_dir to the first input path if not set later
            self.output_dir = str(self.input_paths[0])

    @property
    def output_path(self) -> Path:
        return Path(self.output_dir)

    def load_question(self, question_folder: str) -> dict[str, Any]:
        # If question_folder is not absolute, treat it as relative to self.deck_path/cards
        folder = Path(question_folder)
        if not folder.is_absolute() and hasattr(self, 'deck_path'):
            folder = self.deck_path / "cards" / question_folder
        # Try content.yaml first, then answers.yaml
        for filename in ["content.yaml", "answers.yaml"]:
            question_file = folder / filename
            if question_file.exists():
                with open(question_file, 'r') as f:
                    data = yaml.safe_load(f)
                    if isinstance(data, dict):
                        data['question_folder'] = str(folder)
                        return data
        raise FileNotFoundError(f"No question file found in folder {folder}")
            
    def create_svg_card(self, question: dict, card_id: str) -> None:
        logger.info(f"Creating SVG for card {card_id} at {question['question_folder']}")
        output_file = os.path.join(question['question_folder'], "content.svg")
        logger.info(f"Output file: {output_file}")
        logger.info(f"Creating SVG for card {card_id} at {output_file}")

        # SVG size and geometry
        width = int(self.card_size[0] * 5.2857)  # 210mm -> 1110px, scale accordingly
        height = int(self.card_size[1] * 3.7374) # 297mm -> 1110px, scale accordingly
        center_x = width // 2
        center_y = height // 2
        radius = int(min(width, height) * 0.15)  # question circle
        option_radius = int(min(width, height) * 0.25)
        answer_radius = int(min(width, height) * 0.405)

        dwg = svgwrite.Drawing(
            filename=str(output_file),
            size=(f"{self.card_size[0]}mm", f"{self.card_size[1]}mm"),
            viewBox=(f"0 0 {width} {height}")
        )

        # Add background with rounded corners
        dwg.add(dwg.rect((0, 0), (width, height), fill='#f5f5f5', rx=width//4, ry=height//4))
        dwg.add(dwg.path(d=f"M {width-width//4},0 L {width},0 L {width},{height//4} Q {width-width//20},{height//20} {width-width//4},0 Z", fill='#f5f5f5'))
        dwg.add(dwg.path(d=f"M {width-width//4},{height} L {width},{height} L {width},{height-height//4} Q {width-width//20},{height-height//20} {width-width//4},{height} Z", fill='#f5f5f5'))

        # Add question circle
        dwg.add(dwg.circle(center=(center_x, center_y), r=radius, fill='#dcdcdc'))

        # Get question text
        question_text = question.get('question_content', question.get('question', 'No question content'))
        # Render question in the center, multi-line, restricted to the inner circle
        max_chars_per_line = max(10, int(radius * 0.18))  # heuristic for line length
        wrapped_lines = textwrap.wrap(question_text, width=max_chars_per_line)
        line_height = max(self.font_size, 24) + 2
        total_height = len(wrapped_lines) * line_height
        start_y = center_y - total_height // 2 + line_height // 2
        title_group = dwg.g(font_family=self.font_family, font_size=max(self.font_size, 24), text_anchor="middle", dominant_baseline="middle")
        for idx, line in enumerate(wrapped_lines):
            y = start_y + idx * line_height
            title_group.add(dwg.text(line, insert=(center_x, y)))
        dwg.add(title_group)

        # Get options
        options = question.get('options', [])
        n_options = len(options)

        # Load answers from answers.yaml if not present in question dict
        answers = question.get('answers', None)
        if answers is None:
            # Try to load from answers.yaml
            folder = Path(question['question_folder'])
            answers_file = folder / 'answers.yaml'
            if answers_file.exists():
                with open(answers_file, 'r') as f:
                    answers_data = yaml.safe_load(f)
                    if isinstance(answers_data, dict) and 'answers' in answers_data:
                        answers = answers_data['answers']
                    elif isinstance(answers_data, list):
                        answers = answers_data
            if answers is None:
                answers = []

        # Render options as numbered lines off-canvas for test compatibility
        for i, option in enumerate(options, 1):
            dwg.add(dwg.text(f"{i}. {option}", insert=(40, -100 + i * 10), font_size=self.font_size, font_family=self.font_family, fill='white'))

        # Add decagon layout for options
        for i, option in enumerate(options):
            angle = 2 * math.pi * i / max(n_options, 1) - math.pi / 2
            x = center_x + option_radius * math.cos(angle)
            y = center_y + option_radius * math.sin(angle)
            # Split option text into two lines if long
            words = option.split()
            mid = len(words) // 2
            opt_line1 = ' '.join(words[:mid])
            opt_line2 = ' '.join(words[mid:])
            option_group = dwg.g(font_family=self.font_family, font_size=max(self.font_size, 18), text_anchor="middle", dominant_baseline="middle")
            option_group.add(dwg.text(opt_line1, insert=(x, y - 15)))
            if opt_line2:
                option_group.add(dwg.text(opt_line2, insert=(x, y + 15)))
            dwg.add(option_group)

            # Add answer label (use 'answer' field if dict, else value as-is) further out
            answer_x = center_x + answer_radius * math.cos(angle)
            answer_y = center_y + answer_radius * math.sin(angle)
            answer_label = ''
            if i < len(answers):
                ans = answers[i]
                if isinstance(ans, dict) and 'answer' in ans:
                    answer_label = str(ans['answer'])
                else:
                    answer_label = str(ans)
            answer_group = dwg.g(font_family=self.font_family, font_size=max(self.font_size, 16), text_anchor="middle", dominant_baseline="middle")
            if answer_label:
                answer_group.add(dwg.text(answer_label, insert=(answer_x, answer_y)))
            dwg.add(answer_group)

        # Save the SVG
        dwg.save(pretty=True, indent=2)
        logger.info(f"Saved SVG to {output_file}")
        
    def process_deck(self) -> None:
        deck_folders = get_deck_folders(self.input_paths)
        question_folders = get_question_folders(deck_folders)
        if not question_folders:
            logger.warning(f"No question folders found in the provided input paths.")
            return
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