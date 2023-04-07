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

def run(window: Window):
    subprocess.run([window.program_path])

def move_window(window: Window, primary_monitor: bool) -> None:
    """ Moves window to the right if not primary monitor. """
    x = -8 if primary_monitor else window.primary_width - 8
    y = -8
    window.move(x, y)
    properly_maximize(window)

def properly_maximize(window: Window):
    window.un_maximize()
    window.maximize()

def main():
    primary_monitor = len(sys.argv) == 1
    window = Window('Mozilla Firefox', FIREFOX_PATH)
    run(window)
    move_window(window, primary_monitor=primary_monitor)

if __name__ == '__main__':
    main()
