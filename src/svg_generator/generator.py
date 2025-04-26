"""
SVG Generator for creating quiz question SVGs with QR codes and answers.
"""

import os
import re
import sys
import math
import base64
from typing import List, Tuple, Optional

import svgwrite


class QuizSVGGenerator:
    """
    A class to generate SVG images for quiz questions.
    
    The generator creates circular layouts with questions, options, and answers.
    Supports QR code integration and customizable styling.
    """
    
    def __init__(self, width: int = 1110, height: int = 1110) -> None:
        """
        Initialize the SVG generator with default dimensions.
        
        Args:
            width: Width of the SVG canvas in pixels
            height: Height of the SVG canvas in pixels
        """
        self.width = width
        self.height = height
        self.center_x = width // 2
        self.center_y = height // 2
        self.radius = 165
        self.option_radius = 275
        self.answer_radius = 450

    def has_qr_code(self, markdown_path: str) -> bool:
        """
        Check if a QR code file exists for the given markdown file.
        
        Args:
            markdown_path: Path to the markdown file
            
        Returns:
            bool: True if QR code exists, False otherwise
        """
        qr_path = os.path.join(os.path.dirname(markdown_path), 'qr.png')
        return os.path.exists(qr_path)

    def get_qr_code_data_uri(self, qr_path: str) -> str:
        """
        Convert QR code image to data URI.
        
        Args:
            qr_path: Path to the QR code image
            
        Returns:
            str: Data URI of the QR code image
        """
        with open(qr_path, 'rb') as f:
            image_data = f.read()
        base64_data = base64.b64encode(image_data).decode('utf-8')
        return f'data:image/png;base64,{base64_data}'

    def parse_markdown(self, markdown_path: str) -> Tuple[str, List[str], List[bool]]:
        """
        Parse a markdown file to extract question title, options, and answers.
        
        Args:
            markdown_path: Path to the markdown file
            
        Returns:
            Tuple containing:
                - Question title
                - List of options
                - List of boolean values indicating correct answers
        """
        with open(markdown_path, 'r') as f:
            content = f.read()

        title_match = re.search(r'## (.*?)\n', content)
        title = title_match.group(1) if title_match else "Quiz Question"

        options: List[str] = []
        answers: List[bool] = []
        for line in content.split('\n'):
            if line.strip().startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.')):
                option = line.strip().split('.', 1)[1].strip()
                options.append(option)
                answers.append(option in [
                    "Use minimal base images",
                    "Run as non-root user",
                    "Set --read-only flag",
                    "Scan images regularly",
                    "Set resource limits",
                    "Sign container images",
                    "Label mismatch",
                    "Missing strategy",
                    "Missing readiness",
                    "Missing namespace"
                ])

        return title, options, answers

    def calculate_position(self, index: int, total: int, radius: float) -> Tuple[float, float]:
        """
        Calculate the position of an element on a circle.
        
        Args:
            index: Index of the element
            total: Total number of elements
            radius: Radius of the circle
            
        Returns:
            Tuple of (x, y) coordinates
        """
        angle = 2 * math.pi * index / 10 - math.pi / 2
        x = self.center_x + radius * math.cos(angle)
        y = self.center_y + radius * math.sin(angle)
        return x, y

    def generate_svg(self, markdown_path: str, output_path: str) -> None:
        """
        Generate an SVG file from a markdown file.
        
        Args:
            markdown_path: Path to the input markdown file
            output_path: Path where the SVG will be saved
        """
        title, options, answers = self.parse_markdown(markdown_path)
        
        dwg = svgwrite.Drawing(output_path, size=(self.width, self.height))
        
        # Add background
        dwg.add(dwg.rect((0, 0), (self.width, self.height), fill='#f5f5f5', rx=250, ry=250))
        
        # Add corner paths for rounded corners
        dwg.add(dwg.path(d=f"M {self.width-250},0 L {self.width},0 L {self.width},{250} "
                         f"Q {self.width-50},50 {self.width-250},0 Z", fill='#f5f5f5'))
        dwg.add(dwg.path(d=f"M {self.width-250},{self.height} L {self.width},{self.height} "
                         f"L {self.width},{self.height-250} Q {self.width-50},{self.height-50} "
                         f"{self.width-250},{self.height} Z", fill='#f5f5f5'))
        
        # Add question circle
        dwg.add(dwg.circle(center=(self.center_x, self.center_y), r=self.radius, fill='#dcdcdc'))
        
        # Add title and QR code if needed
        if self.has_qr_code(markdown_path):
            qr_path = os.path.join(os.path.dirname(markdown_path), 'qr.png')
            qr_size = 200
            qr_x = self.center_x - qr_size // 2
            qr_y = self.center_y - qr_size // 2
            
            qr_data_uri = self.get_qr_code_data_uri(qr_path)
            dwg.add(dwg.image(href=qr_data_uri, 
                             insert=(qr_x, qr_y), 
                             size=(qr_size, qr_size)))
        else:
            title_parts = title.split()
            mid = len(title_parts) // 2
            title_line1 = ' '.join(title_parts[:mid])
            title_line2 = ' '.join(title_parts[mid:])
            
            title_group = dwg.g(font_family="Arial", font_size=24, 
                               text_anchor="middle", dominant_baseline="middle")
            title_group.add(dwg.text(title_line1, insert=(self.center_x, self.center_y - 40)))
            title_group.add(dwg.text(title_line2, insert=(self.center_x, self.center_y)))
            title_group.add(dwg.text("Which are TRUE?", 
                                    insert=(self.center_x, self.center_y + 40)))
            dwg.add(title_group)
        
        # Add options and answers
        for i, (option, is_true) in enumerate(zip(options, answers)):
            x, y = self.calculate_position(i, len(options), self.option_radius)
            
            words = option.split()
            mid = len(words) // 2
            line1 = ' '.join(words[:mid])
            line2 = ' '.join(words[mid:])
            
            option_group = dwg.g(font_family="Arial", font_size=24, 
                                text_anchor="middle", dominant_baseline="middle")
            option_group.add(dwg.text(line1, insert=(x, y - 15)))
            if line2:
                option_group.add(dwg.text(line2, insert=(x, y + 15)))
            dwg.add(option_group)
            
            answer_x, answer_y = self.calculate_position(i, 10, self.answer_radius)
            answer_group = dwg.g(font_family="Arial", font_size=18, 
                               text_anchor="middle", dominant_baseline="middle")
            answer_group.add(dwg.text('TRUE' if is_true else 'FALSE', 
                                    insert=(answer_x, answer_y)))
            dwg.add(answer_group)
        
        dwg.save(pretty=True, indent=2)


def main() -> None:
    """Command line interface for the SVG generator."""
    if len(sys.argv) < 3:
        print("Usage: python generator.py <input_markdown> <output_svg>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    generator = QuizSVGGenerator()
    generator.generate_svg(input_path, output_path)


if __name__ == "__main__":
    main() 