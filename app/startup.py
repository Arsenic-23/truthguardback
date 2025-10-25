import spacy
from spacy.cli import download

try:
    spacy.load("en_core_web_sm")
except OSError:
    print("Downloading spaCy 'en_core_web_sm' model...")
    download("en_core_web_sm")
