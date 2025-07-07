import uuid
from io import BytesIO
from unittest.mock import MagicMock, AsyncMock

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.crud import CRUDChat, CRUDCourse, get_chat_crud, get_course_crud
from app.main import app
from app.schemas import Course, CourseBase
from app.services import GoogleAIService, get_google_ai_service


@pytest.fixture
def mock_chat_crud():
    return MagicMock(spec=CRUDChat)


@pytest.fixture
def mock_course_crud():
    crud = MagicMock(spec=CRUDCourse)
    crud.get_courses.return_value = []
    return crud


@pytest.fixture
def mock_ai_service():
    service = MagicMock(spec=GoogleAIService)
    service.generate_structured_output = AsyncMock(return_value=CourseBase(
        title="DS",
        semester="2025.2",
        lectures=[],
        evaluations=[]))
    return service


@pytest.fixture
def client(mock_chat_crud, mock_course_crud, mock_ai_service):
    app.dependency_overrides[get_chat_crud] = lambda: mock_chat_crud
    app.dependency_overrides[get_course_crud] = lambda: mock_course_crud
    app.dependency_overrides[get_google_ai_service] = lambda: mock_ai_service
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides = {}


def test_get_courses(client, mock_course_crud):
    mock_courses = [Course(uuid=str(uuid.uuid4()), title="DS", semester="2025.2", lectures=[], evaluations=[])]
    mock_course_crud.get_courses.return_value = mock_courses

    response = client.get("/course/list")

    assert response.status_code == 200
    assert response.json() == [course.model_dump() for course in mock_courses]
    mock_course_crud.get_courses.assert_called_once()


@pytest.mark.asyncio
async def test_create_course_success(client, mock_course_crud, mock_chat_crud, mock_ai_service):
    file_content = b"pdf content"
    files = [("files", ("mock.pdf", BytesIO(file_content), "application/pdf"))]
    message = "Mock message."

    response = client.post("/course/create", files=files, data={"message": message})

    assert response.status_code == 201
    mock_ai_service.generate_structured_output.assert_awaited_once()
    mock_course_crud.append_course.assert_called_once()
    assert mock_chat_crud.append_llm_context.call_count == 2


def test_create_course_unsupported_media_type(client):
    file_content = b"zip content"
    files = [("files", ("mock.zip", BytesIO(file_content), "application/zip"))]

    response = client.post("/course/create", files=files)

    assert response.status_code == 415
    assert "Unsupported Media Type" in response.json()["detail"]


def test_create_course_entity_too_large(client):
    large_content = b"0" * (20 * 1024 * 1024)
    files = [("files", ("large_file.pdf", BytesIO(large_content), "application/pdf"))]

    response = client.post("/course/create", files=files)

    assert response.status_code == 413
    assert "Request Entity Too Large" in response.json()["detail"]


@pytest.mark.asyncio
async def test_create_course_ai_api_error(client, mock_ai_service):
    mock_ai_service.generate_structured_output.side_effect = Exception("Simulated API Error")
    file_content = b"pdf content"
    files = [("files", ("mock.pdf", BytesIO(file_content), "application/pdf"))]

    response = client.post("/course/create", files=files)

    assert response.status_code == 500
    assert "Internal Server Error" in response.text


@pytest.mark.asyncio
async def test_create_course_pydantic_validation_error(client, mock_ai_service):
    mock_ai_service.generate_structured_output.side_effect = ValidationError.from_exception_data(
        title="CourseBase",
        line_errors=[])
    file_content = b"pdf content"
    files = [("files", ("mock.pdf", BytesIO(file_content), "application/pdf"))]

    response = client.post("/course/create", files=files)

    assert response.status_code == 500
    assert "Internal Server Error" in response.text
