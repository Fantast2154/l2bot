import time
from queue import Queue
from fisher.l2fisher import Fisher


class FishingService:
    fishers = []
    raised_error = False
    win_capture = None

    def __init__(self, windows, wincap):
        self.send_message(f'TEST FishingService created')
        self.number_of_fishers = len(windows)
        self.q = Queue()
        self.wincap = wincap
        for window in windows:
            temp_fisher = Fisher(window, wincap, self.q)
            self.fishers.append(temp_fisher)

        self.start_fishing()

    def __del__(self):
        self.send_message("TEST FishingService destroyed")

        del self

    @classmethod
    def send_message(cls, message):
        print(message)

    def start_fishing(self, fishers_list=None):
        self.send_message(f'TEST FishingService start_fishing() calling')
        if fishers_list is None:
            for fisher in self.fishers:
                fisher.start_fishing()

        else:
            for fisher in fishers_list:
                fisher.start_fishing()

        self.run_loop()

    @classmethod
    def stop_fishing(cls, fishers_list=None):
        cls.send_message(f'TEST FishingService stop_fishing() calling')
        if fishers_list is None:
            for fisher in cls.fishers:
                fisher.stop_fishing()

        else:
            for fisher in fishers_list:
                fisher.stop_fishing()

        del cls.fishers

    # @classmethod
    # def fisher_response(cls, response):
    #
    #     if response == 0:  # OK
    #         pass
    #     if response == 1:  # stopped fishing
    #         cls.send_message(f'TEST FishingService fisher_response(response) calling')
    #         cls.raise_error()
    #     if response == 2:  # fatal problem
    #         cls.send_message(f'TEST FishingService fisher_response(response) calling')
    #         cls.raise_error()

    def run_loop(self):
        # self.send_message(f'TEST FishingService run_loop() calling')
        while True:
            if self.q.qsize() > 0:
                print('Qsize = ', self.q.qsize())
                self.q.get()
            for fisher in self.fishers:
                if not fisher.fishing_is_active:
                    fisher.fishing()
                    # if fisher.fishing_window():
                    #     if fisher.clock() and (fisher.red_bar() or fisher.blue_bar()):
                    #         pass

            # for fisher in self.fishers:
            #     self.fisher_response(fisher.current_state)
            #
            # if self.raised_error:
            #     self.stop_fishing()
            #     break

            # if fisher are not fishing

    # @classmethod
    # def raise_error(cls):
    #     cls.send_message(f'TEST raise_error calling')
    #     cls.raised_error = True
    #     cls.stop_fishing()


def message_gui(message):
    print(message)


def input_number(message):
    while True:
        try:
            userInput = int(input(message))
            if userInput < 0:
                print('The value must be >= 0')
                continue
        except ValueError:
            print("Not an integer! Try again.")
            continue
        else:
            return userInput
