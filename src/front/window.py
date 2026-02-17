import webview as wv
import os
import sys
import threading
import pystray
from PIL import Image

import src.back.util.print as print
from src.back.system.contact import API
from src.back.system.settings import Settings

class WindowManager:
    def __init__(self):
        self.window = None
        self.debugMode = False
        self.projectRoot = self.getProjectRoot()
        self.iconPath = self.getIconPath()

    def getProjectRoot(self):
        if getattr(sys, "frozen", False):
            return sys._MEIPASS
        return os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )

    def getIconPath(self):
        iconExt = ".ico" if sys.platform == "win32" else ".png"
        return os.path.join(
            self.projectRoot, "assets", "icon", f"SendYourFiles{iconExt}"
        )

    def createWindow(self):
        if self.window:
            self.showWindow()
            return

        htmlPath = os.path.join(os.path.dirname(__file__), "main", "index.html")
        print.debug(f"Creating window with URL: {htmlPath}")

        self.window = wv.create_window(
            title="Send Your Files",
            url=htmlPath,
            js_api=API(),
            width=800,
            height=600,
        )

        if Settings().getSetting("minimizeToTray"):
            self.window.events.closing += self.onWindowClosing

    def onWindowClosing(self):
        print.debug("X clicked! Hiding to tray and clearing RAM...")
        self.window.load_html(" ")  # less ram usage :3 (hopefully)
        self.window.hide()
        return False

    def showWindow(self, icon=None, item=None):
        if self.window:
            print.debug("Refreshing UI and showing window...")
            htmlPath = os.path.join(os.path.dirname(__file__), "main", "index.html")
            self.window.load_url(htmlPath)
            self.window.show()
        else:
            self.createWindow()

    def quitApp(self, icon, item):
        print.warning("Shutting down application...")
        icon.stop()
        os._exit(0)

    def setupTray(self):
        try:
            image = Image.open(self.iconPath)
            menu = pystray.Menu(
                pystray.MenuItem("Open", self.showWindow, default=True),
                pystray.MenuItem("Quit", self.quitApp),
            )

            self.trayIcon = pystray.Icon(
                "SendYourFiles", image, "Send Your Files", menu
            )
            self.trayIcon.run()
        except Exception as e:
            print.error(f"Failed to setup tray: {e}")

    def start(self, debugMode):
        self.debugMode = debugMode
        if self.debugMode:
            print.success("Debug mode is active.")

        if Settings().getSetting("minimizeToTray"):
            trayThread = threading.Thread(target=self.setupTray, daemon=True)
            trayThread.start()

        self.createWindow()
        wv.start(
            http_server=True,
            private_mode=True,
            debug=self.debugMode,
            icon=self.iconPath,
        )


def startUp(debugMode):
    manager = WindowManager()
    manager.start(debugMode)
