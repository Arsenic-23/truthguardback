import httpx
import PyPDF2

def extract_from_text(text: str):
    return text

async def extract_from_url(url: str):
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(url)
        return r.text

def extract_from_pdf(file):
    reader = PyPDF2.PdfReader(file.file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text
