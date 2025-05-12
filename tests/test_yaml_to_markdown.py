import os
import tempfile
import unittest
from pathlib import Path
import yaml
from src.yaml_to_markdown.generate_markdown import YAMLToMarkdown, Card, CardLoader, MarkdownGenerator

class TestYAMLToMarkdown(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.input_path = Path(self.test_dir) / "test_deck"
        self.input_path.mkdir()
        
        # Create test YAML files
        self._create_test_yaml_files()
    
    # also create a test_deck/cards/<id>/answers.yaml file , following the format of the schemas/answers.yaml file, generate random answers
    def _create_test_yaml_files(self):
        # Create index.yaml
        readme_data = {
            'title': 'Test Deck',
            'introduction': 'This is a test deck',
            'questions': [
                {'id': '001'},
                {'id': '002'},
                {'id': '003'}  # Added for testing error cases
            ]
        }
        with open(self.input_path / "index.yaml", 'w') as f:
            yaml.dump(readme_data, f)
            
        # Create questions directory
        questions_dir = self.input_path / "cards"
        questions_dir.mkdir()

        # Create answers data
        answers_data = [
                {
                    'order': 1,
                    'option': '64 + 27',
                    'answer': '91'
                },
                {
                    'order': 2,
                    'option': '58 - 19',
                    'answer': '39'
                },
                {
                    'order': 3,
                    'option': '13 × 5',
                    'answer': '65'
                },
                {
                    'order': 4,
                    'option': '81 ÷ 9',
                    'answer': '9'
                },
                {
                    'order': 5,
                    'option': '45 + 36',
                    'answer': '81'
                },
                {
                    'order': 6,
                    'option': '72 - 18',
                    'answer': '54'
                },
                {
                    'order': 7,
                    'option': '9 × 7',
                    'answer': '63'
                },
                {
                    'order': 8,
                    'option': '100 ÷ 4',
                    'answer': '25'
                },
                {
                    'order': 9,
                    'option': '23 + 54',
                    'answer': '77'
                },
                {
                    'order': 10,
                    'option': '49 - 17',
                    'answer': '32'
                }
        ]

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
        with open(question_001_dir / "content.yaml", 'w') as f:
            yaml.dump(question_001_data, f)
        with open(question_001_dir / "answers.yaml", 'w') as f:
            yaml.dump(answers_data, f)
        # Create question 002 with different content format
        question_002_dir = questions_dir / "002"
        question_002_dir.mkdir()
        question_002_data = {
            'question_content': 'Is this a test?',  # Using question_content instead of question
            'question_type': 'short',
            'answers_type': 'binary'
        }
        with open(question_002_dir / "content.yaml", 'w') as f:  # Using content.yaml instead of question.yaml
            yaml.dump(question_002_data, f)
        with open(question_002_dir / "answers.yaml", 'w') as f:
            yaml.dump(answers_data, f)

        # Create invalid YAML for question 003
        question_003_dir = questions_dir / "003"
        question_003_dir.mkdir()
        with open(question_003_dir / "content.yaml", 'w') as f:
            f.write("invalid: yaml: content: [")
        with open(question_003_dir / "answers.yaml", 'w') as f:
            yaml.dump(answers_data, f)
            
    def test_card_question_text_property(self):
        # Test different content formats
        card1 = Card('001', {'question': 'Test question'})
        self.assertEqual(card1.question_text, 'Test question')
        
        card2 = Card('002', {'question_content': 'Test content'})
        self.assertEqual(card2.question_text, 'Test content')
        
        card3 = Card('003', {'content': 'Test content'})
        self.assertEqual(card3.question_text, 'Test content')
        
        card4 = Card('004', {})  # Test missing content
        self.assertEqual(card4.question_text, 'No question content')
        
    def test_card_loader_error_handling(self):
        loader = CardLoader(self.input_path / "cards")
        
        # Test invalid YAML
        with self.assertRaises(Exception):
            loader.load_card('003')
            
        # Test non-existent card
        with self.assertRaises(FileNotFoundError):
            loader.load_card('999')
            
    def test_markdown_generator_variations(self):
        # Test card with all fields
        card1 = Card('001', {
            'question': 'What is 2+2?',
            'options': ['3', '4', '5'],
            'question_type': 'short',
            'answers_type': 'single',
            'sources': ['https://example.com']
        })
        
        content1 = MarkdownGenerator.card_to_markdown(card1)
        self.assertIn('## Question', content1)
        self.assertIn('## Options', content1)
        self.assertIn('## Question Type', content1)
        self.assertIn('## Answer Type', content1)
        self.assertIn('## Sources', content1)
        
        # Test card with minimal fields
        card2 = Card('002', {
            'question': 'Simple question'
        })
        
        content2 = MarkdownGenerator.card_to_markdown(card2)
        self.assertIn('## Question', content2)
        self.assertNotIn('## Options', content2)
        self.assertNotIn('## Question Type', content2)
        self.assertNotIn('## Answer Type', content2)
        self.assertNotIn('## Sources', content2)
        
    def test_create_index_content(self):
        deck_meta = {
            'title': 'Test Deck',
            'introduction': 'Test introduction'
        }
        
        cards = [
            Card('001', {'question': 'Q1'}),
            Card('002', {'question': 'Q2'})
        ]
        
        content = MarkdownGenerator.create_index_content(deck_meta, cards)
        self.assertIn('# Test Deck', content)
        self.assertIn('Test introduction', content)
        self.assertIn('- [Question 001](001.md)', content)
        self.assertIn('- [Question 002](002.md)', content)
        
    def test_yaml_to_markdown_error_handling(self):
        converter = YAMLToMarkdown([str(self.input_path)])
        
        # Test processing invalid card
        converter.process_card('003')  # Should log error but not raise exception
        
        # Test processing non-existent card
        converter.process_card('999')  # Should log error but not raise exception
        
    def test_process_deck_with_errors(self):
        converter = YAMLToMarkdown([str(self.input_path)])
        converter.process_deck()
        
# /var/folders/ky/7b9535s17b1b4kxd3k1bv00r0000gn/T/tmppljf4sq6/output/index.md


        # Should still create index and valid cards
        print(f"Index file: {self.input_path / 'index.md'}")
        self.assertTrue((self.input_path / "index.md").exists())
        self.assertTrue((self.input_path / "cards/001/content.md").exists())
        self.assertTrue((self.input_path / "cards/002/content.md").exists())
        self.assertFalse((self.input_path / "cards/003/content.md").exists())  # Invalid card should not be created
        
    def tearDown(self):
        # Clean up temporary directory
        import shutil
        shutil.rmtree(self.test_dir)

if __name__ == '__main__':
    unittest.main() 