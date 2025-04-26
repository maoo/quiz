"""Tests for the SVG Generator."""
import os
import pytest
from unittest.mock import patch, MagicMock
import math
import sys
import tempfile

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from generator import QuizSVGGenerator, main



def test_init_default():
    """Test QuizSVGGenerator initialization with default values."""
    generator = QuizSVGGenerator()
    assert generator.width == 1110
    assert generator.height == 1110
    assert generator.center_x == 555
    assert generator.center_y == 555



def test_init_custom():
    """Test QuizSVGGenerator initialization with custom values."""
    generator = QuizSVGGenerator(width=1000, height=800)
    assert generator.width == 1000
    assert generator.height == 800
    assert generator.center_x == 500
    assert generator.center_y == 400



def test_has_qr_code_true():
    """Test has_qr_code when QR file exists."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create mock files
        question_path = os.path.join(tmpdir, "test-question.md")
        qr_path = os.path.join(tmpdir, "test-qr.png")
        # Create empty files
        open(question_path, 'w').close()
        open(qr_path, 'w').close()
        generator = QuizSVGGenerator()
        assert generator.has_qr_code(question_path) is True



def test_has_qr_code_false():
    """Test has_qr_code when QR file doesn't exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        question_path = os.path.join(tmpdir, "test-question.md")
        open(question_path, 'w').close()
        generator = QuizSVGGenerator()
        assert generator.has_qr_code(question_path) is False



def test_parse_markdown(test_question_md, temp_markdown_file):
    """Test parsing markdown content."""
    generator = QuizSVGGenerator()
    title, options, answers = generator.parse_markdown(temp_markdown_file)
    assert title == "Container Security Best Practices"
    assert len(options) == 10
    assert "Use minimal base images" in options
    assert "Run as non-root user" in options
    
    # Check that the correct options are marked as true
    assert answers[0] is True  # Use minimal base images
    assert answers[1] is True  # Run as non-root user
    assert answers[2] is True  # Set --read-only flag
    assert answers[3] is True  # Scan images regularly
    assert answers[6] is True  # Sign container images
    assert answers[4] is False  # Pin dependency versions


def test_calculate_position():
    """Test position calculation."""
    generator = QuizSVGGenerator(width=1000, height=1000)

    # Test first position (top)
    x, y = generator.calculate_position(0, 10, 100)
    assert x == pytest.approx(500)
    assert y == pytest.approx(400)
    
    # Test a middle position
    x, y = generator.calculate_position(2, 10, 100)
    expected_angle = 2 * math.pi * 2 / 10 - math.pi / 2
    expected_x = 500 + 100 * math.cos(expected_angle)
    expected_y = 500 + 100 * math.sin(expected_angle)
    assert x == pytest.approx(expected_x)
    assert y == pytest.approx(expected_y)


@patch('generator.svgwrite')
def test_generate_svg_basic(mock_svgwrite, temp_markdown_file, tmp_path):
    """Test SVG generation without QR code."""
    # Setup
    mock_drawing = MagicMock()
    mock_svgwrite.Drawing.return_value = mock_drawing
    output_path = str(tmp_path / "output.svg")
    
    # Run
    generator = QuizSVGGenerator()
    generator.generate_svg(temp_markdown_file, output_path)
    
    # Verify
    mock_svgwrite.Drawing.assert_called_once_with(output_path, size=(1110, 1110))
    assert mock_drawing.add.call_count > 0
    mock_drawing.save.assert_called_once_with(pretty=True, indent=2)


@patch('generator.svgwrite')
def test_generate_svg_with_qr(mock_svgwrite, temp_markdown_file, temp_qr_file, tmp_path):
    """Test SVG generation with QR code."""
    # Setup
    mock_drawing = MagicMock()
    mock_svgwrite.Drawing.return_value = mock_drawing
    # Rename QR file to match the markdown file
    qr_path = os.path.join(
        os.path.dirname(temp_markdown_file),
        os.path.basename(temp_markdown_file).replace('-question.md', '-qr.png'))
    
    # Create QR file
    os.makedirs(os.path.dirname(qr_path), exist_ok=True)
    with open(qr_path, 'wb') as f:
        f.write(b"dummy QR")
    
    output_path = str(tmp_path / "output.svg")
    
    # Run
    generator = QuizSVGGenerator()
    
    # Mock has_qr_code to always return True
    with patch.object(generator, 'has_qr_code', return_value=True):
        generator.generate_svg(temp_markdown_file, output_path)
    
    # Verify
    mock_svgwrite.Drawing.assert_called_once_with(output_path, size=(1110, 1110))
    mock_image_calls = [call for call in mock_drawing.mock_calls if 'image' in str(call)]
    assert len(mock_image_calls) > 0
    mock_drawing.save.assert_called_once_with(pretty=True, indent=2)

@patch('generator.QuizSVGGenerator')
def test_main(mock_generator_class, tmp_path):
    """Test the main function."""
    # Setup
    mock_generator = MagicMock()
    mock_generator_class.return_value = mock_generator
    
    input_path = str(tmp_path / "input.md")
    output_path = str(tmp_path / "output.svg")
    
    # Save original argv
    orig_argv = sys.argv
    
    try:
        # Override sys.argv with test values
        sys.argv = ['generator.py', input_path, output_path]
        
        # Run
        main()
        
        # Verify
        mock_generator_class.assert_called_once_with()
        mock_generator.generate_svg.assert_called_once_with(input_path, output_path)
    finally:
        # Restore original argv
        sys.argv = orig_argv

def test_main_error():
    """Test the main function with insufficient arguments."""
    # Save original argv
    orig_argv = sys.argv
    
    try:
        # Override sys.argv with test values
        sys.argv = ['generator.py']
        
        # Check SystemExit is raised with correct exit code
        with pytest.raises(SystemExit) as excinfo:
            main()
        
        # Check that the exit code is 1
        assert excinfo.value.code == 1
    finally:
        # Restore original argv
        sys.argv = orig_argv

