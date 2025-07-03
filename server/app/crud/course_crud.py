import os
import pickle

from core import settings
from schemas import Course


def get_course_crud():
    return course_crud


class CRUDCourse:
    def __init__(self):
        self.courses: list[Course] = []
        self.read_courses_from_file()

    def read_courses_from_file(self) -> None:
        if os.path.exists(settings.DEBUG_COURSES_FILE_PATH):
            with open(settings.DEBUG_COURSES_FILE_PATH, 'rb') as file:
                self.courses = pickle.load(file)
        return

    def write_courses_to_file(self) -> None:
        with open(settings.DEBUG_COURSES_FILE_PATH, "wb") as f:
            # noinspection PyTypeChecker
            pickle.dump(self.courses, f)
        return

    def get_courses(self) -> list[Course] | None:
        return self.courses

    def append_course(self, course: Course) -> None:
        self.courses.append(course)
        self.write_courses_to_file()


course_crud = CRUDCourse()
