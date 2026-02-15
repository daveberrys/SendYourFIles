import asyncio
from desktop_notifier import DesktopNotifier
import src.back.util.print as print
from sys import platform
from pathlib import Path

baseDir = Path(__file__).resolve().parent.parent.parent.parent
iconExt = "ico" if platform == "win32" else "png"
iconPath = baseDir / "assets" / "icon" / f"SendYourFiles.{iconExt}"

notifier = DesktopNotifier(
    app_name="Send Your Files",
    app_icon=iconPath
)

async def _send(title, message):
    try:
        await notifier.send(title=title, message=message, icon=iconPath)
    except Exception as e:
        print.error(f"Failed to send notification: {e}")

def notify(title, message):
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            loop.create_task(_send(title, message))
        else:
            loop.run_until_complete(_send(title, message))
    except Exception:
        asyncio.run(_send(title, message))