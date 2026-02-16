import os
from sys import platform
import src.back.util.print as print

appID = "dev.pages.codedave.SendYourFiles"
configPath = ""

class Sys:
    def getOSpath(self):
        if platform == "win32":
            configPath = os.path.join(os.getenv("APPDATA"), appID)
        elif platform == "linux":
            configPath = os.path.join(os.getenv("XDG_CONFIG_HOME"), appID)
        elif platform == "darwin":
            configPath = os.path.join(os.getenv("HOME"), "Library", "Application Support", appID)
        else:
            configPath = os.path.join(os.getenv("HOME"), ".config", appID)
        print.debug(f"Config path: {configPath}")
        return configPath

class Settings:
    def checkFolder(self):
        configPath = Sys.getOSpath(self)
        if not os.path.exists(configPath):
            try:
                os.makedirs(configPath)
                print.success(f"Created config path: {configPath}")
            except Exception as e:
                print.error(f"Error creating config path: {e}")
            except OSError as e:
                print.fatal(f"Fatal error creating config path: {e}")
        else:
            print.debug(f"Config path already exists: {configPath}")