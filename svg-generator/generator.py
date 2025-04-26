#!/usr/bin/env python3

import os
import re
import sys
import math
import svgwrite
from pathlib import Path
from typing import List, Tuple

class QuizSVGGenerator:
    def __init__(self, width: int = 1110, height: int = 1110):
        self.width = width
        self.height = height
        self.center_x = width // 2
        self.center_y = height // 2
        self.radius = 165
        self.option_radius = 275
        self.answer_radius = 450  # Half of 900 pixels for the circle

    def has_qr_code(self, markdown_path: str) -> bool:
        # Check if there's a corresponding QR code file
        qr_path = markdown_path.replace('-question.md', '-qr.png')
        return os.path.exists(qr_path)

    def parse_markdown(self, markdown_path: str) -> Tuple[str, List[str], List[bool]]:
        with open(markdown_path, 'r') as f:
            content = f.read()

        # Extract title
        title_match = re.search(r'## (.*?)\n', content)
        title = title_match.group(1) if title_match else "Quiz Question"

        # Extract options and answers
        options = []
        answers = []
        for line in content.split('\n'):
            if line.strip().startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.')):
                option = line.strip().split('.', 1)[1].strip()
                options.append(option)
                # For this example, we'll consider some options as TRUE
                answers.append(option in [
                    "Use minimal base images",
                    "Run as non-root user",
                    "Set --read-only flag",
                    "Scan images regularly",
                    "Set resource limits",
                    "Sign container images",
                    "Label mismatch",  # For question 004
                    "Missing strategy",
                    "Missing readiness",
                    "Missing namespace"
                ])

        return title, options, answers

    def calculate_position(self, index: int, total: int, radius: float) -> Tuple[float, float]:
        # For a regular decagon, we need 10 points
        angle = 2 * math.pi * index / 10 - math.pi / 2
        x = self.center_x + radius * math.cos(angle)
        y = self.center_y + radius * math.sin(angle)
        return x, y

    def generate_svg(self, markdown_path: str, output_path: str):
        title, options, answers = self.parse_markdown(markdown_path)
        
        # Create SVG drawing
        dwg = svgwrite.Drawing(output_path, size=(self.width, self.height))
        
        # Add background
        dwg.add(dwg.rect((0, 0), (self.width, self.height), fill='#f5f5f5', rx=250, ry=250))
        
        # Add corner paths for rounded corners
        dwg.add(dwg.path(d=f"M {self.width-250},0 L {self.width},0 L {self.width},{250} Q {self.width-50},50 {self.width-250},0 Z", fill='#f5f5f5'))
        dwg.add(dwg.path(d=f"M {self.width-250},{self.height} L {self.width},{self.height} L {self.width},{self.height-250} Q {self.width-50},{self.height-50} {self.width-250},{self.height} Z", fill='#f5f5f5'))
        
        # Add question circle
        dwg.add(dwg.circle(center=(self.center_x, self.center_y), r=self.radius, fill='#dcdcdc'))
        
        # Add title and QR code if needed
        if self.has_qr_code(markdown_path):
            # Add QR code image
            qr_path = markdown_path.replace('-question.md', '-qr.png')
            qr_size = 200  # Size of QR code
            qr_x = self.center_x - qr_size // 2
            qr_y = self.center_y - qr_size // 2
            
            # Add QR code as image - strip "../" from the path
            clean_qr_path = qr_path.replace('../', '')
            dwg.add(dwg.image(href=f"https://blog.session.it/quiz/{clean_qr_path}", insert=(qr_x, qr_y), size=(qr_size, qr_size)))
        else:
            # Regular title display for short questions
            title_parts = title.split()
            mid = len(title_parts) // 2
            title_line1 = ' '.join(title_parts[:mid])
            title_line2 = ' '.join(title_parts[mid:])
            
            title_group = dwg.g(font_family="Arial", font_size=24, text_anchor="middle", dominant_baseline="middle")
            title_group.add(dwg.text(title_line1, insert=(self.center_x, self.center_y - 40)))
            title_group.add(dwg.text(title_line2, insert=(self.center_x, self.center_y)))
            title_group.add(dwg.text("Which are TRUE?", insert=(self.center_x, self.center_y + 40)))
            dwg.add(title_group)
        
        # Add options and answers
        for i, (option, is_true) in enumerate(zip(options, answers)):
            x, y = self.calculate_position(i, len(options), self.option_radius)
            
            # Split option text into two lines if needed
            words = option.split()
            mid = len(words) // 2
            line1 = ' '.join(words[:mid])
            line2 = ' '.join(words[mid:])
            
            # Add option text
            option_group = dwg.g(font_family="Arial", font_size=24, text_anchor="middle", dominant_baseline="middle")
            option_group.add(dwg.text(line1, insert=(x, y - 15)))
            if line2:
                option_group.add(dwg.text(line2, insert=(x, y + 15)))
            dwg.add(option_group)
            
            # Add answer on the circle and decagon
            answer_x, answer_y = self.calculate_position(i, 10, self.answer_radius)
            answer_group = dwg.g(font_family="Arial", font_size=18, text_anchor="middle", dominant_baseline="middle")
            answer_group.add(dwg.text('TRUE' if is_true else 'FALSE', insert=(answer_x, answer_y)))
            dwg.add(answer_group)
        
        # Save the SVG with pretty printing
        dwg.save(pretty=True, indent=2)

def main():
    if len(sys.argv) < 3:
        print("Usage: python generator.py <input_markdown> <output_svg>")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    generator = QuizSVGGenerator()
    generator.generate_svg(input_path, output_path)

if __name__ == "__main__":
    main() 