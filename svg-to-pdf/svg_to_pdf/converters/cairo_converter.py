"""CairoSVG converter implementation."""
import logging
import tempfile
from pathlib import Path
from typing import Optional

# Third-party imports
import cairosvg
from lxml import etree

from svg_to_pdf.converters.base import BaseConverter

logger = logging.getLogger(__name__)

class CairoConverter(BaseConverter):
    """SVG to PDF converter using CairoSVG."""
    
    def convert(self, svg_bytes: bytes, output_file: str) -> bool:
        """Convert SVG to PDF using CairoSVG with XML validation.
        
        Args:
            svg_bytes: Raw SVG content as bytes
            output_file: Path to the output PDF file
            
        Returns:
            bool: True if conversion successful, False otherwise
        """
        try:
            # Try to fix the SVG XML using lxml
            try:
                parser = etree.XMLParser(recover=True)
                tree = etree.fromstring(svg_bytes, parser)
                fixed_svg_bytes = etree.tostring(tree, encoding='utf-8', xml_declaration=True)
                logger.info("Successfully fixed SVG XML using lxml")
                
                # Use the fixed SVG
                cairosvg.svg2pdf(
                    bytestring=fixed_svg_bytes,
                    write_to=output_file,
                    dpi=self.dpi,
                    unsafe=True  # Needed to allow loading local resources
                )
            except Exception as lxml_error:
                logger.warning(f"Failed to fix SVG with lxml: {lxml_error}")
                # Fall back to direct CairoSVG conversion
                cairosvg.svg2pdf(
                    bytestring=svg_bytes,
                    write_to=output_file,
                    dpi=self.dpi,
                    unsafe=True  # Needed to allow loading local resources
                )
                
            logger.info(f"Successfully created PDF using {self.name}")
            return True
        except Exception as e:
            logger.error(f"{self.name} failed: {e}")
            return False