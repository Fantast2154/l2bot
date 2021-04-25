import time
from queue import Queue
from fisher.l2fisher import Fisher


class Supplier:
    def __init__(self, window_supplier, wincap, q):
        pass


class FishingService:
    fishers = []
    supplier = None
    raised_error = False
    win_capture = None

    def __init__(self, windows, wincap, window_supplier):
        self.send_message(f'TEST FishingService created')
        self.number_of_fishers = len(windows)
        self.q = Queue()
        self.wincap = wincap

        for window in windows:
            temp_fisher = Fisher(window, wincap, self.q)
            self.fishers.append(temp_fisher)

        if window_supplier:
            self.supplier = Supplier(window_supplier, wincap, self.q)

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

        while True:

            if self.q.qsize() > 0:
                # print('Qsize = ', self.q.qsize())
                self.q.get()
                continue

            for fisher in self.fishers:
                if not fisher.fishing_is_allowed:
                    continue

            self.fisher_update_vision()

            self.fishers_check_fishingwindow()

            self.actions_while_not_fishing()

            self.fishers_check_clock_and_bars()

    def fisher_update_vision(self):
        for fisher in self.fishers:
            if fisher.daytime():
                # print(f'TEST fisher {fisher.fisher_id} day time')
                fisher.update_day_screen()
            else:
                fisher.update_night_screen()

    def fishers_check_fishingwindow(self):
        for fisher in self.fishers:
            if not fisher.fishing_window() and fisher.resting() > fisher.max_rest_time:

                time.sleep(2)  # test
                print(f'TEST fisher {fisher.fisher_id} fishing_window check')
                x = fisher.window.left_top_x + 100  # test
                y = fisher.window.left_top_y + 100  # test
                fisher.fishing_window_pos = [(x, y)]  # test

                x = fisher.window.left_top_x + 111  # test
                y = fisher.window.left_top_y + 111  # test
                fisher.clock_pos = [(x, y)]  # test

                x = fisher.window.left_top_x + 222  # test
                y = fisher.window.left_top_y + 222  # test
                fisher.blue_bar_pos = [(x, y)]  # test

                fisher.fishing()

    def fishers_check_clock_and_bars(self):
        for fisher in self.fishers:
            if fisher.clock():
                time.sleep(2)  # test
                blue_bar_pos = fisher.blue_bar()
                if fisher.daytime():
                    if blue_bar_pos:
                        for coordinates in blue_bar_pos:
                            (fisher.x_border, fisher.y_border) = coordinates
                            print(f'TEST coordinates blue = {coordinates}')
                            fisher.q.put(fisher.mouse_move([(fisher.x_border, fisher.y_border)]))

                            x = fisher.window.left_top_x + 100  # test
                            y = fisher.window.left_top_y + 100  # test
                            fisher.fishing_window_pos = [(x, y)]  # test
                else:
                    red_bar_pos = fisher.red_bar()
                    if blue_bar_pos:
                        for coordinates in blue_bar_pos:
                            (fisher.x_border, fisher.y_border) = coordinates
                            print(f'TEST coordinates blue = {coordinates}')
                            fisher.q.put(fisher.mouse_move([(fisher.x_border, fisher.y_border)]))
                    if red_bar_pos:
                        for coordinates in red_bar_pos:
                            (fisher.x_border, fisher.y_border) = coordinates
                            print(f'TEST coordinates red = {coordinates}')

    def actions_while_not_fishing(self):
        for fisher in self.fishers:
            if not fisher.fishing_window() and fisher.resting() > fisher.max_rest_time:
                self.check_buff()
                self.check_soski_clicked()
                self.check_fishing_problems()
                self.check_soski_baits_overweight()

    def check_buff(self):
        for fisher in self.fishers:
            if fisher.rebuff_time():
                fisher.rebuff()

    def check_soski_clicked(self):
        pass

    def check_fishing_problems(self):
        for fisher in self.fishers:
            if fisher.is_not_fishing_too_long():  # ~20 secs
                fisher.change_bait()

    def check_soski_baits_overweight(self):
        for fisher in self.fishers:
            fisher.pause_fishing()  # to all fishers: STOP FISHING

        for fisher in self.fishers:
            dbaits_count = fisher.check_dbaits_count()
            nbaits_count = fisher.check_nbaits_count()
            soski_count = fisher.check_soski_count()
            overweight = fisher.check_dbaits_count()

    def send_catched_fish(self):
        pass

    def receive_baits_soski(self):
        pass

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
