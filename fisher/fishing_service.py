from fisher.l2fisher import Fisher

from fisher.fishing_window import FishingWindow
from system.action_queue import ActionQueue


# self.send_message(f'{self!r}')

class FishingService:
    def __new__(cls, number_of_fishers, windows):
        if number_of_fishers < 1 or number_of_fishers > 2 or number_of_fishers != len(windows):
            # warning
            return None
        return super(FishingService, cls).__new__(cls)

    def __init__(self, number_of_fishers, windows):
        self.send_message(f'TEST FishingService calling')

        for i in range(number_of_fishers):
            self.fishing_windows.append(windows[i])
            self.fishers.append(Fisher(self.fishing_windows[i], i))

        self.number_of_fishers = number_of_fishers

        self.start_fishing()

    def __del__(self):
        self.send_message("closing fishing")

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



        else:
            for fisher in fishers_list:
                fisher.start()

        cls.run_loop()

    @classmethod
    def stop_fishing(cls, fishers_list=None):
        # cls.send_message(f'TEST FishingService stop_fishing() calling')
        if fishers_list is None:
            for fisher in cls.fishers:
                fisher.stop()
                del fisher
        else:
            for fisher in fishers_list:
                fisher.stop()
                del fisher

    @classmethod
    def fisher_response(cls, response):
        # cls.send_message(f'TEST FishingService fisher_response(response) calling')
        if response == 0:  # OK
            cls.send_message('action 0')
        if response == 1:  # warning
            cls.send_message('action 1')
        if response == 2:  # fatal problem
            cls.send_message('action 2')
            cls.raise_error()

    @classmethod
    def run_loop(cls):
        cls.send_message(f'TEST FishingService run_loop() calling')
        while True:
            for fisher in cls.fishers:
                cls.fisher_response(fisher.get_status())
                if cls.raised_error:
                    cls.stop_fishing()
                    break

    @classmethod
    def raise_error(cls):
        cls.raised_error = True

    number_of_fishers = 0
    fishers = []
    fishing_windows = []
    raised_error = False
