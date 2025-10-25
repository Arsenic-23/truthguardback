from fastapi import APIRouter
from app.schemas import URLPayload
from app.services.extractor import extract_from_url
from app.services.nlp import preprocess
from app.services.checker import evaluate
from app.services.scoring import score_result
import time

router = APIRouter(prefix="/check-url", tags=["url"])

@router.post("/")
async def check_url(payload: URLPayload):
    start = time.time()
    raw = await extract_from_url(payload.url)
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
