import webview
import winsound
import os
import sys
import json
from PIL import Image, ImageDraw


def _base_path():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


def _data_dir():
    """Persistent data directory (not inside MEIPASS for frozen apps)."""
    if getattr(sys, 'frozen', False):
        d = os.path.join(os.path.expanduser("~"), ".pomodoro")
    else:
        d = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(d, exist_ok=True)
    return d


HTML_PATH = os.path.join(_base_path(), "app.html")
ICON_PATH = os.path.join(_base_path(), "icon.png")
DATA_PATH = os.path.join(_data_dir(), "data.json")


def generate_icon():
    if os.path.exists(ICON_PATH):
        return
    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([8, 14, 56, 62], fill="#ff6b6b")
    draw.ellipse([18, 22, 28, 32], fill=(255, 255, 255, 80))
    draw.ellipse([26, 6, 38, 22], fill="#34c759")
    img.save(ICON_PATH)


class Api:
    """JS-Python bridge exposed as window.pywebview.api."""

    def notify(self):
        try:
            winsound.MessageBeep(winsound.MB_ICONINFORMATION)
        except Exception:
            pass

    def save_data(self, data):
        try:
            with open(DATA_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)
        except Exception:
            pass

    def load_data(self):
        try:
            with open(DATA_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}


def main():
    generate_icon()

    api = Api()
    webview.create_window(
        title="番茄钟",
        url=HTML_PATH,
        width=340,
        height=600,
        frameless=False,
        on_top=True,
        resizable=False,
        easy_drag=False,
        js_api=api,
    )

    webview.start(debug=False)


if __name__ == "__main__":
    main()
