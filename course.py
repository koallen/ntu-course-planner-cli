# -*- coding: utf-8 -*-
from courseSchedule import CourseSchedule


class Course:


    def __init__(self, courseCode):
        self.__courseCode = courseCode
        self.__courseSchedule = CourseSchedule()

    def get_course_schedule(self):
        """get the dictionary of the schedule"""

        return self.__courseSchedule.get_schedule()

    def get_course_code(self):
        """get the course code"""

        return self.__courseCode

    def fetch_schedule(self):
        """fetch schedule of the course"""

        self.__courseSchedule.parse_schedule(self.__courseCode)
