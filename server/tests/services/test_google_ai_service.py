from unittest.mock import AsyncMock, MagicMock, patch, create_autospec

import pytest
from google.genai.types import FunctionCall
from pydantic import ValidationError, BaseModel

from app.services import GoogleAIService


class MockCourse(BaseModel):
    title: str
    semester: str


async def mock_async_tool_template(param: str) -> dict:
    return {"status": "async task complete", "param": param}


def mock_sync_tool_template(param: str) -> dict:
    return {"status": "sync task complete", "param": param}


@pytest.fixture
def mock_tools():
    mock_async_tool = create_autospec(mock_async_tool_template, spec_set=True)
    mock_sync_tool = create_autospec(mock_sync_tool_template, spec_set=True)

    mock_async_tool.return_value = {"status": "async task complete"}
    mock_sync_tool.return_value = {"status": "sync task complete"}

    mock_async_tool.__name__ = "mock_async_tool"
    mock_sync_tool.__name__ = "mock_sync_tool"

    with patch('app.services.google_ai_service.tools', [mock_async_tool, mock_sync_tool]) as patched_tools:
        yield patched_tools


@pytest.fixture
def mock_ai_service():
    mock_client = MagicMock()

    mock_generate_content = AsyncMock()
    mock_client.aio.models.generate_content = mock_generate_content

    ai_service = GoogleAIService(api_key="dummy_key_for_test", client=mock_client)

    yield ai_service, mock_generate_content


@pytest.mark.asyncio
async def test_send_message_success(mock_ai_service, mock_tools):
    ai_service, mock_generate_content = mock_ai_service
    mock_async_tool, mock_sync_tool = mock_tools

    mock_response_with_call = MagicMock()
    mock_function_call = FunctionCall(name="mock_async_tool", args={"param": "value"})
    mock_response_with_call.candidates = [
        MagicMock(content=MagicMock(parts=[MagicMock(function_call=mock_function_call)]))]
    mock_response_with_call.candidates[0].content.role = "model"

    mock_final_response = MagicMock()
    mock_final_response.text = "This is the final AI response."
    mock_final_response.candidates = [MagicMock(content=MagicMock(parts=[MagicMock(function_call=None)]))]

    mock_generate_content.side_effect = [
        mock_response_with_call,
        mock_final_response,
    ]

    response_text, new_content = await ai_service.send_message(
        instruction="Test instruction",
        message="Hello, use a tool."
    )

    assert response_text == "This is the final AI response."
    assert len(new_content) == 2
    assert mock_generate_content.call_count == 2
    mock_async_tool.assert_awaited_once_with(param="value")
    mock_sync_tool.assert_not_called()

    call_args = mock_generate_content.call_args_list[1].kwargs['contents']
    assert len(call_args) == 3
    assert call_args[2].parts[0].function_response.name == "mock_async_tool"


@pytest.mark.asyncio
async def test_generate_structured_output_success(mock_ai_service):
    ai_service, mock_generate_content = mock_ai_service

    expected_course = MockCourse(title="Mock Course", semester="2025.2")
    mock_api_response = MagicMock()
    mock_api_response.text = expected_course.model_dump_json()
    mock_generate_content.return_value = mock_api_response

    response = await ai_service.generate_structured_output(
        instruction="Test instruction",
        schema=MockCourse,
        files=[(b'Bytes', "application/pdf")],
        message="Hello.")

    assert response == expected_course
    mock_generate_content.assert_awaited_once()


@pytest.mark.asyncio
async def test_generate_structured_output_validation_error(mock_ai_service):
    ai_service, mock_generate_content = mock_ai_service

    mock_api_response = MagicMock()
    mock_api_response.text = '{"title": "Missing semester field..."}'
    mock_generate_content.return_value = mock_api_response

    with pytest.raises(ValidationError):
        await ai_service.generate_structured_output(
            instruction="Test instruction",
            schema=MockCourse,
            files=[(b'Bytes', "application/pdf")])
    mock_generate_content.assert_awaited_once()


@pytest.mark.asyncio
async def test_generate_structured_output_api_error(mock_ai_service):
    ai_service, mock_generate_content = mock_ai_service

    mock_generate_content.side_effect = Exception("Simulated API Error")

    with pytest.raises(Exception, match="Simulated API Error"):
        await ai_service.generate_structured_output(
            instruction="Test instruction",
            schema=MockCourse,
            files=[(b'Bytes', "application/pdf")],
            message="Hello.")
    mock_generate_content.assert_awaited_once()
