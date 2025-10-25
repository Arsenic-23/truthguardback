from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any

from app.services.nlp_pipeline import extract_claims
from app.services.web_search import gather_sources
from app.services.llm_verifier import verify_with_llms
from app.services.scorer import calculate_final_score

router = APIRouter()

class TextVerificationRequest(BaseModel):
    text: str = Field(..., description="The text content to verify")

class SourceInfo(BaseModel):
    title: str
    url: str

class LLMOpinions(BaseModel):
    chatgpt: str
    gemini: str

class TextVerificationResponse(BaseModel):
    input_type: str = "text"
    authenticity_score: int
    sources_analyzed: int
    sources: List[SourceInfo]
    llm_opinions: LLMOpinions
    final_summary: str

@router.post("/text", response_model=TextVerificationResponse)
async def verify_text(payload: TextVerificationRequest):
    """
    Verify the authenticity of a piece of text using NLP, web search, and LLMs.
    """

    if not payload.text or len(payload.text.strip()) < 10:
        raise HTTPException(status_code=400, detail="Text content is too short or empty.")

    claims = extract_claims(payload.text)

    if not claims:
        raise HTTPException(status_code=400, detail="No valid factual statements found in text.")

    sources = gather_sources(claims)

    llm_results = verify_with_llms(payload.text, sources)

    final_score, summary = calculate_final_score(llm_results, sources)

    return TextVerificationResponse(
        authenticity_score=final_score,
        sources_analyzed=len(sources),
        sources=[SourceInfo(**s) for s in sources],
        llm_opinions=LLMOpinions(**llm_results),
        final_summary=summary
    )

