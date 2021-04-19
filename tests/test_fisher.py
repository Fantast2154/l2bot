import threading
import time
import random
from threading import Lock, Thread
import pyautogui


class TestFisher(threading.Thread):
    random_actions = ['pump', 'reel']

    def __init__(self, fisher_name, test_window, q):
        threading.Thread.__init__(self)
        self.lock = Lock()
        self.fisher_name = fisher_name
        self.q = q

        self.test_x1 = test_window[0]
        self.test_y1 = test_window[1]
        self.test_x2 = test_window[2]
        self.test_y2 = test_window[3]

    def mouse_move(self, action):
        self.lock.acquire()
        if action == 'pump':
            pyautogui.moveTo(self.test_x1, self.test_y1)
        elif action == 'reel':
            pyautogui.moveTo(self.test_x2, self.test_y2)
        self.lock.release()
        # time.sleep(1)

    def run(self):
        print(f'{self.fisher_name} is running ')
        t = time.time()
        while time.time() - t < 10:
            action = random.choice(self.random_actions)
            print(f'{self.fisher_name} is doing {action} ')
            self.q.put(self.mouse_move(action))
