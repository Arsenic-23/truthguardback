from fastapi import FastAPI
from routers import text, url, pdf

app = FastAPI()

app.include_router(text.router)
app.include_router(url.router)
app.include_router(pdf.router)

@app.get("/")
def root():
    return {"status": "ok"}
