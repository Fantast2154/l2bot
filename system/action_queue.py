import win32process
from pywinauto import win32functions

# from lib.AutoHotPy import AutoHotPy
# from lib.InterceptionWrapper import InterceptionMouseState, InterceptionMouseStroke

from system.action_service import ActionService
import time
import queue
import threading
from threading import Lock
import win32gui
import pyautogui
import win32com.client
import win32api
import win32con
import keyboard
import platform
import pywinauto
from ctypes import windll
import ctypes

import sys
import win32gui as wgui
import win32process as wproc
import win32api as wapi

import pyperclip

class ActionQueue(threading.Thread):
    number = None

    actions = []
    action_params = []
    windows = []
    priority_list = []
    action_rate_list = []


    def __init__(self):
        self.send_message(f'Queue created\n')
        threading.Thread.__init__(self)
        # self.action_service = ActionService(wincap)
        self.lock = Lock()
        self.exit = threading.Event()
        # self.queue_list = queue.Queue()
        self.queue_list = []
        self.shell = win32com.client.Dispatch("WScript.Shell")
        self.shell.SendKeys('%')
        self.last_active_window = None
        # self.auto = AutoHotPy()
        # self.auto.registerExit(self.auto.ESC, self.exitAutoHotKey)
        # t = threading.Thread(target=self.auto_start)
        # t.start()


    # def auto_start(self):
          # Registering an end key is mandatory to be able tos top the program gracefully
        # self.auto.start()

    def activate_l2windows(self, windows):
        try:
            for window in windows:
                self.lock.acquire()
                time.sleep(0.05)
                self.shell.SendKeys('%')
                win32gui.SetForegroundWindow(window.hwnd)
                time.sleep(0.05)
                self.lock.release()
        except:
            print('TEST queue window activation error')

    def send_message(self, message):
        temp = 'ActionQueue' + ': ' + message
        print(temp)

    def new_task(self, action, action_param, window, priority='Normal', action_rate='High'):
        self.queue_list.append(1)
        self.actions.append(action)
        self.action_params.append(action_param)
        # for param in self.action_params:
        #     print('ACTION PARAM', param[0])
        self.windows.append(window)
        # self.priority_list.append(priority)
        # self.action_rate_list.append(action_rate)
        # self.action_rate_list.insert(0, action_rate)

    def new_mouse_task(self):
        pass

    def new_keyboard_task(self):
        pass

    def window_init(self, window):

        # x = window.wincap.offset_x[window.window_id] + 10
        # y = window.wincap.offset_y[window.window_id] - 10
        # win32api.SetCursorPos((x, y))
        # time.sleep(0.1)
        # pyautogui.mouseDown()
        # time.sleep(0.1)
        # pyautogui.mouseUp()
        # time.sleep(0.1)
        #
        # for i in range(200):
        #     # win32api.SetCursorPos((x+i, y+i))
        #     self.auto.moveMouseToPosition(x+i, y+i)
        #     time.sleep(0.001)
        time.sleep(1)
        print(f'WINDOW {window.window_id} WAS INITIALIZED')

    def click(self, x, y, param=False):
        # self.lock.acquire()
        win32api.SetCursorPos((x, y))
        #win32api.
        if param:
            time.sleep(0.01)
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
            time.sleep(0.03)
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)
            time.sleep(0.01)

        for i in range(4):
            win32api.SetCursorPos((x+i, y+i))
            #time.sleep(0.01)
        # time.sleep(0.01)
        # pyautogui.mouseDown()
        # time.sleep(0.02)
        # pyautogui.mouseUp()
        # time.sleep(0.01)
        time.sleep(0.01)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        time.sleep(0.03)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        time.sleep(0.01)
        # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        # time.sleep(0.2)
        # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        # self.lock.release()

    def exitAutoHotKey(self, autohotpy, event):
        """
        exit the program when you press ESC
        """
        autohotpy.stop()

    def click_target(self, x, y):
        pass
        # time.sleep(0.02)
        # self.auto.moveMouseToPosition(x, y)


    def task_execution(self, action, params, window, action_rate='High'):
        # try:
        # print('Qsize = ', len(self.queue_list))
        # keyboard.send('s')

        # self.lock.acquire()

        # params = [0]*6
        if action == 'mouse':

            if len(params) != 6:
                return

            [(x_temp, y_temp)] = params[0]
            x = x_temp + window.wincap.offset_x[window.window_id]
            y = y_temp + window.wincap.offset_y[window.window_id]

            if window.hwnd != self.last_active_window:
                self.last_active_window = window.hwnd
                # win32gui.SetForegroundWindow(window.hwnd)
                # self.shell.SendKeys('%')
                # self.focus_by_BOYKO(window.hwnd)
                self.click(x, y, param=True)
            else:

                self.click(x, y, param=False)
            # self.click_target(x, y)

        if action == 'keyboard':
            if len(params) != 2:
                return
            # self.action_service.keyboard_master(params)
        # except:
        # print('TEST queue window activation error')
        # self.lock.release()

    @classmethod
    def start_queueing(cls):
        pass

    def stop(self):
        self.send_message(f'TEST Queue destroyed\n')
        self.exit.set()

    def run(self):
        self.start_queueing()

        while not self.exit.is_set():
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

                    del self.windows[0]
                    del self.actions[0]
                    del self.action_params[0]

                    self.task_execution(action, action_param, window)
                finally:
                    pass

    def focus_by_BOYKO(self, HEX):
        remote_thread, i = wproc.GetWindowThreadProcessId(HEX)
        wproc.AttachThreadInput(wapi.GetCurrentThreadId(), remote_thread, True)
        prev_handle = wgui.SetFocus(HEX)
        self.shell.SendKeys('%')
        win32gui.SetForegroundWindow(HEX)

