import uuid

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.crud.course_crud import course_crud
from tests.mock_models import TestBase, MockCourse, MockEvaluation, MockLecture, MockUser, \
    MockCourseSchema, MockEvaluationSchema, MockLectureSchema


@pytest.fixture(scope="function")
def test_db_session() -> Session:
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    TestBase.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        TestBase.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def mock_models(monkeypatch):
    monkeypatch.setattr(course_crud, 'model', MockCourse)
    monkeypatch.setattr('app.models.Evaluation', MockEvaluation)
    monkeypatch.setattr('app.models.Lecture', MockLecture)


@pytest.fixture(scope="function")
def test_user(test_db_session: Session) -> MockUser:
    user = MockUser(
        uuid=str(uuid.uuid4()),
        name="Test User",
        email="test@example.com",
        hashed_password="fake_password"
    )
    test_db_session.add(user)
    test_db_session.commit()
    test_db_session.refresh(user)
    return user


def test_get_course(test_db_session: Session, test_user: MockUser, mock_models):
    course_in = MockCourseSchema(uuid=str(uuid.uuid4()), title="Calculus I")
    course_crud.create_with_children(db=test_db_session, obj_in=course_in, owner_uuid=test_user.uuid)

    retrieved_course = course_crud.get(db=test_db_session, obj_uuid=course_in.uuid)

    assert retrieved_course is not None
    assert retrieved_course.uuid == course_in.uuid


def test_get_multi_courses(test_db_session: Session, test_user: MockUser):
    for i in range(5):
        course_in = MockCourseSchema(uuid=str(uuid.uuid4()), title=f"Course {i}")
        course_crud.create_with_children(
            db=test_db_session, obj_in=course_in, owner_uuid=test_user.uuid
        )

    first_two = course_crud.get_multi(test_db_session, limit=2)
    assert len(first_two) == 2

    next_two = course_crud.get_multi(test_db_session, skip=2, limit=2)
    assert len(next_two) == 2

    assert first_two[0].title == "Course 0"
    assert next_two[0].title == "Course 2"


def test_get_all_by_owner_uuid(test_db_session: Session, test_user: MockUser, mock_models):
    course_in_1 = MockCourseSchema(uuid=str(uuid.uuid4()), title="Algorithms")
    course_crud.create_with_children(db=test_db_session, obj_in=course_in_1, owner_uuid=test_user.uuid)

    courses = course_crud.get_all_by_owner_uuid(db=test_db_session, owner_uuid=test_user.uuid)

    assert len(courses) == 1
    assert courses[0].title == "Algorithms"


def test_create_with_children(test_db_session: Session, test_user: MockUser, mock_models):
    course_in = MockCourseSchema(
        uuid=str(uuid.uuid4()),
        title="Self-Contained Systems",
        semester="2025.2",
        evaluations=[MockEvaluationSchema(title="Final Project")],
        lectures=[MockLectureSchema(title="Intro to Microservices")]
    )

    db_course = course_crud.create_with_children(db=test_db_session, obj_in=course_in, owner_uuid=test_user.uuid)

    assert db_course is not None
    assert db_course.title == "Self-Contained Systems"
    assert db_course.owner_uuid == test_user.uuid
    assert len(db_course.evaluations) == 1
    assert db_course.evaluations[0].title == "Final Project"
    assert len(db_course.lectures) == 1
    assert db_course.lectures[0].title == "Intro to Microservices"


def test_update_course(test_db_session: Session, test_user: MockUser):
    course_in = MockCourseSchema(uuid=str(uuid.uuid4()), title="Old Title", semester="2025.1")
    db_course = course_crud.create_with_children(
        db=test_db_session, obj_in=course_in, owner_uuid=test_user.uuid
    )

    update_data = {"title": "New Title", "archived": True}
    updated_course = course_crud.update(
        db=test_db_session, db_obj=db_course, obj_in=update_data
    )

    test_db_session.refresh(updated_course)
    assert updated_course.title == "New Title"
    assert updated_course.archived is True
    assert updated_course.semester == "2025.1"  # Assert non-updated field remains the same


def test_remove_course_with_cascading_delete(test_db_session: Session, test_user: MockUser):
    course_in = MockCourseSchema(
        uuid=str(uuid.uuid4()),
        title="Course to Delete",
        semester="2025.2",
        evaluations=[MockEvaluationSchema(title="Midterm")],
        lectures=[MockLectureSchema(title="First Class")]
    )
    db_course = course_crud.create_with_children(
        db=test_db_session, obj_in=course_in, owner_uuid=test_user.uuid
    )
    assert test_db_session.query(MockEvaluation).count() == 1
    assert test_db_session.query(MockLecture).count() == 1

    removed_course = course_crud.remove(test_db_session, obj_uuid=db_course.uuid)

    assert removed_course is not None
    assert test_db_session.query(MockCourse).count() == 0
    assert test_db_session.query(MockEvaluation).count() == 0
    assert test_db_session.query(MockLecture).count() == 0
