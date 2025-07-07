import os
import pickle
import uuid

import pytest

from app.crud import CRUDCourse
from app.schemas import Course


@pytest.fixture
def mock_path(tmp_path):
    return str(tmp_path / "test_courses.pkl")


@pytest.fixture
def crud_course(mock_path):
    return CRUDCourse(courses_file_path=mock_path)


@pytest.fixture
def sample_course():
    return Course(
        uuid=str(uuid.uuid4()),
        title="DS",
        semester="2025.2",
        lectures=[],
        evaluations=[])


def test_initialization_with_no_file(crud_course):
    assert crud_course.courses == []


def test_read_courses_from_file(mock_path, sample_course):
    mock_course_data = [sample_course]
    with open(mock_path, "wb") as f:
        # noinspection PyTypeChecker
        pickle.dump(mock_course_data, f)

    crud = CRUDCourse(courses_file_path=mock_path)
    assert crud.get_courses() == mock_course_data


def test_write_courses_to_file(crud_course, mock_path, sample_course):
    crud_course.courses = [sample_course]

    crud_course.write_courses_to_file(file_path=mock_path)

    assert os.path.exists(mock_path)
    with open(mock_path, "rb") as f:
        data_from_file = pickle.load(f)
    assert data_from_file == [sample_course]


def test_get_courses(crud_course, sample_course):
    crud_course.courses = [sample_course]
    assert crud_course.get_courses() == [sample_course]


def test_append_course(crud_course, sample_course):
    crud_course.append_course(sample_course)
    assert crud_course.courses == [sample_course]

    crud_course.append_course(sample_course)
    assert crud_course.courses == [sample_course, sample_course]
