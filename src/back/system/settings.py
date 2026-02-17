import os
import json

from sys import platform

import src.back.util.print as print

appID = "dev.pages.codedave.SendYourFiles"


class Sys:
    def getOSpath(self):
        if platform == "win32":
            configPath = os.path.join(os.getenv("APPDATA"), appID)
        elif platform == "linux":
            configPath = os.path.join(os.getenv("XDG_CONFIG_HOME"), appID)
        elif platform == "darwin":
            configPath = os.path.join(
                os.getenv("HOME"), "Library", "Application Support", appID
            )
        else:
            configPath = os.path.join(os.getenv("HOME"), ".config", appID)
        print.debug(f"Config path: {configPath}")
        return configPath


class Settings:
    def __init__(self):
        self.configPath = os.path.join(Sys.getOSpath(self))

        self.settingsPath = os.path.join(self.configPath, "settings.json")
        self.defaultSettingsPath = os.path.join(os.path.dirname(__file__), "extra", "settings.json")
        
        if not os.path.exists(self.defaultSettingsPath):
            self.defaultSettingsPath = os.path.abspath(os.path.join("src", "back", "extra", "settings.json"))

        self.defaultSettings = {}
        self.settings = {}

    def checkFolder(self):
        if os.path.exists(self.configPath):
            print.success(f"Config path found at: {self.configPath}")
            return True
        else:
            print.warning(f"Config path not found at: {self.configPath}")
            print.debug(f"Creating config path at: {self.configPath}")
            
            try:
                os.makedirs(self.configPath)
                print.success(f"Config path created at: {self.configPath}")
                return True
            except Exception as e:
                print.error(f"Error creating config path: {e}")
                return False
            except OSError as e:
                print.fatal(f"Fatal OS error creating config path: {e}")
                return False

    def checkFile(self):
        if os.path.exists(self.settingsPath):
            print.success(f"Settings found at: {self.settingsPath}")
            return True
        else:
            print.warning(f"Settings not found at: {self.settingsPath}")
            print.debug(f"Creating settings file at: {self.settingsPath}")

            try:
                with open(self.settingsPath, "w") as f:
                    with open(self.defaultSettingsPath, "r") as f2:
                        data = json.load(f2)
                        newSettings = {}
                        for key, value in data["settings"].items():
                            val = value["default"]
                            if value.get("type") == "boolean":
                                if str(val).lower() == "true":
                                    val = True
                                elif str(val).lower() == "false":
                                    val = False
                            newSettings[key] = val
                        json.dump(newSettings, f, indent=4)
                print.success(f"Settings created at: {self.settingsPath}")
                return True
            except Exception as e:
                print.error(f"Error creating settings: {e}")
                return False
            except OSError as e:
                print.fatal(f"Fatal OS error creating settings: {e}")
                return False

    def updateSetting(self, key, value):
        try:
            data = {}
            if os.path.exists(self.settingsPath):
                with open(self.settingsPath, "r") as f:
                    data = json.load(f)
            
            data[key] = value

            with open(self.settingsPath, "w") as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            print.error(f"Error updating setting: {e}")
            return False
    
    def getSetting(self, key):
        try:
            with open(self.settingsPath, "r") as f:
                return json.load(f).get(key, True)
        except Exception:
            pass