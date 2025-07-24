from unittest.mock import AsyncMock, MagicMock

import pytest
from pydantic import ValidationError, BaseModel

from app.services import GoogleAIService


class MockCourse(BaseModel):
    title: str
    semester: str


@pytest.fixture
def mock_ai_service():
    mock_client = MagicMock()

    mock_generate_content = AsyncMock()
    mock_client.aio.models.generate_content = mock_generate_content

    ai_service = GoogleAIService(api_key="dummy_key_for_test", client=mock_client)

    yield ai_service, mock_generate_content


@pytest.mark.asyncio
async def test_send_message_success(mock_ai_service):
    ai_service, mock_generate_content = mock_ai_service

    mock_api_response = MagicMock()
    mock_api_response.text = "This is a mock AI response."
    mock_generate_content.return_value = mock_api_response

    response_text, new_content = await ai_service.send_message(
        instruction="Test instruction",
        message="Hello.")

    assert response_text == "This is a mock AI response."
    assert len(new_content) == 2
    mock_generate_content.assert_awaited_once()


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
