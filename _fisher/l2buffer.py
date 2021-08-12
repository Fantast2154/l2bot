import math
import random
import time
from multiprocessing import Manager

import pyperclip

from system.botnet import Client
import win32gui
import cv2


class Buffer:

    def __init__(self, buffer_window, buffer_id, number_of_buffers, q):
        manager = Manager()
        self.buffer_window = buffer_window
        self.buffer_id = buffer_id
        self.number_of_buffers = number_of_buffers

        # ['Ready', 'Waiting for trade', 'Busy', 'Disconnected']
        self.q = q
        self.send_message(f'created')

        # communication with fisher service
        self.current_state = manager.list()
        self.current_state.append('available')
        # current_state params
        # 'available'
        # 'busy'
        # 'out of goods'
        # 'paused'
        # 'error'

        self.paused = None  # force pause the fisher

        # self.supply_request[0] = manager.list()
        # self.supply_request[0].append(False)
        # self.trade_request = manager.list()
        # self.trade_request.append(False)

        # self.supply_items = manager.list()
        # self.supply_items = [0]*3

        # send/receive counters
        self.attempt_counter = 0
        # self.attempt_counter = manager.list()
        # self.attempt_counter.append(0)

        # connection params
        self.bot_is_connected = True
        self.it_is_almost_server_restart_time = False
        self.exit_is_set = False
        self.paused = None  # force pause the fisher

    def __del__(self):
        self.send_message(f"destroyed")

    def send_message(self, message):
        temp = '\t' * 10 * self.buffer_id + 'Supplier ' + f'{self.buffer_id}: {message}'
        print(temp)

    def pause_buffer(self, delay):
        if delay is None:
            pass
        else:
            self.pause_thread(delay)

    def run(self):

        if not self.start_buffer():
            self.stop_buffer()
            self.send_message('ERROR start_buffer()')
        self.current_state[0] = 'available'
        while not self.exit_is_set:
            pass
            self.buff()
            self.pause_thread(15)
            # self.wait_for_supply_request()
            #
            # if not self.wait_for_trade():
            #     self.send_message('error exchange menu')
            #     continue
            # if not self.supply_goods():
            #     continue

        if not self.stop_buffer():
            self.send_message('ERROR stop_buffer()')


    def start_buffer(self):
        return True

    def stop_buffer(self):
        self.send_message(f'has finished work\n')
        self.exit_is_set = True

    def search_loop_with_click(self, search_func, task_proc, coordinates, searching_time):
        counter = 0
        time_between_actions = 3
        repeat_times = searching_time // time_between_actions
        temp_timer = time.time()

        while not search_func:

            if time.time() - temp_timer > time_between_actions * counter:
                counter += 1
                task_proc(coordinates)

            if time.time() - temp_timer > searching_time or counter > repeat_times:
                return False

        return True

    def search_loop_without_click(self, condition, searching_time, *args):
        temp_timer = time.time()

        while not condition(*args):
            if time.time() - temp_timer > searching_time:
                return False
        return True

    def enter_number(self, coordinates):
        self.q.new_task('mouse',
                        [coordinates, True, 'LEFT', False, 'insert', False],
                        self.buffer_window)

    def click(self, coordinates):
        self.q.new_task('mouse',
                        [coordinates, True, 'LEFT', False, False, False],
                        self.buffer_window)

    def buff(self):
        self.q.new_task('mouse',
                        [self.buffer_window.get_object('buff_song', False), True, 'LEFT', False, False, False],
                        self.buffer_window)

    def get_status(self):
        return self.current_state[0]

    def pause_thread(self, delay):
        # self.send_message(f'PAUSED for {delay} seconds')
        time.sleep(delay)

    def equipment_bag(self):
        self.q.new_task('mouse',
                        [self.buffer_window.get_object('equipment_bag', False), True, 'RIGHT', False, False, False],
                        self.buffer_window)

    def record_game_time(self):
        self.send_message('record_game_time')
        # self.game_time = None
        return True

    def update_current_attempt(self):
        self.attempt_counter += 1
        # temp = '\t' * 10 * self.buffer_id
        # print(f'{temp}Fisher {self.buffer_id}: Attempt # {self.attempt_counter}')

    def send_mail(self):
        pass

    def receive_mail(self):
        pass

    def send_trade(self):
        pass

    # def wait_for_trade(self):
    #     pass

    def map(self, search=False):
        self.q.new_task('mouse',
                        [self.buffer_window.get_object('map_button', search), True, 'RIGHT', False, False, False],
                        self.buffer_window)
