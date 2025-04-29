import os
import tempfile
import unittest
from pathlib import Path
import yaml
from src.yaml_to_markdown.generate_markdown import YAMLToMarkdown

class TestYAMLToMarkdown(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.input_path = Path(self.test_dir) / "test_deck"
        self.output_path = Path(self.test_dir) / "output"
        self.input_path.mkdir()
        self.output_path.mkdir()
        
        # Create test YAML files
        self._create_test_yaml_files()
        
    def _create_test_yaml_files(self):
        # Create index.yaml
        readme_data = {
            'title': 'Test Deck',
            'introduction': 'This is a test deck',
            'questions': [
                {'id': '001'},
                {'id': '002'}
            ]
        }
        with open(self.input_path / "index.yaml", 'w') as f:
            yaml.dump(readme_data, f)
            
        # Create questions directory
        questions_dir = self.input_path / "cards"
        questions_dir.mkdir()
        
        # Create question 001
        question_001_dir = questions_dir / "001"
        question_001_dir.mkdir()
        question_001_data = {
            'question': 'What is 2+2?',
            'options': ['3', '4', '5'],
            'question_type': 'short',
            'answers_type': 'single',
            'sources': ['https://example.com']
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
        converter = YAMLToMarkdown(str(self.input_path), str(self.output_path))
        question = converter.load_question('001')
        self.assertEqual(question['question'], 'What is 2+2?')
        self.assertEqual(question['options'], ['3', '4', '5'])
        
    def test_create_markdown_content(self):
        converter = YAMLToMarkdown(str(self.input_path), str(self.output_path))
        question = converter.load_question('001')
        content = converter.create_markdown_content(question, '001')
        
        expected_content = """# Question 001

## Question
What is 2+2?

## Options
1. 3
2. 4
3. 5

## Type
short

## Answer Type
single

## Sources
- https://example.com"""
        
        self.assertEqual(content, expected_content)
        
    def test_create_markdown_file(self):
        converter = YAMLToMarkdown(str(self.input_path), str(self.output_path))
        question = converter.load_question('001')
        converter.create_markdown_file(question, '001')
        
        # Check if markdown file was created
        md_path = self.output_path / "001.md"
        self.assertTrue(md_path.exists())
        
        # Verify content
        with open(md_path, 'r') as f:
            content = f.read()
            self.assertIn('# Question 001', content)
            self.assertIn('What is 2+2?', content)
            
    def test_create_index_markdown(self):
        converter = YAMLToMarkdown(str(self.input_path), str(self.output_path))
        with open(self.input_path / "index.yaml", 'r') as f:
            deck_meta = yaml.safe_load(f)
        converter.create_index_markdown(deck_meta)
        
        # Check if index file was created
        index_path = self.output_path / "index.md"
        self.assertTrue(index_path.exists())
        
        # Verify content
        with open(index_path, 'r') as f:
            content = f.read()
            self.assertIn('# Test Deck', content)
            self.assertIn('This is a test deck', content)
            self.assertIn('- [Question 001](001.md)', content)
            self.assertIn('- [Question 002](002.md)', content)
            
    def test_process_deck(self):
        converter = YAMLToMarkdown(str(self.input_path), str(self.output_path))
        converter.process_deck()
        
        # Check if all files were created
        self.assertTrue((self.output_path / "index.md").exists())
        self.assertTrue((self.output_path / "001.md").exists())
        self.assertTrue((self.output_path / "002.md").exists())
        
    def tearDown(self):
        # Clean up temporary directory
        import shutil
        shutil.rmtree(self.test_dir)

if __name__ == '__main__':
    unittest.main() 