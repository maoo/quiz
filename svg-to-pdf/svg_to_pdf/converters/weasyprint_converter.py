"""WeasyPrint converter implementation."""
import logging
import os
import tempfile
from pathlib import Path
from typing import Optional

from svg_to_pdf.converters.base import BaseConverter

logger = logging.getLogger(__name__)

class WeasyPrintConverter(BaseConverter):
    """SVG to PDF converter using WeasyPrint."""
    
    def convert(self, svg_bytes: bytes, output_file: str) -> bool:
        """Convert SVG to PDF using WeasyPrint with HTML embedding.
        
        Args:
            svg_bytes: Raw SVG content as bytes
            output_file: Path to the output PDF file
            
        Returns:
            bool: True if conversion successful, False otherwise
        """
        try:
            import weasyprint
            
            # Create an HTML wrapper for the SVG with proper styling
            html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>SVG to PDF Conversion</title>
    <style>
        @page {{ size: 11cm 11cm; margin: 0; }}
        body, html {{ margin: 0; padding: 0; width: 11cm; height: 11cm; }}
        .svg-container {{ width: 11cm; height: 11cm; }}
    </style>
</head>
<body>
    <div class="svg-container">{svg_bytes.decode('utf-8')}</div>
</body>
</html>"""
            
            with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as html_file:
                html_path = html_file.name
                html_file.write(html_content.encode('utf-8'))
            
            try:
                # Convert using WeasyPrint
                html = weasyprint.HTML(filename=html_path)
                html.write_pdf(output_file, zoom=self.dpi/96)  # Convert DPI to zoom factor
                
                logger.info(f"Successfully created PDF using {self.name}")
                return True
            finally:
                # Clean up temporary file
                if os.path.exists(html_path):
                    os.unlink(html_path)
                    
        except ImportError:
            logger.warning("WeasyPrint not installed, skipping this converter")
            return False
        except Exception as e:
            logger.error(f"{self.name} failed: {e}")
            return False