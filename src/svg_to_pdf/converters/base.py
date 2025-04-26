"""
Base class for SVG to PDF converters.
"""

from abc import ABC, abstractmethod
from typing import Optional


class BaseConverter(ABC):
    """
    Abstract base class for SVG to PDF converters.
    
    All converter implementations must inherit from this class and implement
    the convert method.
    """
    
    def __init__(self, dpi: int = 254):
        """
        Initialize the converter.
        
        Args:
            dpi: DPI to use for PDF generation (default: 254 which gives 100px per cm)
        """
        self.dpi = dpi
        
    @abstractmethod
    def convert(self, svg_bytes: bytes, output_file: str) -> bool:
        """
        Convert SVG bytes to PDF file.
        
        Args:
            svg_bytes: SVG content as bytes
            output_file: Path to the output PDF file
            
        Returns:
            bool: True if conversion was successful, False otherwise
        """
        pass 