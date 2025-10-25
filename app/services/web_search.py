"""
Web Search Service
------------------
Searches the web for factual sources related to extracted claims.
Currently uses DuckDuckGo's open HTML results for simplicity (no API key needed).

Later, this can be replaced by APIs like:
- Serper.dev (Google)
- Tavily API
- Bing Search API
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import urllib.parse

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0 Safari/537.36"
)

HEADERS = {"User-Agent": USER_AGENT}


def search_duckduckgo(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """
    Simple search via DuckDuckGo HTML results.
    Returns a list of sources (title + URL).
    """
    try:
        encoded_query = urllib.parse.quote_plus(query)
        url = f"https://duckduckgo.com/html/?q={encoded_query}"
        response = requests.get(url, headers=HEADERS, timeout=10)

        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        results = []

        for link in soup.select(".result__a")[:max_results]:
            title = link.get_text(strip=True)
            href = link.get("href")
            if href and title:
                results.append({"title": title, "url": href})

        return results
    except Exception:
        return []


def gather_sources(claims: List[str], limit_per_claim: int = 3) -> List[Dict[str, str]]:
    """
    Gather multiple credible sources for a list of factual claims.
    Returns a list of unique {title, url} pairs.
    """
    all_sources = []
    seen_urls = set()

    for claim in claims:
        search_results = search_duckduckgo(claim, max_results=limit_per_claim)
        for res in search_results:
            if res["url"] not in seen_urls:
                seen_urls.add(res["url"])
                all_sources.append(res)

    return all_sources[:15]

