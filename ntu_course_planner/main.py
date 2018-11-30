from .planner import Planner
from .version import get_version

import requests

def main():
    # make sure the user has the newest course schedule
    r = requests.get("https://raw.githubusercontent.com/koallen/ntu-course-planner-cli/master/LATEST")
    latest_version = r.text.rstrip("\n")
    current_version = get_version()
    if latest_version == current_version:
        Planner().start()
    else:
        print("You have version " + current_version + " and the latest version is " + latest_version)
        print("Please update ntu-course-planner to get the latest course schedule")
        exit(-1)
