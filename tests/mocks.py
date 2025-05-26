import pytest
import os
from unittest.mock import patch, mock_open, Mock
from types import SimpleNamespace

@pytest.fixture
def mock_openai_api_key():
    with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
        yield

@pytest.fixture
def mock_openai_client(mock_openai_api_key):
    with patch('openai.OpenAI') as mock_client:
        mock_instance = Mock()
        mock_client.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def mock_card_file_content():
    return """
    card_id: "1"
    question_type: "short"
    question_content: "Test question?"
    options:
      - "Option 1"
      - "Option 2"
      - "Option 3"
      - "Option 4"
      - "Option 5"
      - "Option 6"
      - "Option 7"
      - "Option 8"
    sources:
      - "Source 1"
      - "Source 2"
    url: "https://blog.session.it/quiz/decks/test_deck/cards/1"
    answer_type: "binary"
    """

@pytest.fixture
def mock_deck_file_content():
    return """
    title: "Test Deck"
    introduction: "A test deck for unit testing"
    cards:
      - card_id: "1"
        question_type: "short"
        question_content: "Test question?"
        options:
          - "Option 1"
          - "Option 2"
          - "Option 3"
          - "Option 4"
          - "Option 5"
          - "Option 6"
          - "Option 7"
          - "Option 8"
        sources:
          - "Source 1"
          - "Source 2"
        url: "https://blog.session.it/quiz/decks/test_deck/cards/1"
        answer_type: "binary"
    """

@pytest.fixture
def mock_openai_response():
    # Return an object with .choices[0].message.content
    return SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content="""
title: Test Deck
description: A test deck for unit testing
tags: [test, unit-test]
difficulty: easy
num_cards: 5
"""))]
    ) 