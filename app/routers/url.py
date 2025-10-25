from fastapi import APIRouter
from services.extractor import extract_from_url
from services.nlp import preprocess
from services.checker import evaluate
from services.scoring import score_result
import time

router = APIRouter(prefix="/check-url", tags=["url"])

@router.post("/")
async def check_url(payload: dict):
    start = time.time()
    url = payload.get("url", "")
    raw = await extract_from_url(url)
    processed = preprocess(raw)
    result = await evaluate(processed)
    score = score_result(result)
    duration = (time.time() - start) * 1000
    return {"score": score, "sources": result["sources"], "duration_ms": duration, "details": result["details"]}
