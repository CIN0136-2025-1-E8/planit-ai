from .chat_schemas import ChatRole, ChatMessage
from .course_schema import Course, CourseBase, CoursesList, CourseCreate, CourseUpdate, CourseSummary, \
    CourseDeleteResponse
from .evaluation_schema import EvaluationTypes, Evaluation, EvaluationBase, EvaluationCreate, EvaluationUpdate
from .event_schema import Event, EventBase, EventCreate, EventCreateInDB, EventUpdate, EventsByDay
from .files_schema import FileRecord
from .lecture_schema import Lecture, LectureBase, LectureCreate, LectureUpdate
from .routine_schema import RoutineWeekdays, Routine, RoutineBase, RoutineCreate, RoutineUpdate
from .user_schema import User, UserData, UserBase, UserCreate, UserCreateInDB, UserUpdate
