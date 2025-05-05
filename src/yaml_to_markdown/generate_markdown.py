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
        return self.content.get('question_content', 
                              self.content.get('question', 
                              self.content.get('content', 'No question content')))

class CardLoader:
    """Handles loading card data from YAML files."""
    
    def __init__(self, cards_path: Path):
        self.cards_path = cards_path
        
    def load_card(self, card_id: str) -> Dict[str, Any]:
        """Load a card from its YAML file."""
        for filename in ["content.yaml", "question.yaml"]:
            card_file = self.cards_path / card_id / filename
            if card_file.exists():
                try:
                    with open(card_file, 'r', encoding='utf-8') as f:
                        return yaml.safe_load(f)
                except yaml.YAMLError as e:
                    logger.error(f"Failed to parse YAML file {card_file}: {e}")
                    raise
                    
        raise FileNotFoundError(f"No content.yaml or question.yaml found for card: {card_id}")

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
    
    def __init__(self, input_path: str, output_path: str):
        self.input_path = Path(input_path)
        self.output_path = Path(output_path)
        self.cards_path = self.input_path / "cards"
        self.output_path.mkdir(parents=True, exist_ok=True)
        
        self.card_loader = CardLoader(self.cards_path)
        self.markdown_gen = MarkdownGenerator()
        
    def process_card(self, card_id: str) -> None:
        """Process a single card."""
        try:
            card_data = self.card_loader.load_card(card_id)
            card = Card(card_id, card_data)
            content = self.markdown_gen.card_to_markdown(card)
            
            output_file = self.output_path / f"{card_id}.md"
            output_file.write_text(content, encoding='utf-8')
            logger.info(f"Created markdown file for card {card_id}")
        except Exception as e:
            logger.error(f"Failed to process card {card_id}: {e}")
            
    def process_deck(self) -> None:
        """Process all cards in the deck."""
        try:
            readme_path = self.input_path / "index.yaml"
            if not readme_path.exists():
                logger.warning(f"Skipping deck {self.input_path} - index.yaml not found")
                return
                
            deck_meta = yaml.safe_load(readme_path.read_text(encoding='utf-8'))
            items = deck_meta.get('questions', deck_meta.get('cards', []))
            
            # Process cards
            cards = []
            for item in items:
                card_id = str(item['id']).zfill(3)
                try:
                    card_data = self.card_loader.load_card(card_id)
                    cards.append(Card(card_id, card_data))
                    self.process_card(card_id)
                except Exception as e:
                    logger.error(f"Failed to process card {card_id}: {e}")
                    
            # Create index
            index_content = self.markdown_gen.create_index_content(deck_meta, cards)
            (self.output_path / "index.md").write_text(index_content, encoding='utf-8')
            
        except Exception as e:
            logger.error(f"Failed to process deck: {e}")
            raise

def main() -> int:
    """Main entry point for the script."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Convert YAML cards to Markdown')
    parser.add_argument('input_path', help='Path to the deck directory')
    parser.add_argument('output_path', help='Path to output directory')
    
    args = parser.parse_args()
    
    try:
        input_path = Path(args.input_path)
        decks = []
        
        # Collect deck metadata
        if input_path.is_dir():
            for deck_dir in input_path.iterdir():
                if deck_dir.is_dir() and (deck_dir / "index.yaml").exists():
                    deck_meta = yaml.safe_load((deck_dir / "index.yaml").read_text(encoding='utf-8'))
                    deck_meta['path'] = deck_dir
                    decks.append(deck_meta)
        elif (input_path / "index.yaml").exists():
            deck_meta = yaml.safe_load((input_path / "index.yaml").read_text(encoding='utf-8'))
            deck_meta['path'] = input_path
            decks.append(deck_meta)
            
        # Process decks
        converter = YAMLToMarkdown(args.input_path, args.output_path)
        for deck in decks:
            deck_converter = YAMLToMarkdown(str(deck['path']), args.output_path / deck['path'].name)
            deck_converter.process_deck()
            
        logger.info("Conversion completed successfully")
        return 0
    except Exception as e:
        logger.error(f"Conversion failed: {e}")
        return 1

if __name__ == "__main__":
    exit(main()) 