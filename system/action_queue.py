import time

class CommandQueue:
    def __init__(self):
        pass

    # def command(self, type, window, coordinates=None, key=None):
    #     if type == 'mouse'


class ActionQueue:
    def __init__(self):
        pass

    def send_task(self, action):
        self.actions_list.append(action)

    def task_execution(self, action):
        pass

    def start_loop(self):

        while True:  # break point?

            if actions_list:
                self.task_execution()

            time.sleep(0.1)

    actions_list = []
