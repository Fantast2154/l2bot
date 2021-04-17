import time
import threading

from fisher.l2fisher import Fisher
from system.action_queue import *

from fisher.fishing_window import FishingWindow
from system.action_queue import ActionQueue


# self.send_message(f'{self!r}')

class FishingService:
    number_of_fishers = 0
    fishers = []
    fishing_windows = []
    raised_error = False
    q = None

    def __new__(cls, number_of_fishers, windows, q):
        if number_of_fishers < 1 or number_of_fishers > 2 or number_of_fishers != len(windows):
            # warning
            return None
        return super(FishingService, cls).__new__(cls)

    def __init__(self, number_of_fishers, windows, q):
        self.send_message(f'TEST FishingService calling')

        for i in range(number_of_fishers):
            x = windows[i].left_top_x
            y = windows[i].left_top_y
            width = windows[i].width
            height = windows[i].height

            temp_fishing_window = FishingWindow(x, y, width, height)
            self.fishing_windows.append(temp_fishing_window)

            temp_fisher = Fisher(temp_fishing_window, i, number_of_fishers, q)
            temp_fisher.start()
            self.fishers.append(temp_fisher)

        self.number_of_fishers = number_of_fishers
        self.q = q
        self.start_fishing()

    def __del__(self):
        self.send_message("closing fishing service")

        del self

    @classmethod
    def send_message(cls, message):
        print(message)

    @classmethod
    def start_fishing(cls, fishers_list=None):
        cls.send_message(f'TEST FishingService start_fishing() calling')
        if fishers_list is None:
            for fisher in cls.fishers:
                fisher.start_fishing()
        else:
            for fisher in fishers_list:
                fisher.start_fishing()

        cls.run_loop()

    @classmethod
    def stop_fishing(cls, fishers_list=None):
        cls.send_message(f'TEST FishingService stop_fishing() calling')
        if fishers_list is None:
            for fisher in cls.fishers:
                fisher.stop_fishing()
                fisher.join()

        else:
            for fisher in fishers_list:
                fisher.stop_fishing()
                fisher.join()

        # cls.q.join()
        del cls.fishers

    @classmethod
    def fisher_response(cls, response):

        if response == 0:  # OK
            pass
        if response == 1:  # stopped fishing
            # cls.send_message(f'TEST FishingService fisher_response(response) calling')
            cls.raise_error()
        if response == 2:  # fatal problem
            # cls.send_message(f'TEST FishingService fisher_response(response) calling')
            cls.raise_error()

    @classmethod
    def run_loop(cls):
        # cls.send_message(f'TEST FishingService run_loop() calling')
        while True:
            for fisher in cls.fishers:
                cls.fisher_response(fisher.current_state)

            if cls.raised_error:
                cls.stop_fishing()
                break

    @classmethod
    def raise_error(cls):
        # cls.send_message(f'TEST raise_error calling')
        cls.raised_error = True
