from system.action_service import ActionService
import time
import queue
import threading
from threading import Lock
import win32gui
import win32com.client


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

    def new_task(self, count, action, action_param, window, priority='Normal', action_rate='High'):
        print('TEST queue added')
        self.queue_list.put(count)
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

    def task_execution(self, count, action, params, window, action_rate='High'):
        #try:

        self.lock.acquire()
        time.sleep(0.01)
        print(f'queue {count} fisher {window.window_id} is calling {action} hwnd = {window.hwnd}\n')

        win32gui.SetForegroundWindow(window.hwnd)
        time.sleep(0.01)

        if action == 'mouse':

            if len(params) != 6:
                return
            # print(params)
            self.action_service.mouse_master(params)
        if action == 'keyboard':
            if len(params) != 2:
                return
            self.action_service.keyboard_master(params)
        time.sleep(0.01)
        #except:
            #print('TEST queue window activation error')
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
                        action = self.actions[0]
                        action_param = self.action_params[0]
                    else:
                        continue
                    # action = self.actions[0]

                    # del self.priority_list[0]

                    del self.windows[0]
                    del self.actions[0]
                    # del self.actions[0]

                    # speed = self.speed_list[0]
                    # self.task_execution(self.queue_list.get(), priority, speed)

                    # self.queue_list.get()
                    self.task_execution(self.queue_list.get(), action, action_param, window)
                    time.sleep(0.01)
                finally:
                    pass
