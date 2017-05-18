from .planner import Planner
from .version import VERSION

import requests

def main():
    # make sure the user has the newest course schedule
    r = requests.get("https://raw.githubusercontent.com/koallen/ntu-course-planner-cli/master/LATEST")
    if r.text == VERSION:
        Planner().start()
    else:
        print("Please update ntu-course-planner to get the latest course schedule")
        exit(-1)
