"""
YAML to Markdown Converter.

Converts YAML card files to Markdown format for GitHub Pages.
Creates individual card pages and an index page for navigation.
"""

import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Any

import yaml
from src.file_utils import get_question_folders

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class Card:
    """Represents a quiz card with its content and metadata."""
    id: str
    content: Dict[str, Any]
    
    @property
    def question_text(self) -> str:
        value = self.content.get('question_content', 
                  self.content.get('question', 
                  self.content.get('content', 'No question content')))
        return str(value)

class CardLoader:
    """Handles loading card data from YAML files in question folders."""
    def __init__(self, question_folders: list[str]):
        self.question_folders = question_folders

    def load_card(self, folder: str) -> dict:
        """Load a card from its YAML file in the corresponding question folder."""
        card_file = Path(folder) / "content.yaml"
        with open(card_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            if not isinstance(data, dict):  
                raise ValueError(f"YAML file {card_file} did not return a dict")
            answers_file = Path(folder) / "answers.yaml"
            with open(answers_file, 'r', encoding='utf-8') as f:
                data['answers'] = yaml.safe_load(f)
            data['question_folder'] = folder
            data['id'] = Path(folder).name
            return data

class MarkdownGenerator:
    """Handles generation of markdown content."""
    
    @staticmethod
    def card_to_markdown(card: Card) -> str:
        """Convert a card to markdown format."""
        lines = [
            f"# Question {card.id}",
            "",
            "## Question",
            card.question_text,
            ""
        ]
        
        if 'options' in card.content:
            lines.extend([
                "## Options",
                *[f"{i}. {opt}" for i, opt in enumerate(card.content['options'], 1)],
                ""
            ])
            
        # Map section keys to their display names
        section_names = {
            'question_type': 'Question Type',
            'answers_type': 'Answer Type'
        }
            
        for section, display_name in section_names.items():
            if section in card.content:
                lines.extend([
                    f"## {display_name}",
                    str(card.content[section]),
                    ""
                ])
                
        if 'sources' in card.content and card.content['sources']:
            lines.extend([
                "## Sources",
                *[f"- {source}" for source in card.content['sources']]
            ])
            
        return "\n".join(lines)
    
    @staticmethod
    def create_index_content(deck_meta: Dict, cards: List[Card]) -> str:
        """Create index markdown content."""
        lines = [
            f"# {deck_meta['title']}",
            ""
        ]
        
        if 'introduction' in deck_meta:
            lines.extend([deck_meta['introduction'], ""])
            
        lines.extend([
            "## Questions",
            *[f"- [Question {card.id}]({card.id}.md)" for card in cards]
        ])
        
        return "\n".join(lines)

class YAMLToMarkdown:
    """Main YAML to Markdown conversion class."""
    def __init__(self, input_paths: list[str]):
        self.input_paths = input_paths
        self.question_folders = get_question_folders(self.input_paths)
        self.card_loader = CardLoader(self.question_folders)
        self.markdown_gen = MarkdownGenerator()

    def process_card(self, card_data: dict) -> None:
        try:
            card_id = card_data['id']
            logger.info(f"Processing card: {card_id} -> Output: {Path(card_data['question_folder']) / f'content.md'}")
            card = Card(card_id, card_data)
            content = self.markdown_gen.card_to_markdown(card)
            output_file = Path(card_data['question_folder']) / f"content.md"
            output_file.write_text(content, encoding='utf-8')
            logger.info(f"Created markdown file for card {card_id}")
        except Exception as e:
            logger.error(f"Failed to process card {card_id}: {e}")

    def process_deck(self) -> None:
        try:
            if not self.question_folders:
                logger.warning(f"No question folders found in the provided input paths.")
                return
            # Try to find deck meta (index.yaml) in any parent of the question folders
            deck_meta = None
            for folder in self.input_paths:
                index_path = Path(folder) / "index.yaml"
                if index_path.exists():
                    deck_meta = yaml.safe_load(index_path.read_text(encoding='utf-8'))
                    break
            if not deck_meta:
                deck_meta = {"title": "Quiz Deck", "introduction": "", "questions": []}
            cards = []
            for folder in self.question_folders:
                card_id = Path(folder).name
                try:
                    card_data = self.card_loader.load_card(folder)
                    cards.append(Card(card_id, card_data))
                    self.process_card(card_data)
                except Exception as e:
                    logger.error(f"Failed to process card {card_id}: {e}")
            # Create index
            index_content = self.markdown_gen.create_index_content(deck_meta, cards)
            index_path = Path(folder) / "index.md"
            logger.info(f"Writing deck index to: {index_path}")
            index_path.write_text(index_content, encoding='utf-8')
        except Exception as e:
            logger.error(f"Failed to process deck: {e}")
            raise

def main() -> int:
    """Main entry point for the script."""
    import argparse
    parser = argparse.ArgumentParser(description='Convert YAML cards to Markdown')
    parser.add_argument('input_paths', nargs='+', help='List of folders or content.yaml files to process')
    args = parser.parse_args()
    try:
        converter = YAMLToMarkdown(args.input_paths)
        converter.process_deck()
        logger.info("Conversion completed successfully")
        return 0
    except Exception as e:
        logger.error(f"Conversion failed: {e}")
        return 1

if __name__ == "__main__":
    exit(main()) 