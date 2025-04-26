#!/usr/bin/env python3
"""
SVG to PDF Converter with image support.

Converts SVG files to PDF format, preserving embedded images and
ensuring the 1100x1100 pixel canvas is rendered as 11x11cm in the PDF.
"""

import argparse
import logging
import os
import sys
import tempfile
from pathlib import Path
from typing import List, Optional

from svg_to_pdf.converters.base import BaseConverter
from svg_to_pdf.converters.cairo_converter import CairoConverter
from svg_to_pdf.converters.weasyprint_converter import WeasyPrintConverter
from svg_to_pdf.converters.svglib_converter import SvglibConverter
from svg_to_pdf.converters.system_converter import (
    InkscapeConverter,
    RsvgConverter,
    ChromeConverter,
    ImageMagickConverter
)
from svg_to_pdf.image_handler import ImageHandler

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class SVGToPDFConverter:
    """Main SVG to PDF conversion class."""
    
    def __init__(self, dpi: int = 254):
        """Initialize the SVG to PDF converter.
        
        Args:
            dpi: DPI to use for PDF generation (default: 254 which gives 100px per cm)
        """
        self.dpi = dpi
        self.converters = self._create_converters()
        
    def _create_converters(self) -> List[BaseConverter]:
        """Create all available converters in order of preference.
        
        Returns:
            List of converter instances.
        """
        return [
            CairoConverter(self.dpi),
            WeasyPrintConverter(self.dpi),
            SvglibConverter(self.dpi),
            InkscapeConverter(self.dpi),
            RsvgConverter(self.dpi),
            ChromeConverter(self.dpi),
            ImageMagickConverter(self.dpi)
        ]
        
    def convert_svg_to_pdf(self, svg_file: str, output_file: Optional[str] = None) -> str:
        """Convert SVG file to PDF with proper image handling.
        
        Args:
            svg_file: Path to the SVG file
            output_file: Path to the output PDF file
            
        Returns:
            Path to the generated PDF file
            
        Raises:
            Exception: If all conversion methods fail
        """
        svg_path = Path(svg_file)
        
        # Default output path if not provided
        if output_file is None:
            output_file = str(svg_path.with_suffix('.pdf'))
        
        # Create a temporary file for the modified SVG
        with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as temp_svg:
            temp_svg_path = temp_svg.name
            
            # Read the SVG content
            with open(svg_path, 'r', encoding='utf-8') as f:
                svg_content = f.read()
            
            # Fix image references
            image_handler = ImageHandler(base_dir=svg_path.parent)
            modified_svg = image_handler.fix_image_references(svg_content)
            
            # Write the modified SVG to the temporary file
            temp_svg.write(modified_svg.encode('utf-8'))
        
        try:
            # Convert SVG to PDF using our converters in order
            logger.info(f"Converting {svg_file} to {output_file} at {self.dpi} DPI")
            
            with open(temp_svg_path, 'rb') as f:
                svg_bytes = f.read()
                
            # Try each converter until one succeeds
            success = False
            for converter in self.converters:
                if converter.convert(svg_bytes, output_file):
                    success = True
                    break
            
            if not success:
                raise Exception("All conversion methods failed")
                
            logger.info(f"Successfully created PDF: {output_file}")
            return output_file
            
        except Exception as e:
            logger.error(f"Conversion failed: {e}")
            raise
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_svg_path):
                os.unlink(temp_svg_path)

def main():
    """Command-line interface for the SVG to PDF converter."""
    parser = argparse.ArgumentParser(description='Convert SVG files to PDF with proper image support')
    parser.add_argument('svg_file', help='Path to the SVG file to convert')
    parser.add_argument('-o', '--output', help='Path to the output PDF file')
    parser.add_argument('--width', type=float, default=11, help='Width in centimeters (default: 11)')
    parser.add_argument('--height', type=float, default=11, help='Height in centimeters (default: 11)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--dpi', type=int, default=254, 
                      help='DPI for PDF generation (default: 254, which is ~100px per cm)')
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logger.setLevel(logging.DEBUG)
        # Set all loggers to DEBUG
        for name in logging.root.manager.loggerDict:
            logging.getLogger(name).setLevel(logging.DEBUG)
    
    try:
        converter = SVGToPDFConverter(dpi=args.dpi)
        output_file = converter.convert_svg_to_pdf(
            args.svg_file, 
            args.output
        )
        logger.info(f"Conversion complete: {output_file}")
        return 0
    except Exception as e:
        logger.error(f"Conversion failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())