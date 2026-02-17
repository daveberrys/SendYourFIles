from src.front.window import startUp as s
from src.back.system.history import History
from src.back.system.settings import Settings

import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug", action="store_true", help="enable debug mode")
args = parser.parse_args()

debugMode = args.debug
History().checkHistory()
Settings().checkFile()

if __name__ == "__main__":
    s(debugMode=debugMode)