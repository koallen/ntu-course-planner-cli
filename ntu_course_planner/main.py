from .planner import Planner
from . import config

import requests

def main():
    print("Planning for " + config.ACADYEAR + "/" + config.ACADSEM)
    Planner().start()
