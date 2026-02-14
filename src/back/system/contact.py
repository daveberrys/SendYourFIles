import webview
from src.back.api.sendingFile import catbox, litterbox, buzzheavier

class API:
    def pickFile(self):
        window = webview.active_window()
        file_path = window.create_file_dialog(webview.OPEN_DIALOG)
        if file_path:
            return file_path[0]
        return None

    def uploadTo(self, path, platform):
        if platform == "catbox":
            return catbox(path)
        elif platform == "litterbox":
            return litterbox(path)
        elif platform == "buzzheavier":
            return buzzheavier(path)
        return "Unknown platform"