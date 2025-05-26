from typing import Dict, Any, Union
import os
import yaml
from pathlib import Path
import openai
from src.yaml_validator import validate_yaml, YAMLValidationError

# Module-level map to store chat clients for each deck
DECK_CHAT_CLIENTS: Dict[str, openai.OpenAI] = {}

# Global conversation list
conversation = []

def get_or_create_chat_client(deck_name: str) -> openai.OpenAI:
    """
    Get an existing chat client for a deck or create a new one
    """
    if deck_name not in DECK_CHAT_CLIENTS:
        DECK_CHAT_CLIENTS[deck_name] = openai.OpenAI()
    return DECK_CHAT_CLIENTS[deck_name]

def _read_prompt_file(file_path: Union[str, Path]) -> str:
    """
    Read content from a prompt file.
    
    Args:
        file_path: Path to the prompt file
        
    Returns:
        str: Content of the prompt file
        
    Raises:
        Exception: If file is not found or cannot be read
    """
    try:
        with open(file_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        raise Exception(f"Prompt file not found: {file_path}")
    except Exception as e:
        raise Exception(f"Failed to read prompt file: {str(e)}")

def _generate_content_with_openai(
    client: Any,
    content_type: str,  # "deck" or "card"
    temperature: float = 0.7,
    attempts: int = 0,
) -> Dict[str, Any]:
    """
    Generate content using OpenAI API and parse as YAML.
    
    Args:
        client: OpenAI client instance
        content_type: Type of content to generate ("deck", "content" or "answers")
        attempts: Number of retry attempts
        temperature: Temperature for generation (default: 0.7)
        
    Returns:
        Dict[str, Any]: Parsed YAML content
        
    Raises:
        Exception: If generation or parsing fails
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=conversation,
            temperature=temperature
        )
        content = response.choices[0].message.content
        conversation.append({"role": "assistant", "content": content})

        # Parse the content as YAML
        parsed_content = yaml.safe_load(content)
        
        # Validate content against the appropriate schema
        try:
            schema_path = None
            if content_type == "deck":
                schema_path = "schemas/deck-index.yaml"
            elif content_type == "content":
                schema_path = "schemas/card.yaml"
            elif content_type == "answers":
                schema_path = "schemas/answers.yaml"
            elif content_type == "card":
                schema_path = "schemas/card.yaml"
            
            if schema_path:
                validate_yaml(parsed_content, schema_path)
            else:
                raise Exception(f"Invalid content type: {content_type}")
                
        except YAMLValidationError as e:
            if attempts < 3:
                user_prompt = f"The generated content failed validation: {str(e)}\nPlease generate content that adheres to the {content_type} YAML schema"
                conversation.append({"role": "user", "content": user_prompt})
                return _generate_content_with_openai(
                    client=client,
                    content_type=content_type,
                    temperature=temperature,
                    attempts=attempts + 1
                )
            else:
                # Raise exception, too many attempts to generate content
                raise Exception(f"Failed to generate valid {content_type} content after {attempts} attempts. Last error: {str(e)}")
            
        return parsed_content
    except Exception as e:
        raise Exception(f"Failed to generate content: {str(e)}")

def generate_deck_content(deck_name: str) -> Dict[str, Any]:
    """
    Generate deck content using OpenAI API
    """
    try:      
        # Get or create chat client for this deck
        client = get_or_create_chat_client(deck_name)

        # Append messages to conversation for deck creation
        system_prompt = _read_prompt_file("prompts/system/deck.md")
        system_prompt += _read_prompt_file("prompts/"+deck_name+".yaml")
        conversation.append({"role": "system", "content": system_prompt})
        user_prompt = _read_prompt_file("prompts/user/deck.md")
        conversation.append({"role": "user", "content": user_prompt})
        
        # Generate content
        return _generate_content_with_openai(
            client=client,
            content_type="deck"
        )
    except Exception as e:
        raise Exception(f"Failed to generate deck content: {str(e)}")

def generate_card_content(deck_name: str, card_id: str) -> Dict[str, Any]:
    """
    Generate or regenerate card content using the deck's chat client
    """
    try:
        # Get the chat client for this deck
        client = get_or_create_chat_client(deck_name)
        
        # Append messages to conversation for content card creation
        user_prompt = _read_prompt_file("prompts/user/card-content.md")
        conversation.append({"role": "user", "content": user_prompt})

        # Generate content
        content_data = _generate_content_with_openai(
            client=client,
            content_type="card"
        )

        # Append messages to conversation for answers card creation
        user_prompt = _read_prompt_file("prompts/user/card-answers.md")
        conversation.append({"role": "user", "content": user_prompt})

        answers_data = _generate_content_with_openai(
            client=client,
            content_type="answers"
        )
        return {
            'content':content_data,
            'answers':answers_data
        }
    except Exception as e:
        raise Exception(f"Failed to generate card content: {str(e)}") 