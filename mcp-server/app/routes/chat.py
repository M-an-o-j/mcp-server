from fastapi import APIRouter
from pydantic import BaseModel
from services.dispatcher import dispatch_message

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@router.post("/", response_model=ChatResponse)
async def chat(req: ChatRequest):
    reply = await dispatch_message(req.message)
    return ChatResponse(response=reply)
