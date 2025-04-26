import pytest
from src.svg_to_pdf.converter import SVGToPDFConverter

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
    output_path = tmp_path / "test.pdf"
    
    # Test the conversion
    converter.convert(svg_content, str(output_path))
    
    # Verify the output file exists
    assert output_path.exists()
    assert output_path.stat().st_size > 0

def test_invalid_svg_content():
    converter = SVGToPDFConverter()
    invalid_svg = "not a valid svg content"
    
    with pytest.raises(Exception):
        converter.convert(invalid_svg, "output.pdf") 