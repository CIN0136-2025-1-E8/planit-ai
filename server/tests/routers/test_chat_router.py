from unittest.mock import MagicMock, AsyncMock

import pytest
from fastapi.testclient import TestClient
from google.genai.types import Content, Part

from app.crud import CRUDChat, get_chat_crud
from app.main import app
from app.schemas import ChatMessage, ChatRole
from app.services import GoogleAIService, get_google_ai_service


@pytest.fixture
def mock_chat_crud():
    crud = MagicMock(spec=CRUDChat)
    crud.get_llm_context.return_value = []
    crud.get_chat_history.return_value = []
    return crud


@pytest.fixture
def mock_ai_service():
    service = MagicMock(spec=GoogleAIService)
    service.send_message = AsyncMock(
        return_value=("AI response", [Content(role="model", parts=[Part(text="AI response")])]))
    return service


@pytest.fixture
def client(mock_chat_crud, mock_ai_service):
    app.dependency_overrides[get_chat_crud] = lambda: mock_chat_crud
    app.dependency_overrides[get_google_ai_service] = lambda: mock_ai_service
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides = {}


def test_get_chat_history(client, mock_chat_crud):
    mock_history = [ChatMessage(role=ChatRole.USER, text="Mock message."),
                    ChatMessage(role=ChatRole.MODEL, text="Mock response.")]
    mock_chat_crud.get_chat_history.return_value = mock_history

    response = client.get("/chat/history")

    assert response.status_code == 200
    assert response.json() == [msg.model_dump(mode='json') for msg in mock_history]
    mock_chat_crud.get_chat_history.assert_called_once()


@pytest.mark.asyncio
async def test_send_chat_message(client, mock_chat_crud, mock_ai_service):
    user_message = "Mock message."
    ai_response_text = "Mock response."
    new_llm_content = [Content(role="user", parts=[Part(text=user_message)]),
                       Content(role="model", parts=[Part(text=ai_response_text)])]
    mock_ai_service.send_message.return_value = (ai_response_text, new_llm_content)

    response = client.post("/chat/message", data={"message": user_message})

    assert response.status_code == 200
    assert response.json() == ai_response_text
    mock_ai_service.send_message.assert_awaited_once()
    mock_chat_crud.append_llm_context.assert_called_once_with(new_llm_content)
    assert mock_chat_crud.append_chat_history.call_count == 2
    mock_chat_crud.append_chat_history.assert_any_call(ChatMessage(role=ChatRole.USER, text=user_message))
    mock_chat_crud.append_chat_history.assert_any_call(ChatMessage(role=ChatRole.MODEL, text=ai_response_text))


@pytest.mark.asyncio
async def test_send_chat_message_ai_api_error(client, mock_ai_service):
    mock_ai_service.send_message.side_effect = Exception("Simulated API Error")

    response = client.post("/chat/message", data={"message": "This will fail."})

    assert response.status_code == 500
    assert "Internal Server Error" in response.text
