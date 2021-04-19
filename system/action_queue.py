import time
import queue
import threading


class CommandQueue:
    def __init__(self):
        pass

    # def command(self, type, window, coordinates=None, key=None):
    #     if type == 'mouse'


class ActionQueue(threading.Thread):

    number = None
    priority_list = []
    windows_list = []
    actions = []
    action_rate_list = []

    # speed_list = []

    def __init__(self):
        self.send_message(f'TEST Queue created\n')
        threading.Thread.__init__(self)
        self.exit = threading.Event()
        self.actions_list = queue.Queue()

    def new_task(self, action, window, priority='Normal', action_rate='High'):
        self.actions_list.put(action)
        self.windows_list.insert(0, window)
        self.actions.insert(0, action)
        self.priority_list.insert(0, priority)
        self.action_rate_list.append(action_rate)

    @classmethod
    def send_message(cls, message):
        print(message)

    @classmethod
    def task_execution(cls, action, window, priority='Normal', speed='High'):
        print(f'queue is doing execution {action} from fisher {window.window_id}\n')
        window.activate_window()
        print(f'Window {window.window_id} is active\n')

    @classmethod
    def start_queueing(cls):
        pass

    def stop(self):
        self.send_message(f'TEST Queue destroyed\n')
        self.exit.set()

    def run(self):
        self.start_queueing()
        while not self.exit.is_set():
            while not self.actions_list.empty():
                try:
                    # priority = self.priority_list[0]
                    window = self.windows_list[0]
                    # action = self.actions[0]

                    # del self.priority_list[0]
                    del self.windows_list[0]
                    # del self.actions[0]

                    # speed = self.speed_list[0]
                    # self.task_execution(self.actions_list.get(), priority, speed)

                    self.task_execution(self.actions_list.get(), window)
                finally:
                    time.sleep(0.1)
