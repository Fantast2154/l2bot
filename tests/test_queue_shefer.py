from system.action_service import ActionService
import time
import queue
import threading
from threading import Lock
import win32gui
import win32com.client
import pyautogui


class ActionQueue(threading.Thread):

    number = None

    actions = []
    action_params = []
    windows = []
    priority_list = []
    action_rate_list = []

    def __init__(self, wincap):
        self.send_message(f'TEST Queue created\n')
        threading.Thread.__init__(self)
        self.action_service = ActionService(wincap)
        self.lock = Lock()
        self.exit = threading.Event()
        self.queue_list = queue.Queue()
        self.shell = win32com.client.Dispatch("WScript.Shell")
        self.shell.SendKeys('%')
        self.offset_x = wincap.offset_x
        self.offset_y = wincap.offset_y

    def activate_l2windows(self, windows):
        try:
            for window in windows:
                time.sleep(0.01)
                self.lock.acquire()
                time.sleep(0.5)
                self.shell.SendKeys('%')
                win32gui.SetForegroundWindow(window.hwnd)
                time.sleep(0.5)
                self.lock.release()
                time.sleep(0.01)
        except:
            print('TEST queue window activation error')

    @classmethod
    def send_message(cls, message):
        print(message)

    def new_task(self, coordinates, hwnd):
        print('Qsize = ', self.queue_list.qsize())
        self.windows.append(hwnd)
        self.queue_list.put(coordinates)
        print(coordinates, hwnd)
        print()

    def new_mouse_task(self):
        pass

    def new_keyboard_task(self):
        pass

    def task_execution(self, coordinates, hwnd):
        #try:

        self.lock.acquire()

        win32gui.SetForegroundWindow(hwnd)

        [(x_temp, y_temp)] = coordinates
        x = x_temp + self.offset_x
        y = y_temp + self.offset_y
        pyautogui.moveTo(x, y)
        time.sleep(0.02)
        pyautogui.mouseDown()
        time.sleep(0.02)
        pyautogui.mouseUp()
        time.sleep(0.03)
        self.lock.release()

    @classmethod
    def start_queueing(cls):
        pass

    def stop(self):
        self.send_message(f'TEST Queue destroyed\n')
        self.exit.set()

    def run(self):
        self.start_queueing()

        while not self.exit.is_set():
            while not self.queue_list.empty():
                try:
                    # priority = self.priority_list[0]
                    if self.windows[0]:
                        window = self.windows[0]
                        # action_param = self.action_params[0]
                    else:
                        continue

                    del self.windows[0]

                    action_param = 1
                    self.task_execution(self.queue_list.get(), window)
                finally:
                    pass
