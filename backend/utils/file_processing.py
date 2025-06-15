import fitz  # PyMuPDF
import docx
from typing import Optional
from backend.utils.text_cleaner import clean_text

def extract_text_from_pdf(file_path: str) -> Optional[str]:
    try:
        text = ""
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
        return clean_text(text)  # ⬅️ CLEAN BEFORE RETURNING
    except Exception as e:
        print(f"PDF extraction error: {e}")
        return None

def extract_text_from_docx(file_path: str) -> Optional[str]:
    try:
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return clean_text(text)  # ⬅️ CLEAN BEFORE RETURNING
    except Exception as e:
        print(f"DOCX extraction error: {e}")
        return None
