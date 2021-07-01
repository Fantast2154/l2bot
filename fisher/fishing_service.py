import time
import threading

from fisher.l2fisher import Fisher
from system.action_queue import *
import threading
from fisher.fishing_window import FishingWindow
from system.action_queue import ActionQueue


# self.send_message(f'{self!r}')

class FishingService:
    fishers = []
    fishing_windows = []
    raised_error = False
    exit = threading.Event()

    def __new__(cls, number_of_fishers, windows, q):
        if number_of_fishers < 1 or number_of_fishers > 3 or number_of_fishers != len(windows):
            # warning
            return None
        return super(FishingService, cls).__new__(cls)

    def __init__(self, number_of_fishers, windows, q):
        self.send_message(f'created')
        self.exit = threading.Event()

        q.activate_l2windows(windows)
        for fisher_id in range(number_of_fishers):

            win_capture = windows[fisher_id].wincap
            window_name = windows[fisher_id].window_name
            hwnd = windows[fisher_id].hwnd
            temp_fishing_window = FishingWindow(fisher_id, win_capture, window_name, hwnd)
            self.fishing_windows.append(temp_fishing_window)
            # temp_fishing_window.start() # TEST
            temp_fisher = Fisher(temp_fishing_window, fisher_id, number_of_fishers, q)
            # temp_fisher.start()
            self.fishers.append(temp_fisher)
            self.win_capture = win_capture

        self.number_of_fishers = number_of_fishers
        self.q = q

        self.offset_x = 0
        self.offset_y = 0

        self.start()

    def __del__(self):
        self.send_message("destroyed")

        del self

    @classmethod
    def send_message(cls, message):
        temp = 'FishingService: ' + message
        print(temp)

    @classmethod
    def start_fishing(cls, fishers_list=None):
        time.sleep(1)
        cls.send_message(f'start_fishing() calling')
        if fishers_list is None:
            for fisher in cls.fishers:
                fisher.start()
        else:
            for fisher in fishers_list:
                fisher.start()


    @classmethod
    def stop_fishers(cls, fishers_list=None):
        cls.send_message(f'stop_fishing() calling')
        if fishers_list is None:
            for fisher in cls.fishers:
                fisher.stop_fishing()
                # fisher.join()

        else:
            for fisher in fishers_list:
                fisher.stop_fishing()
                # fisher.join()

    @classmethod
    def pause_fishers(cls, fisher, delay=None):
        cls.send_message(f'stop_fishing() calling')
        if delay is None: # infinit pausing
            pass
            # while True:
            #     fisher.pause_fisher(None)
        else:
            fisher.pause_fisher(delay)

    @classmethod
    def fisher_response(cls, id, response):
        # fisher params
        # 0 - not fishing
        # 1 - fishing
        # 2 - busy with actions (mail,trade and etc.)
        # 8 - paused
        # 9 - error/stucked

        if response == 0:
            pass
            # cls.send_message(f'fisher {id} is not fishing')
        if response == 1:
            pass
            # cls.send_message(f'fisher {id} is fishing')
        if response == 2:
            pass
            # cls.send_message(f'fisher {id} busy with action (mailing, trading and etc.)')
        if response == 8:
            cls.send_message(f'fisher {id} is paused')
        if response == 9:
            cls.send_message(f'fisher {id} stucked (ERROR)')
            # cls.raise_error()

    @classmethod
    def run(cls):
        # cls.send_message(f'TEST FishingService run_loop() calling')
        while not cls.exit.is_set():
            if cls.fishers:
                for fisher in cls.fishers:
                    cls.fisher_response(fisher.fisher_id, fisher.get_status())
            time.sleep(5)
            #if key is pressed:
                # cls.pause_fishers(fisher)

            # if cls.raised_error:
            #     cls.stop_fishers()
            #     break

    @classmethod
    def start(cls):
        cls.send_message('thread starts')
        t = threading.Thread(target=cls.run)
        t.start()

    @classmethod
    def stop(cls):
        cls.stop_fishers()
        cls.send_message('thread stops')
        cls.exit.set()
        closing_time = 5
        timer = time.time()
        while time.time() - timer < closing_time:
            cls.send_message(f'timer before close ..... {time.time() - timer}')
            time.sleep(1)

        del cls.fishers
        del cls.fishing_windows

