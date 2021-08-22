import random

import keyboard

from system.action_service import ActionService
import time
import threading
import win32gui
import win32com.client
import win32api
import win32con
import math
import win32gui as wgui
import win32process as wproc
import win32api as wapi
from multiprocessing import Manager

from pynput.mouse import Button
import pynput


class ActionQueue:
    number = None

    actions = []
    action_params = []
    windows = []
    priority_list = []
    action_rate_list = []

    def __init__(self, windows):
        # self.send_message(f'Queue created\n')

        # threading.Thread.__init__(self)
        # self.action_service = ActionService(wincap)

        # self.exit = threading.Event()
        # self.queue_list = queue.Queue()

        # self.shell = win32com.client.Dispatch("WScript.Shell")
        # self.shell.SendKeys('%')
        self.last_window_action = [0] * len(windows)
        self.last_active_window = None
        self.test_avg = []
        self.action_counter = 0
        self.mouse = pynput.mouse.Controller()
        # self.keyboard = pynput.keyboard.Controller()
        manager = Manager()
        self.actions = manager.list()
        self.action_params = manager.list()
        self.windows = manager.list()
        self.priority_list = manager.list()
        self.action_rate_list = manager.list()
        self.queue_list = manager.list()

        self.exit_is_set = False

        self.VK_CODE = {'backspace': 0x08,
                        'tab': 0x09,
                        'clear': 0x0C,
                        'enter': 0x0D,
                        'shift': 0x10,
                        'ctrl': 0x11,
                        'alt': 0x12,
                        'pause': 0x13,
                        'caps_lock': 0x14,
                        'esc': 0x1B,
                        'spacebar': 0x20,
                        'page_up': 0x21,
                        'page_down': 0x22,
                        'end': 0x23,
                        'home': 0x24,
                        'left_arrow': 0x25,
                        'up_arrow': 0x26,
                        'right_arrow': 0x27,
                        'down_arrow': 0x28,
                        'select': 0x29,
                        'print': 0x2A,
                        'execute': 0x2B,
                        'print_screen': 0x2C,
                        'ins': 0x2D,
                        'del': 0x2E,
                        'help': 0x2F,
                        '0': 0x30,
                        '1': 0x31,
                        '2': 0x32,
                        '3': 0x33,
                        '4': 0x34,
                        '5': 0x35,
                        '6': 0x36,
                        '7': 0x37,
                        '8': 0x38,
                        '9': 0x39,
                        'a': 0x41,
                        'b': 0x42,
                        'c': 0x43,
                        'd': 0x44,
                        'e': 0x45,
                        'f': 0x46,
                        'g': 0x47,
                        'h': 0x48,
                        'i': 0x49,
                        'j': 0x4A,
                        'k': 0x4B,
                        'l': 0x4C,
                        'm': 0x4D,
                        'n': 0x4E,
                        'o': 0x4F,
                        'p': 0x50,
                        'q': 0x51,
                        'r': 0x52,
                        's': 0x53,
                        't': 0x54,
                        'u': 0x55,
                        'v': 0x56,
                        'w': 0x57,
                        'x': 0x58,
                        'y': 0x59,
                        'z': 0x5A,
                        'numpad_0': 0x60,
                        'numpad_1': 0x61,
                        'numpad_2': 0x62,
                        'numpad_3': 0x63,
                        'numpad_4': 0x64,
                        'numpad_5': 0x65,
                        'numpad_6': 0x66,
                        'numpad_7': 0x67,
                        'numpad_8': 0x68,
                        'numpad_9': 0x69,
                        'multiply_key': 0x6A,
                        'add_key': 0x6B,
                        'separator_key': 0x6C,
                        'subtract_key': 0x6D,
                        'decimal_key': 0x6E,
                        'divide_key': 0x6F,
                        'F1': 0x70,
                        'F2': 0x71,
                        'F3': 0x72,
                        'F4': 0x73,
                        'F5': 0x74,
                        'F6': 0x75,
                        'F7': 0x76,
                        'F8': 0x77,
                        'F9': 0x78,
                        'F10': 0x79,
                        'F11': 0x7A,
                        'F12': 0x7B,
                        'F13': 0x7C,
                        'F14': 0x7D,
                        'F15': 0x7E,
                        'F16': 0x7F,
                        'F17': 0x80,
                        'F18': 0x81,
                        'F19': 0x82,
                        'F20': 0x83,
                        'F21': 0x84,
                        'F22': 0x85,
                        'F23': 0x86,
                        'F24': 0x87,
                        'num_lock': 0x90,
                        'scroll_lock': 0x91,
                        'left_shift': 0xA0,
                        'right_shift ': 0xA1,
                        'left_control': 0xA2,
                        'right_control': 0xA3,
                        'left_menu': 0xA4,
                        'right_menu': 0xA5,
                        'browser_back': 0xA6,
                        'browser_forward': 0xA7,
                        'browser_refresh': 0xA8,
                        'browser_stop': 0xA9,
                        'browser_search': 0xAA,
                        'browser_favorites': 0xAB,
                        'browser_start_and_home': 0xAC,
                        'volume_mute': 0xAD,
                        'volume_Down': 0xAE,
                        'volume_up': 0xAF,
                        'next_track': 0xB0,
                        'previous_track': 0xB1,
                        'stop_media': 0xB2,
                        'play/pause_media': 0xB3,
                        'start_mail': 0xB4,
                        'select_media': 0xB5,
                        'start_application_1': 0xB6,
                        'start_application_2': 0xB7,
                        'attn_key': 0xF6,
                        'crsel_key': 0xF7,
                        'exsel_key': 0xF8,
                        'play_key': 0xFA,
                        'zoom_key': 0xFB,
                        'clear_key': 0xFE,
                        '+': 0xBB,
                        ',': 0xBC,
                        '-': 0xBD,
                        '.': 0xBE,
                        '/': 0xBF,
                        '`': 0xC0,
                        ';': 0xBA,
                        '[': 0xDB,
                        '\\': 0xDC,
                        ']': 0xDD,
                        "'": 0xDE,
                        '`': 0xC0}

    def activate_l2windows(self, windows):
        try:

            for window in windows:
                time.sleep(0.05)
                # self.shell.SendKeys('%')
                win32gui.SetForegroundWindow(window.hwnd)
                time.sleep(0.05)

        except:
            print('TEST queue window activation error')

    def send_message(self, message):
        temp = 'ActionQueue' + ': ' + message
        print(temp)

    def new_task(self, action, action_param, window, priority='Normal', action_rate='High'):
        # print(action_param)
        self.queue_list.append(1)
        self.actions.append(action)
        self.action_params.append(action_param)
        self.windows.append(window)
        self.priority_list.append(priority)
        self.action_rate_list.append(action_rate)
        # self.action_rate_list.insert(0, action_rate)

    def keyboard_button_press(self, x, y, k, param):
        if param:
            self.mouse.position = (x - random.randint(0, 3), y - random.randint(0, 3))
            time.sleep(0.03)
            self.mouse.press(Button.left)
            time.sleep(0.02)
            self.mouse.release(Button.left)
            time.sleep(0.03)
            self.mouse.move(4, 4)
            time.sleep(0.03)

        # self.mouse.press(Button.left)
        # time.sleep(0.07)
        # self.mouse.release(Button.left)
        # time.sleep(0.03)
        keyboard.send(k)
        time.sleep(0.01)

    def click(self, x, y, swtich_window=False, params=False):
        # print('params', params)
        self.mouse.position = (x - random.randint(0, 3), y - random.randint(0, 3))
        time.sleep(0.03)
        if swtich_window:
            time.sleep(0.02)
            self.mouse.press(Button.left)
            time.sleep(0.02)
            self.mouse.release(Button.left)
            time.sleep(0.03)
            self.mouse.move(4, 4)
            time.sleep(0.03)

        if 'double' in params:
            print('double click')
            self.mouse.press(Button.left)
            time.sleep(0.02)
            self.mouse.release(Button.left)
            time.sleep(0.03)
            self.mouse.press(Button.left)
            time.sleep(0.02)
            self.mouse.release(Button.left)
            time.sleep(0.03)
            return

        if params[1] and params[5] == 'drag_and_drop':
            self.mouse.press(Button.left)
            time.sleep(0.04)
            VK_CODE = {'alt':0x12}
            args = []
            args.append('alt')
            for i in args:
                win32api.keybd_event(VK_CODE[i], 0,0,0)
                time.sleep(0.1)

            [(temp_x, temp_y)] = params[1]
            self.mouse.position = (temp_x, temp_y)
            time.sleep(0.04)

            for i in args:
                win32api.keybd_event(VK_CODE[i],0 ,win32con.KEYEVENTF_KEYUP ,0)
                time.sleep(0.1)

            self.mouse.release(Button.left)
            time.sleep(0.04)
            return

        self.mouse.press(Button.left)
        time.sleep(0.07)
        self.mouse.release(Button.left)
        time.sleep(0.03)

    def click2(self, x, y, params=False):

        win32api.SetCursorPos((x, y))
        if params:

            time.sleep(0.01)
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
            time.sleep(0.01)
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)

            for i in range(4):
                win32api.SetCursorPos((x + i, y + i))

        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        time.sleep(0.01)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

    def click_target(self, x, y):
        pass

    def task_execution(self, action, params, window, action_rate='High'):
        if action == 'mouse':

            if len(params) != 6:
                return
            [(x_temp, y_temp)] = params[0]
            x = x_temp + window.wincap.offset_x[window.window_id]
            y = y_temp + window.wincap.offset_y[window.window_id]

            if window.hwnd != self.last_active_window:
                self.last_active_window = window.hwnd
                self.click(x, y, swtich_window=True, params=params)
            else:
                self.click(x, y, swtich_window=False, params=params)

            if 'insert' in params:
                keyboard.send('ctrl+v')

    @classmethod
    def start_queueing(cls):
        pass

    def initial_task(self, action, action_param, window, priority='Normal', action_rate='High'):
        pass
    # def start(self):
    #     # self.send_message('start queueing')
    #     t = threading.Thread(target=self.run)
    #     t.start()

    def stop(self):
        self.exit_is_set = True
        self.send_message(f'destroyed\n')
        # self.exit.set()

    def run(self):

        while not self.exit_is_set:
            # while not self.queue_list.empty():
            while self.queue_list:
                try:
                    # priority = self.priority_list[0]
                    if self.windows:
                        window = self.windows[0]
                        action = self.actions[0]
                        action_param = self.action_params[0]
                    else:
                        continue
                    # action = self.actions[0]

                    # del self.priority_list[0]

                    self.windows.pop(0)
                    self.actions.pop(0)
                    self.action_params.pop(0)
                    # self.priority_list.pop(0)
                    # self.action_rate_list.pop(0)

                    self.task_execution(action, action_param, window)
                finally:
                    pass
