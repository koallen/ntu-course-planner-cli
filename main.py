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
    """fetch course schedule basing on course code from NTU website"""

    # generate URL for a course
    url = "https://wish.wis.ntu.edu.sg/webexe/owa/AUS_SCHEDULE.main_display1?acadsem=2015;1&r_search_type=F&r_subj_code=" + \
        courseCode + "&boption=Search&staff_access=false&acadsem=2015;1&r_course_yr="

    try:
        r = s.post(url) # try connecting to the server
    # exit program if server is not reachable
    except requests.exceptions.ConnectionError:
        print("Connection error. Cannot connect to NTU server.")
        print("Please try to run this script again.")
        exit()

    soup = BeautifulSoup(r.text) # create BeautifulSoup object for later parsing

    # save the table which contains the course schedule
    schedule = soup.find_all("table")[1].find_all("td")
    schedule = schedule[:]

    return schedule

def parseSchedule(courseCode, indexOfDay_dict):
    """parse the html table and convert the course schedule to a binary string"""

    global courseSchedule

    print("Getting schedule for " + courseCode.upper() + "...", end=" ")
    schedule = getSchedule(courseCode) # get html table format of course schedule
    print("Done")

    # convert the course schedule to a binary string
    # it is a 120 bit string and every bit represents half an hour
    # bit 1 means that there is a class at that time, bit 0 means there is none
    # for each day the time is from 8:30 am to 8:30 am
    # this should be able to cover the schedule of most of the courses in NTU
    for i in range(len(schedule) // 7):
        for j in range(7):
            string = str(schedule[i * 7 + j])
            string = string[7:len(string) - 9]
            if j == 0 and string != "": # get the index of the course
                currentIndex = string
                courseSchedule[courseCode][string]  = "0" * 120
            elif j == 3: # get the days that have this course
                indexOfDay = indexOfDay_dict[string]
            elif j == 4: # get the time of that course in a day
                numOfTimeSlots = getTime(string)
                indexOfTime    = (int(string[:4]) - 830) // 50
            # if j reaches 6, prasing is done
            # the following code is to modify the binary string according to the pasring result
            elif j == 6:
                startingIndex = indexOfDay + indexOfTime
                endingIndex   = startingIndex + numOfTimeSlots
                courseSchedule[courseCode][currentIndex] = courseSchedule[courseCode][currentIndex][:startingIndex] + \
                                                           "1" * numOfTimeSlots + \
                                                           courseSchedule[courseCode][currentIndex][endingIndex:]
            else:
                pass

def getTime(string):
    """convert the time format '0830-0930' to number of bits in the binary string"""

    timeInterval   = int(string[5:]) - int(string[:4])
    numOfTimeSlots = timeInterval // 50

    return numOfTimeSlots

def checkClash(time1, time2):
    """simply check whether the schedules of two courses clash"""

    for i in range(120):
        if time1[i] == time2[i] == "1": # schedules clash when the bits at the same index is both 1
            return True
        else:
            continue
    return False

def combineTime(time1, time2):
    """combine the schedules of two courses to form a new binary string containing schedule for both courses"""

    newTime = "0" * 120
    for i in range(120):
        if time1[i] == time2[i] == "0":
            continue
        else:
            newTime = newTime[:i] + "1" + newTime[i + 1:]
    return newTime

def testAllCombinations(combinations):
    """test all possible combinations of indexs for clashing"""

    global courseSchedule, bufferList

    # create a bufferList to store every index for every course in nested loops
    bufferList = []
    for course in courses:
        bufferList.append([index for index in courseSchedule[course].keys()])

    result = combinations[:] # make a copy of combinations to store the results

    for combination in combinations:
        currentTime = "0" * 120
        for i in range(len(combination)):
            nextTime = courseSchedule[courses[i]][bufferList[i][combination[i]]]
            if checkClash(currentTime, nextTime):
                result.remove(combination)
                break
            else:
                currentTime = combineTime(currentTime, nextTime)
                #if meetsRequirement(currentTime):
                #    continue
                #else:
                #    result.remove(combination)
                #    break

    return result

def meetsRequirement(time):
    """check whether a possible schedule meets my requirement"""

    for i in range(0,120,24):
        if "1" in time[i:i + 2]: # classes start after 9:30 am
            return False
        else:
            continue
    return True

def saveResult(result):

    """save all schedules that meet my requirement to a text file"""

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

#for code in courseSchedule:
#    for index in code:
#        print(index)

#create a list to store all combination
courseAndIndex = []
for course in courses:
    courseAndIndex.append([i for i in range(len(courseSchedule[course]))])

combinations = list(product(*courseAndIndex))

#plan courses
print("Planning your courses, please wait")
result = testAllCombinations(combinations)

saveResult(result)
