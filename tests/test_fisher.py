import threading
import time
import random
from threading import Lock, Thread
import pyautogui
import win32gui, win32com.client


class TestFisher(threading.Thread):
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys('%')
    random_actions = ['pump', 'reel']

    def __init__(self, fisher_name, test_window, q):
        threading.Thread.__init__(self)
        self.lock = Lock()
        self.fisher_name = fisher_name
        self.q = q
        self.test_window = test_window

    def mouse_move(self, action):
        self.lock.acquire()
        if action == 'pump':
            pyautogui.moveTo(self.test_x1, self.test_y1)
        elif action == 'reel':
            pyautogui.moveTo(self.test_x2, self.test_y2)
        self.lock.release()
        # time.sleep(1)

    def window_set_active(self, hwnd):
        self.lock.acquire()
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(0.1)
        self.lock.release()

    def run(self):
        print(f'{self.fisher_name} is running ')
        t = time.time()
        while time.time() - t < 10:
            try:
                action = random.choice(self.random_actions)
                print(f'{self.fisher_name} is doing {action} ')
                # self.q.put(self.mouse_move(action))
                self.q.put(self.window_set_active(self.test_window))
            except:
                break
