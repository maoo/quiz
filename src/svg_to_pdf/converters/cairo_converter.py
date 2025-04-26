"""
Cairo-based SVG to PDF converter.
"""

import os
from typing import Optional

import cairosvg

from .base import BaseConverter


class CairoConverter(BaseConverter):
    """
    SVG to PDF converter using CairoSVG.
    """
    
    def convert(self, svg_bytes: bytes, output_file: str) -> bool:
        """
        Convert SVG bytes to PDF using CairoSVG.
        
        Args:
            svg_bytes: SVG content as bytes
            output_file: Path to the output PDF file
            
        Returns:
            bool: True if conversion was successful, False otherwise
        """
        try:
            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            # Convert SVG to PDF
            cairosvg.svg2pdf(
                bytestring=svg_bytes,
                write_to=output_file,
                dpi=self.dpi
            )
            return True
        except Exception as e:
            print(f"Cairo conversion failed: {e}")
            return False 