import time
from pathlib import Path

import win32api
import win32con
import win32gui


class Window:
    def __init__(self, window_title: str, program_path: str):
        self.window_title = window_title
        self.program_path = Path(program_path)
        self._hwnd = None

    def _find_hwnd(self):
        # This works until a better version is found via StartupInfo or somehow directly getting the hwnd
        while win32gui.GetWindowText(hwnd := win32gui.GetForegroundWindow()) != self.window_title:
            time.sleep(0.1)
        self._hwnd = hwnd

    @property
    def hwnd(self):
        if not self._hwnd:
            self._find_hwnd()
        return self._hwnd

    @property
    def primary_width(self):
        return win32api.GetSystemMetrics(win32con.SM_CXSCREEN)

    @property
    def primary_height(self):
        return win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

    @property
    def scaled_width(self):
        return round(self.primary_width // 1.5)

    @property
    def scaled_height(self):
        return round(self.primary_height // 1.5)

    @property
    def is_maximized(self):
        return win32gui.GetWindowPlacement(self.hwnd)[1] == win32con.SW_SHOWMAXIMIZED

    def un_maximize(self):
        if self.is_maximized:
            win32gui.ShowWindow(self.hwnd, win32con.SW_HIDE)
        else:
            win32gui.ShowWindow(self.hwnd, win32con.SW_SHOWDEFAULT)

    def maximize(self):
        win32gui.ShowWindow(self.hwnd, win32con.SW_MAXIMIZE)

    def move(self, x, y):
        win32gui.SetWindowPos(self.hwnd, None, x, y, self.scaled_width, self.scaled_height, win32con.SWP_NOSIZE)
