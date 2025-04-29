"""
YAML to Markdown Converter.

Converts YAML question files to Markdown format for GitHub Pages.
Creates individual question pages and an index page for navigation.
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
    
    This class provides functionality to convert YAML question files
    to Markdown format suitable for GitHub Pages. It handles both
    individual question files and deck metadata.
    """
    
    def __init__(self, deck_path: str):
        """
        Initialize the YAML to Markdown converter.
        
        Args:
            deck_path: Path to the deck directory containing questions
        """
        self.deck_path = Path(deck_path)
        self.questions_path = self.deck_path / "questions"
        self.output_path = self.deck_path / "docs"
        self.output_path.mkdir(exist_ok=True)
        
    def load_question(self, question_id: str) -> Dict:
        """
        Load a question from its YAML file.
        
        Args:
            question_id: ID of the question to load
            
        Returns:
            Dict containing the question data
            
        Raises:
            FileNotFoundError: If question file doesn't exist
            yaml.YAMLError: If YAML parsing fails
        """
        question_file = self.questions_path / question_id / "question.yaml"
        try:
            with open(question_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.error(f"Question file not found: {question_file}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Failed to parse YAML file {question_file}: {e}")
            raise
            
    def create_markdown_content(self, question: Dict, question_id: str) -> str:
        """
        Create markdown content for a question.
        
        Args:
            question: Dictionary containing question data
            question_id: ID of the question
            
        Returns:
            Formatted markdown content as string
        """
        lines = []
        
        # Add question title
        lines.append(f"# Question {question_id}")
        lines.append("")
        
        # Add question text
        lines.append("## Question")
        lines.append(question['question'])
        lines.append("")
        
        # Add options if they exist
        if 'options' in question:
            lines.append("## Options")
            for i, option in enumerate(question['options'], 1):
                lines.append(f"{i}. {option}")
            lines.append("")
                
        # Add question type
        lines.append("## Type")
        lines.append(question['question_type'])
        lines.append("")
        
        # Add answer type
        lines.append("## Answer Type")
        lines.append(question['answers_type'])
        lines.append("")
        
        # Add sources if they exist
        if 'sources' in question and question['sources']:
            lines.append("## Sources")
            for source in question['sources']:
                lines.append(f"- {source}")
                
        return "\n".join(lines)
        
    def create_markdown_file(self, question: Dict, question_id: str) -> None:
        """
        Create a markdown file for a question.
        
        Args:
            question: Dictionary containing question data
            question_id: ID of the question
            
        Raises:
            IOError: If file creation fails
        """
        try:
            content = self.create_markdown_content(question, question_id)
            output_file = self.output_path / f"{question_id}.md"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.debug(f"Created markdown file: {output_file}")
        except IOError as e:
            logger.error(f"Failed to create markdown file for question {question_id}: {e}")
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
            
        # Add questions list
        lines.append("## Questions")
        for question in deck_meta['questions']:
            question_id = str(question['id']).zfill(3)
            lines.append(f"- [Question {question_id}]({question_id}.md)")
            
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
        Process all questions in the deck.
        
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
                
            # Process each question
            for question in deck_meta['questions']:
                question_id = str(question['id']).zfill(3)
                try:
                    question_data = self.load_question(question_id)
                    self.create_markdown_file(question_data, question_id)
                    logger.info(f"Processed question {question_id}")
                except Exception as e:
                    logger.error(f"Failed to process question {question_id}: {e}")
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
        converter = YAMLToMarkdown("decks/fun-math/questions/decks/fun-math")
        converter.process_deck()
        logger.info("Successfully converted YAML to Markdown")
        return 0
    except Exception as e:
        logger.error(f"Conversion failed: {e}")
        return 1
    
if __name__ == "__main__":
    import sys
    sys.exit(main()) 