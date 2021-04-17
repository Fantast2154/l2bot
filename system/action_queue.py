import time
import queue
import threading


class CommandQueue:
    def __init__(self):
        pass

    # def command(self, type, window, coordinates=None, key=None):
    #     if type == 'mouse'


class ActionQueue(threading.Thread):
    actions_list = None
    number = None
    priority_list = []

    # speed_list = []

    def __init__(self):
        threading.Thread.__init__(self)
        self.exit = threading.Event()
        self.actions_list = queue.Queue()
        self.self_exit = False

    def new_task(self, action, priority='Normal', speed='High'):
        self.actions_list.put(action)
        self.priority_list.insert(0, priority)
        # self.speed_list.append(speed)

    @classmethod
    def send_message(cls, message):
        print(message)

    @classmethod
    def task_execution(cls, action, priority='Normal', speed='High'):
        print(f'queue is doing execution {action} from fisher {priority}\n')

    @classmethod
    def start_queueing(cls):
        cls.send_message(f'TEST queue starts\n')

    def stop(self):
        self.send_message(f'TEST queue has finished its work\n')
        self.exit.set()

    def run(self):
        self.start_queueing()
        while not self.exit.is_set():
            while not self.actions_list.empty():
                try:
                    priority = self.priority_list[0]
                    del self.priority_list[0]
                    # speed = self.speed_list[0]
                    # self.task_execution(self.actions_list.get(), priority, speed)
                    self.task_execution(self.actions_list.get(), priority)
                finally:
                    time.sleep(0.1)
