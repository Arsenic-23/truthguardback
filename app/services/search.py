import os
import httpx

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

async def search_web(query: str):
    if not SERPAPI_KEY:
        return []

    url = "https://serpapi.com/search"
    params = {"q": query, "api_key": SERPAPI_KEY, "num": 5}

    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(url, params=params)
        data = r.json()

    results = data.get("organic_results", [])
    links = [item.get("link") for item in results if item.get("link")]
    return links
