import win32gui
import win32com.client
import re
import win32con
import psutil
import win32process
import win32process as wproc
import win32api as wapi
import time
import pythoncom
from threading import Lock


class L2window:

    window_id = 0

    def __init__(self, window_id, wincap, window_name, hwnd, screenhot):
        self.window_id = window_id
        x = 0
        y = 0
        width = 650
        height = 650
        self.left_top_x = width * window_id + 640
        self.left_top_y = y
        self.width = width
        self.height = height
        self.window_name = window_name
        self.screenshot = screenhot
        self.hwnd = hwnd
        self.wincap = wincap
        self.enum_handler()
        self.send_message(f'created')

    # def __del__(self):
    #     self.send_message(f'destroyed')

    def enum_handler(self):
        if win32gui.IsWindowVisible(self.hwnd):
            if self.window_name in win32gui.GetWindowText(self.hwnd):
                win32gui.MoveWindow(self.hwnd, self.left_top_x, self.left_top_y, self.width, self.height, True)

    def send_message(self, message):
        temp = 'L2window' + f' {self.window_id}' + ': ' + message
        print(temp)
