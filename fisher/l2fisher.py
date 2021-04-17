import threading
import time


class Fisher(threading.Thread):

    fishing_window = None
    fisher_number = None
    number_of_fishers = None
    current_state = None

    def __init__(self, fishing_window, fisher_number, number_of_fishers):
        self.send_message(f'TEST fisher {fisher_number} calling')
        threading.Thread.__init__(self)
        self.exit = threading.Event()
        self.fishing_window = fishing_window
        self.fisher_number = fisher_number
        self.number_of_fishers = number_of_fishers
        self.current_state = 0
        self.self_exit = False

    def run(self):
        count = 0
        while not self.exit.is_set():
            print(f'fisher {self.fisher_number} is fishing count {count}\n')
            time.sleep(0.1)
            count += 1
            if count > 10:
                self.current_state = 1
                return
        self.current_state = 2

    def get_status(self):
        return self.current_state

    def callback(self):
        pass

    @classmethod
    def send_message(cls, message):
        print(message)

    def stop_run(self):
        self.exit.set()

    def start_fishing(self):
        self.send_message(f'TEST fisher {self.fisher_number} starts fishing\n')
        # self.start()

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
