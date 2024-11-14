from PyPDF2 import PdfReader
import requests
from io import BytesIO

def extractTextFromPDF(pdf_url: str) -> str:
    text = ""
    response = requests.get(pdf_url)
    response.raise_for_status()
    pdf_file = BytesIO(response.content)
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text
