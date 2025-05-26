from ninja import Router
from typing import Dict, Any
from pathlib import Path
import yaml
from src.yaml_generator.content_generator import generate_deck_content, generate_card_content

router = Router()

@router.put("/deck")
def create_deck_endpoint(request, deck_name: str):
    """
    Create a new deck with index.yaml file
    """
    try:
        deck_content = generate_deck_content(deck_name)

        # Create deck directory if it doesn't exist
        deck_path = Path("decks") / deck_name
        deck_path.mkdir(parents=True, exist_ok=True)

        # Create index.yaml
        index_file = deck_path / "index.yaml"
        with open(index_file, "w") as f:
            yaml.dump(deck_content, f, default_flow_style=False)

        return {
            "status": "success",
            "message": f"Deck '{deck_name}' created successfully",
            "deck_path": str(deck_path)
        }
    except Exception as e:
        # Always return 200 with error JSON
        return {"status": "error", "message": str(e)}

@router.put("/deck/{deck_name}/card")
def create_card_endpoint(request, deck_name: str):
    """
    Create a new card in the specified deck
    """
    try:
        deck_path = Path("decks") / deck_name
        
        # Get next card ID
        cards_dir = deck_path / "cards"
        cards_dir.mkdir(exist_ok=True)
        existing_cards = [d for d in cards_dir.iterdir() if d.is_dir()]
        next_id = str(len(existing_cards) + 1)
        
        # Generate content
        card_data = generate_card_content(deck_name, next_id)

        # Create card directory
        card_path = cards_dir / next_id
        card_path.mkdir(exist_ok=True)        

        content_file = card_path / "content.yaml"
        with open(content_file, "w") as f:
            yaml.dump(card_data['content'], f, default_flow_style=False)
        
        # Create empty answers.yaml
        answers_file = card_path / "answers.yaml"
        with open(answers_file, "w") as f:
            yaml.dump(card_data['answers'], f, default_flow_style=False)
        
        return {
            "status": "success",
            "message": f"Card created successfully in deck '{deck_name}'",
            "card_id": next_id,
            "card_path": str(card_path)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}