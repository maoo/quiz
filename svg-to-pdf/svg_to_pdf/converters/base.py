"""Base converter abstract class."""
import abc
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

class BaseConverter(abc.ABC):
    """Base class for SVG converters."""
    
    def __init__(self, dpi: int = 254):
        """Initialize the converter.
        
        Args:
            dpi: DPI to use for conversion (default: 254 which gives 100px per cm)
        """
        self.dpi = dpi
        
    @abc.abstractmethod
    def convert(self, svg_bytes: bytes, output_file: str) -> bool:
        """Convert SVG bytes to a PDF file.
        
        Args:
            svg_bytes: Raw SVG content as bytes
            output_file: Path to the output PDF file
            
        Returns:
            bool: True if conversion successful, False otherwise
        """
        pass
        
    @property
    def name(self) -> str:
        """Get the name of the converter."""
        return self.__class__.__name__