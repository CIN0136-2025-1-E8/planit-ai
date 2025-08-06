import json

from fastapi import APIRouter, HTTPException, Depends, Form, UploadFile
from google.genai.types import Content
from sqlalchemy.orm import Session
from starlette import status

from app.core import settings
from app.core.security import get_current_user
from app.crud import get_chat_crud
from app.dependencies import get_db
from app.models import User
from app.schemas import ChatMessage, ChatMessageBase, ChatRole, ChatFile
from app.services import get_google_ai_service

chat_router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@chat_router.get("/history", response_model=list[ChatMessageBase])
async def get_chat_history(
        chat_crud=Depends(get_chat_crud),
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Not authorized")
    return chat_crud.get_chat_history(db=db, user_uuid=user.uuid)


@chat_router.delete("/history", status_code=status.HTTP_200_OK)
async def delete_chat_history(
        chat_crud=Depends(get_chat_crud),
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Not authorized")
    chat_crud.delete_chat_history(db=db, user_uuid=user.uuid)


@chat_router.post("/message", response_model=str)
async def send_chat_message(
        message: str = Form(),
        files: list[UploadFile] | None = None,
        chat_crud=Depends(get_chat_crud),
        ai_service=Depends(get_google_ai_service),
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Not authorized")

    chat_files = []
    if files:
        if len(files) > 10:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="Cannot upload more than 10 files.",
            )
        total_size = sum(file.size for file in files)
        if total_size > 19922944:  # 19MB
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="Total file size exceeds the 19MB limit.",
            )
        for file in files:
            if file.content_type not in settings.SUPPORTED_FILE_TYPES:
                raise HTTPException(
                    status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                    detail=f"File type not supported: {file.content_type}",
                )
            chat_files.append(ChatFile(filename=file.filename, mimetype=file.content_type))

    history = chat_crud.get_chat_history(db=db, user_uuid=user.uuid)
    llm_context: list[Content] = [
        Content.model_validate(content_item)
        for message in history
        for content_item in json.loads(message.content)
    ]
    response, new_content = await ai_service.send_message(
        instruction=settings.CHAT_SYSTEM_INSTRUCTIONS,
        message=message,
        files=[(await file.read(), file.content_type) for file in files] if files else None,
        llm_context=llm_context)

    user_message = ChatMessage(
        role=ChatRole.USER,
        text=message,
        files=chat_files if len(chat_files) else None,
        content=json.dumps([new_content[0].model_dump(mode='json')]),
    )
    model_message = ChatMessage(
        role=ChatRole.MODEL,
        text=response,
        content=json.dumps([new_content[1].model_dump(mode='json')]),
    )

    chat_crud.append_chat_history(db=db, user_uuid=user.uuid, obj_in=user_message)
    chat_crud.append_chat_history(db=db, user_uuid=user.uuid, obj_in=model_message)

    return response
