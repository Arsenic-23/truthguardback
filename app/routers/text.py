from fastapi import APIRouter
from app.schemas import TextPayload
from app.services.extractor import extract_from_text
from app.services.nlp import preprocess
from app.services.checker import evaluate
from app.services.scoring import score_result
import time

router = APIRouter(prefix="/check-text", tags=["text"])

@router.options("/")
async def options():
    return {}
@router.post("/")
async def check_text(payload: TextPayload):
    start = time.time()
    raw = extract_from_text(payload.text)
    processed = preprocess(raw)
    result = await evaluate(processed)
    score = score_result(result)
    duration = (time.time() - start) * 1000
    return {
        "score": score,
        "sources": result["sources"],
        "duration_ms": duration,
        "details": result["details"]
    }
