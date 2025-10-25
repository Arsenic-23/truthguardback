from fastapi import APIRouter, UploadFile, File
from services.extractor import extract_from_pdf
from services.nlp import preprocess
from services.checker import evaluate
from services.scoring import score_result
import time

router = APIRouter(prefix="/check-pdf", tags=["pdf"])

@router.post("/")
async def check_pdf(file: UploadFile = File(...)):
    start = time.time()
    raw = extract_from_pdf(file)
    processed = preprocess(raw)
    result = await evaluate(processed)
    score = score_result(result)
    duration = (time.time() - start) * 1000
    return {"score": score, "sources": result["sources"], "duration_ms": duration}
