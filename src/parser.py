import fitz

def extract_text_from_pdf(file_path):
    """
    Extracts text from a PDF file.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        str: The extracted text.
    """
    doc=fitz.open(file_path)
    full_text=""
    for page in doc:
        full_text += page.get_text()
    return full_text.strip()
