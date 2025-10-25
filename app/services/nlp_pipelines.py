"""
NLP Pipeline for extracting factual claims and key statements
from text, URLs, and PDFs for authenticity verification.
"""

import re
import spacy
from typing import List

nlp = spacy.load("en_core_web_sm")

def clean_text(text: str) -> str:
    """Remove unwanted characters and normalize spacing."""
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'http\S+', '', text)  # remove links
    text = re.sub(r'[^A-Za-z0-9,.!?\'"()%-\s]', '', text)
    return text.strip()


def extract_sentences(text: str) -> List[str]:
    """Split text into meaningful sentences using spaCy."""
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents if len(sent.text.strip()) > 30]
    return sentences


def extract_claims(text: str) -> List[str]:
    """
    Extracts factual statements (claims) that can be checked for truthfulness.
    Basic heuristic: select sentences with entities and verbs, indicating an assertion.
    """
    cleaned = clean_text(text)
    doc = nlp(cleaned)

    claims = []
    for sent in doc.sents:
        if len(sent.text) < 25 or len(sent.text) > 300:
            continue

        has_subject = any(tok.dep_ in ("nsubj", "nsubjpass") for tok in sent)
        has_verb = any(tok.pos_ == "VERB" for tok in sent)
        has_entity = len(sent.ents) > 0 or re.search(r"\d+", sent.text)

        if has_subject and has_verb and has_entity:
            claims.append(sent.text.strip())

    claims = list(dict.fromkeys(claims))[:10]
    return claims


def summarize_claims(claims: List[str]) -> str:
    """
    Simple text summary of claims for display or logging.
    """
    if not claims:
        return "No factual statements detected."
    return "\n".join([f"- {c}" for c in claims])

