"""SVGLib/ReportLab converter implementation."""
import logging
import os
import tempfile
from pathlib import Path
from typing import Optional

from svg_to_pdf.converters.base import BaseConverter

logger = logging.getLogger(__name__)

class SvglibConverter(BaseConverter):
    """SVG to PDF converter using svglib/reportlab."""
    
    def convert(self, svg_bytes: bytes, output_file: str) -> bool:
        """Convert SVG to PDF using svglib and reportlab.
        
        Args:
            svg_bytes: Raw SVG content as bytes
            output_file: Path to the output PDF file
            
        Returns:
            bool: True if conversion successful, False otherwise
        """
        try:
            from svglib.svglib import svg2rlg
            from reportlab.graphics import renderPDF
            
            # Fix common SVG issues by adding a new line before closing tag
            fixed_svg = svg_bytes.decode('utf-8').replace('</svg>', '\n</svg>')
            
            with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as temp_svg:
                temp_svg_path = temp_svg.name
                temp_svg.write(fixed_svg.encode('utf-8'))
            
            try:
                # Convert using svglib/reportlab
                drawing = svg2rlg(temp_svg_path)
                renderPDF.drawToFile(drawing, output_file)
                
                logger.info(f"Successfully created PDF using {self.name}")
                return True
            finally:
                # Clean up temporary file
                if os.path.exists(temp_svg_path):
                    os.unlink(temp_svg_path)
                    
        except ImportError:
            logger.warning("svglib/reportlab not installed, skipping this converter")
            return False
        except Exception as e:
            logger.error(f"{self.name} failed: {e}")
            return False