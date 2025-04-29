import os
import tempfile
import unittest
from pathlib import Path
import yaml
import svgwrite
from src.yaml_to_svg.generate_svg import YAMLToSVG

class TestYAMLToSVG(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.deck_path = Path(self.test_dir) / "test_deck"
        self.deck_path.mkdir()
        
        # Create test YAML files
        self._create_test_yaml_files()
        
    def _create_test_yaml_files(self):
        # Create README.yaml
        readme_data = {
            'title': 'Test Deck',
            'questions': [
                {'id': '001'},
                {'id': '002'}
            ]
        }
        with open(self.deck_path / "README.yaml", 'w') as f:
            yaml.dump(readme_data, f)
            
        # Create questions directory
        questions_dir = self.deck_path / "questions"
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
        with open(question_001_dir / "question.yaml", 'w') as f:
            yaml.dump(question_001_data, f)
            
        # Create question 002
        question_002_dir = questions_dir / "002"
        question_002_dir.mkdir()
        question_002_data = {
            'question': 'Is this a test?',
            'question_type': 'short',
            'answers_type': 'binary'
        }
        with open(question_002_dir / "question.yaml", 'w') as f:
            yaml.dump(question_002_data, f)
            
    def test_load_question(self):
        converter = YAMLToSVG(str(self.deck_path))
        question = converter.load_question('001')
        self.assertEqual(question['question'], 'What is 2+2?')
        self.assertEqual(question['options'], ['3', '4', '5'])
        
    def test_create_svg_card(self):
        converter = YAMLToSVG(str(self.deck_path))
        question = converter.load_question('001')
        converter.create_svg_card(question, '001')
        
        # Check if SVG file was created
        svg_path = self.deck_path / "cards" / "001.svg"
        self.assertTrue(svg_path.exists())
        
        # Verify SVG content
        with open(svg_path, 'r') as f:
            svg_content = f.read()
            self.assertIn('What is 2+2?', svg_content)
            self.assertIn('1. 3', svg_content)
            self.assertIn('2. 4', svg_content)
            self.assertIn('3. 5', svg_content)
            
    def test_process_deck(self):
        converter = YAMLToSVG(str(self.deck_path))
        converter.process_deck()
        
        # Check if both SVG files were created
        self.assertTrue((self.deck_path / "cards" / "001.svg").exists())
        self.assertTrue((self.deck_path / "cards" / "002.svg").exists())
        
    def tearDown(self):
        # Clean up temporary directory
        import shutil
        shutil.rmtree(self.test_dir)

if __name__ == '__main__':
    unittest.main() 