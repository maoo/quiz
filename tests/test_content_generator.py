import pytest
from pathlib import Path
import yaml
from unittest.mock import Mock, MagicMock, patch, mock_open
from src.yaml_generator.content_generator import (
    get_or_create_chat_client,
    generate_deck_content,
    generate_card_content,
    DECK_CHAT_CLIENTS
)
from src.api.routers.content_generator import create_deck_endpoint, create_card_endpoint

@pytest.fixture(autouse=True)
def patch_openai(monkeypatch):
    mock_client = Mock()
    monkeypatch.setattr("openai.OpenAI", lambda *args, **kwargs: mock_client)
    yield mock_client

@pytest.fixture(autouse=True)
def clear_deck_chat_clients():
    DECK_CHAT_CLIENTS.clear()
    yield

@pytest.fixture
def mock_file_content():
    return """
    title: Test Deck
    description: A test deck
    difficulty: medium
    cards:
      - id: 1
        question: Test question?
        answer: Test answer
    """

@pytest.fixture
def mock_openai_api_key(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    yield

def make_openai_response(content):
    mock_message = MagicMock()
    mock_message.content = content
    mock_choice = MagicMock()
    mock_choice.message = mock_message
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]
    return mock_response

def test_get_or_create_chat_client(mock_openai_api_key):
    # Test creating a new client
    client1 = get_or_create_chat_client("test_deck")
    assert client1 is not None
    
    # Test getting existing client
    client2 = get_or_create_chat_client("test_deck")
    assert client1 is client2  # Should return the same instance

def test_generate_deck_content(patch_openai, mock_file_content, mock_openai_api_key):
    # Mock the file reading
    with patch('builtins.open', mock_open(read_data=mock_file_content)):
        # Mock the API response
        patch_openai.chat.completions.create.return_value = make_openai_response(mock_file_content)
        
        # Test the function
        result = generate_deck_content("test_deck")
        assert result is not None
        assert "title" in result
        assert result["title"] == "Test Deck"

def test_create_deck_endpoint(patch_openai, mock_file_content, mock_openai_api_key):
    # Mock the file operations
    with patch('builtins.open', mock_open(read_data=mock_file_content)):
        # Mock the API response
        patch_openai.chat.completions.create.return_value = make_openai_response(mock_file_content)
        
        # Mock Path operations
        with patch('pathlib.Path.mkdir') as mock_mkdir:
            # Test the endpoint
            response = create_deck_endpoint(None, "test_deck")
            assert response["status"] == "success"
            assert "test_deck" in response["message"]
            assert "deck_path" in response

def test_create_card_endpoint(patch_openai, mock_file_content, mock_openai_api_key):
    # Mock the file operations
    with patch('builtins.open', mock_open(read_data=mock_file_content)):
        # Mock the API response
        patch_openai.chat.completions.create.return_value = make_openai_response(mock_file_content)
        
        # Mock Path operations
        with patch('pathlib.Path.mkdir') as mock_mkdir:
            with patch('pathlib.Path.iterdir') as mock_iterdir:
                mock_iterdir.return_value = []  # No existing cards
                
                # Test the endpoint
                response = create_card_endpoint(None, "test_deck")
                assert response["status"] == "success"
                assert "card_id" in response
                assert response["card_id"] == "1"  # First card should have ID 1

def test_error_handling(mock_openai_api_key, clear_deck_chat_clients):
    # Test deck creation with missing prompt file
    with patch('pathlib.Path.exists', return_value=False):
        response = create_deck_endpoint(None, "nonexistent_deck")
        assert response["status"] == "error"
        assert "Prompt file not found" in response["message"]

    # Test card creation with API error
    with patch('openai.OpenAI') as mock_client:
        mock_instance = Mock()
        mock_instance.chat.completions.create.side_effect = Exception("API Error")
        mock_client.return_value = mock_instance
        
        with patch('src.yaml_validator.validator.validate_yaml', return_value=True):
            response = create_card_endpoint(None, "test_deck")
            assert response["status"] == "error"
            assert "API Error" in response["message"] 