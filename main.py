import sys

from window import Window
from window_handler import WindowHandler


FIREFOX_PATH = r'C:\Program Files\Mozilla Firefox\firefox.exe'

def main():
    primary_monitor = len(sys.argv) == 1
    window_handler = WindowHandler(Window('Mozilla Firefox', FIREFOX_PATH))
    window_handler.run()
    window_handler.move_window(primary_monitor=primary_monitor)
    window_handler.properly_maximize()

if __name__ == '__main__':
    main()
