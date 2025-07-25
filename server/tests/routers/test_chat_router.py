import json
import uuid
from unittest.mock import MagicMock, AsyncMock, call

import pytest
from fastapi.testclient import TestClient
from google.genai.types import Content, Part
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.crud import get_chat_crud
from app.dependencies import get_db
from app.main import app
from app.schemas import ChatMessageBase, ChatMessage, ChatRole
from app.services import get_google_ai_service


@pytest.fixture
def mock_chat_crud():
    return MagicMock()


@pytest.fixture
def mock_ai_service():
    service = MagicMock()
    user_content = Content(role="user", parts=[Part(text="Hello")])
    model_content = Content(role="model", parts=[Part(text="Hi back")])
    service.send_message = AsyncMock(return_value=("Hi back", [user_content, model_content]))
    return service


@pytest.fixture
def mock_user():
    return MagicMock(uuid=str(uuid.uuid4()))


@pytest.fixture
def mock_db_session():
    return MagicMock(spec=Session)


@pytest.fixture
def client(mock_chat_crud, mock_ai_service, mock_user, mock_db_session):
    app.dependency_overrides[get_chat_crud] = lambda: mock_chat_crud
    app.dependency_overrides[get_google_ai_service] = lambda: mock_ai_service
    app.dependency_overrides[get_current_user] = lambda: mock_user
    app.dependency_overrides[get_db] = lambda: mock_db_session

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides = {}


def test_get_chat_history(client, mock_chat_crud, mock_user, mock_db_session):
    mock_history = [
        ChatMessage(role=ChatRole.USER, text="Test message", content="[]")
    ]
    mock_chat_crud.get_chat_history.return_value = mock_history

    expected_response_data = [
        ChatMessageBase(role=ChatRole.USER, text="Test message").model_dump(mode='json')
    ]

    response = client.get("/chat/history")

    assert response.status_code == 200
    assert response.json() == expected_response_data
    mock_chat_crud.get_chat_history.assert_called_once_with(db=mock_db_session, user_uuid=mock_user.uuid)


def test_delete_chat_history(client, mock_chat_crud, mock_user, mock_db_session):
    response = client.delete("/chat/history")

    assert response.status_code == 200
    mock_chat_crud.delete_chat_history.assert_called_once_with(db=mock_db_session, user_uuid=mock_user.uuid)


@pytest.mark.asyncio
async def test_send_chat_message(client, mock_chat_crud, mock_ai_service, mock_user, mock_db_session):
    user_message_text = "Hello AI"
    ai_response_text = "Hello User"

    user_content = Content(role="user", parts=[Part(text=user_message_text)])
    model_content = Content(role="model", parts=[Part(text=ai_response_text)])
    mock_ai_service.send_message.return_value = (ai_response_text, [user_content, model_content])

    history_content = Content(role="user", parts=[Part(text="Old message")])
    mock_chat_crud.get_chat_history.return_value = [
        ChatMessage(role=ChatRole.USER, text="Old message", content=json.dumps([history_content.model_dump()]))
    ]

    response = client.post("/chat/send_message", data={"message": user_message_text})

    assert response.status_code == 200
    assert response.json() == ai_response_text
    mock_ai_service.send_message.assert_awaited_once()

    assert mock_chat_crud.append_chat_history.call_count == 2

    expected_user_msg = ChatMessage(role=ChatRole.USER, text=user_message_text,
                                    content=json.dumps([user_content.model_dump()]))
    expected_model_msg = ChatMessage(role=ChatRole.MODEL, text=ai_response_text,
                                     content=json.dumps([model_content.model_dump()]))

    expected_calls = [
        call(db=mock_db_session, user_uuid=mock_user.uuid, obj_in=expected_user_msg),
        call(db=mock_db_session, user_uuid=mock_user.uuid, obj_in=expected_model_msg)
    ]
    mock_chat_crud.append_chat_history.assert_has_calls(expected_calls, any_order=True)
