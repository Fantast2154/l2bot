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
from threading import Lock


# self.send_message(f'{self!r}')

class FishingService(Client):
    fishers = []
    suppliers = []
    buffers = []
    windows = []
    fishing_windows = []
    process_fishers = []
    process_buffer = []
    process_supplier = []
    raised_error = False
    fishing_service_client = {}
    sg_gui = None

    def __init__(self, window_fishers, window_buffers, window_suppliers, window_teleporters, q):
        manager = Manager()
        # self.fishers = manager.list()
        for f in window_fishers:
            self.windows.append(f)
        for b in window_buffers:
            self.windows.append(b)
        for s in window_suppliers:
            self.windows.append(s)
        for t in window_teleporters:
            self.windows.append(t)
        self.machine_id = random.randint(0, 10000000)
        super().__init__(self.machine_id)  # ИНИЦИАЛИЗИРУЕМ РОДИТЕЛЬСКИЙ КЛАСС Client И ПРИСОЕДИНЯЕМСЯ К СЕРВАЧКУ
        #     # warning
        #     return None
        number_of_fishers = len(window_fishers)
        number_of_buffers = len(window_buffers)
        number_of_suppliers = len(window_suppliers)
        number_of_teleporters = len(window_teleporters)

        self.number_of_fishers_ = len(window_fishers)
        self.number_of_buffers_ = len(window_buffers)
        self.number_of_suppliers_ = len(window_suppliers)
        self.number_of_teleporters_ = len(window_teleporters)

        self.fishers = []
        self.buffers = []
        self.suppliers = []
        self.teleporters = []
        self.process_fishers = list(range(number_of_fishers))
        self.process_suppliers = list(range(number_of_suppliers))

        self.fishers_request = {}
        self.suppliers_request = {}
        self.teleporters_request = {}
        self.buffers_request = {}

        self.message = {}

        if number_of_fishers < 1 or number_of_fishers > 3:
            print('FISHING SERVICE ERROR')
        # return super(FishingService, cls).__new__(cls)
        if number_of_suppliers != 0:
            self.has_supplier = True
            self.queue_list = []
        else:
            self.has_supplier = False

        self.send_message(f'created')
        # self.exit = threading.Event()

        q.activate_l2windows(self.windows)

        for fisher_id in range(number_of_fishers):
            # print('fisher_id', fisher_id)
            # window_fishers
            win_capture = window_fishers[fisher_id].wincap
            window_name = window_fishers[fisher_id].window_name
            hwnd = window_fishers[fisher_id].hwnd
            screenshot = window_fishers[fisher_id].screenshot
            temp_fishing_window = FishingWindow(fisher_id, win_capture, window_name, hwnd, screenshot)
            temp_fishing_window.window_id = window_fishers[fisher_id].window_id
            self.fishing_windows.append(temp_fishing_window)

            # fishers
            temp_fisher = Fisher(temp_fishing_window, fisher_id, number_of_fishers, q)
            self.fishers.append(temp_fisher)


        # for buffer_id in range(number_of_buffers):
        #     pass
        # windows
        # win_capture = windows[buffer_id].wincap
        # window_name = windows[buffer_id].window_name
        # hwnd = windows[buffer_id].hwnd
        # screenshot = windows[buffer_id].screenshot
        # temp_buffer_window = FishingWindow(buffer_id, win_capture, window_name, hwnd, screenshot)
        # self.fishing_windows.append(temp_buffer_window)

        # buffers
        # temp_buffer = Buffer(temp_buffer_window, buffer_id, number_of_buffers, q)
        # temp_buffer_process = Process(target=temp_buffer.run)
        # temp_buffer_process.start()
        # temp_buffer.start()
        # self.process_buffer.append(temp_buffer_process)
        # self.buffers.append(temp_buffer)

        for supplier_id in range(number_of_suppliers):
            win_capture = window_suppliers[supplier_id].wincap
            window_name = window_suppliers[supplier_id].window_name
            hwnd = window_suppliers[supplier_id].hwnd
            screenshot = window_suppliers[supplier_id].screenshot
            temp_supplier_window = FishingSupplierWindow(supplier_id, win_capture, window_name, hwnd, screenshot)
            temp_supplier_window.window_id = window_suppliers[supplier_id].window_id
            self.fishing_windows.append(temp_supplier_window)

            temp_supplier = Supplier(temp_supplier_window, supplier_id, number_of_suppliers, q)
            self.suppliers.append(temp_supplier)

        # wincap
        self.win_capture = self.windows[0].wincap

        self.number_of_fishers = number_of_fishers
        self.q = q

        self.offset_x = 0
        self.offset_y = 0

        self.start_fishers()
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
        self.send_message(f'start_fishing')
        if fisher_id is None:
            for fisher in self.fishers:
                temp_fisher_process = Process(target=fisher.start_fishing)
                self.process_fishers[fisher.fisher_id] = temp_fisher_process
                temp_fisher_process.start()
        else:
            if fisher_id < len(self.process_fishers):
                temp_fisher_process = Process(target=self.fishers[fisher_id].start_fishing)
                self.process_fishers[fisher_id] = temp_fisher_process
                self.process_fishers[fisher_id].start()

    def stop_fishers(self, fisher_id=None):
        self.send_message(f'stop_fishing')
        if fisher_id is None:
            for fisher in self.fishers:
                fisher.stop_fishing()
                self.process_fishers[fisher.fisher_id].terminate()

        else:
            if fisher_id < len(self.process_fishers):
                self.fishers[fisher_id].stop_fishing()
                self.process_fishers[fisher_id].terminate()

    # def pause_fishers(self, fisher_id=None, delay=None):
    #     self.send_message(f'pause_fishing() calling')
    #     if fisher_id is None:
    #         for fisher in self.fishers:
    #             fisher.stop_fishing()
    #             # self.process_fishers[fisher.fisher_id].terminate()
    #
    #     else:
    #         if fisher_id < len(self.process_fishers):
    #             self.fishers[fisher_id].stop_fishing()
    #             # self.process_fishers[fisher_id].terminate()

    def start_suppliers(self, supplier_id=None):
        time.sleep(1)
        self.send_message(f'start_suppliers')
        if supplier_id is None:
            for supplier in self.suppliers:
                temp_supplier_process = Process(target=supplier.run)
                self.process_suppliers[supplier.supplier_id] = temp_supplier_process
                temp_supplier_process.start()
        else:
            if supplier_id < len(self.process_suppliers):
                temp_supplier_process = Process(target=self.suppliers[supplier_id].run)
                self.process_suppliers[supplier_id] = temp_supplier_process
                self.process_suppliers[supplier_id].start()

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

    def send_to_server(self, status):
        # print('super().is_connected()', super().is_connected())
        if super().is_connected():
            super().client_send(status)  # ШЛЁМ СООБЩЕНИЕ НА СЕРВЕР

    def get_status_from_server(self):
        if super().is_connected():
            return super().client_receive_message()  # ПОЛУЧАЕМ СООБЩЕНИЯ С СЕРВЕРА

    def fisher_response(self, fisher_id, response):
        pass
        # print('fisher_response', response)
        # lock = Lock()
        # if response == 'requests supplying':
        #     lock.acquire()
        #     self.fishers_request[fisher_id] = response
        #     temp_dict = {'dbaits': 0, 'nbaits': 0, 'soski': 0}
        #     for index, key in enumerate(temp_dict):
        #         temp_dict[key] = self.fishers[fisher_id].requested_items_to_supply[index]
        #
        #     resource = temp_dict.copy()
        #     print('++++++++++++++++++++++++++++++++++request_server_for_supplying fisher_id resource', fisher_id,
        #           resource)
        #     self.request_server_for_supplying(fisher_id, resource)
        #     lock.release()
        # self.send_status_to_server(id, response)

        # current_state params
        # 'not fishing'
        # 'fishing'
        # 'busy'
        # 'requests supplying'
        # 'paused'
        # 'error'
        # if response == 'requests supplying':
        #     self.send_message('fisher requests supplying')
        #     if self.has_supplier:
        #         self.fishers[id].supply_request_proceed[0] = True
        #         exit = False
        #         while not exit:
        #             for sup in self.suppliers:
        #                 if sup.current_state[0] == 'available':
        #                     self.fishers[id].current_state[0] = 'busy'
        #                     sup.supply(id, self.fishers[id].requested_items_to_supply)
        #                     time.sleep(0.5)
        #                     self.fishers[id].trading_is_allowed[0] = True
        #                     exit = True
        #                 else:
        #                     continue
        #     else:
        #         # self.request_server_for_supplying(self.fishers[id].fisher_id, self.fishers[id].requested_items_to_supply)
        #         # self.allow_fisher_to_trade(self.fishers[id].fisher_id)
        #         # self.fishers[id].supply_request[0] = False
        #         # self.fishers[id].request_proceed[0] = True
        #         pass

    def request_server_for_supplying(self, fisher_id, dic):
        # print('request_server_for_supplying fisher_id, dic', fisher_id, dic)
        # data_to_send = {fisher_id: dic}
        self.fishers_request = {fisher_id: dic}
        # print('data_to_send', data_to_send)
        # self.send_to_server(data_to_send)

    def start_supply(self, supplies):
        # supplies = supplies[sender_id] = {fisher_id: dic_resource}
        # supplies = {sender_id: {fisher_id: {'d_baits': a, 'n_baits': b, 'soski': c}}}
        print('^^^^^^^^^^^^start_supply^^^^^^^^^^^^^^^^^^^^^^^^')
        exit_ = False
        while not exit_:
            for supp in self.suppliers:
                if supp.current_state[0] == 'available':
                    for sender_id, supps in supplies.copy().items():
                        # supps = {fisher_id: dic_resource}
                        # dic_resource = {'d_baits': a, 'n_baits': b, 'soski': c}
                        for fisher_id, dic_resource in supps.items():
                            supp.supply(sender_id, fisher_id, dic_resource)
                            exit_ = True
                        # del supplies[sender_id]
                else:
                    continue

    # def start_supply(self, supplies):
    #     # supplies = supplies[sender_id] = {fisher_id: dic_resource}
    #     # supplies = {sender_id: {fisher_id: {'d_baits': a, 'n_baits': b, 'soski': c}}}
    #     exit_ = False
    #     while not exit_:
    #         for supp in self.suppliers:
    #             if supp.current_state[0] == 'available':
    #                 for t in q:
    #                     for fisher_ID, resource in t.items():
    #                         self.fishers[fisher_ID].supply_request_proceed[0] = True
    #                         self.fishers[fisher_ID].current_state[0] = 'busy'
    #                         print('fisher_ID', fisher_ID)
    #                         self.fishers[fisher_ID].trading_is_allowed[0] = True
    #                         time.sleep(0.5)
    #                         supp.supply(fisher_ID, resource)
    #                         time.sleep(0.5)
    #                         print('!!!!!!!!!!!!!!!!!!!!!!.trading_is_allowed[0]',
    #                               self.fishers[fisher_ID].trading_is_allowed[0])
    #                         exit_ = True
    #             else:
    #                 continue
    #
    #     print('start_supply q', q)

    def listen_to_server(self):
        amount = {'amount': {
            'fishers': self.number_of_fishers_,
            'suppliers': self.number_of_suppliers_,
            'teleporters': self.number_of_teleporters_,
            'buffers': self.number_of_buffers_
        }}

        status = {'status': {
            'fishers': [{fisher.fisher_id: fisher.current_state[0]} for fisher in self.fishers],
            'suppliers': [{supplier.supplier_id: supplier.current_state[0]} for supplier in self.suppliers],
            'teleporters': [{teleporter.teleporter_id: teleporter.current_state[0]} for teleporter in self.teleporters],
            'buffers': [{buffer.buffer_id: buffer.current_state[0]} for buffer in self.buffers]
        }}

        request = {'request': {
            'fishers': self.fishers_request,
            'suppliers': self.suppliers_request,
            'teleporters': self.teleporters_request,
            'buffers': self.buffers_request
        }}

        data = {}
        data.update(amount)
        data.update(status)
        data.update(request)

        self.send_to_server(data)

    def process_server_data(self):

        # {уникальный ID машины-отправителя: [сообщение1, сообщение2, ...]} - вид отправляемого сообщения сообщение1
        # имеет вид {fisher_id: dict} -> {fisher_id: {'d_baits': a, 'n_baits': b, 'soski': c}}, где a,
        # b и c - количество дневных наживок, ночных наживок и сосок соответственно

        self_proceed = False
        proceed = False
        any_supp_is_available = []
        who_requests_supplying = {}
        supplies = {}
        supplying = False

        while True:
            self.message = self.get_status_from_server()

            if self.message:
                for sender_id, data_ in self.message.items():
                    temp_fishers_ids = []
                    for datum in data_:
                        for fisher_status in datum['status']['fishers']:
                            for fisher_id, status in fisher_status.items():
                                if status == 'requests supplying':
                                    #print('self.message', self.message)
                                    temp_fishers_ids.append(fisher_id)

                        if datum['request']['fishers'].items():
                            #print('ITEMS request fishers', datum['request']['fishers'].items())
                            # dic_resource = {'d_baits': a, 'n_baits': b, 'soski': c}
                            for fisher_id, dic_resource in datum['request']['fishers'].items():
                                supplies[sender_id] = {fisher_id: dic_resource}
                                proceed = True

                        for supp_status in datum['status']['suppliers']:
                            if 'available' in supp_status.values():
                                any_supp_is_available.append(True)
                    if temp_fishers_ids:
                        who_requests_supplying[sender_id] = temp_fishers_ids
                    # print('who_requests_supplying', who_requests_supplying)

                if self.message.get(self.machine_id) is not None:
                    shefer = self.message.get(self.machine_id)
                    self_proceed = True

            if self_proceed:
                # print('self_proceed', self_proceed)
                for data in shefer:
                    # print("data['status']['fishers']", data['status']['fishers'])
                    # print('fishers amount', data['amount']['fishers'])
                    # print('fishers status ', data['status']['fishers'])
                    # print('fishers request', data['request']['fishers'])
                    for fishers_status in data['status']['fishers']:
                        for fisher_id, status in fishers_status.items():
                            if status == 'requests supplying' and numpy.array(any_supp_is_available).any():
                                # print("status", status)
                                temp_dict = {'dbaits': 0, 'nbaits': 0, 'soski': 0}
                                for index, key in enumerate(temp_dict):
                                    temp_dict[key] = self.fishers[fisher_id].requested_items_to_supply[index]

                                resource = temp_dict.copy()
                                # print('++++++++++++++++++++++++++++++++++request_server_for_supplying fisher_id resource', fisher_id, resource)

                                self.request_server_for_supplying(fisher_id, resource)
                                self.fishers[fisher_id].supply_request_proceed[0] = True
                                self.fishers[fisher_id].current_state[0] = 'busy'
                                self.fishers[fisher_id].trading_is_allowed[0] = True

                                print('PARAMETERS ARE CHANGED')
                                self_proceed = False

            if self.has_supplier and proceed:
                # print('!!!!!!!!!!!!!!self.has_supplier and proceed!!!!!!!!!!!!!!!!!!', who_requests_supplying)
                need_to_supply = False
                proceed = False
                # print('(((((((((((((((((((( who_requests_supplying', who_requests_supplying)
                for sender_id, fishers_ids in who_requests_supplying.items():
                    for fisher_index in fishers_ids:
                        # dic_resource = {'d_baits': a, 'n_baits': b, 'soski': c}
                        if supplies[sender_id][fisher_index].values():
                            # print('000000000000000000need_to_supply!!!!')
                            need_to_supply = True


                if need_to_supply:
                    # print('start_supply', supplies)
                    self.start_supply(supplies)
                    who_requests_supplying.clear()

                who_requests_supplying = {}
                any_supp_is_available = []
                supplies = {}

            # if self.has_supplier:
            #     q = []
            #     need_to_supply = False
            #     for sender_id, [msg] in self.message.items():
            #         print('[MSG]', [msg])
            #         fisher_dict = {}
            #         for fisher, supplies in msg.items():
            #             for resource, amount in supplies.items():
            #                 if amount != 0:
            #                     need_to_supply = True
            #                     if fisher_dict.get(fisher) is not None:
            #                         fisher_dict[fisher].update({resource: amount})
            #                     else:
            #                         fisher_dict[fisher] = {resource: amount}
            #             q.append(fisher_dict.copy())
            #         fisher_dict.clear()
            #     if need_to_supply:
            #         print('Q', q)
            #         self.start_supply(q)

    def run(self):
        flag = False
        self.send_message(f'TEST FishingService run_loop() calling')
        # self.connect()  # МОЖНО ПОСТАВИТЬ В НУЖНОЕ МЕСТО МЕТОД ПОДКЛЮЧЕНИЯ К СЕРВЕРУ
        self.server_update_start()
        while True:
            self.process_server_data()

            # for fisher in self.fishers:
            # print('fisher.current_state[0]', fisher.current_state[0])
            # self.fisher_response(fisher.fisher_id, fisher.current_state[0])

            # self.listen_to_server()
            time.sleep(1)

    def stop(cls):
        cls.stop_fishers()
        cls.send_message('thread stops')
        closing_time = 5
        timer = time.time()
        while time.time() - timer < closing_time:
            cls.send_message(f'timer before close ..... {time.time() - timer}')
            time.sleep(1)

        del cls.fishers
        del cls.fishing_windows

    # def update_fishers_attempt(self, id, attempt):
    #     temp = f'fisher_{id}'
    #     print(attempt)
    #     global sg_gui
    #     sg_gui[temp].update(f'{attempt}')

    def server_update(self):
        while True:
            time.sleep(0.2)
            self.listen_to_server()

    def process_server_data_start(self):
        while True:
            time.sleep(0.2)
            self.process_server_data()

    def server_update_start(self):
        t1 = Thread(target=self.server_update, args=())
        # t2 = Thread(target=self.process_server_data_start, args=())
        t1.start()
        # t2.start()
