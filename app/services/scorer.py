"""
Scoring Service
---------------
Combines the outputs from ChatGPT, Gemini, and the number of
credible sources to generate a final authenticity score and
summary.

This acts as the "decision engine" of the whole verification pipeline.
"""

from typing import Dict, List
import re


def extract_confidence_score(llm_text: str) -> int:
    """
    Estimate a confidence score (0–100) from LLM response text.
    Simple keyword and sentiment-based scoring heuristic.
    """

    if not llm_text or "failed" in llm_text.lower():
        return 40  

    text = llm_text.lower()
    
    if any(word in text for word in ["accurate", "factual", "true", "verified", "credible", "correct"]):
        base = 85
   
    elif any(word in text for word in ["mostly", "largely", "generally", "partially", "somewhat accurate"]):
        base = 70
   
    elif any(word in text for word in ["uncertain", "doubt", "possibly", "not sure", "unclear"]):
        base = 50
   
    elif any(word in text for word in ["false", "incorrect", "misleading", "not factual", "fabricated"]):
        base = 25
    else:
        base = 60

    if "highly" in text:
        base += 5
    if "minor" in text:
        base += 5
    if "major" in text or "significant" in text:
        base -= 10

    return max(0, min(100, base))


def calculate_final_score(llm_results: Dict[str, str], sources: List[Dict[str, str]]) -> (int, str):
    """
    Combines ChatGPT and Gemini evaluations + source count
    to compute an overall authenticity percentage.
    Returns (score, summary)
    """

    chatgpt_score = extract_confidence_score(llm_results.get("chatgpt", ""))
    gemini_score = extract_confidence_score(llm_results.get("gemini", ""))

    llm_avg = (chatgpt_score + gemini_score) / 2

    num_sources = len(sources)
    if num_sources >= 8:
        llm_avg += 5
    elif num_sources <= 2:
        llm_avg -= 5

    final_score = round(max(0, min(100, llm_avg)))

    if final_score >= 85:
        summary = "Highly credible — supported by multiple reliable sources and both LLMs agree."
    elif final_score >= 70:
        summary = "Mostly credible — the majority of evidence supports the claims."
    elif final_score >= 50:
        summary = "Uncertain — mixed signals or insufficient evidence to confirm authenticity."
    else:
        summary = "Likely inaccurate — limited sources or conflicting information detected."

    return final_score, summary

