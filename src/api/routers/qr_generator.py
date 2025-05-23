from ninja import Router, Body
from typing import Dict, Any
import qrcode

router = Router()

@router.post("/generate")
def generate_qr_code_endpoint(request, data: dict = Body(...)):
    """
    Generate QR code
    """
    try:
        if "content" not in data:
            return {"status": "error", "message": "Missing 'content' field in request data"}
        
        if not data["content"]:
            return {"status": "error", "message": "Content cannot be empty"}
        
        # Generate QR code in memory
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data["content"])
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64 for API response
        import base64
        from io import BytesIO
        buffer = BytesIO()
        qr_image.save(buffer, format="PNG")
        qr_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        return {"status": "success", "qr_content": qr_base64}
    except Exception as e:
        return {"status": "error", "message": str(e)} 