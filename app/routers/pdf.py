from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List

import fitz
from io import BytesIO

from app.services.nlp_pipeline import extract_claims
from app.services.web_search import gather_sources
from app.services.llm_verifier import verify_with_llms
from app.services.scorer import calculate_final_score

router = APIRouter()

class SourceInfo(BaseModel):
    title: str
    url: str

class LLMOpinions(BaseModel):
    chatgpt: str
    gemini: str

class PDFVerificationResponse(BaseModel):
    input_type: str = "pdf"
    authenticity_score: int
    sources_analyzed: int
    sources: List[SourceInfo]
    llm_opinions: LLMOpinions
    final_summary: str


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extract text from a PDF file using PyMuPDF (fitz).
    Returns first 5000 characters for processing.
    """
    try:
        doc = fitz.open(stream=BytesIO(file_bytes), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text("text")

        cleaned_text = " ".join(text.split())
        return cleaned_text[:5000]  
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to extract text from PDF: {str(e)}")


@router.post("/pdf", response_model=PDFVerificationResponse)
async def verify_pdf(file: UploadFile = File(...)):
    """
    Verify authenticity of claims within an uploaded PDF document.
    """
    file_bytes = await file.read()

    pdf_text = extract_text_from_pdf(file_bytes)
    if not pdf_text or len(pdf_text) < 50:
        raise HTTPException(status_code=400, detail="PDF does not contain enough textual data.")

    claims = extract_claims(pdf_text)
    if not claims:
        raise HTTPException(status_code=400, detail="No factual claims found in the PDF.")

    sources = gather_sources(claims)

    llm_results = verify_with_llms(pdf_text, sources)

    final_score, summary = calculate_final_score(llm_results, sources)

    return PDFVerificationResponse(
        authenticity_score=final_score,
        sources_analyzed=len(sources),
        sources=[SourceInfo(**s) for s in sources],
        llm_opinions=LLMOpinions(**llm_results),
        final_summary=summary
    )

