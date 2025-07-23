from fastapi import APIRouter, HTTPException, Depends, Form
from sqlalchemy.orm import Session

from app.core import settings
from app.core.security import get_current_user
from app.crud import get_chat_crud
from app.dependencies import get_db
from app.models import User
from app.schemas import ChatMessage, ChatRole
from app.services import get_google_ai_service

chat_router = APIRouter(
    prefix="/chat",
    tags=["chat"],
    responses={404: {"description": "Not found"}},
)

@chat_router.get("/history", response_model=list[ChatMessage])
async def get_chat_history(
    crud=Depends(get_chat_crud),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.get_chat_history(db=db, user=current_user)

@chat_router.post("/message", response_model=str)
async def send_chat_message(
    message: str = Form(),
    crud=Depends(get_chat_crud),
    ai_service=Depends(get_google_ai_service),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    llm_context = crud.get_llm_context()
    try:
        response, new_content = await ai_service.send_message(
            instruction=settings.CHAT_SYSTEM_INSTRUCTIONS,
            message=message,
            llm_context=llm_context)
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    crud.append_llm_context(new_content)
    
    user_message = ChatMessage(role=ChatRole.USER, text=message)
    model_message = ChatMessage(role=ChatRole.MODEL, text=response)
    
    crud.append_chat_history(db=db, user=current_user, chat_message=user_message)
    crud.append_chat_history(db=db, user=current_user, chat_message=model_message)
    
    return response #o