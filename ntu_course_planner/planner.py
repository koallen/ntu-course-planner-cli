# -*- coding: utf-8 -*-
"""
Planner that plans the timetable
"""

from itertools import product
from .course import Course
import re


class Planner:
    """planner handles the planning of timetable"""

    def plan(self, course_list, output_file=None):
        """
        Execute the planner

        parameters:
            course_list: A list of courses
            output_file: The file to save the result to
        """

        # course code validation
        if not self.validate(course_list):
            return {'error': 'invalid course code'}

        # save courses
        self.__courses = []
        for course_code in course_list:
            self.__courses.append(Course(course_code))

        # fetch schedule
        self.__fetch_schedule()

        # generate permutations and test them
        courseAndIndex = []
        for course in self.__courses:
            courseAndIndex.append(
                [i for i in range(len(course.get_course_schedule()))]
            )

        combinations = list(product(*courseAndIndex))
        self.__test_all_combinations(combinations)

        # output results
        if output_file is not None:
            pass

        result = []

        for combination in self.__result:
            single_result = []
            for i in range(len(combination)):
                single_dict = {}
                single_dict['course code'] = self.__courses[i].get_course_code().upper()
                single_dict['index'] = self.__bufferList[i][combination[i]]
                single_result.append(single_dict)
            result.append(single_result)

        return result


    def validate(self, course_list):
        """
        Validates the course code

        parameters:
            course_list: A list of courses
        """

        pattern = r"^\w{2}\d{4}$" # course code regex pattern

        # validate every course code
        for course in course_list:
            if not re.search(pattern, course):
                return False
        return True

    def start(self):
        """start the planner"""

        # get courses and fetch their schedule first
        self.__get_courses()
        self.__fetch_schedule()

        # create a list to store all combination
        courseAndIndex = []
        for course in self.__courses:
            courseAndIndex.append(
                [i for i in range(len(course.get_course_schedule()))]
                )

        combinations = list(product(*courseAndIndex))

        # plan courses
        print("\nPlanning your courses, please wait...")
        self.__test_all_combinations(combinations)

        # save the result
        self.__save_result()

    def __get_courses(self):
        """get the number of courses and corresponding course code(s)"""

        while True:
            try:
                numOfCourses = int(
                    input("How many courses do you wanna take? > ")
                    )
                if numOfCourses < 1:
                    print("Please enter a number larger than 0")
                else:
                    break
            except ValueError:
                print("Please enter a valid number")

        self.__courses = []

        for num in range(numOfCourses):
            courseCode = input("Input course code > ")
            self.__courses.append(Course(courseCode))
        print()

    def __fetch_schedule(self):
        """fetch all the schedules"""

        for course in self.__courses:
            course.fetch_schedule()

    def __check_clash(self, time1, time2):
        """simply check whether the schedules of two courses clash"""

        for i in range(120):
            # schedules clash when the bits at the same index is both 1
            if time1[i] == time2[i] == "1":
                return True
            else:
                continue
        return False

    def __combine_time(self, time1, time2):
        """combine the schedules of two courses to
        form a new binary string containing schedule
        for both courses
        """

        newTime = "0" * 120

        for i in range(120):
            if time1[i] == time2[i] == "0":
                continue
            else:
                newTime = newTime[:i] + "1" + newTime[i + 1:]

        return newTime

    def __test_all_combinations(self, combinations):
        """test all possible combinations of indexs for clashing"""

        # create a bufferList to store every index
        # for every course in nested loops
        self.__bufferList = []
        for course in self.__courses:
            self.__bufferList.append(
                [index for index in course.get_course_schedule().keys()]
                )

        # make a copy of combinations to store the results
        self.__result = combinations[:]

        for combination in combinations:
            currentTime = "0" * 120
            for i in range(len(combination)):
                schedule = self.__courses[i].get_course_schedule()
                nextTime = schedule[self.__bufferList[i][combination[i]]]
                if self.__check_clash(currentTime, nextTime):
                    self.__result.remove(combination)
                    break
                else:
                    currentTime = self.__combine_time(currentTime, nextTime)
                    # if self.__meetsRequirement(currentTime):
                    #     continue
                    # else:
                    #     self.result.remove(combination)
                    #     break

    def __meets_requirement(self, time):
        """check whether a possible schedule meets my requirement"""

        for i in range(0, 120, 24):
            if "1" in time[i:i + 2]:  # classes start after 9:30 am
                return False
            else:
                continue
        return True

    def __save_result(self):
        """save all schedules that meet my requirement to a text file"""

        with open("result.txt", "w") as finalResult:
            counter = 1
            finalResult.write("Possible choices(s):\n\n")
            for combination in self.__result:
                finalResult.write(str(counter) + ":\n")
                counter += 1
                for i in range(len(combination)):
                    finalResult.write(
                        self.__courses[i].get_course_code().upper() +
                        ": " + self.__bufferList[i][combination[i]] +
                        "\n"
                        )
                finalResult.write("\n")

        print("\nResults have been saved to file 'result.txt'")

