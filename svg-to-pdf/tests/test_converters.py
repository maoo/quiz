"""Tests for SVG converter modules."""
import os
import pytest
from unittest.mock import patch, MagicMock

from svg_to_pdf.converters.base import BaseConverter
from svg_to_pdf.converters.cairo_converter import CairoConverter
from svg_to_pdf.converters.svglib_converter import SvglibConverter
from svg_to_pdf.converters.system_converter import (
    InkscapeConverter,
    RsvgConverter,
    ChromeConverter,
    ImageMagickConverter
)

# Test base converter
def test_base_converter_abstract():
    """Test that BaseConverter is abstract and can't be instantiated."""
    with pytest.raises(TypeError):
        BaseConverter()

def test_base_converter_name():
    """Test the name property of converter classes."""
    class TestConverter(BaseConverter):
        def convert(self, svg_bytes, output_file):
            return True
    
    converter = TestConverter()
    assert converter.name == "TestConverter"

# Test CairoConverter
@patch('svg_to_pdf.converters.cairo_converter.cairosvg')
@patch('svg_to_pdf.converters.cairo_converter.etree')
def test_cairo_converter_success(mock_etree, mock_cairosvg, sample_svg):
    """Test successful conversion with CairoConverter."""
    # Setup
    mock_etree.XMLParser.return_value = "parser"
    mock_etree.fromstring.return_value = "tree"
    mock_etree.tostring.return_value = b"fixed_svg"
    
    converter = CairoConverter()
    result = converter.convert(sample_svg.encode('utf-8'), '/tmp/output.pdf')
    
    # Verify
    assert result is True
    mock_etree.XMLParser.assert_called_once_with(recover=True)
    mock_etree.fromstring.assert_called_once()
    mock_etree.tostring.assert_called_once_with("tree", encoding='utf-8', xml_declaration=True)
    mock_cairosvg.svg2pdf.assert_called_once()

@patch('svg_to_pdf.converters.cairo_converter.cairosvg')
@patch('svg_to_pdf.converters.cairo_converter.etree')
def test_cairo_converter_lxml_failure_fallback(mock_etree, mock_cairosvg, sample_svg):
    """Test fallback when lxml fails."""
    # Setup
    mock_etree.XMLParser.side_effect = Exception("Test error")
    
    converter = CairoConverter()
    result = converter.convert(sample_svg.encode('utf-8'), '/tmp/output.pdf')
    
    # Verify
    assert result is True
    mock_cairosvg.svg2pdf.assert_called_once()

@patch('svg_to_pdf.converters.cairo_converter.cairosvg')
def test_cairo_converter_failure(mock_cairosvg, sample_svg):
    """Test failure handling in CairoConverter."""
    # Setup
    mock_cairosvg.svg2pdf.side_effect = Exception("Test error")
    
    converter = CairoConverter()
    result = converter.convert(sample_svg.encode('utf-8'), '/tmp/output.pdf')
    
    # Verify
    assert result is False

# Test SvglibConverter
@patch('svglib.svglib.svg2rlg')
@patch('reportlab.graphics.renderPDF')
def test_svglib_converter_success(mock_renderPDF, mock_svg2rlg, sample_svg):
    """Test successful conversion with SvglibConverter."""
    # Setup
    mock_svg2rlg.return_value = "drawing"
    
    converter = SvglibConverter()
    with patch('tempfile.NamedTemporaryFile') as mock_temp:
        mock_temp.return_value.__enter__.return_value.name = '/tmp/test.svg'
        result = converter.convert(sample_svg.encode('utf-8'), '/tmp/output.pdf')
    
    # Verify
    assert result is True
    mock_svg2rlg.assert_called_once_with('/tmp/test.svg')
    mock_renderPDF.drawToFile.assert_called_once_with('drawing', '/tmp/output.pdf')

@patch('svglib.svglib.svg2rlg')
def test_svglib_converter_failure(mock_svg2rlg, sample_svg):
    """Test failure handling in SvglibConverter."""
    # Setup
    mock_svg2rlg.side_effect = Exception("Test error")
    
    converter = SvglibConverter()
    with patch('tempfile.NamedTemporaryFile') as mock_temp:
        mock_temp.return_value.__enter__.return_value.name = '/tmp/test.svg'
        result = converter.convert(sample_svg.encode('utf-8'), '/tmp/output.pdf')
    
    # Verify
    assert result is False

@patch('svg_to_pdf.converters.svglib_converter.svg2rlg', None)
def test_svglib_converter_import_error(sample_svg):
    """Test import error handling in SvglibConverter."""
    converter = SvglibConverter()
    result = converter.convert(sample_svg.encode('utf-8'), '/tmp/output.pdf')
    assert result is False

# Test system converters
@patch('svg_to_pdf.converters.system_converter.shutil.which')
@patch('svg_to_pdf.converters.system_converter.subprocess.run')
def test_inkscape_converter_not_found(mock_run, mock_which, sample_svg):
    """Test behavior when Inkscape is not installed."""
    # Setup
    mock_which.return_value = None
    
    converter = InkscapeConverter()
    result = converter.convert(sample_svg.encode('utf-8'), '/tmp/output.pdf')
    
    # Verify
    assert result is False
    mock_run.assert_not_called()

@patch('svg_to_pdf.converters.system_converter.shutil.which')
@patch('svg_to_pdf.converters.system_converter.subprocess.run')
def test_inkscape_converter_success(mock_run, mock_which, sample_svg):
    """Test successful conversion with InkscapeConverter."""
    # Setup
    mock_which.return_value = '/usr/bin/inkscape'
    mock_run.return_value.returncode = 0
    mock_run.return_value.stdout = "Inkscape 1.0"
    
    converter = InkscapeConverter()
    with patch('tempfile.NamedTemporaryFile') as mock_temp:
        mock_temp.return_value.__enter__.return_value.name = '/tmp/test.svg'
        result = converter.convert(sample_svg.encode('utf-8'), '/tmp/output.pdf')
    
    # Verify
    assert result is True
    assert mock_run.call_count == 2  # Once for version check, once for conversion

@patch('svg_to_pdf.converters.system_converter.shutil.which')
@patch('svg_to_pdf.converters.system_converter.subprocess.run')
def test_rsvg_converter_success(mock_run, mock_which, sample_svg):
    """Test successful conversion with RsvgConverter."""
    # Setup
    mock_which.return_value = '/usr/bin/rsvg-convert'
    mock_run.return_value.returncode = 0
    
    converter = RsvgConverter()
    with patch('tempfile.NamedTemporaryFile') as mock_temp:
        mock_temp.return_value.__enter__.return_value.name = '/tmp/test.svg'
        result = converter.convert(sample_svg.encode('utf-8'), '/tmp/output.pdf')
    
    # Verify
    assert result is True
    mock_run.assert_called_once()

@patch('svg_to_pdf.converters.system_converter.shutil.which')
@patch('svg_to_pdf.converters.system_converter.subprocess.run')
@patch('svg_to_pdf.converters.system_converter.os.path.exists')
def test_chrome_converter_success(mock_exists, mock_run, mock_which, sample_svg):
    """Test successful conversion with ChromeConverter."""
    # Setup
    mock_which.return_value = '/usr/bin/chrome'
    mock_run.return_value.returncode = 0
    mock_exists.return_value = True
    
    converter = ChromeConverter()
    with patch('tempfile.NamedTemporaryFile') as mock_temp:
        mock_temp.return_value.__enter__.return_value.name = '/tmp/test.html'
        result = converter.convert(sample_svg.encode('utf-8'), '/tmp/output.pdf')
    
    # Verify
    assert result is True
    mock_run.assert_called_once()

@patch('svg_to_pdf.converters.system_converter.shutil.which')
@patch('svg_to_pdf.converters.system_converter.subprocess.run')
def test_imagemagick_converter_success(mock_run, mock_which, sample_svg):
    """Test successful conversion with ImageMagickConverter."""
    # Setup
    mock_which.side_effect = lambda x: '/usr/bin/convert' if x == 'convert' else None
    mock_run.return_value.returncode = 0
    
    converter = ImageMagickConverter()
    with patch('tempfile.NamedTemporaryFile') as mock_temp:
        mock_temp.return_value.__enter__.return_value.name = '/tmp/test.svg'
        result = converter.convert(sample_svg.encode('utf-8'), '/tmp/output.pdf')
    
    # Verify
    assert result is True
    mock_run.assert_called_once()