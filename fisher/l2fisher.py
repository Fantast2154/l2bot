import threading
import time
import cv2


class Fisher(threading.Thread):

    fishing_window = None
    fisher_number = None
    number_of_fishers = None
    current_state = None
    stopped = None
    q = None
    screen_master = None

    def __init__(self, fishing_window, fisher_number, number_of_fishers, q):
        self.send_message(f'TEST fisher {fisher_number} calling')
        threading.Thread.__init__(self)

        self.exit = threading.Event()
        self.fishing_window = fishing_window
        self.fisher_number = fisher_number
        self.number_of_fishers = number_of_fishers
        self.current_state = 0
        self.q = q
        self.screen_master = fishing_window.win_capture

    def run(self):
        time.sleep(3)
        count = 0
        self.start_fishing()

        while not self.exit.is_set():
            self.test_action(count)
            time.sleep(1)
            count += 1
            if count == 3:
                s = self.screen_master.get_screenshot()
                cv2.imshow('Test', s)
                cv2.waitKey(1)
            if count > 3:
                self.current_state = 1
                return

        self.current_state = 2

    def get_status(self):
        return self.current_state

    def test_action(self, count):
        self.q.new_task(count, self.fisher_number)

    @classmethod
    def send_message(cls, message):
        print(message)

    def start_fishing(self):
        self.send_message(f'TEST fisher {self.fisher_number} starts fishing\n')
        self.stopped = False

    def stop_fishing(self):
        self.send_message(f'TEST fisher {self.fisher_number} has finished fishing\n')
        self.exit.set()

    def pumping(self):
        pass

    def reeling(self):
        pass

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
