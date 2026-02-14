import webview as wv
import os

import src.back.util.print as print
from src.back.system.contact import API

def startUp(debugMode):
    def loadCSS(window):
        whereCss = os.path.join(os.path.dirname(__file__), "cacaStyle.css")
        with open(whereCss, "r") as f:
            css = f.read()
        window.load_css(css)

    here = os.path.join(os.path.dirname(__file__), "main", "index.html")
    print.debug(f"URL for HTTP is at {here}")

    if debugMode:
        print.success("Debug mode is enabled. I don't know why you'd want this.")

    window = wv.create_window(
        title="Send Your Files",
        url=here,
        width=800,
        height=600,
        js_api=API()
    )

    window.events.loaded += loadCSS
    wv.start(
        http_server=True,
        debug=debugMode,
        private_mode=True,
    )