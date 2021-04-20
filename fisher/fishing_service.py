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
    win_capture = None

    def __new__(cls, number_of_fishers, windows, q):
        if number_of_fishers < 1 or number_of_fishers > 2 or number_of_fishers != len(windows):
            # warning
            return None
        return super(FishingService, cls).__new__(cls)

    def __init__(self, number_of_fishers, windows, q):
        self.send_message(f'TEST FishingService created')

        for fisher_id in range(number_of_fishers):

            win_capture = windows[fisher_id].win_capture
            window_name = windows[fisher_id].window_name
            hwnd = windows[fisher_id].hwnd
            temp_fishing_window = FishingWindow(fisher_id, win_capture, window_name, hwnd)
            self.fishing_windows.append(temp_fishing_window)

            temp_fisher = Fisher(temp_fishing_window, fisher_id, number_of_fishers, q)
            # temp_fisher.start()

            self.fishers.append(temp_fisher)
            self.win_capture = win_capture

        self.number_of_fishers = number_of_fishers
        self.q = q
        self.start_fishing()

    def __del__(self):
        self.send_message("TEST FishingService destroyed")

        del self

    @classmethod
    def send_message(cls, message):
        print(message)

    @classmethod
    def start_fishing(cls, fishers_list=None):
        cls.send_message(f'TEST FishingService start_fishing() calling')
        if fishers_list is None:
            for fisher in cls.fishers:
                fisher.start()
                # fisher.start_fishing()
        else:
            for fisher in fishers_list:
                fisher.start()
                # fisher.start_fishing()
        cls.run_loop()

    @classmethod
    def stop_fishing(cls, fishers_list=None):
        cls.send_message(f'TEST FishingService stop_fishing() calling')
        if fishers_list is None:
            for fisher in cls.fishers:
                fisher.stop_fishing()
                # fisher.join()

        else:
            for fisher in fishers_list:
                fisher.stop_fishing()
                # fisher.join()

        del cls.fishers
        del cls.fishing_windows

    @classmethod
    def fisher_response(cls, response):

        if response == 0:  # OK
            pass
        if response == 1:  # stopped fishing
            cls.send_message(f'TEST FishingService fisher_response(response) calling')
            cls.raise_error()
        if response == 2:  # fatal problem
            cls.send_message(f'TEST FishingService fisher_response(response) calling')
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
        cls.send_message(f'TEST raise_error calling')
        cls.raised_error = True
