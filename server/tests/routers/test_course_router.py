from io import BytesIO
from unittest.mock import MagicMock, AsyncMock

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.core.security import get_current_user
from app.crud import get_course_crud, get_chat_crud
from app.dependencies import get_db
from app.main import app
from app.services import get_google_ai_service
from mock_models import MockCourseGenerate, MockCourse, MockUser


def override_get_db():
    pass


@pytest.fixture
def mock_course_crud():
    crud = MagicMock()
    crud.get_all_by_owner_uuid.return_value = [
        MockCourse(uuid="test-uuid-1", title="DS", semester="2025.2")
    ]
    new_course = MockCourse(
        uuid="new-course-uuid", title="New Course", semester="2025.2"
    )
    new_course.lectures = []
    new_course.evaluations = []
    crud.create_with_children.return_value = new_course
    return crud


@pytest.fixture
def mock_chat_crud():
    crud = MagicMock()
    crud.append_llm_context = MagicMock()
    return crud


@pytest.fixture
def mock_ai_service():
    service = MagicMock()
    service.generate_structured_output = AsyncMock(
        return_value=MockCourseGenerate()
    )
    return service


@pytest.fixture
def mock_current_user():
    return MockUser(uuid="user-from-token")


@pytest.fixture
def client(mock_course_crud, mock_chat_crud, mock_ai_service, mock_current_user):
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_course_crud] = lambda: mock_course_crud
    app.dependency_overrides[get_chat_crud] = lambda: mock_chat_crud
    app.dependency_overrides[get_google_ai_service] = lambda: mock_ai_service
    app.dependency_overrides[get_current_user] = lambda: mock_current_user

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides = {}


def test_list_courses(client, mock_course_crud, mock_current_user):
    response = client.get("/course/list")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "DS"
    mock_course_crud.get_all_by_owner_uuid.assert_called_once_with(
        db=None, owner_uuid=mock_current_user.uuid
    )


@pytest.mark.asyncio
async def test_create_course_success(client, mock_course_crud, mock_chat_crud, mock_ai_service, mock_current_user):
    file_content = b"pdf content"
    files = [("files", ("mock.pdf", BytesIO(file_content), "application/pdf"))]
    message = "Mock message."

    response = client.post("/course/create", files=files, data={"message": message})

    assert response.status_code == 201, f"Response text: {response.text}"
    assert response.json()["title"] == "New Course"

    mock_ai_service.generate_structured_output.assert_awaited_once()

    mock_course_crud.create_with_children.assert_called_once()
    call_args = mock_course_crud.create_with_children.call_args[1]
    assert call_args['owner_uuid'] == mock_current_user.uuid
    created_course_obj = call_args['obj_in']
    assert created_course_obj.title == "New Course"
    assert len(created_course_obj.lectures) == 1
    assert len(created_course_obj.evaluations) == 1
    assert created_course_obj.lectures[0].title == "AI Generated Lecture"

    assert mock_chat_crud.append_llm_context.call_count == 2


@pytest.mark.asyncio
async def test_create_course_unsupported_media_type(client):
    file_content = b"zip content"
    files = [("files", ("mock.zip", BytesIO(file_content), "application/zip"))]

    response = client.post("/course/create", files=files)

    assert response.status_code == 415
    assert "Unsupported Media Type" in response.json()["detail"]


@pytest.mark.asyncio
async def test_create_course_entity_too_large(client):
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
    assert response.json()["detail"] == "Error while parsing course information"


@pytest.mark.asyncio
async def test_create_course_pydantic_validation_error(client, mock_ai_service):
    mock_ai_service.generate_structured_output.side_effect = ValidationError.from_exception_data(
        title="CourseGenerate",
        line_errors=[])
    file_content = b"pdf content"
    files = [("files", ("mock.pdf", BytesIO(file_content), "application/pdf"))]

    response = client.post("/course/create", files=files)

    assert response.status_code == 500
    assert response.json()["detail"] == "Error while parsing course information"
