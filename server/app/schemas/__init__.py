from .chat_schemas import ChatRole, ChatMessage, ChatMessageBase, ChatFile
from .course_schema import Course, CourseBase, CourseCreate, CourseUpdate, CourseGenerate, CourseSummary, \
    CourseDeleteResponse
from .evaluation_schema import EvaluationTypes, Evaluation, EvaluationBase, EvaluationCreate, EvaluationUpdate, \
    EvaluationInSchedule
from .event_schema import Event, EventBase, EventCreate, EventCreateInDB, EventUpdate, EventsByDay, EventInSchedule
from .lecture_schema import Lecture, LectureBase, LectureCreate, LectureUpdate, LectureInSchedule
from .routine_schema import RoutineWeekdays, Routine, RoutineBase, RoutineCreate, RoutineCreateInDB, RoutineUpdate
from .user_schema import User, UserData, UserBase, UserCreate, UserCreateInDB, UserUpdate, DailySchedule, \
    ScheduleResponse
