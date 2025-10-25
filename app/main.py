from dotenv import load_dotenv
import os

load_dotenv() 

from fastapi import FastAPI
from app.routers import text, url, pdf

app = FastAPI(title="Authenticity Checker")

app.include_router(text.router)
app.include_router(url.router)
app.include_router(pdf.router)

@app.get("/")
def root():
    return {"status": "ok"}

