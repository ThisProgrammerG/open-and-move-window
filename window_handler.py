import subprocess


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



































