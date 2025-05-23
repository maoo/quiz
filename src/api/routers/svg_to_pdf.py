from ninja import Router, Body
from typing import Dict, Any
from src.svg_to_pdf.converter import SVGToPDFConverter

router = Router()

@router.post("/convert")
def convert_svg_to_pdf_endpoint(request, data: dict = Body(...)):
    """
    Convert SVG to PDF
    """
    try:
        if "svg" not in data:
            return {"status": "error", "message": "Missing 'svg' field in request data"}
        
        svg_content = data["svg"]
        if not svg_content or not svg_content.strip():
            return {"status": "error", "message": "Empty SVG content"}
        
        if not svg_content.startswith("<svg") or not svg_content.endswith("</svg>"):
            return {"status": "error", "message": "Invalid SVG content"}
        
        # Create a temporary directory for processing
        import tempfile
        import os
        with tempfile.TemporaryDirectory() as temp_dir:
            # Write the SVG data to a file
            svg_file = os.path.join(temp_dir, "content.svg")
            with open(svg_file, "w") as f:
                f.write(svg_content)
            
            # Convert to PDF
            converter = SVGToPDFConverter()
            pdf_file = os.path.join(temp_dir, "content.pdf")
            converter.convert_svg_to_pdf(svg_file, pdf_file)
            
            # Read the generated PDF
            with open(pdf_file, "rb") as f:
                pdf_content = f.read()
            
            # Convert to base64 for API response
            import base64
            pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')
            
            return {"status": "success", "pdf_content": pdf_base64}
    except Exception as e:
        return {"status": "error", "message": str(e)} 