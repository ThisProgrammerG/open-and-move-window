import sys

import win32api
import win32con
import win32event
import win32gui
import win32process

from window import Window
from window_handler import WindowHandler


FIREFOX_PATH = r'C:\Program Files\Mozilla Firefox\firefox.exe'

def run():
    primary_monitor = len(sys.argv) == 1
    window_handler = WindowHandler(Window('Mozilla Firefox', FIREFOX_PATH))
    window_handler.run()
    window_handler.move_window(primary_monitor=primary_monitor)
    window_handler.properly_maximize()

def find_firefox_window():
    firefox_windows = []

    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetClassName(hwnd) == "MozillaWindowClass":
            print(f"window text: '{win32gui.GetWindowText(hwnd)}'")
            hwnds.append(hwnd)
        return True

    win32gui.EnumWindows(callback, firefox_windows)
    return firefox_windows

def find_hwnds():
    hwnds = find_firefox_window()
    print('Handles:')
    print(*hwnds, sep='\n')
    print('=' * 50)
    return hwnds

def main():
    # run()
    primary = False
    startupinfo = win32process.STARTUPINFO()
    startupinfo.dwFlags = win32process.STARTF_USESHOWWINDOW
    startupinfo.dwX = -8 if primary else win32api.GetSystemMetrics(win32con.SM_CXSCREEN) + 80
    startupinfo.dwY = -8
    startupinfo.dwXSize = int(win32api.GetSystemMetrics(win32con.SM_CXSCREEN) + 16 // 1.5)
    startupinfo.dwYSize = int(win32api.GetSystemMetrics(win32con.SM_CYSCREEN) + 16 // 1.5)
    startupinfo.wShowWindow = win32con.SW_MINIMIZE


    proc_info = win32process.CreateProcess(
            FIREFOX_PATH,  # ApplicationName (None means use command line)
            None,  # CommandLine
            None,  # ProcessAttributes (None means inherit from parent process)
            None,  # ThreadAttributes (None means inherit from parent process)
            False,  # bInheritHandles (False means don't inherit any handles)
            0,  # dwCreationFlags (0 means create process normally)
            None,  # NewEnvironment (None means use parent process's environment)
            None,  # CurrentDirectory (optional)
            startupinfo  # StartupInfo
    )
    process_handle = proc_info[0]
    win32event.WaitForInputIdle(process_handle, win32event.INFINITE)


if __name__ == '__main__':
    main()
