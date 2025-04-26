"""
Image handling utilities for SVG to PDF conversion.
"""

import base64
import logging
import os
from pathlib import Path
import re
from typing import Optional
from urllib.parse import urlparse

from PIL import Image

logger = logging.getLogger(__name__)


class ImageHandler:
    """
    Handles image references in SVG files.
    
    This class provides functionality to:
    - Convert remote image URLs to local file paths
    - Embed small images as data URIs
    - Handle case-sensitive file systems
    """
    
    def __init__(self, base_dir: Optional[str] = None):
        """
        Initialize the image handler.
        
        Args:
            base_dir: Base directory for image resolution
        """
        self.base_dir = base_dir or os.getcwd()
        
    def fix_image_references(self, svg_content: str) -> str:
        """
        Replace remote image references with local file paths and embed small images.
        
        Args:
            svg_content: SVG file content
            
        Returns:
            Modified SVG content with fixed image references
        """
        # Regular expression to find image references in the SVG
        image_pattern = r'<image([^>]*?)xlink:href="([^"]+)"([^>]*?)/?>'
        
        # Define a replacement function for each matched image
        def replace_image_ref(match: re.Match[str]) -> str:
            before_url = match.group(1)
            url = match.group(2)
            after_url = match.group(3)
            
            parsed_url = urlparse(url)
            
            # If it's already a local file or data URI, no need to change
            if parsed_url.scheme == 'file' or url.startswith('data:'):
                return match.group(0)
            
            # If it's a remote URL or any other type of URL, try to find a local file
            filename = os.path.basename(parsed_url.path)
            
            # First, try the exact filename from the path
            local_path = os.path.join(self.base_dir, filename)
            
            # If not found, try with different case patterns (important for case-sensitive filesystems)
            if not os.path.exists(local_path):
                # Try with the base name without any suffixes
                base_name = os.path.splitext(filename)[0]
                if base_name.endswith('-qr'):
                    base_name = base_name[:-3]  # Remove -qr suffix
                local_path = os.path.join(self.base_dir, base_name, 'qr.png')
            
            # If we found a local file, use it
            if os.path.exists(local_path):
                abs_path = os.path.abspath(local_path)
                logger.info(f"Found local file for {url} at {abs_path}")
                
                # For small images like QR codes, embed them directly as data URIs
                if os.path.getsize(local_path) < 1000000:  # < 1MB
                    try:
                        # Determine the MIME type
                        ext = os.path.splitext(local_path)[1].lower()
                        mime_type = {
                            '.png': 'image/png',
                            '.jpg': 'image/jpeg',
                            '.jpeg': 'image/jpeg',
                            '.gif': 'image/gif',
                            '.svg': 'image/svg+xml'
                        }.get(ext, 'image/png')
                        
                        # Read the image file and encode as base64
                        with open(local_path, 'rb') as img_file:
                            img_data = base64.b64encode(img_file.read()).decode('utf-8')
                        
                        # Create a data URI
                        data_uri = f"data:{mime_type};base64,{img_data}"
                        logger.info("Embedded image as data URI")
                        
                        # Return the updated image tag with the data URI
                        return f'<image{before_url}xlink:href="{data_uri}"{after_url}>'
                    except Exception as e:
                        logger.warning(f"Could not embed image as data URI: {e}")
                        # Fall back to file URL if embedding fails
                        return f'<image{before_url}xlink:href="file://{abs_path}"{after_url}>'
                else:
                    # For larger images, just use file:// URL
                    return f'<image{before_url}xlink:href="file://{abs_path}"{after_url}>'
            
            logger.warning(f"Could not find local file for {url}")
            # If no local file found, return unchanged
            return match.group(0)
        
        # Replace all image references
        modified_content = re.sub(image_pattern, replace_image_ref, svg_content)
        return modified_content 