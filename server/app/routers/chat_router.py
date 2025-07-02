from fastapi import APIRouter, HTTPException, Depends, Form

from crud import get_chat_crud
from schemas import ChatMessage, ChatRole
from services import get_google_ai_service

chat_router = APIRouter(
    prefix="/chat",
    tags=["chat"],
    responses={404: {"description": "Not found"}},
)


@chat_router.post("/history", response_model=list[ChatMessage])
async def get_chat_history(crud=Depends(get_chat_crud)):
    return crud.get_chat_history()


@chat_router.post("/message", response_model=str)
async def send_chat_message(message: str = Form(None),
                            crud=Depends(get_chat_crud),
                            ai_service=Depends(get_google_ai_service)):
    response, llm_context = await ai_service.send_message(message=message, llm_context=crud.get_llm_context())
    crud.set_llm_context(llm_context)
    crud.append_chat_history(ChatMessage(role=ChatRole.USER, text=message))
    crud.append_chat_history(ChatMessage(role=ChatRole.MODEL, text=response))
    return response
