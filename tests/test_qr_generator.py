import os
import pytest
import shutil
import tempfile
from pathlib import Path
from src.qr_generator import generate_qr_code, generate_question_qr_code
import subprocess
import sys
import logging

logger = logging.getLogger(__name__)

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
        output_dir=str(tmp_path / deck_name / "cards" / card_id)
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
        output_dir=str(custom_output_prefix),
        url_prefix=custom_url_prefix,
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
        output_dir=str(tmp_path / deck_name / "cards" / card_id)
    )
    
    expected_path = os.path.join(tmp_path, deck_name, "cards", card_id, "qr.png")
    assert result == expected_path

def create_content_yaml_structure(base_dir, deck_name, card_ids):
    deck_root = Path(base_dir) / "decks" / deck_name
    deck_root.mkdir(parents=True, exist_ok=True)
    (deck_root / "index.yaml").write_text("title: Test Deck\n")
    deck_dir = deck_root / "cards"
    paths = []
    for card_id in card_ids:
        card_dir = deck_dir / card_id
        card_dir.mkdir(parents=True, exist_ok=True)
        content_path = card_dir / "content.yaml"
        content_path.write_text(f"card_id: '{card_id}'\nquestion_type: short\nquestion_content: test\n")
        answers_path = card_dir / "answers.yaml"
        answers_path.write_text("[]\n")
        paths.append(str(content_path))

    logger.info(f"Generated deck in root folder: {deck_root}, with the following contents...")
    logger.info(f"Deck root: {deck_root}")
    logger.info(f"Deck dir: {deck_dir}")
    logger.info(f"Paths: {paths}")
    return paths

def test_batch_qr_generation(tmp_path):
    # Create a mock deck with two cards
    deck_name = "batch-deck"
    card_ids = ["001", "002"]
    create_content_yaml_structure(tmp_path, deck_name, card_ids)
    output_dir = tmp_path / "decks"
    # Call the CLI as a subprocess, passing the actual deck directory
    result = subprocess.run([
        sys.executable, "-m", "src.qr_generator", str(output_dir / deck_name)],
        cwd=Path(__file__).parent.parent,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    for card_id in card_ids:
        qr_path = output_dir / deck_name / "cards" / card_id / "qr.png"
        assert qr_path.exists(), f"QR code not generated for card {card_id}"

def test_batch_qr_generation_single_file(tmp_path):
    # Create a mock deck with one card
    deck_name = "singlefile-deck"
    card_ids = ["003"]
    content_paths = create_content_yaml_structure(tmp_path, deck_name, card_ids)
    output_dir = tmp_path / "decks"
    # Call the CLI with a single content.yaml file
    result = subprocess.run([
        sys.executable, "-m", "src.qr_generator", content_paths[0]],
        cwd=Path(__file__).parent.parent,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    qr_path = output_dir / deck_name / "cards" / card_ids[0] / "qr.png"
    assert qr_path.exists(), f"QR code not generated for card {card_ids[0]}" 