"""Tests for the image handler module."""
import base64
import os
import pytest
from svg_to_pdf.image_handler import ImageHandler

def test_init_default():
    """Test ImageHandler initialization with default values."""
    handler = ImageHandler()
    assert handler.base_dir == os.getcwd()

def test_init_with_base_dir():
    """Test ImageHandler initialization with specified base directory."""
    handler = ImageHandler(base_dir="/tmp")
    assert handler.base_dir == "/tmp"

def test_fix_image_references_no_change(sample_svg):
    """Test that SVG without images is unchanged."""
    handler = ImageHandler()
    result = handler.fix_image_references(sample_svg)
    assert result == sample_svg

def test_fix_image_references_remote_unchanged(svg_with_image):
    """Test that remote image references are unchanged when local file not found."""
    handler = ImageHandler()
    result = handler.fix_image_references(svg_with_image)
    assert "https://example.com/image.png" in result
    assert "file://" not in result
    assert "data:" not in result

def test_fix_image_references_with_qr(svg_with_qr_file, qr_image_dir):
    """Test that QR code references are replaced with data URIs."""
    # Setup the handler with the directory containing the QR code
    qr_dir = os.path.join(qr_image_dir, "decks", "devops-hero", "questions")
    handler = ImageHandler(base_dir=qr_dir)
    
    # Read the SVG file
    with open(svg_with_qr_file, 'r') as f:
        svg_content = f.read()
    
    # Fix image references
    result = handler.fix_image_references(svg_content)
    
    # Verify that the image reference was replaced with a data URI
    assert "https://blog.session.it/quiz/decks/devops-hero/questions/002-qr.png" not in result
    assert "data:image/png;base64," in result

def test_fix_image_references_data_uri_unchanged():
    """Test that data URIs are left unchanged."""
    svg_with_data_uri = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg width="200" height="200" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <rect x="10" y="10" width="180" height="180" fill="blue" />
  <image x="50" y="50" width="100" height="100" xlink:href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+P+/HgAFDQIZB8SR1wAAAABJRU5ErkJggg==" />
</svg>"""
    
    handler = ImageHandler()
    result = handler.fix_image_references(svg_with_data_uri)
    
    assert result == svg_with_data_uri

def test_fix_image_references_multiple_patterns(qr_image_dir):
    """Test handling of various filename patterns."""
    # Create test files
    qr_dir = os.path.join(qr_image_dir, "decks", "devops-hero", "questions")
    
    # Create additional test images
    from PIL import Image
    
    # Standard QR image
    img1 = Image.new('RGB', (100, 100), color='black')
    img1_path = os.path.join(qr_dir, "test-qr.png")
    img1.save(img1_path)
    
    # Output-style image - save as PNG (Pillow doesn't support SVG)
    img2 = Image.new('RGB', (100, 100), color='red')
    img2_path = os.path.join(qr_dir, "test-output.png")
    img2.save(img2_path)
    
    # Create an empty SVG file
    svg_path = os.path.join(qr_dir, "test-output.svg")
    with open(svg_path, 'w') as f:
        f.write('<svg></svg>')
    
    # Test SVG with different patterns
    svg_content = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <image id="img1" xlink:href="https://example.com/test-qr.png" />
  <image id="img2" xlink:href="https://example.com/test-output.svg" />
</svg>"""
    
    # Test the handler
    handler = ImageHandler(base_dir=qr_dir)
    result = handler.fix_image_references(svg_content)
    
    # Check that QR image was replaced
    assert "https://example.com/test-qr.png" not in result
    assert "data:image/png;base64," in result    # QR code embedded
    
    # Check the SVG file reference - it's also being embedded as data URI
    assert "https://example.com/test-output.svg" not in result
    assert "data:image/svg+xml;base64," in result   # Both are embedded as data URIs