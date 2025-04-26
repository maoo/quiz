import os
import tempfile
from pathlib import Path

import pytest
from svg_to_pdf.converter import SVGToPDFConverter

def test_convert_svg_to_pdf():
    # Create a temporary SVG file
    with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as tmp:
        svg_content = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">
  <rect width="100" height="100" fill="red"/>
</svg>"""
        tmp.write(svg_content.encode())
        svg_path = tmp.name

    try:
        # Create output PDF path
        pdf_path = svg_path.replace('.svg', '.pdf')
        
        # Convert SVG to PDF
        converter = SVGToPDFConverter()
        converter.convert_svg_to_pdf(svg_path, pdf_path)
        
        # Verify PDF was created
        assert os.path.exists(pdf_path)
        assert os.path.getsize(pdf_path) > 0
        
    finally:
        # Clean up
        if os.path.exists(svg_path):
            os.unlink(svg_path)
        if os.path.exists(pdf_path):
            os.unlink(pdf_path) 