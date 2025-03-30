import base64
import os

def encode_file_to_base64(file_path: str) -> str:
    with open(file_path, "rb") as file:
        encoded_data = base64.b64encode(file.read()).decode('utf-8')
    return encoded_data

def get_mime_type(file_path: str) -> str:
    """
    Determine the MIME type for a given file path based on its extension.

    Supported file types:
      - PDF: application/pdf
      - PNG: image/png
      - JPG/JPEG: image/jpeg

    :param file_path: The path to the file.
    :return: The MIME type as a string.
    :raises ValueError: If the file extension is not supported.
    """
    valid_types = {
        '.pdf': "application/pdf",
        '.png': "image/png",
        '.jpg': "image/jpeg",
        '.jpeg': "image/jpeg"
    }
    ext = os.path.splitext(file_path)[1].lower()
    if ext in valid_types:
        return valid_types[ext]
    else:
        return None
    
