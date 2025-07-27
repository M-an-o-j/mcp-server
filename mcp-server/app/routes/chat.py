from fastapi import APIRouter, Query
from pydantic import BaseModel
from services.dispatcher import dispatch_message

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@router.post("/")
async def chat(req: ChatRequest, session_id: str = Query(default="default_session")):
    reply = await dispatch_message(req.message, session_id=session_id)
    return reply
