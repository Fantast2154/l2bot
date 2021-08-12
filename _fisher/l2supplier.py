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
        manager = Manager()
        self.supplier_window = supplier_window
        self.supplier_id = supplier_id
        self.number_of_suppliers = number_of_suppliers

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
        self.supply_request = manager.list()
        self.supply_request.append(False)
        self.supply_request_proceed = manager.list()
        self.supply_request_proceed.append(False)
        self.trading_is_allowed = manager.list()
        self.trading_is_allowed.append(False)
        self.requested_items_to_supply = manager.list()


        # self.supply_request[0] = manager.list()
        # self.supply_request[0].append(False)
        # self.trade_request = manager.list()
        # self.trade_request.append(False)

        # self.supply_items = manager.list()
        # self.supply_items = [0]*3

        # send/receive counters
        self.attempt_counter = 0
        self.supplied_clients = []
        # self.attempt_counter = manager.list()
        # self.attempt_counter.append(0)

        # connection params
        self.bot_is_connected = True
        self.it_is_almost_server_restart_time = False
        self.exit_is_set = False
        self.paused = None  # force pause the fisher

    def supply(self, machine_id, bot_id, goods):
        print('goods', goods)
        self.supply_request[0] = True
        self.current_state[0] = 'busy'
        self.supplied_clients.append(bot_id)
        self.requested_items_to_supply.append(goods['dbaits'])
        self.requested_items_to_supply.append(goods['nbaits'])
        self.requested_items_to_supply.append(goods['soski'])
        print('111111111', self.requested_items_to_supply)

    def __del__(self):
        self.send_message(f"destroyed")

    def send_message(self, message):
        try:
            temp = '\t' * 10 * self.supplier_id + 'Supplier ' + f'{self.supplier_id}: {message}'
            print(temp)
        except:
            pass

    def pause_supplier(self, delay):
        if delay is None:
            pass
        else:
            self.pause_thread(delay)

    def run(self):

        if not self.start_supplier():
            self.stop_supplier()
            self.send_message('ERROR start_supplier()')
        self.current_state[0] = 'available'
        while not self.exit_is_set:

            self.wait_for_supply_request()

            if not self.wait_for_trade():
                self.send_message('error exchange menu')
                continue
            if not self.supply_goods():
                continue

        if not self.stop_supplier():
            self.send_message('ERROR stop_supplier()')

    def wait_for_supply_request(self):
        while not self.supply_request[0]:
            self.pause_thread(0.1)
        self.send_message('SUPPLY REQUEST RECEVIED')

    def wait_for_trade(self):
        self.send_message('waiting for trade')
        waiting_time = 180
        temp_timer = time.time()
        while time.time() - temp_timer < waiting_time:
            self.pause_thread(0.1)
            temp = self.supplier_window.is_confirm_button()
            if temp:
                print('TRADE WAS FOUND')


                waiting_time2 = 15
                temp_timer2 = time.time()
                while time.time() - temp_timer2 < waiting_time2 and not self.supplier_window.is_exchange_menu():
                    self.click(temp)
                    self.pause_thread(2)

                self.pause_thread(0.5)
                self.supply_request[0] = False
                return True

        return False

    def supply_goods(self):
        self.send_message('chlen BAGANCA')
        if not self.search_loop_without_click(self.supplier_window.is_exchange_menu, 15):
            return False



        self.pause_thread(0.7)
        request_soski = self.requested_items_to_supply.pop(2)
        request_nbaits = self.requested_items_to_supply.pop(1)
        request_dbaits = self.requested_items_to_supply.pop(0)
        print('dbaits', request_dbaits)
        print('nbaits', request_nbaits)
        print('soski', request_soski)

        self.send_message('dbaits')
        self.send_message(f'{request_dbaits}')
        soski_pos = self.supplier_window.is_soski()
        if not soski_pos:
            return False

        dbaits_pos = self.supplier_window.is_baits()
        if not dbaits_pos:
            return False

        ok_button_pos = self.supplier_window.is_ok_button()
        if not ok_button_pos:
            return False

        pyperclip.copy(request_soski)
        while not self.supplier_window.is_input_field() or not self.supplier_window.is_confirm_button():
            print('HERE!SUKI')

            self.trade_item(soski_pos)
            self.pause_thread(2)

        input_field_pos = self.supplier_window.is_input_field()
        if not input_field_pos:
            return False
        print('input_field_pos')
        confirm_button_pos = self.supplier_window.is_confirm_button()
        if not confirm_button_pos:
            return False
        print('confirm_button_pos')
        self.pause_thread(0.7)
        self.enter_number(input_field_pos)
        self.pause_thread(0.7)
        self.click(confirm_button_pos)
        self.pause_thread(0.7)

        pyperclip.copy(request_dbaits)
        if len(dbaits_pos) > 1:
            self.trade_item(dbaits_pos[0])
        else:
            self.trade_item(dbaits_pos)
        self.pause_thread(0.7)
        self.enter_number(input_field_pos)
        self.pause_thread(0.7)
        self.click(confirm_button_pos)
        self.pause_thread(0.7)
        self.click(ok_button_pos)
        self.pause_thread(0.7)

        pyperclip.copy(0)

        self.supply_request[0] = False
        self.update_current_attempt()
        self.current_state[0] = 'available'
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
        return self.current_state[0]

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
        self.attempt_counter += 1
        # temp = '\t' * 10 * self.supplier_id
        # print(f'{temp}Fisher {self.supplier_id}: Attempt # {self.attempt_counter}')

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
