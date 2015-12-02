"""
Planner that plans the timetable
"""

from itertools import product
from course import Course

class Planner:
    """planner handles the planning of timetable"""

    def start(self):
        """start the planner"""

        # get courses and fetch their schedule first
        self.__getCourses()
        self.__fetchSchedule()

        # create a list to store all combination
        courseAndIndex = []
        for course in self.courses:
            courseAndIndex.append([i for i in range(len(course.getCourseSchedule()))])

        combinations = list(product(*courseAndIndex))

        # plan courses
        print("\nPlanning your courses, please wait...")
        self.__testAllCombinations(combinations)

        # save the result
        self.__saveResult()

    def __getCourses(self):
        """get the number of courses and corresponding course code(s)"""

        while True:
            try:
                numOfCourses = int(input("How many courses do you wanna take? > "))
                if numOfCourses < 1:
                    print("Please enter a number larger than 0")
                else:
                    break
            except ValueError:
                print("Please enter a valid number")

        self.courses = []

        for num in range(numOfCourses):
            courseCode = input("Input course code > ")
            self.courses.append(Course(courseCode))
        print()

    def __fetchSchedule(self):
        """fetch all the schedules"""

        for course in self.courses:
            course.fetchSchedule()

    def __checkClash(self, time1, time2):
        """simply check whether the schedules of two courses clash"""

        for i in range(120):
            if time1[i] == time2[i] == "1": # schedules clash when the bits at the same index is both 1
                return True
            else:
                continue
        return False

    def __combineTime(self, time1, time2):
        """combine the schedules of two courses to form a new binary string containing schedule for both courses"""

        newTime = "0" * 120

        for i in range(120):
            if time1[i] == time2[i] == "0":
                continue
            else:
                newTime = newTime[:i] + "1" + newTime[i + 1:]

        return newTime

    def __testAllCombinations(self, combinations):
        """test all possible combinations of indexs for clashing"""

        # create a bufferList to store every index for every course in nested loops
        self.bufferList = []
        for course in self.courses:
            self.bufferList.append([index for index in course.getCourseSchedule().keys()])

        self.result = combinations[:] # make a copy of combinations to store the results

        for combination in combinations:
            currentTime = "0" * 120
            for i in range(len(combination)):
                schedule = self.courses[i].getCourseSchedule()
                nextTime = schedule[self.bufferList[i][combination[i]]]
                if self.__checkClash(currentTime, nextTime):
                    self.result.remove(combination)
                    break
                else:
                    currentTime = self.__combineTime(currentTime, nextTime)
                    #if self.__meetsRequirement(currentTime):
                    #    continue
                    #else:
                    #    self.result.remove(combination)
                    #    break

    def __meetsRequirement(self, time):
        """check whether a possible schedule meets my requirement"""

        for i in range(0,120,24):
            if "1" in time[i:i + 2]: # classes start after 9:30 am
                return False
            else:
                continue
        return True

    def __saveResult(self):
        """save all schedules that meet my requirement to a text file"""

        with open("result.txt", "w") as finalResult:
            counter = 1
            finalResult.write("Possible choices(s):\n\n")
            for combination in self.result:
                finalResult.write(str(counter) + ":\n")
                counter += 1
                for i in range(len(combination)):
                    finalResult.write(self.courses[i].getCourseCode().upper() + ": " + self.bufferList[i][combination[i]] + "\n")
                finalResult.write("\n")

        print("\nResults have been saved to file 'result.txt'")


# program starting point
if __name__ == '__main__':
    Planner().start()
