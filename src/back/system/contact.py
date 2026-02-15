import webview
import os

from src.back.api.sendingFile import catbox, litterbox, buzzheavier
from src.back.api.checkForUpdate import isUpdateAvailable
from src.back.util.notify import notify

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
            notify("Upload Success!", f"Link: {result}")
        else:
            notify("Upload Failed", f"Problem with {platform}: {result}")

        return result

    def checkForUpdates(self):
        try:
            with open("version.txt", "r") as f:
                currentVersion = f.read().strip()
            return isUpdateAvailable(currentVersion)
        except Exception as e:
            return {"status": "error", "message": str(e)}