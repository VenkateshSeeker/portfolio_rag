from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
from main import ask_question

app = FastAPI(title="Resume RAG API")

app.mount("/data", StaticFiles(directory="data"), name="data")

class QuestionRequest(BaseModel):
    question: str
    session_id: Optional[str] = "default"

class AnswerResponse(BaseModel):
    answer: str

@app.post("/ask", response_model=AnswerResponse)
async def ask(request: QuestionRequest):
    try:
        answer = ask_question(request.question, request.session_id)
        return AnswerResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse)
async def get_frontend():
    with open("index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)
