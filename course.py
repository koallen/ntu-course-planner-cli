from courseSchedule import CourseSchedule

class Course:
    """Course class that contains relevant information about a course"""

    def __init__(self, courseCode):
        self.__courseCode = courseCode
        self.__courseSchedule = CourseSchedule()

    def getCourseSchedule(self):
        """get the dictionary of the schedule"""

        return self.__courseSchedule.getSchedule()

    def getCourseCode(self):
        """get the course code"""

        return self.__courseCode

    def fetchSchedule(self):
        """fetch schedule of the course"""

        self.__courseSchedule.parseSchedule(self.__courseCode)
