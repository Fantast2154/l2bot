from system.action_service import ActionService
import time
import threading
import win32gui
import win32com.client
import win32api
import win32con

import win32gui as wgui
import win32process as wproc
import win32api as wapi
from multiprocessing import Manager

from pynput.mouse import Controller, Button


class ActionQueue():
    number = None

    actions = []
    action_params = []
    windows = []
    priority_list = []
    action_rate_list = []

    def __init__(self):
        # self.send_message(f'Queue created\n')

        # threading.Thread.__init__(self)
        # self.action_service = ActionService(wincap)

        # self.exit = threading.Event()
        # self.queue_list = queue.Queue()

        # self.shell = win32com.client.Dispatch("WScript.Shell")
        # self.shell.SendKeys('%')
        self.last_active_window = None
        self.test_avg = []
        self.action_counter = 0
        self.mouse = Controller()
        manager = Manager()
        self.actions = manager.list()
        self.action_params = manager.list()
        self.windows = manager.list()
        self.priority_list = manager.list()
        self.action_rate_list = manager.list()
        self.queue_list = manager.list()

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
        self.queue_list.append(1)
        self.actions.append(action)
        self.action_params.append(action_param)
        self.windows.append(window)
        self.priority_list.append(priority)
        self.action_rate_list.append(action_rate)
        # self.action_rate_list.insert(0, action_rate)

    def new_mouse_task(self):
        pass

    def new_keyboard_task(self):
        pass

    def click(self, x, y, param=False):

        self.mouse.position = (x, y)
        time.sleep(0.03)

        if param:
            self.mouse.press(Button.right)
            time.sleep(0.02)
            self.mouse.release(Button.right)
            time.sleep(0.03)

            # for i in range(4):
            #     win32api.SetCursorPos((x+i, y+i))

            self.mouse.move(4, 4)
            time.sleep(0.01)

        self.mouse.press(Button.left)
        time.sleep(0.07)
        self.mouse.release(Button.left)
        time.sleep(0.03)

    def click2(self, x, y, param=False):

        win32api.SetCursorPos((x, y))
        if param:

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
                self.click(x, y, param=True)
            else:
                self.click(x, y, param=False)

    @classmethod
    def start_queueing(cls):
        pass
    def start(self):
        # self.send_message('start queueing')
        t = threading.Thread(target=self.run)
        t.start()

    def stop(self):
        self.send_message(f'destroyed\n')
        # self.exit.set()

    def run(self):

        while True:
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
