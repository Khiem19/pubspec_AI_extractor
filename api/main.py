import os
from fastapi import FastAPI
from pydantic import BaseModel
from core.pipeline import run_extraction

app = FastAPI(title="pubspec-ai-extractor", version="0.1.0")

MAX_REPAIRS = int(os.environ.get("MAX_REPAIRS", "1"))

class ExtractRequest(BaseModel):
    pubspec_text: str

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/extract")
def extract(req: ExtractRequest):
    return run_extraction(req.pubspec_text)
