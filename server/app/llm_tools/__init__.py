from .course_tools import course_tools
from .evaluation_tools import evaluation_tools
from .lecture_tools import lecture_tools
from .misc_tools import misc_tools

tools = []
tools.extend(course_tools)
tools.extend(misc_tools)
tools.extend(evaluation_tools)
tools.extend(lecture_tools)
