import os
import pickle

from core import settings
from schemas import Course


def get_course_crud():
    return course_crud


class CRUDCourse:
    def __init__(self, courses_file_path: str = settings.DEBUG_COURSES_FILE_PATH):
        self.courses: list[Course] = []
        self.read_courses_from_file(courses_file_path)

    def read_courses_from_file(self, file_path: str = settings.DEBUG_COURSES_FILE_PATH) -> None:
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                self.courses = pickle.load(file)
        return

    def write_courses_to_file(self, file_path: str = settings.DEBUG_COURSES_FILE_PATH) -> None:
        with open(file_path, "wb") as f:
            # noinspection PyTypeChecker
            pickle.dump(self.courses, f)
        return

    def get_courses(self) -> list[Course] | None:
        return self.courses

    def append_course(self, course: Course) -> None:
        self.courses.append(course)
        self.write_courses_to_file()


course_crud = CRUDCourse()
