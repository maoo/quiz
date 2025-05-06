import os
import tempfile
from typing import Optional
import qrcode
from pathlib import Path

def generate_qr_code(
    url: str,
    output_path: str,
    size: int = 10,
    border: int = 4,
    error_correction: int = qrcode.constants.ERROR_CORRECT_L
) -> Optional[str]:
    """
    Generate a QR code for the given URL and save it to the specified path.
    
    Args:
        url (str): The URL to encode in the QR code
        output_path (str): The path where to save the QR code image
        size (int): The size of the QR code (default: 10)
        border (int): The border size (default: 4)
        error_correction (int): The error correction level (default: ERROR_CORRECT_L)
        
    Returns:
        Optional[str]: The path to the generated QR code if successful, None otherwise
    """
    try:
        # Create QR code instance
        qr = qrcode.QRCode(
            version=1,
            error_correction=error_correction,
            box_size=size,
            border=border,
        )
        
        # Add data
        qr.add_data(url)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        os.makedirs(output_dir, exist_ok=True)
        
        # Save image
        img.save(output_path)
        
        return output_path
    except Exception as e:
        print(f"Error generating QR code: {str(e)}")
        return None

def generate_question_qr_code(
    deck_name: str,
    card_id: str,
    output_dir: str,
    url_prefix: str = "https://blog.session.it/quiz/decks") -> Optional[str]:
    """
    Generate a QR code for a quiz question.
    
    Args:
        deck_name (str): The name of the deck
        card_id (str): The question ID
        url_prefix (str): The prefix for the URL (default: "https://blog.session.it/quiz/decks")
        output_dir (Optional[str]): The directory where the QR code PNG should be saved. If None, uses a temporary directory.
        
    Returns:
        Optional[str]: The path to the generated QR code if successful, None otherwise
    """
    url = f"{url_prefix}/{deck_name}/cards/{card_id}"

    output_path = os.path.join(output_dir, "qr.png")

    return generate_qr_code(url, output_path) 