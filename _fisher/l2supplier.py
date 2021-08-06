import math
import random
import time
from multiprocessing import Manager

import pyperclip

from system.botnet import Client
import win32gui
import cv2


class Supplier:

    def __init__(self, supplier_window, supplier_id, number_of_suppliers, q):
        self.supplier_window = supplier_window
        self.supplier_id = supplier_id
        self.number_of_suppliers = number_of_suppliers

            # ['Ready', 'Waiting for trade', 'Busy', 'Disconnected']
        self.q = q
        self.send_message(f'created')
        manager = Manager()
        self.current_state = manager.list()
        self.current_state.append('Ready')
        self.new_task_temp = manager.list()

        # communication with fisher service

        self.supply_request = manager.list()
        self.supply_request.append(False)
        self.trade_request = manager.list()
        self.trade_request.append(False)

        self.supply_items = manager.list()
        self.supply_items = [0]*3

        # send/receive counters
        self.attempt_counter = manager.list()
        self.attempt_counter.append(0)

        # connection params
        self.bot_is_connected = True
        self.it_is_almost_server_restart_time = False
        self.exit_is_set = False
        self.paused = None # force pause the fisher

    def supply(self, bot_id, list):
        pass

    def __del__(self):
        self.send_message(f"destroyed")

    def send_message(self, message):
        temp = '\t' * 10 * self.supplier_id + 'Supplier ' + f'{self.supplier_id}: {message}'
        print(temp)

    def pause_supplier(self, delay):
        if delay is None:
            pass
        else:
            self.pause_thread(delay)

    def run(self):

        if not self.start_supplier():
            self.stop_supplier()
            self.send_message('ERROR start_supplier()')

        while not self.exit_is_set:
            self.current_state[0] = 'Ready'
            self.wait_for_supply_request()
            self.current_state[0] = 'Waiting for trade'
            if not self.wait_for_trade():
                self.send_message('error exchange menu')
                continue
            if not self.supply_goods():
                continue

        if not self.stop_supplier():
            self.send_message('ERROR stop_supplier()')


    def wait_for_supply_request(self):
        while not self.supply_request[0] and self.exit_is_set:
            self.pause_thread(0.1)

    def wait_for_trade(self):
        waiting_time = 180
        temp = time.time()
        while self.exit_is_set or time.time() - temp < waiting_time:
            self.pause_thread(0.1)
            if self.supplier_window.is_trade_request():
                self.pause_thread(0.5)
                if not self.search_loop_with_click(self.supplier_window.is_exchange_menu, self.click, self.supplier_window.is_ok_button, 15):
                    return True

        return False

    def supply_goods(self):

        if not self.search_loop_without_click(self.supplier_window.is_small_bag, 15):
            return False

        self.pause_thread(0.7)

        soski_pos = self.supplier_window.is_soski()
        if not soski_pos:
            return False

        baits_pos = self.supplier_window.is_baits()
        if not baits_pos:
            return False

        ok_button_pos = self.supplier_window.is_ok_button()
        if not ok_button_pos:
            return False

        pyperclip.copy(self.supply_items[2])
        self.trade_item(soski_pos)
        self.pause_thread(0.7)


        input_field_pos = self.supplier_window.is_input_field()
        if not input_field_pos:
            return False

        confirm_button_pos = self.supplier_window.is_confirm_button()
        if not confirm_button_pos:
            return False

        self.pause_thread(0.7)
        self.enter_number(input_field_pos)
        self.pause_thread(0.7)
        self.click(confirm_button_pos)
        self.pause_thread(0.7)


        pyperclip.copy(self.supply_items[0])
        if len(baits_pos) > 1:
            self.trade_item(baits_pos[0])
        else:
            self.trade_item(baits_pos)
        self.pause_thread(0.7)
        self.enter_number(input_field_pos)
        self.pause_thread(0.7)
        self.click(confirm_button_pos)
        self.pause_thread(0.7)
        self.click(ok_button_pos)
        self.pause_thread(0.7)

        pyperclip.copy(0)
        self.supply_items[2] = 0
        self.supply_items[1] = 0
        self.supply_items[0] = 0

        self.supply_request = False
        self.trade_request = False
        self.supply = False

        return True


    def start_supplier(self):
        return True

    def stop_supplier(self):
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
                        self.supplier_window)

    def click(self, coordinates):
        self.q.new_task('mouse',
                        [coordinates, True, 'LEFT', False, False, False],
                        self.supplier_window)

    def trade_item(self, coordinates):
        self.q.new_task('mouse',
                        [coordinates, True, 'LEFT', False, False, 'double'],
                        self.supplier_window)



    def get_status(self):
        return self.current_state

    def pause_thread(self, delay):
        # self.send_message(f'PAUSED for {delay} seconds')
        time.sleep(delay)

    def equipment_bag(self):
        self.q.new_task('mouse',
                        [self.supplier_window.get_object('equipment_bag', False), True, 'RIGHT', False, False, False],
                        self.supplier_window)

    def record_game_time(self):
        self.send_message('record_game_time')
        # self.game_time = None
        return True

    def update_current_attempt(self):
        self.attempt_counter[0] += 1
        temp = '\t' * 10 * self.supplier_id
        print(f'{temp}Fisher {self.supplier_id}: Attempt # {self.attempt_counter[0]}')

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
                        [self.supplier_window.get_object('map_button', search), True, 'RIGHT', False, False, False],
                        self.supplier_window)

