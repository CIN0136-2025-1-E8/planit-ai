from unittest.mock import AsyncMock, MagicMock

import pytest
from pydantic import ValidationError

from app.services.google_ai_service import GoogleAIService
from schemas import CourseBase
from schemas.course_schema import Lecture, Evaluation, EvaluationTypes


@pytest.fixture
def mocked_ai_service_simple_output(mocker):
    ai_service = GoogleAIService(api_key="dummy_key")
    mock_api_response = MagicMock()
    mock_api_response.text = "This is a mock AI response."
    mock = mocker.patch.object(
        ai_service.client.aio.models, 'generate_content',
        new_callable=AsyncMock, return_value=mock_api_response)
    return ai_service, mock


@pytest.fixture
def mocked_ai_service_structured_output(mocker):
    ai_service = GoogleAIService(api_key="dummy_key")
    course = CourseBase(
        title="Mock Course",
        semester="2025.2",
        lectures=[Lecture(
            title="Mock Lecture",
            start_datetime="2025-07-06T10:00:00",
            end_datetime="2025-07-06T12:00:00",
            summary="Mock Lecture Summary")],
        evaluations=[Evaluation(
            type=EvaluationTypes.EXAM,
            title="Mock Evaluation",
            start_datetime="2025-07-06T13:00:00",
            end_datetime="2025-07-06T15:00:00")])
    mock_api_response = MagicMock()
    mock_api_response.text = course.model_dump_json()
    mock = mocker.patch.object(
        ai_service.client.aio.models, 'generate_content',
        new_callable=AsyncMock, return_value=mock_api_response)
    return ai_service, mock, course, mock_api_response


@pytest.mark.asyncio
async def test_send_message_success(mocked_ai_service_simple_output):
    ai_service, mock_generate_content = mocked_ai_service_simple_output

    response_text, new_content = await ai_service.send_message(
        instruction="Test instruction",
        message="Hello.")

    assert response_text == "This is a mock AI response."
    assert len(new_content) == 2
    assert new_content[0].role == "user"
    assert new_content[1].role == "model"
    assert new_content[1].parts[0].text == "This is a mock AI response."
    mock_generate_content.assert_awaited_once()


@pytest.mark.asyncio
async def test_send_message_api_error(mocked_ai_service_simple_output):
    ai_service, mock_generate_content = mocked_ai_service_simple_output
    mock_generate_content.side_effect = Exception("Simulated API Error")

    with pytest.raises(Exception, match="Simulated API Error"):
        await ai_service.send_message(instruction="Test", message="Fail")
    mock_generate_content.assert_awaited_once()


@pytest.mark.asyncio
async def test_generate_structured_output_success_valid_course(mocked_ai_service_structured_output):
    ai_service, mock_generate_content, course, _ = mocked_ai_service_structured_output

    response = await ai_service.generate_structured_output(
        instruction="Test instruction",
        schema=CourseBase,
        files=[(b'Bytes', "application/pdf")],
        message="Hello.")

    assert response == course
    mock_generate_content.assert_awaited_once()


@pytest.mark.asyncio
async def test_generate_structured_output_error_invalid_course_eof(mocked_ai_service_structured_output):
    ai_service, mock_generate_content, _, mock_response = mocked_ai_service_structured_output
    mock_response.text = mock_response.text[:-6]  # Simulates reaching max_output_tokens

    with pytest.raises(ValidationError):
        await ai_service.generate_structured_output(
            instruction="Test instruction",
            schema=CourseBase,
            files=[(b'Bytes', "application/pdf")])
    mock_generate_content.assert_awaited_once()


@pytest.mark.asyncio
async def test_generate_structured_output_api_error(mocked_ai_service_structured_output):
    ai_service, mock_generate_content, _, _ = mocked_ai_service_structured_output
    mock_generate_content.side_effect = Exception("Simulated API Error")

    with pytest.raises(Exception, match="Simulated API Error"):
        await ai_service.generate_structured_output(
            instruction="Test instruction",
            schema=CourseBase,
            files=[(b'Bytes', "application/pdf")],
            message="Hello.")
    mock_generate_content.assert_awaited_once()
