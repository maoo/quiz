"""
YAML to Markdown Converter.

Converts YAML card files to Markdown format for GitHub Pages.
Creates individual card pages and an index page for navigation.
"""

import logging
import os
from pathlib import Path
from typing import Dict

import yaml

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class YAMLToMarkdown:
    """
    Main YAML to Markdown conversion class.
    
    This class provides functionality to convert YAML card files
    to Markdown format suitable for GitHub Pages. It handles both
    individual card files and deck metadata.
    """
    
    def __init__(self, deck_path: str):
        """
        Initialize the YAML to Markdown converter.
        
        Args:
            deck_path: Path to the deck directory containing cards
        """
        self.deck_path = Path(deck_path)
        self.docs_path = self.deck_path / "docs"
        self.docs_path.mkdir(exist_ok=True)
        self.questions_path = self.deck_path / "questions"
        
    def load_question(self, card_id: str) -> Dict:
        """
        Load a card from its YAML file.
        
        Args:
            card_id: ID of the card to load
            
        Returns:
            Dict containing the card data
            
        Raises:
            FileNotFoundError: If card file doesn't exist
            yaml.YAMLError: If YAML parsing fails
        """
        card_file = self.questions_path / card_id / "question.yaml"
        try:
            with open(card_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.error(f"Card file not found: {card_file}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Failed to parse YAML file {card_file}: {e}")
            raise
            
    def create_markdown_content(self, card: Dict, card_id: str) -> str:
        """
        Create markdown content for a card.
        
        Args:
            card: Dictionary containing card data
            card_id: ID of the card
            
        Returns:
            Formatted markdown content as string
        """
        lines = []
        
        # Add card title
        lines.append(f"# Question {card_id}")
        lines.append("")
        
        # Add card text
        lines.append("## Question")
        lines.append(card['question'])
        lines.append("")
        
        # Add options if they exist
        if 'options' in card:
            lines.append("## Options")
            for i, option in enumerate(card['options'], 1):
                lines.append(f"{i}. {option}")
            lines.append("")
                
        # Add card type
        lines.append("## Type")
        lines.append(card['question_type'])
        lines.append("")
        
        # Add answer type
        lines.append("## Answer Type")
        lines.append(card['answers_type'])
        lines.append("")
        
        # Add sources if they exist
        if 'sources' in card and card['sources']:
            lines.append("## Sources")
            for source in card['sources']:
                lines.append(f"- {source}")
                
        return "\n".join(lines)
        
    def create_markdown_file(self, card: Dict, card_id: str) -> None:
        """
        Create a markdown file for a card.
        
        Args:
            card: Dictionary containing card data
            card_id: ID of the card
            
        Raises:
            IOError: If file creation fails
        """
        try:
            content = self.create_markdown_content(card, card_id)
            output_file = self.docs_path / f"{card_id}.md"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.debug(f"Created markdown file: {output_file}")
        except IOError as e:
            logger.error(f"Failed to create markdown file for card {card_id}: {e}")
            raise
            
    def create_index_markdown(self, deck_meta: Dict) -> None:
        """
        Create an index markdown file for the deck.
        
        Args:
            deck_meta: Dictionary containing deck metadata
            
        Raises:
            IOError: If file creation fails
        """
        lines = []
        
        # Add deck title
        lines.append(f"# {deck_meta['title']}")
        lines.append("")
        
        # Add introduction
        if 'introduction' in deck_meta:
            lines.append(deck_meta['introduction'])
            lines.append("")
            
        # Add cards list
        lines.append("## Questions")
        for card in deck_meta['questions']:
            card_id = str(card['id']).zfill(3)
            lines.append(f"- [Question {card_id}]({card_id}.md)")
            
        # Write index file
        try:
            with open(self.docs_path / "index.md", 'w', encoding='utf-8') as f:
                f.write("\n".join(lines))
            logger.debug("Created index markdown file")
        except IOError as e:
            logger.error(f"Failed to create index markdown file: {e}")
            raise
            
    def process_deck(self) -> None:
        """
        Process all cards in the deck.
        
        Raises:
            FileNotFoundError: If deck metadata file doesn't exist
            yaml.YAMLError: If YAML parsing fails
            IOError: If file operations fail
        """
        try:
            # Load deck metadata
            with open(self.deck_path / "README.yaml", 'r', encoding='utf-8') as f:
                deck_meta = yaml.safe_load(f)
                
            # Create index markdown
            self.create_index_markdown(deck_meta)
            logger.info("Created index markdown file")
                
            # Process each card
            for card in deck_meta['questions']:
                card_id = str(card['id']).zfill(3)
                try:
                    card_data = self.load_question(card_id)
                    self.create_markdown_file(card_data, card_id)
                    logger.info(f"Processed card {card_id}")
                except Exception as e:
                    logger.error(f"Failed to process card {card_id}: {e}")
                    raise
                    
        except FileNotFoundError:
            logger.error("Deck metadata file (README.yaml) not found")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Failed to parse deck metadata: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to process deck: {e}")
            raise
            
def main() -> int:
    """
    Command-line interface for the YAML to Markdown converter.
    
    Returns:
        int: Exit code (0 for success, 1 for failure)
    """
    try:
        converter = YAMLToMarkdown("decks/fun-math")
        converter.process_deck()
        logger.info("Successfully converted YAML to Markdown")
        return 0
    except Exception as e:
        logger.error(f"Conversion failed: {e}")
        return 1
    
if __name__ == "__main__":
    import sys
    sys.exit(main()) 