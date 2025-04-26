"""Tests for the main converter module."""
import os
import pytest
from unittest.mock import patch, MagicMock, call

from svg_to_pdf.converter import SVGToPDFConverter
from svg_to_pdf.converters.base import BaseConverter

# Custom converter for testing
class TestConverter(BaseConverter):
    def __init__(self, dpi=254, should_succeed=True):
        super().__init__(dpi)
        self.should_succeed = should_succeed
        self.called = False
        
    def convert(self, svg_bytes, output_file):
        self.called = True
        return self.should_succeed

def test_converter_init():
    """Test converter initialization."""
    converter = SVGToPDFConverter(dpi=300)
    assert converter.dpi == 300
    assert len(converter.converters) > 0

def test_create_converters():
    """Test that all converters are created."""
    converter = SVGToPDFConverter()
    assert len(converter.converters) >= 5  # Should have at least 5 converters

@patch('svg_to_pdf.converter.ImageHandler')
def test_convert_svg_to_pdf_success(mock_image_handler, sample_svg_file, temp_dir):
    """Test successful conversion."""
    # Setup
    mock_handler = MagicMock()
    mock_handler.fix_image_references.return_value = "fixed_svg"
    mock_image_handler.return_value = mock_handler
    
    # Create test converter that always succeeds
    test_converter = TestConverter(should_succeed=True)
    
    converter = SVGToPDFConverter()
    converter.converters = [test_converter]
    
    # Test
    output_path = os.path.join(temp_dir, "output.pdf")
    result = converter.convert_svg_to_pdf(sample_svg_file, output_path)
    
    # Verify
    assert result == output_path
    assert test_converter.called
    mock_handler.fix_image_references.assert_called_once()

@patch('svg_to_pdf.converter.ImageHandler')
def test_convert_svg_to_pdf_try_all_converters(mock_image_handler, sample_svg_file, temp_dir):
    """Test that all converters are tried until one succeeds."""
    # Setup
    mock_handler = MagicMock()
    mock_handler.fix_image_references.return_value = "fixed_svg"
    mock_image_handler.return_value = mock_handler
    
    # Create test converters
    failing_converter1 = TestConverter(should_succeed=False)
    failing_converter2 = TestConverter(should_succeed=False)
    succeeding_converter = TestConverter(should_succeed=True)
    not_used_converter = TestConverter(should_succeed=True)
    
    converter = SVGToPDFConverter()
    converter.converters = [
        failing_converter1,
        failing_converter2,
        succeeding_converter,
        not_used_converter
    ]
    
    # Test
    output_path = os.path.join(temp_dir, "output.pdf")
    result = converter.convert_svg_to_pdf(sample_svg_file, output_path)
    
    # Verify
    assert result == output_path
    assert failing_converter1.called
    assert failing_converter2.called
    assert succeeding_converter.called
    assert not not_used_converter.called

@patch('svg_to_pdf.converter.ImageHandler')
def test_convert_svg_to_pdf_all_fail(mock_image_handler, sample_svg_file, temp_dir):
    """Test exception when all converters fail."""
    # Setup
    mock_handler = MagicMock()
    mock_handler.fix_image_references.return_value = "fixed_svg"
    mock_image_handler.return_value = mock_handler
    
    # Create test converters that all fail
    failing_converter1 = TestConverter(should_succeed=False)
    failing_converter2 = TestConverter(should_succeed=False)
    
    converter = SVGToPDFConverter()
    converter.converters = [failing_converter1, failing_converter2]
    
    # Test
    output_path = os.path.join(temp_dir, "output.pdf")
    with pytest.raises(Exception) as e:
        converter.convert_svg_to_pdf(sample_svg_file, output_path)
    
    # Verify
    assert "All conversion methods failed" in str(e.value)
    assert failing_converter1.called
    assert failing_converter2.called

def test_convert_svg_to_pdf_default_output(sample_svg_file, temp_dir):
    """Test that default output path is created correctly."""
    # Setup
    test_converter = TestConverter(should_succeed=True)
    
    with patch('svg_to_pdf.converter.ImageHandler') as mock_image_handler:
        mock_handler = MagicMock()
        mock_handler.fix_image_references.return_value = "fixed_svg"
        mock_image_handler.return_value = mock_handler
        
        converter = SVGToPDFConverter()
        converter.converters = [test_converter]
        
        # Test - don't specify output path
        result = converter.convert_svg_to_pdf(sample_svg_file)
        
        # Verify
        expected_output = sample_svg_file.replace('.svg', '.pdf')
        assert result == expected_output

@patch('svg_to_pdf.converter.argparse.ArgumentParser')
@patch('svg_to_pdf.converter.SVGToPDFConverter')
def test_main_success(mock_converter_class, mock_argparse):
    """Test main function with successful conversion."""
    # Setup
    mock_args = MagicMock()
    mock_args.svg_file = '/test/input.svg'
    mock_args.output = '/test/output.pdf'
    mock_args.verbose = False
    mock_args.dpi = 300
    mock_parser = MagicMock()
    mock_parser.parse_args.return_value = mock_args
    mock_argparse.return_value = mock_parser
    
    mock_converter = MagicMock()
    mock_converter.convert_svg_to_pdf.return_value = '/test/output.pdf'
    mock_converter_class.return_value = mock_converter
    
    # Test
    from svg_to_pdf.converter import main
    result = main()
    
    # Verify
    assert result == 0
    mock_converter_class.assert_called_once_with(dpi=300)
    mock_converter.convert_svg_to_pdf.assert_called_once_with('/test/input.svg', '/test/output.pdf')

@patch('svg_to_pdf.converter.argparse.ArgumentParser')
@patch('svg_to_pdf.converter.SVGToPDFConverter')
def test_main_failure(mock_converter_class, mock_argparse):
    """Test main function when conversion fails."""
    # Setup
    mock_args = MagicMock()
    mock_args.svg_file = '/test/input.svg'
    mock_args.output = '/test/output.pdf'
    mock_args.verbose = False
    mock_args.dpi = 300
    mock_parser = MagicMock()
    mock_parser.parse_args.return_value = mock_args
    mock_argparse.return_value = mock_parser
    
    mock_converter = MagicMock()
    mock_converter.convert_svg_to_pdf.side_effect = Exception("Test error")
    mock_converter_class.return_value = mock_converter
    
    # Test
    from svg_to_pdf.converter import main
    result = main()
    
    # Verify
    assert result == 1