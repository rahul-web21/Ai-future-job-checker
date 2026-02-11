from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict

from ai_engine import answer_question_with_knowledge
from evaluation import evaluate_answer
from scoring import calculate_future_score

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    history: List[Dict] = []

class ChatResponse(BaseModel):
    answer: str
    sources: list
    evaluation: dict
    future_score: int

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    result = answer_question_with_knowledge(request.message, request.history)
    evaluation = evaluate_answer(result["answer"])
    future_score = calculate_future_score(result["answer"])

    return {
        "answer": result["answer"],
        "sources": result["sources"],
        "evaluation": evaluation,
        "future_score": future_score
    }
{
  "message": "Will AI replace software developers?",
  "history": []
}