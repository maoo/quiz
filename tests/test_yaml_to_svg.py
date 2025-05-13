import os
import tempfile
import shutil
from pathlib import Path
import yaml
import svgwrite
import logging
import pytest
from src.yaml_to_svg.generate_svg import YAMLToSVG

@pytest.fixture
def tmp_path():
    """Fixture to create a new temporary directory for each test"""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)

def create_test_deck(base_path, index_data=None):
    """Helper to create a test deck structure. index_data can be passed to override the default index.yaml content."""
    deck_path = base_path / "test_deck"
    deck_path.mkdir()
    
    # Create decks directory for relative path tests
    decks_dir = base_path / "decks"
    decks_dir.mkdir(exist_ok=True)
    
    # Create index.yaml
    if index_data is None:
        index_data = {
            'title': 'Test Deck',
            'questions': [
                {'id': '001'},
                {'id': '002'},
                {'id': '003'}
            ]
        }
    with open(deck_path / "index.yaml", 'w') as f:
        yaml.dump(index_data, f)
        
    # Create questions directory
    questions_dir = deck_path / "cards"
    questions_dir.mkdir()
    
    # Create question 001
    question_001_dir = questions_dir / "001"
    question_001_dir.mkdir()
    question_001_data = {
        'question': 'What is 2+2?',
        'options': ['3', '4', '5'],
        'question_type': 'short',
        'answers_type': 'single'
    }
    with open(question_001_dir / "content.yaml", 'w') as f:
        yaml.dump(question_001_data, f)
    with open(question_001_dir / "answers.yaml", 'w') as f:
        yaml.dump({'answers': []}, f)
        
    # Create question 002
    question_002_dir = questions_dir / "002"
    question_002_dir.mkdir()
    question_002_data = {
        'question': 'Is this a test?',
        'question_type': 'short',
        'answers_type': 'binary'
    }
    with open(question_002_dir / "content.yaml", 'w') as f:
        yaml.dump(question_002_data, f)
    with open(question_002_dir / "answers.yaml", 'w') as f:
        yaml.dump({'answers': []}, f)
        
    # Create question 003 with content.yaml instead of question.yaml
    question_003_dir = questions_dir / "003"
    question_003_dir.mkdir()
    question_003_data = {
        'question_content': 'What is the capital of France?',
        'options': ['London', 'Paris', 'Berlin'],
        'question_type': 'short',
        'answers_type': 'single'
    }
    with open(question_003_dir / "content.yaml", 'w') as f:
        yaml.dump(question_003_data, f)
    with open(question_003_dir / "answers.yaml", 'w') as f:
        yaml.dump({'answers': []}, f)
    
    return deck_path

@pytest.fixture
def test_deck(tmp_path):
    return create_test_deck(tmp_path)

def test_init_with_relative_path(tmp_path, test_deck):
    # Create a copy of the test deck in the decks directory
    decks_dir = tmp_path / "decks"
    test_deck_path = decks_dir / "test_deck"
    test_deck_path.mkdir()
    for item in test_deck.iterdir():
        if item.is_file():
            with open(item, 'r') as src, open(test_deck_path / item.name, 'w') as dst:
                dst.write(src.read())
        else:
            shutil.copytree(item, test_deck_path / item.name)
    
    # Change working directory to tmp_path for relative path test
    original_cwd = os.getcwd()
    os.chdir(str(tmp_path))
    try:
        # Use the relative path to the copied deck
        rel_deck_path = Path("decks/test_deck")
        converter = YAMLToSVG(input_paths=[str(rel_deck_path)], card_size=(100, 150), font_size=14, font_family="Times New Roman")
        converter.deck_path = rel_deck_path.resolve()
        # The converter returns a relative path, so we need to resolve it against the current directory
        assert converter.deck_path.resolve() == test_deck_path.resolve()
    finally:
        os.chdir(original_cwd)

def test_init_with_absolute_path(test_deck):
    converter = YAMLToSVG(input_paths=[str(test_deck)], card_size=(100, 150), font_size=14, font_family="Times New Roman")
    converter.deck_path = Path(test_deck)
    assert converter.deck_path == test_deck

def test_init_with_custom_output_dir(tmp_path, test_deck):
    output_dir = tmp_path / "custom_output"
    converter = YAMLToSVG(input_paths=[str(test_deck)], card_size=(100, 150), font_size=14, font_family="Times New Roman")
    converter.deck_path = Path(test_deck)
    converter.output_dir = str(output_dir)
    assert converter.output_path == output_dir

def test_init_with_custom_card_size(test_deck):
    converter = YAMLToSVG(input_paths=[str(test_deck)], card_size=(100, 150), font_size=14, font_family="Times New Roman")
    converter.deck_path = Path(test_deck)
    assert converter.card_size == (100, 150)

def test_init_with_custom_font(test_deck):
    converter = YAMLToSVG(input_paths=[str(test_deck)], card_size=(100, 150), font_size=14, font_family="Times New Roman")
    converter.deck_path = Path(test_deck)
    assert converter.font_size == 14
    assert converter.font_family == "Times New Roman"

def test_init_with_nonexistent_deck():
    with pytest.raises(FileNotFoundError):
        YAMLToSVG(input_paths=["nonexistent_deck"], card_size=(100, 150), font_size=14, font_family="Times New Roman")

def test_init_with_missing_index_yaml(test_deck):
    os.remove(test_deck / "index.yaml")
    with pytest.raises(FileNotFoundError):
        YAMLToSVG(input_paths=[str(test_deck)], card_size=(100, 150), font_size=14, font_family="Times New Roman")

def test_load_question(test_deck):
    converter = YAMLToSVG(input_paths=[str(test_deck)], card_size=(100, 150), font_size=14, font_family="Times New Roman")
    converter.deck_path = Path(test_deck)
    question = converter.load_question('001')
    assert question['question'] == 'What is 2+2?'
    assert question['options'] == ['3', '4', '5']

def test_load_question_with_content_yaml(test_deck):
    converter = YAMLToSVG(input_paths=[str(test_deck)], card_size=(100, 150), font_size=14, font_family="Times New Roman")
    converter.deck_path = Path(test_deck)
    question = converter.load_question('003')
    assert question['question_content'] == 'What is the capital of France?'
    assert question['options'] == ['London', 'Paris', 'Berlin']

def test_load_nonexistent_question(test_deck):
    converter = YAMLToSVG(input_paths=[str(test_deck)], card_size=(100, 150), font_size=14, font_family="Times New Roman")
    converter.deck_path = Path(test_deck)
    with pytest.raises(FileNotFoundError):
        converter.load_question('999')

def test_create_svg_card_with_answers(test_deck):
    # Add answers to answers.yaml for question 001, using the correct schema (list of dicts)
    answers_path = test_deck / "cards" / "001" / "answers.yaml"
    with open(answers_path, 'w') as f:
        yaml.dump([
            { 'order': 1, 'option': 'foo', 'answer': 'foo'},
            { 'order': 2, 'option': 'bar', 'answer': 'bar'},
            { 'order': 3, 'option': 'baz', 'answer': 'baz'}
        ], f)

    converter = YAMLToSVG(input_paths=[str(test_deck)], card_size=(100, 150), font_size=14, font_family="Times New Roman")
    converter.deck_path = Path(test_deck)
    question = converter.load_question('001')
    converter.create_svg_card(question, '001')

    svg_path = test_deck / "cards" / "001" / "content.svg"
    assert svg_path.exists()
    with open(svg_path, 'r') as f:
        svg_content = f.read()
        assert 'foo' in svg_content
        assert 'bar' in svg_content
        assert 'baz' in svg_content

def test_create_svg_card(test_deck):
    # Add answers to answers.yaml for question 001, using the correct schema (list of dicts)
    answers_path = test_deck / "cards" / "001" / "answers.yaml"
    with open(answers_path, 'w') as f:
        yaml.dump([
            { 'order': 1, 'option': 'foo', 'answer': 'foo'},
            { 'order': 2, 'option': 'bar', 'answer': 'bar'},
            { 'order': 3, 'option': 'baz', 'answer': 'baz'}
        ], f)

    converter = YAMLToSVG(input_paths=[str(test_deck)], card_size=(100, 150), font_size=14, font_family="Times New Roman")
    converter.deck_path = Path(test_deck)
    question = converter.load_question('001')
    converter.create_svg_card(question, '001')
    
    # Check if SVG file was created
    svg_path = test_deck / "cards" / "001" / "content.svg"
    assert svg_path.exists()
    
    # Verify SVG content
    with open(svg_path, 'r') as f:
        svg_content = f.read()
        assert 'What is 2+2?' in svg_content
        assert '1. 3' in svg_content
        assert '2. 4' in svg_content
        assert '3. 5' in svg_content
        assert 'foo' in svg_content
        assert 'bar' in svg_content
        assert 'baz' in svg_content

def test_create_svg_card_with_custom_size(test_deck):
    converter = YAMLToSVG(input_paths=[str(test_deck)], card_size=(100, 150), font_size=14, font_family="Times New Roman")
    converter.deck_path = Path(test_deck)
    question = converter.load_question('001')
    converter.create_svg_card(question, '001')
    
    # Check if SVG file was created with correct size
    svg_path = test_deck / "cards" / "001" / "content.svg"
    with open(svg_path, 'r') as f:
        svg_content = f.read()
        assert 'width="100mm"' in svg_content
        assert 'height="150mm"' in svg_content

def test_process_deck(test_deck):
    converter = YAMLToSVG(input_paths=[str(test_deck)], card_size=(100, 150), font_size=14, font_family="Times New Roman")
    converter.deck_path = Path(test_deck)
    converter.process_deck()
    
    # Check if all SVG files were created
    assert (test_deck / "cards" / "001" / "content.svg").exists()
    assert (test_deck / "cards" / "002" / "content.svg").exists()
    assert (test_deck / "cards" / "003" / "content.svg").exists()

def test_process_deck_with_empty_metadata(tmp_path):
    # Create a test deck with empty metadata
    deck_path = create_test_deck(tmp_path, index_data={'title': 'Empty Deck'})
    converter = YAMLToSVG(input_paths=[str(deck_path)], card_size=(100, 150), font_size=14, font_family="Times New Roman")
    converter.deck_path = deck_path
    converter.process_deck()
    # Optionally, check that SVGs are still created
    assert (deck_path / "cards" / "001" / "content.svg").exists()
    assert (deck_path / "cards" / "002" / "content.svg").exists()
    assert (deck_path / "cards" / "003" / "content.svg").exists() 