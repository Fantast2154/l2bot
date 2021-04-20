from system.action_service import ActionService
import time
import queue
import threading
from threading import Lock
import win32gui
import win32com.client

class CommandQueue:
    def __init__(self):
        pass

    # def command(self, type, window, coordinates=None, key=None):
    #     if type == 'mouse'


class ActionQueue(threading.Thread):

    number = None
    priority_list = []
    windows = []
    actions = []
    action_rate_list = []

    def __init__(self):
        self.send_message(f'TEST Queue created\n')
        threading.Thread.__init__(self)
        self.lock = Lock()
        self.exit = threading.Event()
        self.queue_list = queue.Queue()
        self.shell = win32com.client.Dispatch("WScript.Shell")

    def new_task(self, count, window, priority='Normal', action_rate='High'):
        self.queue_list.put(count)
        self.windows.append(window)
        self.priority_list.append(priority)
        self.action_rate_list.append(action_rate)
        # self.action_rate_list.insert(0, action_rate)

    @classmethod
    def send_message(cls, message):
        print(message)

    def task_execution(self, count, window, priority='Normal', action_rate='High'):

        self.lock.acquire()
        time.sleep(0.01)
        try:
            print(f'queue is doing execution {count}. Window {window.window_id} hwnd = {window.hwnd} is active\n')
            self.shell.SendKeys('%')
            win32gui.SetForegroundWindow(window.hwnd)
        except:
            print('TEST queue window activation error')
        time.sleep(0.01)
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
                    else:
                        continue
                    # action = self.actions[0]

                    # del self.priority_list[0]

                    del self.windows[0]
                    # del self.actions[0]

                    # speed = self.speed_list[0]
                    # self.task_execution(self.queue_list.get(), priority, speed)

                    # self.queue_list.get()
                    self.task_execution(self.queue_list.get(), window)
                    time.sleep(0.01)
                finally:
                    pass
