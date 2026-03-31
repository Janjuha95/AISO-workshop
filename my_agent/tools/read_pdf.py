import fitz


def read_pdf(file_path: str) -> str:
    """Read a PDF file and return its full text content.

    Use this tool when a question references a PDF file or an attached file with a .pdf extension.

    Args:
        file_path: The path to the PDF file to read.

    Returns:
        The extracted text content of the PDF, with tables preserved as rows.
    """
    doc = fitz.open(file_path)
    parts = []
    for page in doc:
        text = page.get_text("text", sort=True, flags=fitz.TEXT_PRESERVE_WHITESPACE)
        parts.append(text)
    doc.close()
    return "\n".join(parts)
