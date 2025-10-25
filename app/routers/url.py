from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl, Field
from typing import List

import requests
from bs4 import BeautifulSoup

from app.services.nlp_pipeline import extract_claims
from app.services.web_search import gather_sources
from app.services.llm_verifier import verify_with_llms
from app.services.scorer import calculate_final_score

router = APIRouter()

class URLVerificationRequest(BaseModel):
    url: HttpUrl = Field(..., description="The webpage URL to verify")

class SourceInfo(BaseModel):
    title: str
    url: str

class LLMOpinions(BaseModel):
    chatgpt: str
    gemini: str

class URLVerificationResponse(BaseModel):
    input_type: str = "url"
    authenticity_score: int
    sources_analyzed: int
    sources: List[SourceInfo]
    llm_opinions: LLMOpinions
    final_summary: str

def extract_text_from_url(url: str) -> str:
    """
    Simple function to fetch and clean text from a webpage.
    For large pages, truncates to first 3000 characters.
    """
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Unable to fetch webpage.")
        soup = BeautifulSoup(response.text, "html.parser")

        for script in soup(["script", "style", "noscript"]):
            script.extract()

        text = " ".join(soup.stripped_strings)
        return text[:3000] 
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to extract text from URL: {str(e)}")


@router.post("/url", response_model=URLVerificationResponse)
async def verify_url(payload: URLVerificationRequest):
    """
    Verify authenticity of a webpage’s content.
    """

    page_text = extract_text_from_url(payload.url)
    if not page_text or len(page_text) < 50:
        raise HTTPException(status_code=400, detail="Not enough textual content on the webpage.")

    claims = extract_claims(page_text)
    if not claims:
        raise HTTPException(status_code=400, detail="No valid claims found on the page.")

    sources = gather_sources(claims)

    llm_results = verify_with_llms(page_text, sources)

    final_score, summary = calculate_final_score(llm_results, sources)

    return URLVerificationResponse(
        authenticity_score=final_score,
        sources_analyzed=len(sources),
        sources=[SourceInfo(**s) for s in sources],
        llm_opinions=LLMOpinions(**llm_results),
        final_summary=summary
    )

