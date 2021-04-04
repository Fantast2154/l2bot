import threading
import time
from fisher.fishing_window import FishingWindow
from fisher.action_queue import ActionQueue


class Fisher(threading.Thread):
    def __init__(self, fishing_window, number):
        threading.Thread.__init__(self)
        self.fishing_window = fishing_window
        self.number = number

    def fishing_message(message):
        print(message) #how to send message to main file?

    def start(self):
        # while True:
        self.fishing_message('fisher - ' + str(self.number) + ' is fishing')
            # time.sleep(self.number)

    def start_fishing(self):
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

    fishing_window = None
    number = None
