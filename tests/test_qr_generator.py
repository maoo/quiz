import os
import pytest
import shutil
import tempfile
from pathlib import Path
from src.qr_generator import generate_qr_code, generate_question_qr_code

@pytest.fixture
def tmp_path():
    """Fixture to create a new temporary directory for each test"""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)

@pytest.fixture(autouse=True)
def cleanup_test_deck(tmp_path):
    """Fixture to clean up test-deck directory after tests"""
    yield
    test_deck_path = os.path.join(tmp_path, "decks", "test-deck")
    if os.path.exists(test_deck_path):
        shutil.rmtree(test_deck_path)

def test_generate_qr_code(tmp_path):
    """Test basic QR code generation"""
    url = "https://example.com"
    output_path = os.path.join(tmp_path, "test_qr.png")
    
    result = generate_qr_code(url, output_path)
    
    assert result == output_path
    assert os.path.exists(output_path)
    assert os.path.getsize(output_path) > 0

def test_generate_question_qr_code(tmp_path, monkeypatch):
    """Test question QR code generation"""
    # Mock the generate_qr_code function
    def mock_generate_qr_code(url, output_path, **kwargs):
        return output_path
    
    monkeypatch.setattr("src.qr_generator.generate_qr_code", mock_generate_qr_code)
    
    deck_name = "test-deck"
    card_id = "001"
    
    result = generate_question_qr_code(
        deck_name, 
        card_id,
        output_prefix=str(tmp_path)
    )
    
    expected_path = os.path.join(tmp_path, deck_name, "cards", card_id, "qr.png")
    assert result == expected_path

def test_generate_qr_code_invalid_path():
    """Test QR code generation with invalid path"""
    url = "https://example.com"
    output_path = "/nonexistent/path/test_qr.png"
    
    result = generate_qr_code(url, output_path)
    
    assert result is None

def test_generate_qr_code_empty_url(tmp_path):
    """Test QR code generation with empty URL"""
    url = ""
    output_path = os.path.join(tmp_path, "test_qr.png")
    
    result = generate_qr_code(url, output_path)
    
    assert result == output_path
    assert os.path.exists(output_path)
    assert os.path.getsize(output_path) > 0

def test_generate_question_qr_code_custom_prefixes(tmp_path, monkeypatch):
    """Test question QR code generation with custom URL and output path prefixes"""
    # Mock the generate_qr_code function
    def mock_generate_qr_code(url, output_path, **kwargs):
        return output_path
    
    monkeypatch.setattr("src.qr_generator.generate_qr_code", mock_generate_qr_code)
    
    deck_name = "test-deck"
    card_id = "001"
    custom_url_prefix = "https://custom.domain/quiz/decks"
    custom_output_prefix = str(tmp_path / "custom" / "output" / "path")
    
    result = generate_question_qr_code(
        deck_name,
        card_id,
        url_prefix=custom_url_prefix,
        output_prefix=custom_output_prefix
    )
    
    expected_path = os.path.join(custom_output_prefix, deck_name, "cards", card_id, "qr.png")
    assert result == expected_path

def test_generate_question_qr_code_default_prefixes(tmp_path, monkeypatch):
    """Test question QR code generation with default URL and output path prefixes"""
    # Mock the generate_qr_code function
    def mock_generate_qr_code(url, output_path, **kwargs):
        return output_path
    
    monkeypatch.setattr("src.qr_generator.generate_qr_code", mock_generate_qr_code)
    
    deck_name = "test-deck"
    card_id = "001"
    
    result = generate_question_qr_code(
        deck_name, 
        card_id,
        output_prefix=str(tmp_path)
    )
    
    expected_path = os.path.join(tmp_path, deck_name, "cards", card_id, "qr.png")
    assert result == expected_path 