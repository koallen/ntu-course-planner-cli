import requests
import sslType
import ssl
from bs4 import BeautifulSoup
from itertools import product

def getCourses():
    """get the number of courses and corresponding course code(s)"""
    numOfCourses = int(input("How many courses do you wanna take? > "))
    global courses, courseSchedule
    courses      = []

    for num in range(numOfCourses):
        courses.append(input("Input course code > "))
    print()

    courseSchedule = {}
    for i in range(len(courses)):
        courseSchedule[courses[i]] = {}

def getSchedule(courseCode):
    url      = "https://wish.wis.ntu.edu.sg/webexe/owa/AUS_SCHEDULE.main_display1?acadsem=2014;2&r_search_type=F&r_subj_code=" + courseCode + "&boption=Search&staff_access=false&acadsem=2014;2&r_course_yr="
    try:
        r    = s.post(url)
    except requests.exceptions.ConnectionError:
        print("Connection error. Cannot connect to NTU server.")
        print("Please try to run this script again.")
        exit()
    soup     = BeautifulSoup(r.text)
    schedule = soup.find_all("table")[1].find_all("td")
    schedule = schedule[:]
    return schedule

def parseSchedule(courseCode, indexOfDay_dict):
    global courseSchedule
    print("Getting schedule for " + courseCode.upper() + "...")
    schedule = getSchedule(courseCode)
    for i in range(len(schedule) // 7):
        for j in range(7):
            string = str(schedule[i * 7 + j])
            string = string[7:len(string) - 9]
            if j == 0 and string != "":
                currentIndex = string
                courseSchedule[courseCode][string]  = "0" * 120
            if j == 3:
                indexOfDay = indexOfDay_dict[string]
            if j == 4:
                numOfTimeSlots = getTime(string)
                indexOfTime    = (int(string[:4]) - 830) // 50
            if j == 6:
                startingIndex = indexOfDay + indexOfTime
                endingIndex   = startingIndex + numOfTimeSlots
                courseSchedule[courseCode][currentIndex] = courseSchedule[courseCode][currentIndex][:startingIndex] + \
                                                           "1" * numOfTimeSlots + \
                                                           courseSchedule[courseCode][currentIndex][endingIndex:]

def getTime(string):
    timeInterval   = int(string[5:]) - int(string[:4])
    numOfTimeSlots = timeInterval // 50
    return numOfTimeSlots

def checkClash(time1, time2):
    for i in range(10):
        for j in range(12):
            if time1[12 * i + j] == time2[12 * i + j] == "1":
                return True
            else:
                continue
    return False

def combineTime(time1, time2):
    newTime = "0" * 120
    for i in range(120):
        if time1[i] == time2[i] == "0":
            continue
        else:
            newTime = newTime[:i] + "1" + newTime[i + 1:]
    return newTime

def testAllCombinations(combinations):
    global courseSchedule, bufferList
    bufferList = []
    for course in courses:
        bufferList.append([index for index in courseSchedule[course].keys()])

    result = combinations[:]

    for combination in combinations:
        currentTime = "0" * 120
        for i in range(len(combination)):
            nextTime = courseSchedule[courses[i]][bufferList[i][combination[i]]]
            if checkClash(currentTime, nextTime):
                result.remove(combination)
                break
            else:
                currentTime = combineTime(currentTime, nextTime)
                if meetsRequirement(currentTime):
                    continue
                else:
                    result.remove(combination)
                    break

    return result

def meetsRequirement(time):
    for i in range(0,120,24):
        if "1" in time[i:i + 2]: # classes start after 9:30 A.M.
            return False
        else:
            continue
    return True

def saveResult(result):
    with open("result.txt", "w") as finalResult:
        counter = 1
        finalResult.write("Possible choices(s):\n\n")
        for combination in result:
            finalResult.write(str(counter) + ":\n")
            counter += 1
            for i in range(len(combination)):
                finalResult.write(courses[i].upper() + ": " + bufferList[i][combination[i]] + "\n")
            finalResult.write("\n")
    print("\nResults have been saved to file 'result.txt'")


##############################
## main program starts here ##
##############################

#force requests to use SSL v1 to connect to the server
s = requests.Session()
s.mount("https://", sslType.SSLAdapter(ssl.PROTOCOL_TLSv1))

#dictionary that stores information of index
indexOfDay = {"MON" : 0, "TUE" : 24, "WED" : 48, "THU" : 72, "FRI" : 96}

#get courses the user wants to take
getCourses()

#get schedule of selected courses
for course in courses:
    parseSchedule(course, indexOfDay)

#create a list to store all combination
courseAndIndex = []
for course in courses:
    courseAndIndex.append([i for i in range(len(courseSchedule[course]))])

combinations = list(product(*courseAndIndex))

#plan courses
print("Planning your courses, please wait")
result = testAllCombinations(combinations)

saveResult(result)
