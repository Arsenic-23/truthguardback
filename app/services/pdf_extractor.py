"""
PDF Extractor Service
--------------------
Extracts text from uploaded PDF files for verification.
Uses pdfplumber for stable, dependency-light extraction.
"""

from typing import Optional
from io import BytesIO
import pdfplumber
from fastapi import HTTPException


def extract_text_from_pdf(file_bytes: bytes, max_chars: Optional[int] = 5000) -> str:
    """
    Extracts text from PDF bytes using pdfplumber.
    Limits to `max_chars` characters for performance.
    Raises HTTPException if extraction fails.
    """
    try:
        text = ""
        with pdfplumber.open(BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                text += page_text + " "

        cleaned_text = " ".join(text.split())
        if max_chars:
            cleaned_text = cleaned_text[:max_chars]

        if not cleaned_text.strip():
            raise HTTPException(status_code=400, detail="PDF contains no extractable text.")

        return cleaned_text

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to extract text from PDF: {str(e)}")
