import os
from openai import AsyncOpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

async def verify_with_llm(text: str, sources: list):
    if not OPENAI_API_KEY:
        return {"verified": False}

    prompt = f"Check authenticity. Text: {text[:500]}. Sources: {sources}. Return yes or no."
    resp = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=20
    )
    answer = resp.choices[0].message.content.strip().lower()
    return {"verified": "yes" in answer}
