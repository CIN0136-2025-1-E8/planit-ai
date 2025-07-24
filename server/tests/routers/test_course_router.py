from io import BytesIO
from unittest.mock import MagicMock, AsyncMock

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.core.security import get_current_user
from app.crud import get_course_crud
from app.dependencies import get_db
from app.main import app
from app.services import get_google_ai_service
from mock_models import MockCourse, MockUser


def override_get_db():
    pass


@pytest.fixture
def mock_course_crud():
    crud = MagicMock()
    crud.get_all_by_owner_uuid.return_value = [
        MockCourse(uuid="test-uuid-1", title="DS", semester="2025.2")
    ]
    crud.create_with_children.return_value = MockCourse(
        uuid="new-course-uuid", title="New Course", semester="2025.2"
    )
    return crud


@pytest.fixture
def mock_ai_service():
    service = MagicMock()

    from app.routers.course_router import LecturesCreate, EvaluationsCreate
    from app.schemas import CourseBase

    service.generate_structured_output = AsyncMock(side_effect=[
        CourseBase(title="New Course", semester="2025.2"),
        LecturesCreate(lectures=[], has_more=True),
        LecturesCreate(lectures=[], has_more=False),
        EvaluationsCreate(evaluations=[], has_more=True),
        EvaluationsCreate(evaluations=[], has_more=False),
    ])
    return service


@pytest.fixture
def mock_current_user():
    return MockUser(uuid="user-from-token")


@pytest.fixture
def client(mock_course_crud, mock_ai_service, mock_current_user):
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_course_crud] = lambda: mock_course_crud
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
async def test_create_course_success(client, mock_course_crud, mock_ai_service, mock_current_user):
    file_content = b"pdf content"
    files = [("files", ("mock.pdf", BytesIO(file_content), "application/pdf"))]
    message = "Mock message."

    response = client.post("/course/create", files=files, data={"message": message})

    assert response.status_code == 201, f"Response text: {response.text}"
    assert response.json()["title"] == "New Course"

    mock_course_crud.create_with_children.assert_called_once()
    call_args = mock_course_crud.create_with_children.call_args[1]
    assert call_args['owner_uuid'] == mock_current_user.uuid

    assert mock_ai_service.generate_structured_output.await_count == 5


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
