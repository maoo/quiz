import pytest
import os
import sys
import tempfile
from pathlib import Path
from src.svg_to_pdf.converter import SVGToPDFConverter
from unittest.mock import patch

@pytest.fixture
def tmp_path():
    """Fixture to create a new temporary directory for each test"""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)

def test_converter_initialization():
    converter = SVGToPDFConverter()
    assert converter is not None

def test_convert_svg_to_pdf(tmp_path):
    converter = SVGToPDFConverter()
    # Create a simple SVG content
    svg_content = """
    <svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">
        <rect width="100" height="100" fill="red"/>
    </svg>
    """
    svg_file = tmp_path / "test.svg"
    output_path = tmp_path / "test.pdf"
    
    # Write SVG content to file
    svg_file.write_text(svg_content)
    
    # Test the conversion
    converter.convert_svg_to_pdf(str(svg_file), str(output_path))
    
    # Verify the output file exists
    assert output_path.exists()
    assert output_path.stat().st_size > 0

def test_invalid_svg_content():
    converter = SVGToPDFConverter()
    invalid_svg = "not a valid svg content"
    
    with pytest.raises(Exception):
        converter.convert_svg_to_pdf(invalid_svg, "output.pdf")

def test_cli_interface(tmp_path):
    # Create a test SVG file
    svg_file = tmp_path / "test.svg"
    svg_content = """
    <svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">
        <rect width="100" height="100" fill="red"/>
    </svg>
    """
    svg_file.write_text(svg_content)
    
    # Create a non-SVG file to test filtering
    non_svg_file = tmp_path / "index.md"
    non_svg_file.write_text("# Test README")
    
    # Test the CLI with a single SVG file
    with patch.object(sys, 'argv', ['converter.py', str(svg_file)]):
        from src.svg_to_pdf.converter import main
        assert main() == 0  # Should succeed
    
    # Verify the output PDF was created
    output_pdf = tmp_path / "test.pdf"
    assert output_pdf.exists()
    assert output_pdf.stat().st_size > 0
    
    # Test that non-SVG files are rejected
    with patch.object(sys, 'argv', ['converter.py', str(non_svg_file)]):
        assert main() == 1  # Should fail with error code 1 