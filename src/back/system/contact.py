import webview
import os
import sys
import json

from src.back.api.sendingFile import catbox, litterbox, buzzheavier
from src.back.api.checkForUpdate import isUpdateAvailable
from src.back.util.notify import notify
import src.back.util.print as print
from src.back.system.settings import Settings

class API:
    def pickFile(self):
        window = webview.active_window()
        file_path = window.create_file_dialog(webview.FileDialog.OPEN)
        if file_path:
            path = file_path[0]
            size = os.path.getsize(path)
            return {"path": path, "size": size}
        return None

    def uploadTo(self, path, platform, duration="1h"):
        filename = os.path.basename(path)
        
        if Settings().getSetting("notifyYou"):
            notify("Upload Started", f"Sending {filename} to {platform}...")

        result = ""
        if platform == "catbox":
            result = catbox(path)
        elif platform == "litterbox":
            result = litterbox(path, duration)
        elif platform == "buzzheavier":
            result = buzzheavier(path)
        else:
            result = "Unknown platform"

        if result.startswith("http"):
            if Settings().getSetting("notifyYou"):
                notify("Upload Success!", f"Link: {result}")
        else:
            if Settings().getSetting("notifyYou"):
                notify("Upload Failed", f"Problem with {platform}: {result}")

        return result

    def checkForUpdates(self):
        if not Settings().getSetting("checkForUpdates"):
            print.debug("Updates disabled by user.")
            return {"status": "disabled"}

        # checks if the local file exists
        try:
            if getattr(sys, 'frozen', False):
                basePath = sys._MEIPASS
            else:
                basePath = os.path.abspath(".")
            
            versionPath = os.path.join(basePath, "version.txt")
            with open(versionPath, "r") as f:
                currentVersion = f.read().strip()
            print.success(f"Local file found! Current version: {currentVersion}")
        except Exception as e:
            print.error(f"Local file error: {e}")
            return {"status": "error", "message": f"Local file error: {e}"}

        # contacts github for the latest update
        try:
            print.debug("Checking for updates...")
            return isUpdateAvailable(currentVersion)
        except Exception as e:
            print.error(f"Network error: {e}")
            return {"status": "error", "message": f"Network error: {e}"}

    def localCurrentVersion(self):
        try:
            if getattr(sys, 'frozen', False):
                basePath = sys._MEIPASS
            else:
                basePath = os.path.abspath(".")

            versionPath = os.path.join(basePath, "version.txt")
            with open(versionPath, "r") as f:
                currentVersion = f.read().strip()
                return currentVersion
        except Exception as e:
            print.error(f"Local file error: {e}")
            return None

    def getSettings(self):
        print.debug("API: getSettings called")
        try:
            settings = Settings()
            
            # Load the settings definitions (names, descriptions)
            if os.path.exists(settings.defaultSettingsPath):
                with open(settings.defaultSettingsPath, "r") as f:
                    data = json.load(f)
                print.success(f"Default settings loaded from: {settings.defaultSettingsPath}")
            else:
                print.error(f"Default settings MISSING at: {settings.defaultSettingsPath}")
                return {"settings": {}}
            
            # Load the user's current saved settings
            user_settings = {}
            if os.path.exists(settings.settingsPath):
                with open(settings.settingsPath, "r") as f:
                    user_settings = json.load(f)
                print.success(f"User settings loaded from: {settings.settingsPath}")
            
            # Update the definitions with the user's values
            for key, value in data["settings"].items():
                if key in user_settings:
                    data["settings"][key]["default"] = str(user_settings[key]).lower()
            
            return data
        except Exception as e:
            print.error(f"Error fetching settings: {e}")
            return {"settings": {}}

    def saveSettings(self, key, value):
        settings = Settings()
        return settings.updateSetting(key, value)