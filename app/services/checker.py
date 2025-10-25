from .nlp import extract_keywords, extract_claims
from .search import search_web
from .llm import verify_with_llm

async def evaluate(text: str):
    keywords = extract_keywords(text)
    claims = extract_claims(text)

    results = []
    sources = set()
    verified_count = 0

    for claim in claims:
        query = claim if len(claim) < 120 else " ".join(keywords)
        web_sources = await search_web(query)
        sources.update(web_sources)

        llm_check = await verify_with_llm(claim, web_sources)
        if llm_check.get("verified"):
            verified_count += 1

        results.append({
            "claim": claim,
            "verified": llm_check.get("verified", False),
            "sources": web_sources
        })

    return {
        "claims_checked": len(claims),
        "verified_count": verified_count,
        "sources": list(sources),
        "details": results
    }
