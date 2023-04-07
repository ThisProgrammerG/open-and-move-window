import subprocess

import win32process

from window import Window


class WindowHandler:
    def __init__(self, window: Window):
        self.window = window

    def run(self):
        win32process.CreateProcess(
                str(self.window.program_path),  # ApplicationName (None means use command line)
                None,  # CommandLine
                None,  # ProcessAttributes (None means inherit from parent process)
                None,  # ThreadAttributes (None means inherit from parent process)
                False,  # bInheritHandles (False means don't inherit any handles)
                0,  # dwCreationFlags (0 means create process normally)
                None,  # NewEnvironment (None means use parent process's environment)
                None,  # CurrentDirectory (optional)
                win32process.STARTUPINFO()  # StartupInfo
        )

    def move_window(self, primary_monitor: bool) -> None:
        """ Moves window to the right if not primary monitor. """
        x = -8 if primary_monitor else self.window.primary_width - 8
        y = -8
        self.window.move(x, y)

    def properly_maximize(self):
        self.window.un_maximize()
        self.window.maximize()



































