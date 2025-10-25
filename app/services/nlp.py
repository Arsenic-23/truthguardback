import re
from typing import List

def preprocess(text: str):
    t = text.strip()
    t = re.sub(r"\s+", " ", t)
    return t

def extract_keywords(text: str) -> List[str]:
    words = re.findall(r"[a-zA-Z]{4,}", text.lower())
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    ranked = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    top = [w for w, _ in ranked[:5]]
    return top

def extract_claims(text: str) -> List[str]:
    sentences = re.split(r"[.!?]", text)
    claims = [s.strip() for s in sentences if len(s.split()) > 6]
    return claims[:5]
