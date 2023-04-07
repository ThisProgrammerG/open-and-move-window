import subprocess
import sys
import time
from pathlib import Path

import win32con
from win32api import GetSystemMetrics
from win32gui import FindWindow
from win32gui import GetWindowPlacement
from win32gui import SetWindowPos
from win32gui import ShowWindow


FIREFOX_PATH = r'C:\Program Files\Mozilla Firefox\firefox.exe'

class Window:
    def __init__(self, window_title: str, program_path: str):
        self.window_title = window_title
        self.program_path = Path(program_path)
        self._hwnd = None

    def _find_hwnd(self):
        while (hwnd := FindWindow(None, self.window_title)) in [0, None]:
            time.sleep(0.1)
        self._hwnd = hwnd

    @property
    def hwnd(self):
        if not self._hwnd:
            self._find_hwnd()
        return self._hwnd

    @property
    def primary_width(self):
        return GetSystemMetrics(win32con.SM_CXSCREEN)

    @property
    def primary_height(self):
        return GetSystemMetrics(win32con.SM_CYSCREEN)

    @property
    def scaled_width(self):
        return round(self.primary_width // 1.5)

    @property
    def scaled_height(self):
        return round(self.primary_height // 1.5)

    @property
    def is_maximized(self):
        return GetWindowPlacement(self.hwnd)[1] == win32con.SW_SHOWMAXIMIZED

    def un_maximize(self):
        if self.is_maximized:
            ShowWindow(self.hwnd, win32con.SW_HIDE)
        else:
            ShowWindow(self.hwnd, win32con.SW_SHOWDEFAULT)

    def maximize(self):
        ShowWindow(self.hwnd, win32con.SW_MAXIMIZE)

    def move(self, x, y):
        SetWindowPos(self.hwnd, None, x, y, self.scaled_width, self.scaled_height, win32con.SWP_NOSIZE)

class WindowHandler:
    def __init__(self, window):
        self.window = window

    def run(self):
        subprocess.run([self.window.program_path])

    def move_window(self, primary_monitor: bool) -> None:
        """ Moves window to the right if not primary monitor. """
        x = -8 if primary_monitor else self.window.primary_width - 8
        y = -8
        self.window.move(x, y)

    def properly_maximize(self):
        self.window.un_maximize()
        self.window.maximize()

def main():
    primary_monitor = len(sys.argv) == 1
    window_handler = WindowHandler(Window('Mozilla Firefox', FIREFOX_PATH))
    window_handler.run()
    window_handler.move_window(primary_monitor=primary_monitor)
    window_handler.properly_maximize()

if __name__ == '__main__':
    main()
