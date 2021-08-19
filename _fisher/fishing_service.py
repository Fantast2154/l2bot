import time

import numpy

from _fisher.l2fisher import Fisher
from _fisher.l2supplier import Supplier
from _fisher.l2buffer import Buffer
from system.action_queue import *
import threading
from _fisher.fishing_window_fisher import FishingWindow
from _fisher.fishing_window_buffer import *
from _fisher.fishing_window_supplier import *
from multiprocessing import Process, Value, Manager
from system.action_queue import ActionQueue
from system.botnet import Client
import random
import math
from threading import Lock


# self.send_message(f'{self!r}')

class FishingService:
    fishers = []
    suppliers = []
    buffers = []
    windows = []
    fishing_windows = []
    supplier_windows = []
    buffer_windows = []
    teleporter_windows = []

    process_fishers = []
    process_buffer = []
    process_supplier = []
    raised_error = False
    fishing_service_client = {}
    sg_gui = None

    def __init__(self, windows, user_input, q):
        self.machine_id = random.randint(0, 10000000)
        # super().__init__(self.machine_id)  # ИНИЦИАЛИЗИРУЕМ РОДИТЕЛЬСКИЙ КЛАСС Client И ПРИСОЕДИНЯЕМСЯ К СЕРВАЧКУ
        manager = Manager()
        # self.fishing_service_client = Client(self.machine_id)
        self.exit_is_set = False
        self.windows = windows
        self.window_fishers = user_input[0]
        self.window_buffers = user_input[1]
        self.window_suppliers = user_input[2]
        self.window_teleporters = user_input[3]

        self.number_of_fishers = len(user_input[0])
        self.number_of_buffers = len(user_input[1])
        self.number_of_suppliers = len(user_input[2])
        self.number_of_teleporters = len(user_input[3])

        self.fishers = []
        self.buffers = []
        self.suppliers = []
        self.teleporters = []
        # self.process_fishers = list(range(self.number_of_fishers))
        self.process_suppliers = list(range(self.number_of_suppliers))
        self.process_buffers = list(range(self.number_of_buffers))

        self.fishers_request = ''
        self.suppliers_request = ''
        self.teleporters_request = ''
        self.buffers_request = ''

        self.fishers_items = {}
        self.suppliers_items = {}
        self.teleporters_items = {}
        self.buffers_items = {}

        self.any_supp_is_available = False

        self.message = {}
        self.none_command = [-1, -2, '', -3, '', 0, '']
        self.command = [-1, -2, '', -3, '', 0, '']
        self.previous_command_id = -1

        self.data_to_transmit = manager.list()
        self.data_to_receive = manager.list()

        self.data_to_transmit.append(0)
        self.data_to_receive.append(0)

        self.has_supplier = False

        self.fishing_service_client = Client(self.machine_id, self.data_to_transmit, self.data_to_receive)

        if self.number_of_fishers < 1 or self.number_of_fishers > 3:
            print('FISHING SERVICE ERROR')
        # return super(FishingService, cls).__new__(cls)
        if self.number_of_suppliers != 0:
            print('self.has_supplier?', self.has_supplier)
            self.has_supplier = True
            self.queue_list = []
        else:
            self.has_supplier = False

        self.send_message(f'created')
        # self.exit = threading.Event()

        q.activate_l2windows(self.windows)

        for fisher_id in range(self.number_of_fishers):
            # print('fisher_id', fisher_id)
            # window_fishers
            win_capture = self.window_fishers[fisher_id].wincap
            window_name = self.window_fishers[fisher_id].window_name
            hwnd = self.window_fishers[fisher_id].hwnd
            screenshot = self.window_fishers[fisher_id].screenshot
            temp_fishing_window = FishingWindow(fisher_id, win_capture, window_name, hwnd, screenshot)
            temp_fishing_window.window_id = self.window_fishers[fisher_id].window_id
            self.fishing_windows.append(temp_fishing_window)

            # fishers
            temp_fisher = Fisher(temp_fishing_window, fisher_id, self.number_of_fishers, q)
            self.fishers.append(temp_fisher)

        # for buffer_id in range(self.number_of_buffers):
        #     pass
        # windows
        # win_capture = windows[buffer_id].wincap
        # window_name = windows[buffer_id].window_name
        # hwnd = windows[buffer_id].hwnd
        # screenshot = windows[buffer_id].screenshot
        # temp_buffer_window = FishingWindow(buffer_id, win_capture, window_name, hwnd, screenshot)
        # self.fishing_windows.append(temp_buffer_window)

        # buffers
        # temp_buffer = Buffer(temp_buffer_window, buffer_id, self.number_of_buffers, q)
        # temp_buffer_process = Process(target=temp_buffer.run)
        # temp_buffer_process.start()
        # temp_buffer.start()
        # self.process_buffer.append(temp_buffer_process)
        # self.buffers.append(temp_buffer)

        for buffer_id in range(self.number_of_buffers):
            win_capture = self.window_buffers[buffer_id].wincap
            window_name = self.window_buffers[buffer_id].window_name
            hwnd = self.window_buffers[buffer_id].hwnd
            screenshot = self.window_buffers[buffer_id].screenshot
            temp_buffer_window = FishingBufferWindow(buffer_id, win_capture, window_name, hwnd, screenshot)
            temp_buffer_window.window_id = self.window_buffers[buffer_id].window_id
            self.buffer_windows.append(temp_buffer_window)

            temp_buffer = Buffer(temp_buffer_window, buffer_id, self.number_of_buffers, q)
            self.buffers.append(temp_buffer)

        for supplier_id in range(self.number_of_suppliers):
            win_capture = self.window_suppliers[supplier_id].wincap
            window_name = self.window_suppliers[supplier_id].window_name
            hwnd = self.window_suppliers[supplier_id].hwnd
            screenshot = self.window_suppliers[supplier_id].screenshot
            temp_supplier_window = FishingSupplierWindow(supplier_id, win_capture, window_name, hwnd, screenshot)
            temp_supplier_window.window_id = self.window_suppliers[supplier_id].window_id
            self.supplier_windows.append(temp_supplier_window)

            temp_supplier = Supplier(temp_supplier_window, supplier_id, self.number_of_suppliers, q)
            self.suppliers.append(temp_supplier)

        # wincap
        self.win_capture = self.windows[0].wincap

        self.q = q

        self.offset_x = 0
        self.offset_y = 0

        self.start_fishers()
        self.start_buffers()
        self.start_suppliers()

    def __del__(self):
        self.send_message("destroyed")

        del self

    @classmethod
    def send_message(cls, message):
        temp = 'FishingService: ' + message
        print(temp)

    def start_fishers(self, fisher_id=None):
        time.sleep(1)
        if fisher_id is None:
            for fisher in self.fishers:
                temp_fisher_process = Process(target=fisher.start_fishing)
                self.process_fishers.append(temp_fisher_process)
                # self.process_fishers[fisher.fisher_id].start()
                # self.process_fishers[fisher.fisher_id] = None
                temp_fisher_process.start()
        # else:
        #     if fisher_id < len(self.process_fishers):
        #         temp_fisher_process = Process(target=self.fishers[fisher_id].start_fishing)
        #         self.process_fishers[fisher_id] = temp_fisher_process
        #         # self.process_fishers[fisher_id].start()
        #         # self.process_fishers[fisher_id] = None
        #         temp_fisher_process.start()

    def stop_fishers(self, fisher_id=None):
        self.send_message(f'STOP FISHING EVENT')
        if fisher_id is None:
            for fisher in self.fishers:
                fisher.stop_fisher()
                self.process_fishers[fisher.fisher_id].join()
        #
        # else:
        #     if fisher_id < len(self.process_fishers):
        #         self.fishers[fisher_id].stop_fishing()
        # self.process_fishers[fisher_id].terminate()

    def pause_fishers(self, fisher_id=None, delay=None, except_param=False):
        if fisher_id is None:
            if delay is None:
                self.send_message(f'pause permanently for all fishers has been registered')
            else:
                self.send_message(f'pause {delay} sec for all fishers has been registered')
            for fisher in self.fishers:
                fisher.paused[0] = delay
        else:
            if except_param:
                if delay is None:
                    self.send_message(
                        f'pause permanently for all fishers, EXCEPT fisher_{fisher_id} has been registered')
                else:
                    self.send_message(
                        f'pause {delay} sec for all fishers, EXCEPT fisher_{fisher_id} has been registered')

                for fisher in self.fishers:
                    if fisher.fisher_id == fisher_id:
                        continue
                    fisher.paused[0] = delay
            if fisher_id < self.number_of_fishers:
                if delay is None:
                    self.send_message(
                        f'pause permanently for all fishers, EXCEPT fisher_{fisher_id} has been registered')
                else:
                    self.send_message(
                        f'pause {delay} sec for all fishers, EXCEPT fisher_{fisher_id} has been registered')
                self.fishers[fisher_id].paused[0] = delay

    def resume_fishers(self):
        self.send_message(f'resume fishers has been registered')
        for fisher in self.fishers:
            fisher.paused[0] = 0

    def start_suppliers(self, supplier_id=None):
        time.sleep(1)
        if len(self.suppliers) == 0:
            return
        self.send_message(f'start_suppliers')
        if supplier_id is None:
            for supplier in self.suppliers:
                temp_supplier_process = Process(target=supplier.run)
                self.process_suppliers[supplier.supplier_id] = temp_supplier_process
                self.process_suppliers[supplier.supplier_id].start()
                self.process_suppliers[supplier.supplier_id] = None
                # temp_supplier_process.start()
        else:
            if supplier_id < len(self.process_suppliers):
                temp_supplier_process = Process(target=self.suppliers[supplier_id].run)
                self.process_suppliers[supplier_id] = temp_supplier_process
                self.process_suppliers[supplier_id].start()
                self.process_suppliers[supplier_id] = None

    def start_buffers(self, buffer_id=None):
        time.sleep(1)
        if len(self.buffers) == 0:
            return
        self.send_message(f'start_buffers')
        if buffer_id is None:
            for buffer in self.buffers:
                temp_buffer_process = Process(target=buffer.run)
                self.process_buffers[buffer.buffer_id] = temp_buffer_process
                self.process_buffers[buffer.buffer_id].start()
                self.process_buffers[buffer.buffer_id] = None
                # temp_buffer_process.start()
        else:
            if buffer_id < len(self.process_buffers):
                temp_buffer_process = Process(target=self.buffers[buffer_id].run)
                self.process_buffers[buffer_id] = temp_buffer_process
                self.process_buffers[buffer_id].start()
                self.process_buffers[buffer_id] = None

    # def stop_suppliers(self, supplier_id=None):
    #     self.send_message(f'stop_suppliers)
    #     if supplier_id is None:
    #         for supplier in self.suppliers:
    #             supplier.stop_fishing()
    #             self.process_suppliers[supplier.supplier_id].terminate()
    #
    #     else:
    #         if supplier_id < len(self.process_suppliers):
    #             self.suppliers[supplier_id].stop_fishing()
    #             self.process_suppliers[supplier_id].terminate()

    def antiphase_fishing(self, param='off'):
        if param == 'off':
            return
        elif param == 'on':
            timing_list = []
            for fisher in self.fishers:
                if fisher.press_fishing_timer[0] == 0:
                    timer = 0
                else:
                    timer = time.time() - fisher.press_fishing_timer[0]

                if 40 > timer >= 0:
                    timing_list.append(timer)

            if not timing_list or len(timing_list) < 2:
                return

            for i, timing_val in enumerate(timing_list):
                if i == 0:
                    continue

                temp = abs(timing_val - timing_list[i - 1])
                difference = 12
                if temp < difference:
                    if self.fishers[i].paused[0] == 0:
                        self.pause_fishers(i, round(difference - temp))
                    # if timing_val > timing_list[i-1]:
                    #     if self.fishers[i-1].paused[0] == 0:
                    #         self.pause_fishers(i-1, round(difference - temp))
                    # else:
                    #     if self.fishers[i].paused[0] == 0:
                    #         self.pause_fishers(i, round(difference - temp))

    def update_to_server(self):
        # print('update_to_server')
        number = {'number': {
            'fishers': self.number_of_fishers,
            'suppliers': self.number_of_suppliers,
            'teleporters': self.number_of_teleporters,
            'buffers': self.number_of_buffers
        }}

        fisher_dict = {}
        supplier_dict = {}
        teleporter_dict = {}
        buffer_dict = {}

        for fisher in self.fishers:
            fisher_dict.update({fisher.fisher_id: fisher.current_state[0]})
            if fisher.fishers_request[0] == 'requests supplying':
                print("fisher.fishers_request[0] == 'requests supplying'!!!!!!")
                self.fishers_request = 'requests supplying'
                self.fishers_items.update({fisher.fisher_id: fisher.fishers_requested_supps[0]})
            else:
                self.fishers_request = ''

        for supplier in self.suppliers:
            supplier_dict.update({supplier.supplier_id: supplier.current_state[0]})

        for teleporter in self.teleporters:
            teleporter_dict.update({teleporter.teleporter_id: teleporter.current_state[0]})

        for buffer in self.buffers:
            buffer_dict.update({buffer.buffer_id: buffer.current_state[0]})

        status = {'status': {
            'fishers': fisher_dict,
            'suppliers': supplier_dict,
            'teleporters': teleporter_dict,
            'buffers': buffer_dict
        }}

        request = {'request': {
            'fishers': self.fishers_request,
            'suppliers': self.suppliers_request,
            'teleporters': self.teleporters_request,
            'buffers': self.buffers_request
        }}

        supplies = {'supplies': {
            'fishers': self.fishers_items,
            # {fisher_id: dict} -> {fisher_id: {'d_baits': a, 'n_baits': b, 'soski': c}}
            'suppliers': self.suppliers_items,
            'teleporters': self.teleporters_items,
            'buffers': self.buffers_items
        }}

        command = {'command': self.command}
        # [получатель - целое число,
        # уникальный номер команды - целое число,
        # 'тип бота' - строка,
        # номер бота - целое число,
        # 'команда' - строка]

        data = {}

        data.update(number)
        data.update(status)
        data.update(request)
        data.update(supplies)
        data.update(command)

        self.data_to_transmit[0] = data
        self.fishing_service_client.client_send()
        self.command = self.none_command
        # self.data_to_receive.append(0)

        # x = fishing_service_client
        # print('x', x)
        # x.client_send(data)
        if self.fishers_request:
            print('////////////////////////////////////FISHING SERVICE', self.fishers_request)

    def start_supply(self, machine_id, fishers_and_items):
        exit_ = False
        self.fishers_request = ''
        while not exit_:
            for supp in self.suppliers:
                if supp.current_state[0] == 'available':
                    for fisher_id, supps in fishers_and_items.copy().items():
                        # supps = {'d_baits': a, 'n_baits': b, 'soski': c}
                        self.send_command(machine_id, 'fisher', fisher_id, 'allow_to_trade')
                        print('COMMAND WAS SENT')
                        supp.supply(machine_id, fisher_id, supps)
                    exit_ = True
                else:
                    continue

    def offline_supply(self):
        for fisher in self.fishers:
            if fisher.fishers_request[0] == 'requests supplying':
                print("fisher.fishers_request[0] == 'requests supplying'!!!!!!")
                self.fishers_request = 'requests supplying'
                self.fishers_items.update({fisher.fisher_id: fisher.fishers_requested_supps[0]})
            else:
                self.fishers_request = ''
        if self.fishers_request:
            self.start_supply(self.machine_id, self.fishers_items)

    def offline_requests(self):
        while not self.exit_is_set:
            time.sleep(0.1)
            if self.has_supplier:
                self.offline_supply()

    def command_process(self, sender, data: dict):
        command_sentence = data['command']
        if command_sentence:
            recipient = command_sentence[0]
            current_command_id = command_sentence[1]
            if recipient == self.machine_id and current_command_id != self.previous_command_id:
                if not command_sentence[5]:
                    bot = command_sentence[2]
                    bot_id = command_sentence[3]
                    what_to_do = command_sentence[4]

                    s = 'self.' + bot + 's' + f'[{bot_id}]' + f'.{what_to_do}()'
                    eval(s)
                    self.previous_command_id = current_command_id
                else:
                    s_ = command_sentence[6]
                    for _ in range(3):
                        time.sleep(1)
                        print('ВНИМАНИЕ! ПОЛУЧЕНА КОМАНДА ВЫСШЕГО ПРИОРИТЕТА', s_)
                    eval(s_)

    def send_command(self, recipient, bot, bot_id, what_to_do):
        r = random.randint(0, 100000000)
        self.command = [recipient, r, bot, bot_id, what_to_do]

    def process_server_data(self):
        print('process_server_data')

        # {уникальный ID машины-отправителя: [сообщение1, сообщение2, ...]} - вид отправляемого сообщения сообщение1
        # имеет вид {fisher_id: dict} -> {fisher_id: {'d_baits': a, 'n_baits': b, 'soski': c}}, где a,
        # b и c - количество дневных наживок, ночных наживок и сосок соответственно

        who_requests_supplying = {}
        anyone_is_requesting = False
        while not self.exit_is_set:
            self.fishing_service_client.client_receive_message()
            self.message = self.data_to_receive[0]
            # print('fishing service', self.message)

            if self.message:
                for sender_id, data_ in self.message.items():
                    self.command_process(sender_id, data_)
                    # print('sender_id - is me?', sender_id == self.machine_id)
                    if sender_id != self.machine_id and self.has_supplier:
                        if data_['request']['fishers'] == 'requests supplying':
                            who_requests_supplying[sender_id] = data_['supplies']['fishers']
                            anyone_is_requesting = True
                            print('anyone_is_requesting? not me - YES!!!')
                        else:
                            pass
                    elif sender_id == self.machine_id and self.has_supplier:
                        # print(data_['request'])
                        if data_['request']['fishers'] == 'requests supplying':
                            who_requests_supplying[sender_id] = data_['supplies']['fishers']
                            anyone_is_requesting = True
                            print('anyone_is_requesting? me - YES!!!')
                    else:
                        pass

                    if not self.any_supp_is_available:
                        for supp_status in data_['status']['suppliers'].values():
                            if supp_status == 'available':
                                self.any_supp_is_available = True

            # print('self.has_supplier and anyone_is_requesting', self.has_supplier, anyone_is_requesting)
            if self.has_supplier and anyone_is_requesting:
                print('who', who_requests_supplying)
                for sender_id, fishers_data in who_requests_supplying.items():
                    self.start_supply(sender_id, fishers_data)
                    print('sender_id fishers_data and who_requests_supplying')
                    print(sender_id)
                    print(fishers_data)

                who_requests_supplying.clear()
                anyone_is_requesting = False

            self.any_supp_is_available = False

    def run(self):
        flag = False
        timer_fishing_service_start = time.time()
        self.server_update_start()
        while not self.exit_is_set:
            # if time.time() - timer_fishing_service_start > self.number_of_fishers * 9:
            #     self.antiphase_fishing('on')
            time.sleep(1)

    def stop(self):
        self.exit_is_set = True
        self.stop_fishers()

        closing_time = 6
        timer = time.time()
        counter = 0
        while time.time() - timer < closing_time:
            counter += 1
            self.send_message(f'thread stops in ..... {closing_time - counter}')
            time.sleep(1)

        self.send_message(f'destroyed')

        # del self.fishers
        # del self.fishing_windows

    # def update_fishers_attempt(self, id, attempt):
    #     temp = f'fisher_{id}'
    #     print(attempt)
    #     global sg_gui
    #     sg_gui[temp].update(f'{attempt}')

    def up_to_serv(self):
        print('up')
        while not self.exit_is_set:
            self.update_to_server()
            time.sleep(0.5)

    def proc_serv_dat(self):
        print('proc')
        self.process_server_data()

    def server_update(self):
        # fishing_service_client = Client(self.machine_id)
        # t1 = Thread(target=self.up_to_serv, args=(fishing_service_client,))
        # t2 = Thread(target=self.proc_serv_dat, args=(fishing_service_client,))
        # t1.start()
        # t2.start()
        pass

    def server_update_start(self):
        # self.data_to_transmit.append(0)
        # self.data_to_receive.append(0)
        if self.fishing_service_client.is_connected():
            print('IS CONNECTED')
            server_update_process1 = Process(target=self.up_to_serv)
            server_update_process1.start()
            server_update_process2 = Process(target=self.proc_serv_dat)
            server_update_process2.start()

        else:
            print('NO CONNECTION')
            server_update_process3 = Process(target=self.offline_requests)
            server_update_process3.start()
