from fastapi import APIRouter
from services.extractor import extract_from_text
from services.nlp import preprocess
from services.checker import evaluate
from services.scoring import score_result
import time

router = APIRouter(prefix="/check-text", tags=["text"])

@router.post("/")
async def check_text(payload: dict):
    start = time.time()
    text = payload.get("text", "")
    raw = extract_from_text(text)
    processed = preprocess(raw)
    result = await evaluate(processed)
    score = score_result(result)
    duration = (time.time() - start) * 1000
    return {"score": score, "sources": result["sources"], "duration_ms": duration}
