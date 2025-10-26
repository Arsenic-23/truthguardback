from dotenv import load_dotenv
import os

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import text, url, pdf

app = FastAPI(title="truth guard")
origins = [
    "http://localhost:3000", 
    "https://truthguard-pearl.vercel.app/", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],    
)

app.include_router(text.router)
app.include_router(url.router)
app.include_router(pdf.router)

@app.get("/")
def root():
    return {"status": "chal raha hai yoo^^"}
