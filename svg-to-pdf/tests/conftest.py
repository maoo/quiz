"""Pytest fixtures for testing."""
import os
import pytest
import tempfile
from pathlib import Path

@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir
        
@pytest.fixture
def sample_svg():
    """Simple sample SVG for testing."""
    return """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg width="200" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="10" width="180" height="180" fill="blue" />
  <circle cx="100" cy="100" r="50" fill="red" />
</svg>"""

@pytest.fixture
def svg_with_image():
    """SVG with an image reference."""
    return """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg width="200" height="200" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <rect x="10" y="10" width="180" height="180" fill="blue" />
  <image x="50" y="50" width="100" height="100" xlink:href="https://example.com/image.png" />
</svg>"""

@pytest.fixture
def svg_with_qr():
    """SVG with a QR code reference."""
    return """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg width="200" height="200" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <rect x="10" y="10" width="180" height="180" fill="blue" />
  <image x="50" y="50" width="100" height="100" xlink:href="https://blog.session.it/quiz/decks/devops-hero/questions/002-qr.png" />
</svg>"""

@pytest.fixture
def invalid_svg():
    """Invalid SVG for testing error handling."""
    return """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg width="200" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="10" width="180" height="180" fill="blue" 
  <circle cx="100" cy="100" r="50" fill="red" />
</svg>"""

@pytest.fixture
def sample_svg_file(temp_dir, sample_svg):
    """Create a sample SVG file."""
    svg_path = os.path.join(temp_dir, "sample.svg")
    with open(svg_path, 'w') as f:
        f.write(sample_svg)
    return svg_path

@pytest.fixture
def svg_with_image_file(temp_dir, svg_with_image):
    """Create an SVG file with an image reference."""
    svg_path = os.path.join(temp_dir, "sample_with_image.svg")
    with open(svg_path, 'w') as f:
        f.write(svg_with_image)
    return svg_path

@pytest.fixture
def qr_image_dir(temp_dir):
    """Create a directory structure with QR image."""
    qr_dir = os.path.join(temp_dir, "decks", "devops-hero", "questions")
    os.makedirs(qr_dir, exist_ok=True)
    
    # Create a sample QR code image
    qr_path = os.path.join(qr_dir, "002-qr.png")
    
    # Create a small black square as a fake QR code
    from PIL import Image
    img = Image.new('RGB', (100, 100), color='black')
    img.save(qr_path)
    
    return temp_dir

@pytest.fixture
def svg_with_qr_file(temp_dir, qr_image_dir, svg_with_qr):
    """Create an SVG file with a QR code reference."""
    svg_path = os.path.join(temp_dir, "sample_with_qr.svg")
    with open(svg_path, 'w') as f:
        f.write(svg_with_qr)
    return svg_path

@pytest.fixture
def invalid_svg_file(temp_dir, invalid_svg):
    """Create an invalid SVG file."""
    svg_path = os.path.join(temp_dir, "invalid.svg")
    with open(svg_path, 'w') as f:
        f.write(invalid_svg)
    return svg_path