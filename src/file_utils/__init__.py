"""
file_utils: Utilities for finding, extracting, and processing quiz content.yaml files for QR code generation and other purposes. Can be reused across modules in the src folder.
"""
import os
from pathlib import Path
import logging
from typing import List, Tuple, Optional

logging.basicConfig(level=logging.INFO)

def get_question_folders(deck_paths: List[str]) -> List[str]:
    logger = logging.getLogger(__name__)
    logger.info(f"Getting question folders from {deck_paths}")
    folders = []
    for path in deck_paths:
        logger.info(f"Processing path: {path}")
        for file in os.listdir(path + "/cards"):
            p = Path(path) / "cards" / file
            has_content = (p / "content.yaml").exists()
            has_answers = (p / "answers.yaml").exists()
            if p.is_dir() and has_content and has_answers:
                folders.append(str(p))
    return folders

def get_deck_folders(input_paths: List[str], seen: Optional[set] = None) -> List[str]:
    if seen is None:
        seen = set()
    folders_to_process = []
    deck_folders = []
    logger = logging.getLogger(__name__)
    logger.info(f"Getting deck folders from {input_paths}")
    if not input_paths or all(str(Path(p).resolve()) == '/' for p in input_paths):
        return []
    for path in input_paths:
        p = Path(path)
        resolved_p = str(p.resolve())
        if resolved_p in seen:
            continue
        seen.add(resolved_p)
        if not p.is_dir():
            continue
        if (p / "index.yaml").exists():
            logger.info(f"Found deck folder: {p}")
            cards_path = p / "cards"
            if cards_path.exists() and cards_path.is_dir():
                logger.info(f"Found cards folder: {cards_path}")
                if any(cards_path.iterdir()):
                    logger.info(f"Found non-empty cards folder: {cards_path}")
                    deck_folders.append(str(p))
        else:
            if resolved_p == '/':
                continue
            folders_to_process.append(str(p))
            logger.info(f"Adding folder to process: {p}")
    if len(folders_to_process) > 0:
        logger.info(f"Processing remaining folders: {folders_to_process}")
        deck_folders += get_deck_folders(folders_to_process, seen)
    return deck_folders

def extract_deck_and_card_id(content_yaml_path: str) -> Tuple[Optional[str], Optional[str]]:
    parts = Path(content_yaml_path).parts
    try:
        card_id = parts[-1]
        deck_name = parts[-3]
        return deck_name, card_id
    except (ValueError, IndexError):
        return None, None

__all__ = ['get_question_folders', 'extract_deck_and_card_id', 'get_deck_folders'] 