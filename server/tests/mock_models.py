import uuid
from enum import Enum

from pydantic import BaseModel, Field
from sqlalchemy import Column, String, Boolean, ForeignKey, Text, Integer
from sqlalchemy.orm import declarative_base, relationship

TestBase = declarative_base()


class MockChatRole(Enum):
    USER = "user"
    MODEL = "model"


class MockChatMessageSchema(BaseModel):
    role: MockChatRole
    text: str
    content: str | None = None


class MockChatMessage(TestBase):
    __tablename__ = "chat_messages"
    uuid = Column(String, primary_key=True)
    role = Column(String)
    text = Column(Text)
    content = Column(Text, nullable=True)
    order = Column(Integer)
    owner_uuid = Column(String, ForeignKey("users.uuid"))
    owner = relationship("MockUser", back_populates="chat_history")


class MockEvaluationTypes(Enum):
    ASSIGNMENT = "assignment"


class MockLectureCreate(BaseModel):
    title: str = "AI Generated Lecture"
    start_datetime: str = "2025-08-01T10:00:00"
    end_datetime: str = "2025-08-01T12:00:00"


class MockLectureSchema(BaseModel):
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str = "Test Lecture"
    start_datetime: str = "2025-07-23T14:00:00Z"
    end_datetime: str = "2025-07-23T15:00:00Z"


class MockEvaluationCreate(BaseModel):
    title: str = "AI Generated Evaluation"
    type: MockEvaluationTypes = MockEvaluationTypes.ASSIGNMENT
    start_datetime: str = "2025-08-01T12:00:00"
    end_datetime: str = "2025-08-08T23:59:59"


class MockEvaluationSchema(BaseModel):
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: MockEvaluationTypes = MockEvaluationTypes.ASSIGNMENT
    title: str = "Test Evaluation"
    start_datetime: str = "2025-07-23T09:00:00Z"
    end_datetime: str = "2025-07-28T23:59:59Z"


class MockCourseGenerate(BaseModel):
    title: str = "New Course"
    semester: str = "2025.2"
    lectures: list[MockLectureCreate] = [MockLectureCreate()]
    evaluations: list[MockEvaluationCreate] = [MockEvaluationCreate()]


class MockCourseSchema(BaseModel):
    uuid: str
    title: str
    semester: str | None = None
    archived: bool = False
    lectures: list[MockLectureSchema] = []
    evaluations: list[MockEvaluationSchema] = []

    class Config:
        from_attributes = True


class MockUser(TestBase):
    __tablename__ = "users"
    uuid = Column(String, primary_key=True)
    name = Column(String)
    nickname = Column(String, nullable=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    courses = relationship("MockCourse", back_populates="owner")
    chat_history = relationship("MockChatMessage", back_populates="owner", cascade="all, delete-orphan",
                                order_by="MockChatMessage.order")


class MockEvaluation(TestBase):
    __tablename__ = "evaluations"
    uuid = Column(String, primary_key=True)
    title = Column(String)
    type = Column(String)
    start_datetime = Column(String)
    end_datetime = Column(String)
    present = Column(Boolean, nullable=True)
    course_uuid = Column(String, ForeignKey("courses.uuid"))
    course = relationship("MockCourse", back_populates="evaluations")


class MockLecture(TestBase):
    __tablename__ = "lectures"
    uuid = Column(String, primary_key=True)
    title = Column(String)
    summary = Column(Text, nullable=True)
    start_datetime = Column(String)
    end_datetime = Column(String)
    present = Column(Boolean, nullable=True)
    course_uuid = Column(String, ForeignKey("courses.uuid"))
    course = relationship("MockCourse", back_populates="lectures")


class MockCourse(TestBase):
    __tablename__ = "courses"
    uuid = Column(String, primary_key=True)
    title = Column(String)
    description = Column(Text, nullable=True)
    semester = Column(String)
    archived = Column(Boolean, default=False)
    owner_uuid = Column(String, ForeignKey("users.uuid"))
    owner = relationship("MockUser", back_populates="courses")
    evaluations = relationship("MockEvaluation", back_populates="course", cascade="all, delete-orphan")
    lectures = relationship("MockLecture", back_populates="course", cascade="all, delete-orphan")
