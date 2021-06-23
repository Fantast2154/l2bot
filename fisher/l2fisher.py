import threading
import random
from threading import Lock
import time
import win32gui
import cv2


class Fisher(threading.Thread):
    # fisher params
    fishing_window = None
    fisher_id = None
    number_of_fishers = None
    current_state = None
    # 0 - not fishing
    # 1 - fishing
    # 2 - busy with actions (mail,trade and etc.)
    # 9 - error/stucked
    paused = None
    q = None

    # send/receive counters
    send_counter = 0
    receive_counter = 0
    attempt_counter = 0

    # fishing timers
    total_fishing_time = 0
    rod_cast_time = 0
    buff_time = time.time()

    # overweight, soski, baits
    current_baits = None
    max_weight = 0
    used_weight = 0
    baits_colored = 0
    baits_luminous = 0
    soski = 0
    baits_colored_max = 0
    baits_luminous_max = 0
    soski_max = 0

    # connection params
    bot_is_connected = True
    it_is_almost_server_restart_time = False

    def __init__(self, fishing_window, fisher_id, number_of_fishers, q):
        threading.Thread.__init__(self)
        self.exit = threading.Event()
        self.fishing_window = fishing_window
        self.fisher_id = fisher_id
        self.number_of_fishers = number_of_fishers
        self.current_state = 0
        self.q = q
        self.send_message(f'created')

        self.send_counter = 0
        self.receive_counter = 0
        self.attempt_counter = 0

    def __del__(self):
        self.send_message(f"destroyed")

    def send_message(self, message):
        temp = 'Fisher' + f' {self.fisher_id}' + ': ' + message
        print(temp)

    def test_action(self, count):
        self.q.new_task(count, self.fishing_window)

    def pause_fisher(self, delay):
        pass

    def run(self):
        count = -1
        self.start_fishing(count)

        while not self.exit.is_set():  # or keyboard was pressed and not disconnected
            count += 1
            time.sleep(0.1)
            cv2.imshow(f'fisher {self.fisher_id}', self.fishing_window.update_screenshot())
            cv2.waitKey(1)
            if count < 300:
                rand = self.fisher_id + 1
                if rand == 1:
                    self.pumping(count)
                if rand == 2:
                    self.reeling(count)
            if count > 400:
                self.current_state = 1
            self.send_message(f'count {count}')
        self.current_state = 0

    def test_run(self):
        queue_count = 0
        if not self.start_fishing(queue_count):
            self.stop_fishing()
            self.send_message('ERROR start_fishing()')
            return

        while not self.exit.is_set():  # or keyboard was pressed and not disconnected

            if not self.actions_while_fishing(queue_count):
                self.stop_fishing()
                self.send_message('ERROR actions_while_fishing()')
                return

            if not self.actions_between_fishing_rod_casts(queue_count):
                self.stop_fishing()
                self.send_message('ERROR actions_between_fishing_rod_casts()')
                return

        if not self.stop_fishing():
            self.send_message('ERROR stop_fishing()')
            return

    def start_fishing(self, count):
        self.current_state = 0
        delay = 2
        delay_correction = delay + 3 / self.number_of_fishers
        self.send_message(f'will start fishing in ........ {delay_correction} sec')
        time.sleep(delay_correction)
        self.send_message(f'starts fishing\n')
        self.attempt_counter = 0

        if not self.fishing_window.init_search():
            self.stop_fishing()

        if not self.trial_rod_cast(count):
            self.stop_fishing()

        # if not self.buff_is_active():
        #     self.rebuff(count)

        # if not self.overweight_baits_soski_correction(count):
        #     pass

    def actions_while_fishing(self, count):
        pass

    def actions_between_fishing_rod_casts(self, count):
        pass

    def stop_fishing(self):
        self.send_message(f'has finished fishing\n')
        self.paused = True
        self.exit.set()
        self.current_state = 9
        self.paused = False

    def get_status(self):
        return self.current_state

    def trial_rod_cast(self, count):
        self.q.new_task(count, 'mouse',
                        [self.fishing_window.get_object('fishing', False), True, 'LEFT', False, False, False],
                        self.fishing_window)

        temp_timer = time.time()
        searching_time = 10
        while (not self.fishing_window.get_object('fishing_window')) and (time.time() - temp_timer < searching_time):
            continue
        else:
            self.stop_fishing()

        self.fishing_window.start_accurate()

    def overweight_baits_soski_correction(self, count):
        return True

    def buff_is_active(self):
        if time.time() - self.buff_time < 30:
            return False
        else:
            return True

    def fishing_window_is_active(self):
        if self.fishing_window.fishing_window():
            return True
        else:
            return False

    def got_the_bait(self):
        pass

    def baits_clicked(self, count):
        if time.time() - self.buff_time < 30:
            return False
        else:
            return True

    def pause_thread(self, delay):
        # self.send_message(f'PAUSED for {delay} seconds')
        time.sleep(delay)

    def pumping(self, count):
        # self.q.new_task([(100, 100)], self.fishing_window.hwnd)
        self.q.new_task(count, 'mouse',
                        [self.fishing_window.get_object('fishing', False), True, 'LEFT', False, False, False],
                        self.fishing_window)
        # self.q.new_task(count, 'mouse', [[(100, 100)], True, 'LEFT', False, False, False], self.fishing_window)

    def reeling(self, count):
        # self.q.new_task([(500, 500)], self.fishing_window.hwnd)
        self.q.new_task(count, 'mouse',
                        [self.fishing_window.get_object('reeling', False), True, 'LEFT', False, False, False],
                        self.fishing_window)
        # self.q.new_task(count, 'mouse', [[(500, 500)], True, 'LEFT', False, False, False], self.fishing_window)

    def rebuff(self, count):
        self.q.new_task(count, 'mouse',
                        [self.fishing_window.get_object('buff', False), True, 'LEFT', False, False, False],
                        self.fishing_window)
        self.buff_time = time.time()
        self.pause_thread(1.5)

    def turn_on_soski(self, count):
        self.q.new_task(count, 'mouse',
                        [self.fishing_window.get_object('soski', True), True, 'RIGHT', False, False, False],
                        self.fishing_window)

    def choose_night_bait(self, count):
        self.q.new_task(count, 'mouse',
                        [self.fishing_window.get_object('luminous', False), True, 'RIGHT', False, False, False],
                        self.fishing_window)
        self.current_baits = 'n_baits'
        self.pause_thread(0.7)

    def choose_day_bait(self, count):
        self.q.new_task(count, 'mouse',
                        [self.fishing_window.get_object('colored', False), True, 'RIGHT', False, False, False],
                        self.fishing_window)
        self.current_baits = 'd_baits'
        self.pause_thread(0.7)

    # def equipment_bag(self, count):
    #     self.q.new_task(count, 'mouse', [self.fishing_window.get_object('equipment_bag', False), True, 'RIGHT', False, False, False], self.fishing_window)

    def send_mail(self, count):
        pass

    def send_trade(self, count):
        pass

    def wait_for_trade(self, count):
        pass

    def receive_mail(self, count):
        pass

    def change_bait(self, count):
        pass

    def map(self, count):
        self.q.new_task(count, 'mouse',
                        [self.fishing_window.get_object('map_button', False), True, 'RIGHT', False, False, False],
                        self.fishing_window)
