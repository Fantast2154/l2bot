import time
import threading

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


# self.send_message(f'{self!r}')

class FishingService(Client):
    fishers = []
    suppliers = []
    buffers = []
    windows = []
    fishing_windows = []
    process_fisher = []
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
        if number_of_fishers < 1 or number_of_fishers > 3:
            #     # warning
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
            print('fisher_id', fisher_id)
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
            # self.cur_state = manager.list()
            # temp_fisher_process = Process(target=temp_fisher.run, args=(self.cur_state,))
            temp_fisher_process = Process(target=temp_fisher.run)
            temp_fisher_process.start()
            # temp_fisher.start()
            self.process_fisher.append(temp_fisher_process)
            self.fishers.append(temp_fisher)
            # self.fishers.append(cur_state)

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
            temp_supplier_process = Process(target=temp_supplier.run)
            temp_supplier_process.start()
            # temp_supplier.start()
            self.process_supplier.append(temp_supplier_process)
            self.suppliers.append(temp_supplier)

        # wincap
        self.win_capture = self.windows[0].wincap

        self.number_of_fishers = number_of_fishers
        self.q = q

        self.offset_x = 0
        self.offset_y = 0

    def __del__(self):
        self.send_message("destroyed")

        del self

    @classmethod
    def send_message(cls, message):
        temp = 'FishingService: ' + message
        print(temp)

    def start_fishing(cls, fishers_list=None):
        time.sleep(1)
        cls.send_message(f'start_fishing() calling')
        if fishers_list is None:
            for fisher in cls.fishers:
                fisher.start()
        else:
            for fisher in fishers_list:
                fisher.start()

    def stop_fishers(cls, fishers_list=None):
        cls.send_message(f'stop_fishing() calling')
        if fishers_list is None:
            for fisher in cls.fishers:
                fisher.stop_fishing()
                cls.process_fisher[fisher.fisher_id].join()

        else:
            for fisher in fishers_list:
                fisher.stop_fishing()
                cls.process_fisher[fisher.fisher_id].join()

    def pause_fishers(cls, fisher, delay=None):
        cls.send_message(f'stop_fishing() calling')
        if delay is None:  # infinit pausing
            pass
            # while True:
            #     fisher.pause_fisher(None)
        else:
            fisher.pause_fisher(delay)

    def send_status_to_server(self, status):
        # print('super().is_connected()', super().is_connected())
        if super().is_connected():
            super().client_send(status)  # ШЛЁМ СООБЩЕНИЕ НА СЕРВЕР

    def get_status_from_server(self):
        if super().is_connected():
            return super().client_receive_message()  # ПОЛУЧАЕМ СООБЩЕНИЯ С СЕРВЕРА

    def fisher_response(self, fisher_id, response):
        if response == 'requests supplying':
            temp_dict = {'dbaits': 0, 'nbaits': 0, 'soski': 0}
            for index, key in enumerate(temp_dict):
                temp_dict[key] = self.fishers[fisher_id].requested_items_to_supply[index]

            resource = temp_dict.copy()
            self.request_server_for_supplying(fisher_id, resource)
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
        print('request_server_for_supplying fisher_id, dic', fisher_id, dic)
        data_to_send = {fisher_id: dic}
        print('data_to_send', data_to_send)
        self.send_status_to_server(data_to_send)

    def start_supply(self, q):

        exit_ = False
        while not exit_:
            for supp in self.suppliers:
                if supp.current_state[0] == 'available':
                    for t in q:
                        for fisher_ID, resource in t.items():
                            self.fishers[fisher_ID].supply_request_proceed[0] = True
                            self.fishers[fisher_ID].current_state[0] = 'busy'
                            print('fisher_ID', fisher_ID)
                            self.fishers[fisher_ID].trading_is_allowed[0] = True
                            time.sleep(0.5)
                            supp.supply(fisher_ID, resource)
                            time.sleep(0.5)
                            print('!!!!!!!!!!!!!!!!!!!!!!.trading_is_allowed[0]', self.fishers[fisher_ID].trading_is_allowed[0])
                            exit_ = True
                else:
                    continue

        print('start_supply q', q)

    def listen_to_server(self):
        # print('self.has_supplier', self.has_supplier)
        # {уникальный ID машины-отправителя: [сообщение1, сообщение2, ...]} - вид отправляемого сообщения сообщение1
        # имеет вид {fisher_id: dict} -> {fisher_id: {'d_baits': a, 'n_baits': b, 'soski': c}}, где a,
        # b и c - количество дневных наживок, ночных наживок и сосок соответственно
        if self.has_supplier:
            message = self.get_status_from_server()
            print('message', message)
            if message:
                q = []
                need_to_supply = False
                for sender_id, [msg] in message.items():
                    print('[MSG]', [msg])
                    fisher_dict = {}
                    for fisher, supplies in msg.items():
                        for resource, amount in supplies.items():
                            if amount != 0:
                                need_to_supply = True
                                if fisher_dict.get(fisher) is not None:
                                    fisher_dict[fisher].update({resource: amount})
                                else:
                                    fisher_dict[fisher] = {resource: amount}
                        q.append(fisher_dict.copy())
                    fisher_dict.clear()
                if need_to_supply:
                    print('Q', q)
                    self.start_supply(q)

    def run(self):
        flag = False
        self.send_message(f'TEST FishingService run_loop() calling')
        # self.connect()  # МОЖНО ПОСТАВИТЬ В НУЖНОЕ МЕСТО МЕТОД ПОДКЛЮЧЕНИЯ К СЕРВЕРУ
        while True:

            for fisher in self.fishers:
                print('fisher.current_state[0]', fisher.current_state[0])
                self.fisher_response(fisher.fisher_id, fisher.current_state[0])

            self.listen_to_server()
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
