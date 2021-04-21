import win32gui
import win32com.client
import time
from threading import Lock



class L2window:

    def __init__(self, window_id, window_name, hwnd):
        self.send_message(f'TEST L2window {window_id} created')
        self.window_id = window_id
        self.window_name = window_name
        self.hwnd = hwnd
        self.lock = Lock()
        self.shell = win32com.client.Dispatch("WScript.Shell")
        self.shell.SendKeys('%')

        x = 0
        y = 0
        width = 650
        height = 650

        self.left_top_x = width * window_id
        self.left_top_y = y
        self.width = width
        self.height = height

        self.enum_handler()

    def __del__(self):
        self.send_message(f"TEST Window {self.window_id} destroyed")

    def enum_handler(self):
        if win32gui.IsWindowVisible(self.hwnd):
            if self.window_name in win32gui.GetWindowText(self.hwnd):
                win32gui.MoveWindow(self.hwnd, self.left_top_x, self.left_top_y, self.width, self.height, True)

    def activate_window(self):
        try:
            # self.lock.acquire()
            win32gui.SetForegroundWindow(self.hwnd)
            time.sleep(0.01)
            # self.lock.release()
        except:
            print(f'TEST window {self.window_id} activation error')

    @classmethod
    def send_message(cls, message):
        print(message)
