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
    
    def __init__(self, input_path: str, output_path: str):
        """
        Initialize the YAML to Markdown converter.
        
        Args:
            input_path: Path to the input deck directory containing cards
            output_path: Path to the output directory for markdown files
        """
        self.input_path = Path(input_path)
        self.output_path = Path(output_path)
        self.cards_path = self.input_path / "cards"
        
        # Create output directory if it doesn't exist
        self.output_path.mkdir(parents=True, exist_ok=True)
        
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
        # Try content.yaml first, then question.yaml
        for filename in ["content.yaml", "question.yaml"]:
            card_file = self.cards_path / card_id / filename
            if card_file.exists():
                try:
                    with open(card_file, 'r', encoding='utf-8') as f:
                        return yaml.safe_load(f)
                except yaml.YAMLError as e:
                    logger.error(f"Failed to parse YAML file {card_file}: {e}")
                    raise
        
        logger.error(f"No content.yaml or question.yaml found for card: {card_id}")
        raise FileNotFoundError(f"No content.yaml or question.yaml found for card: {card_id}")
            
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
        question_text = card.get('question_content', card.get('question', card.get('content', 'No question content')))
        lines.append(question_text)
        lines.append("")
        
        # Add options if they exist
        if 'options' in card:
            lines.append("## Options")
            for i, option in enumerate(card['options'], 1):
                lines.append(f"{i}. {option}")
            lines.append("")
                
        # Add card type if it exists
        if 'question_type' in card:
            lines.append("## Type")
            lines.append(card['question_type'])
            lines.append("")
        
        # Add answer type if it exists
        if 'answers_type' in card:
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
            output_file = self.output_path / f"{card_id}.md"
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
        # Support both 'questions' and 'cards' keys
        items = deck_meta.get('questions', deck_meta.get('cards', []))
        for card in items:
            card_id = str(card['id']).zfill(3)
            lines.append(f"- [Question {card_id}]({card_id}.md)")
            
        # Write index file
        try:
            with open(self.output_path / "index.md", 'w', encoding='utf-8') as f:
                f.write("\n".join(lines))
            logger.debug("Created index markdown file")
        except IOError as e:
            logger.error(f"Failed to create index markdown file: {e}")
            raise
            
    def process_deck(self) -> None:
        """
        Process all cards in the deck.
        
        Raises:
            yaml.YAMLError: If YAML parsing fails
            IOError: If file operations fail
        """
        try:
            # Check if README.yaml exists
            readme_path = self.input_path / "README.yaml"
            if not readme_path.exists():
                logger.warning(f"Skipping deck {self.input_path} - README.yaml not found")
                return
                
            # Load deck metadata
            with open(readme_path, 'r', encoding='utf-8') as f:
                deck_meta = yaml.safe_load(f)
                
            # Create index markdown
            self.create_index_markdown(deck_meta)
            logger.info("Created index markdown file")
                
            # Process each card
            # Support both 'questions' and 'cards' keys
            items = deck_meta.get('questions', deck_meta.get('cards', []))
            for card in items:
                card_id = str(card['id']).zfill(3)
                try:
                    card_data = self.load_question(card_id)
                    self.create_markdown_file(card_data, card_id)
                    logger.info(f"Created markdown file for card {card_id}")
                except (FileNotFoundError, yaml.YAMLError, IOError) as e:
                    logger.error(f"Failed to process card {card_id}: {e}")
                    continue
                    
        except yaml.YAMLError as e:
            logger.error(f"Failed to process deck: {e}")
            raise
        except Exception as e:
            logger.error(f"Conversion failed: {e}")
            raise
            
def main() -> int:
    """
    Main entry point for the script.
    
    Returns:
        0 on success, non-zero on error
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Convert YAML cards to Markdown')
    parser.add_argument('input_path', help='Path to the deck directory')
    parser.add_argument('output_path', help='Path to output directory')
    
    args = parser.parse_args()
    
    try:
        converter = YAMLToMarkdown(args.input_path, args.output_path)
        converter.process_deck()
        logger.info("Conversion completed successfully")
        return 0
    except Exception as e:
        logger.error(f"Conversion failed: {e}")
        return 1
        
if __name__ == "__main__":
    exit(main()) 