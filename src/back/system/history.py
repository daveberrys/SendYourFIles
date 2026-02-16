"""

~~~~~~~~~~ HISTORY ~~~~~~~~~~

What it stores:
- Provider you used
- Time you uploaded it
- File name you uploaded it
- The link that was given to you
- LitterBox duration (if used)

Stores it in:
Windows: ~/Appdata/Roaming/dev.pages.codedave.SendYourFiles
macOS: ~/Library/Application Support/dev.pages.codedave.SendYourFiles
Linux: ~/.config/dev.pages.codedave.SendYourFiles
Android: ~/Android/media/dev.pages.codedave.SendYourFiles

NONE OF THE THINGS THAT ARE LISTED IS SHARED ONLINE. IT'S ALL LOCAL IN YOUR SYSTEM.
WE CARE ABOUT YOUR PRIVACY AND YOUR PRIVACY IS OUR NUMBER ONE PRIORITY.
OPEN SOURCE IS LOVE, OPEN SOURCE IS LIFE.

"""


import json
import os
import datetime

import src.back.util.print as print
from src.back.system.settings import Settings as se
from src.back.system.settings import Sys as sy

class History:
    def __init__(self):
        self.configPath = sy.getOSpath(self)
        self.historyPath = os.path.join(self.configPath, "history.json")

    def checkHistory(self):
        if os.path.exists(self.historyPath):
            print.success(f"History found at: {self.historyPath}")
            return True
        else:
            print.error(f"History not found at: {self.historyPath}")
            print.success(f"Creating history at: {self.historyPath}")

            try:
                se.checkFolder(self)
                with open(self.historyPath, "a") as f:
                    json.dump([], f)
                print.success(f"History created at: {self.historyPath}")
                return True
            except Exception as e:
                print.error(f"Error creating history: {e}")
                return False
            except OSError as e:
                print.fatal(f"Fatal error creating history: {e}")
                return False

    def storeHistory(self, service, filename, link, litterboxdur):
        try:
            with open(self.historyPath, "r") as f:
                self.historyContent = json.load(f)
            self.historyContent.append({
                "service": service,
                "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "filename": filename,
                "link": link,
                "litterboxdur": litterboxdur
            })
            with open(self.historyPath, "w") as f:
                json.dump(self.historyContent, f)

            return print.success(f"History stored at: {self.historyPath}")
        except Exception as e:
            return print.error(f"Error storing history: {e}")

