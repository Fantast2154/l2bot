import threading
import random
from threading import Lock
import time
import win32gui
import cv2


class Fisher(threading.Thread):

    fishing_window = None
    fisher_id = None
    number_of_fishers = None
    current_state = None
    stopped = None
    q = None

    last_buff_time = time.time()

    def __init__(self, fishing_window, fisher_id, number_of_fishers, q):
        self.send_message(f'TEST fisher {fisher_id} created')
        threading.Thread.__init__(self)
        self.exit = threading.Event()
        self.fishing_window = fishing_window
        self.fisher_id = fisher_id
        self.number_of_fishers = number_of_fishers
        self.current_state = 0
        self.q = q

    def __del__(self):
        self.send_message(f"TEST fisher {self.fisher_id} destroyed")

    @classmethod
    def send_message(cls, message):
        print(message)

    def test_action(self, count):
        self.q.new_task(count, self.fishing_window)

    def run(self):
        count = -1
        self.start_fishing()
        self.fishing_window.init_search()
        while not self.exit.is_set(): # or keyboard was pressed and not disconnected
            count += 1

            time.sleep(0.1)
            print('ACTION', count)
            self.fishing_window.update_screenshot()
            if count < 300:
                rand = self.fisher_id + 1
                if rand == 1:
                    self.pumping(count)
                if rand == 2:
                    self.reeling(count)
            if count > 400:
                self.current_state = 1
                return

        self.current_state = 2

    # def test_run(self):
    #     if connection_is_lost:
    #         pass
    #
    #     if not self.fishing_window.find('fishing_window'):
    #         if not self.buff_is_active():
    #             self.rebuff()




    def get_status(self):
        return self.current_state


    def overweight_baits_soski_correction(f_try_count, m_send_counter, m_receive_counter):
        pass

    def start_fishing(self):
        delay = 3
        print(f'The fisher {self.fisher_id} will start in ........ {delay} sec')
        time.sleep(delay)
        self.send_message(f'TEST fisher {self.fisher_id} starts fishing\n')
        self.stopped = False

        # before start fishing
        #click buff
        self.last_buff_time = time.time()

    def stop_fishing(self):
        # before stop fishing

        self.send_message(f'TEST fisher {self.fisher_id} has finished fishing\n')
        self.exit.set()

    def buff_is_active(self):
        if time.time() - self.last_buff_time < 30:
            return False
        else:
            return True

    def pumping(self, count):
        # self.q.new_task([(100, 100)], self.fishing_window.hwnd)
        self.q.new_task(count, 'mouse', [[(100, 100)], True, 'LEFT', False, False, False], self.fishing_window)

    def reeling(self, count):
        # self.q.new_task([(500, 500)], self.fishing_window.hwnd)
        self.q.new_task(count, 'mouse', [[(500, 500)], True, 'LEFT', False, False, False], self.fishing_window)

    # def rebuff(self):
    #     self.q.new_task(count, 'mouse', self.fishing_window, True, 'LEFT', False, False, False], self.fishing_window)

    def turn_on_soski(self):
        pass

    def choose_nigtly_bait(self):
        pass

    def choose_daily_bait(self):
        pass

    def send_mail(self):
        pass

    def send_trade(self):
        pass

    def receive_trade(self):
        pass

    def receive_mail(self):
        pass

    def change_bait(self):
        pass
