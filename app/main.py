from dotenv import load_dotenv
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import text, url, pdf 

load_dotenv()

app = FastAPI(title="truth guard")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://truthguard-pearl.vercel.app/"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(text.router)
app.include_router(url.router)
app.include_router(pdf.router)

@app.get("/")
def root():
    return {"status": "ping pong"}
