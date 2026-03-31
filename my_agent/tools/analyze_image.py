import base64
import mimetypes
import os

from google import genai


def analyze_image(file_path: str, question: str) -> str:
    """Analyze an image file and answer a question about it.

    Use this tool when a question references an image file (e.g. .png, .jpg, .webp).
    Provide the exact file path and the specific question to answer about the image.

    Args:
        file_path: The path to the image file.
        question: The specific question to answer about the image content.

    Returns:
        A detailed description or answer based on the image content.
    """
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        mime_type = "image/png"

    with open(file_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            {
                "parts": [
                    {"inline_data": {"mime_type": mime_type, "data": image_data}},
                    {"text": question},
                ]
            }
        ],
    )
    return response.text
