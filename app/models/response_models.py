from pydantic import BaseModel
from typing import List

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

class URLVerificationResponse(BaseModel):
    input_type: str = "url"
    authenticity_score: int
    sources_analyzed: int
    sources: List[SourceInfo]
    llm_opinions: LLMOpinions
    final_summary: str

class PDFVerificationResponse(BaseModel):
    input_type: str = "pdf"
    authenticity_score: int
    sources_analyzed: int
    sources: List[SourceInfo]
    llm_opinions: LLMOpinions
    final_summary: str
