from fisher.action_service import ActionService
import time
class  ActionQueue:
    def __init__(self):
        pass
    def send_task(action):
        self.actions_list.append(action)

    def task_execution(self, action):
        pass

    def start_loop(self):

        while True: #break point?

            if actions_list:
                self.task_execution()

            time.sleep(0.1)

    actions_list = []
