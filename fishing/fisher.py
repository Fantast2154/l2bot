import threading
import time


class Fisher(threading.Thread):
    def __init__(self, fishing_window, number):
        threading.Thread.__init__(self)
        self.fishing_window = fishing_window
        self.number = number

    def run(self):
        while True:
            print('fisher - ' + str(self.number) + ' is fishing')
            time.sleep(self.number)
