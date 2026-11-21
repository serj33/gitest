import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from database.db_manager import (
    get_facts, save_facts, get_persona, save_persona,
    save_interview_message, get_interview_history,
    save_expert_message, get_expert_history,
    clear_interview_history, clear_expert_history,
)
from backend.services.facts_builder import build_facts
from backend.n8n_client import n8n_client

app = FastAPI(title="ModeusAristo API", description="Backend проекта ModeusAristo", version="1.0.0")


class InterviewMessage(BaseModel):
    message: str


class ExpertQuestion(BaseModel):
    question: str


class FactsInput(BaseModel):
    facts: list
    profession: str = "general"


def unwrap(result, key):
    if not isinstance(result, dict):
        return None
    data = result.get("data", result)
    if isinstance(data, dict):
        return data.get(key, result.get(key))
    return result.get(key)


@app.get("/")
def root():
    return {"status": "ok", "project": "ModeusAristo"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/facts")
def get_all_facts(profession: str | None = None):
    return {"facts": get_facts(profession)}


@app.post("/facts")
def add_facts(data: FactsInput):
    try:
        save_facts(data.facts, data.profession)
        return {"status": "success", "count": len(data.facts)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/persona")
def get_saved_persona():
    return {"persona": get_persona()}


@app.post("/persona/build")
def build_persona(profession: str = "general"):
    facts = build_facts(profession)
    if not facts:
        raise HTTPException(status_code=400, detail="Нет фактов для создания персоны")
    try:
        result = n8n_client.build_persona(facts)
        persona = unwrap(result, "persona")
        if isinstance(persona, str):
            import json
            persona = json.loads(persona)
        if not persona:
            # Some n8n workflows return the model result directly.
            persona = result.get("text") if isinstance(result, dict) else None
            if isinstance(persona, str):
                import json
                persona = json.loads(persona)
        if not isinstance(persona, dict):
            raise HTTPException(status_code=502, detail="n8n не вернул корректную персону")
        save_persona(persona)
        return {"status": "success", "persona": persona}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@app.get("/interview/history")
def interview_history():
    return {"history": get_interview_history()}


@app.post("/interview")
def interview(data: InterviewMessage):
    history = get_interview_history()
    try:
        result = n8n_client.get_question(data.message, history)
        question = unwrap(result, "question") or result.get("text")
        if not question:
            raise HTTPException(status_code=502, detail="n8n не вернул вопрос")
        save_interview_message("user", data.message)
        save_interview_message("assistant", question)
        return {"question": question}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@app.delete("/interview/history")
def delete_interview_history():
    clear_interview_history()
    return {"status": "success"}


@app.get("/expert/history")
def expert_history():
    return {"history": get_expert_history()}


@app.post("/expert")
def ask_expert(data: ExpertQuestion):
    persona = get_persona()
    facts = build_facts()
    history = get_expert_history()
    if not persona:
        raise HTTPException(status_code=400, detail="Сначала необходимо создать персону")
    try:
        result = n8n_client.ask_expert(data.question, persona, facts, history)
        answer = unwrap(result, "answer") or result.get("text")
        if not answer:
            raise HTTPException(status_code=502, detail="n8n не вернул ответ")
        save_expert_message("user", data.question)
        save_expert_message("assistant", answer)
        return {"answer": answer}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@app.delete("/expert/history")
def delete_expert_history():
    clear_expert_history()
    return {"status": "success"}
