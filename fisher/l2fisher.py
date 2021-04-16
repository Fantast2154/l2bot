import threading
import time


class Fisher(threading.Thread):

    fishing_window = None
    fisher_number = None
    stop_thread = None
    current_state = None

    def __init__(self, fishing_window, fisher_number):
        self.send_message(f'TEST fisher {fisher_number} calling')
        threading.Thread.__init__(self)
        self.fishing_window = fishing_window
        self.fisher_number = fisher_number
        self.current_state = 0

    def run(self):
        count = 0
        self.stop_thread = False
        while not self.stop_thread:
            print(f'fisher {self.fisher_number} is fishing\n')
            time.sleep(2)
            count += 1
            if count > 2:
                self.stop_fishing()

    def get_status(self):
        return self.current_state


    def callback(self):
        pass


    @classmethod
    def send_message(cls, message):
        print(message)

    def start_fishing(self):
        self.start()
        self.send_message(f'TEST fisher {self.fisher_number} starts fishing\n')

    def stop_fishing(self):
        self.stop_thread = True
        self.current_state = 1
        self.send_message(f'TEST fisher {self.fisher_number} has finished fishing\n')

    def get_status(self):
        pass

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


