from .search import search_web
from .llm import verify_with_llm

async def evaluate(text: str):
    search_results = await search_web(text)
    llm_check = await verify_with_llm(text, search_results)
    return {"sources": search_results, "llm": llm_check}
