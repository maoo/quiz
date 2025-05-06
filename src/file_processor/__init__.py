"""
file_processor: Utilities for finding, extracting, and processing quiz content.yaml files for QR code generation and other purposes. Can be reused across modules in the src folder.
"""
import os
from pathlib import Path
import logging

def get_question_folders(input_paths):
    logger = logging.getLogger(__name__)
    folders = []
    for path in input_paths:
        p = Path(path)
        if p.is_file() and p.name == "content.yaml":
            folder = p.parent
            required_files = [
                folder / "content.yaml",
                folder / "answers.yaml",
                folder / "qr.png",
                folder / "content.svg" ]
            missing = [f.name for f in required_files if not f.exists()]
            if missing:
                logger.warning(f"{folder}: missing files: {', '.join(missing)}")
            else:
                folders.append(str(folder))
        elif p.is_dir():
            for f in p.rglob("content.yaml"):
                folder = f.parent
                required_files = [
                    folder / "content.yaml",
                    folder / "answers.yaml" ]
                missing = [f.name for f in required_files if not f.exists()]
                if missing:
                    logger.warning(f"{folder}: missing files: {', '.join(missing)}")
                else:
                    folders.append(str(folder))
    return folders

def extract_deck_and_card_id(content_yaml_path):
    # Expecting that path ends with cards/<card_id>/content.yaml
    parts = Path(content_yaml_path).parts
    try:
        card_id = parts[-2]
        deck_name = parts[-4]
        return deck_name, card_id
    except (ValueError, IndexError):
        return None, None

__all__ = ['get_question_folders', 'extract_deck_and_card_id'] 