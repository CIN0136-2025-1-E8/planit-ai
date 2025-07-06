from fastapi import APIRouter, HTTPException, Depends, Form

from core import settings
from crud import get_chat_crud
from schemas import ChatMessage, ChatRole
from services import get_google_ai_service
from utils import system_message_current_datetime

chat_router = APIRouter(
    prefix="/chat",
    tags=["chat"],
    responses={404: {"description": "Not found"}},
)


@chat_router.get("/history", response_model=list[ChatMessage])
async def get_chat_history(crud=Depends(get_chat_crud)):
    return crud.get_chat_history()


@chat_router.post("/message", response_model=str)
async def send_chat_message(message: str = Form(),
                            crud=Depends(get_chat_crud),
                            ai_service=Depends(get_google_ai_service)):
    llm_context = crud.get_llm_context()
    try:
        response, new_content = await ai_service.send_message(
            instruction=settings.CHAT_SYSTEM_INSTRUCTIONS,
            message="".join([system_message_current_datetime(), message]),
            llm_context=llm_context)
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    crud.append_llm_context(new_content)
    crud.append_chat_history(ChatMessage(role=ChatRole.USER, text=message))
    crud.append_chat_history(ChatMessage(role=ChatRole.MODEL, text=response))
    return response
