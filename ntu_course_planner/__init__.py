import requests
from . import config

r = requests.get("https://raw.githubusercontent.com/koallen/ntu-course-planner-cli/master/LATEST")
latest_version = r.text.rstrip("\n")
config.init(latest_version[0:4], latest_version[-1])
