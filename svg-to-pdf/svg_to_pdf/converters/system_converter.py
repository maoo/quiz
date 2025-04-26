"""External tool converters using system utilities."""
import logging
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import List, Optional

from svg_to_pdf.converters.base import BaseConverter

logger = logging.getLogger(__name__)

class InkscapeConverter(BaseConverter):
    """SVG to PDF converter using Inkscape."""
    
    def convert(self, svg_bytes: bytes, output_file: str) -> bool:
        """Convert SVG to PDF using Inkscape.
        
        Args:
            svg_bytes: Raw SVG content as bytes
            output_file: Path to the output PDF file
            
        Returns:
            bool: True if conversion successful, False otherwise
        """
        inkscape_path = shutil.which('inkscape')
        if not inkscape_path:
            logger.warning("Inkscape not found, skipping this converter")
            return False
            
        try:
            with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as temp_svg:
                temp_svg_path = temp_svg.name
                temp_svg.write(svg_bytes)
            
            try:
                # Construct the command based on Inkscape version
                version_cmd = [inkscape_path, "--version"]
                version_result = subprocess.run(version_cmd, capture_output=True, text=True)
                
                # Check if it's Inkscape 1.0+ (which uses different CLI syntax)
                is_inkscape_1_plus = "Inkscape 1." in version_result.stdout
                
                if is_inkscape_1_plus:
                    cmd = [
                        inkscape_path,
                        "--export-filename={}".format(output_file),
                        "--export-dpi={}".format(self.dpi),
                        temp_svg_path
                    ]
                else:
                    cmd = [
                        inkscape_path,
                        "--without-gui",
                        "--export-pdf={}".format(output_file),
                        "--export-dpi={}".format(self.dpi),
                        temp_svg_path
                    ]
                
                logger.info(f"Running Inkscape command: {' '.join(cmd)}")
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    logger.info(f"Successfully created PDF using {self.name}")
                    return True
                else:
                    logger.error(f"Inkscape failed: {result.stderr}")
                    return False
            finally:
                # Clean up temporary file
                if os.path.exists(temp_svg_path):
                    os.unlink(temp_svg_path)
                    
        except Exception as e:
            logger.error(f"{self.name} failed: {e}")
            return False


class RsvgConverter(BaseConverter):
    """SVG to PDF converter using rsvg-convert."""
    
    def convert(self, svg_bytes: bytes, output_file: str) -> bool:
        """Convert SVG to PDF using rsvg-convert.
        
        Args:
            svg_bytes: Raw SVG content as bytes
            output_file: Path to the output PDF file
            
        Returns:
            bool: True if conversion successful, False otherwise
        """
        rsvg_convert_path = shutil.which('rsvg-convert')
        if not rsvg_convert_path:
            logger.warning("rsvg-convert not found, skipping this converter")
            return False
            
        try:
            with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as temp_svg:
                temp_svg_path = temp_svg.name
                temp_svg.write(svg_bytes)
            
            try:
                cmd = [
                    rsvg_convert_path,
                    "-f", "pdf",
                    "-o", output_file,
                    "--dpi-x", str(self.dpi),
                    "--dpi-y", str(self.dpi),
                    temp_svg_path
                ]
                
                logger.info(f"Running rsvg-convert command: {' '.join(cmd)}")
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    logger.info(f"Successfully created PDF using {self.name}")
                    return True
                else:
                    logger.error(f"rsvg-convert failed: {result.stderr}")
                    return False
            finally:
                # Clean up temporary file
                if os.path.exists(temp_svg_path):
                    os.unlink(temp_svg_path)
                    
        except Exception as e:
            logger.error(f"{self.name} failed: {e}")
            return False


class ChromeConverter(BaseConverter):
    """SVG to PDF converter using Chrome/Chromium headless."""
    
    def convert(self, svg_bytes: bytes, output_file: str) -> bool:
        """Convert SVG to PDF using Chrome/Chromium headless.
        
        Args:
            svg_bytes: Raw SVG content as bytes
            output_file: Path to the output PDF file
            
        Returns:
            bool: True if conversion successful, False otherwise
        """
        chrome_paths = ['chrome', 'chromium', 'google-chrome', 'chromium-browser']
        chrome_path = None
        
        for path in chrome_paths:
            if shutil.which(path):
                chrome_path = shutil.which(path)
                break
                
        if not chrome_path:
            logger.warning("Chrome/Chromium not found, skipping this converter")
            return False
            
        try:
            # Create an HTML wrapper for the SVG
            html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>SVG to PDF Conversion</title>
    <style>
        body, html {{ margin: 0; padding: 0; height: 100%; }}
        svg {{ width: 100%; height: 100%; }}
    </style>
</head>
<body>
    {svg_bytes.decode('utf-8')}
</body>
</html>"""
            
            with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as html_file:
                html_path = html_file.name
                html_file.write(html_content.encode('utf-8'))
            
            try:
                cmd = [
                    chrome_path,
                    "--headless",
                    "--disable-gpu",
                    f"--print-to-pdf={output_file}",
                    f"file://{os.path.abspath(html_path)}"
                ]
                
                logger.info(f"Running Chrome headless command: {' '.join(cmd)}")
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0 and os.path.exists(output_file):
                    logger.info(f"Successfully created PDF using {self.name}")
                    return True
                else:
                    logger.error(f"Chrome headless failed: {result.stderr}")
                    return False
            finally:
                # Clean up temporary file
                if os.path.exists(html_path):
                    os.unlink(html_path)
                    
        except Exception as e:
            logger.error(f"{self.name} failed: {e}")
            return False


class ImageMagickConverter(BaseConverter):
    """SVG to PDF converter using ImageMagick."""
    
    def convert(self, svg_bytes: bytes, output_file: str) -> bool:
        """Convert SVG to PDF using ImageMagick.
        
        Args:
            svg_bytes: Raw SVG content as bytes
            output_file: Path to the output PDF file
            
        Returns:
            bool: True if conversion successful, False otherwise
        """
        magick_path = shutil.which('convert') or shutil.which('magick')
        if not magick_path:
            logger.warning("ImageMagick not found, skipping this converter")
            return False
            
        try:
            with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as temp_svg:
                temp_svg_path = temp_svg.name
                temp_svg.write(svg_bytes)
            
            try:
                # Check if using newer ImageMagick 7 syntax
                if 'magick' in magick_path and shutil.which('magick'):
                    cmd = [
                        'magick', 
                        'convert',
                        temp_svg_path,
                        "-density", str(self.dpi),
                        output_file
                    ]
                else:
                    cmd = [
                        magick_path,
                        temp_svg_path,
                        "-density", str(self.dpi),
                        output_file
                    ]
                
                logger.info(f"Running ImageMagick command: {' '.join(cmd)}")
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    logger.info(f"Successfully created PDF using {self.name}")
                    return True
                else:
                    logger.error(f"ImageMagick failed: {result.stderr}")
                    return False
            finally:
                # Clean up temporary file
                if os.path.exists(temp_svg_path):
                    os.unlink(temp_svg_path)
                    
        except Exception as e:
            logger.error(f"{self.name} failed: {e}")
            return False