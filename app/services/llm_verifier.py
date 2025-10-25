"""
LLM Verifier Service
--------------------
Uses ChatGPT and Gemini to cross-check claims against sources
and generate an authenticity evaluation.

Both models are queried independently for redundancy and
cross-verification. Results are combined in scoring later.
"""

import os
import json
import requests
from typing import Dict, List

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")



def verify_with_chatgpt(text: str, sources: List[Dict[str, str]]) -> str:
    """
    Use OpenAI ChatGPT to verify if the content appears factual.
    """
    try:
        if not OPENAI_API_KEY:
            return "No ChatGPT API key configured."

        source_summary = "\n".join([f"- {s['title']}: {s['url']}" for s in sources[:5]])

        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are an expert fact-checking assistant."},
                {
                    "role": "user",
                    "content": f"""
Please evaluate whether the following text is factually correct based on these online sources.

Text:
{text[:2000]}

Sources:
{source_summary}

Respond briefly (3–5 sentences) summarizing your factual judgment.
"""
                }
            ]
        }

        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"},
            data=json.dumps(payload),
            timeout=20
        )

        data = response.json()
        return data["choices"][0]["message"]["content"].strip()

    except Exception as e:
        return f"ChatGPT verification failed: {str(e)}"


def verify_with_gemini(text: str, sources: List[Dict[str, str]]) -> str:
    """
    Use Google Gemini to check factual correctness using the given sources.
    """
    try:
        if not GEMINI_API_KEY:
            return "No Gemini API key configured."

        source_summary = "\n".join([f"- {s['title']}: {s['url']}" for s in sources[:5]])

        prompt = f"""
You are an AI fact-checking assistant.
Review the following text and determine if it is factually accurate,
considering the online sources provided.

Text:
{text[:2000]}

Sources:
{source_summary}

Respond concisely (3–5 sentences) summarizing the factual validity.
"""

        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"contents": [{"parts": [{"text": prompt}]}]}),
            timeout=20
        )

        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()

    except Exception as e:
        return f"Gemini verification failed: {str(e)}"


def verify_with_llms(text: str, sources: List[Dict[str, str]]) -> Dict[str, str]:
    """
    Calls both ChatGPT and Gemini and returns their opinions.
    """
    chatgpt_result = verify_with_chatgpt(text, sources)
    gemini_result = verify_with_gemini(text, sources)

    return {
        "chatgpt": chatgpt_result,
        "gemini": gemini_result
    }

