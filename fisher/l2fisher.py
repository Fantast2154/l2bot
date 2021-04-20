import threading
import random
from threading import Lock
import time
import win32gui
import cv2


class Fisher(threading.Thread):

    fishing_window = None
    fisher_id = None
    number_of_fishers = None
    current_state = None
    stopped = None
    q = None

    def __init__(self, fishing_window, fisher_id, number_of_fishers, q):
        self.send_message(f'TEST fisher {fisher_id} created')
        threading.Thread.__init__(self)
        self.exit = threading.Event()
        self.fishing_window = fishing_window
        self.fisher_id = fisher_id
        self.number_of_fishers = number_of_fishers
        self.current_state = 0
        self.q = q

    def __del__(self):
        self.send_message(f"TEST fisher {self.fisher_id} destroyed")

    def test_action(self, count):
        self.q.new_task(count, self.fishing_window)

    def run(self):
        count = 0
        self.start_fishing()

        while not self.exit.is_set():

            time.sleep(0.3)
            self.fishing_window.update_screenshot()
            if count < 15:
                rand = random.randint(1, 2)
                if rand == 1:
                    self.pumping(count)
                if rand == 2:
                    self.reeling(count)
            if count > 70:
                self.current_state = 1
                return
            count += 1
        self.current_state = 2

    def get_status(self):
        return self.current_state



    @classmethod
    def send_message(cls, message):
        print(message)

    def start_fishing(self):
        delay = 3
        print(f'The fisher {self.fisher_id} will start in ........ {delay} sec')
        time.sleep(delay)
        self.send_message(f'TEST fisher {self.fisher_id} starts fishing\n')
        self.stopped = False

    def stop_fishing(self):
        self.send_message(f'TEST fisher {self.fisher_id} has finished fishing\n')
        self.exit.set()

    def pumping(self, count):
        self.q.new_task(count, 'mouse', [[(100, 100)], True, 'LEFT', False, False, False], self.fishing_window)

    def reeling(self, count):
        self.q.new_task(count, 'mouse', [[(500, 500)], True, 'LEFT', False, False, False], self.fishing_window)

    def turn_on_soski(self):
        pass

    def choose_nigtly_bait(self):
        pass

    def choose_daily_bait(self):
        pass

    def send_mail(self):
        pass

    def receive_mail(self):
        pass

    def change_bait(self):
        pass
