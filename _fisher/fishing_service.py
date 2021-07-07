import time
import threading

from _fisher.l2fisher import Fisher
from _fisher.l2supplier import Supplier
from _fisher.l2buffer import Buffer
from system.action_queue import *
import threading
from _fisher.fishing_window import FishingWindow
from _fisher.fishing_window_buffer import *
from _fisher.fishing_window_supplier import *
from multiprocessing import Process, Value, Manager
from system.action_queue import ActionQueue
from system.botnet import Client


# self.send_message(f'{self!r}')

class FishingService(Client):
    fishers = []
    suppliers = []
    buffers = []
    fishing_windows = []
    process_fisher = []
    process_buffer = []
    raised_error = False
    fishing_service_client = {}

    exit = threading.Event()

    def __init__(self, number_of_fishers, number_of_buffers, number_of_suppliers, number_of_teleporters, windows, q):
        super().__init__()  # ИНИЦИАЛИЗИРУЕМ РОДИТЕЛЬСКИЙ КЛАСС Client И ПРИСОЕДИНЯЕМСЯ К СЕРВАЧКУ
        self.machine_id = 0
        if number_of_fishers + number_of_buffers + number_of_suppliers + number_of_teleporters != len(windows):
            print('FISHING SERVICE ERROR')
        #     # warning
        #     return None
        if number_of_fishers < 1 or number_of_fishers > 3 or number_of_fishers != len(windows):
            #     # warning
            print('FISHING SERVICE ERROR')
        # return super(FishingService, cls).__new__(cls)
        if number_of_suppliers != 0:
            self.has_supplier = True
            self.queue_list = []

        self.send_message(f'created')
        self.exit = threading.Event()

        q.activate_l2windows(windows)
        for fisher_id in range(number_of_fishers):
            # windows
            win_capture = windows[fisher_id].wincap
            window_name = windows[fisher_id].window_name
            hwnd = windows[fisher_id].hwnd
            screenshot = windows[fisher_id].screenshot
            temp_fishing_window = FishingWindow(fisher_id, win_capture, window_name, hwnd, screenshot)
            self.fishing_windows.append(temp_fishing_window)

            # fishers
            temp_fisher = Fisher(temp_fishing_window, fisher_id, number_of_fishers, q)
            temp_fisher_process = Process(target=temp_fisher.run)
            temp_fisher_process.start()
            # temp_fisher.start()
            self.process_fisher.append(temp_fisher_process)
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

        # for supplier_id in range(number_of_suppliers):
        #     pass
        # win_capture = windows[supplier_id].wincap
        # window_name = windows[supplier_id].window_name
        # hwnd = windows[supplier_id].hwnd
        # screenshot = windows[supplier_id].screenshot
        # temp_supplier_window = FishingWindow(supplier_id, win_capture, window_name, hwnd, screenshot)
        # self.fishing_windows.append(temp_supplier_window)

        # suppliers
        # temp_supplier = Supplier(temp_supplier_window, supplier_id, number_of_suppliers, q)
        # temp_supplier_process = Process(target=temp_supplier.run)
        # temp_supplier_process.start()
        # temp_supplier.start()
        # self.process_supplier.append(temp_supplier_process)
        # self.suppliers.append(temp_supplier)

        # wincap
        self.win_capture = windows[0].wincap

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

    @classmethod
    def start_fishing(cls, fishers_list=None):
        time.sleep(1)
        cls.send_message(f'start_fishing() calling')
        if fishers_list is None:
            for fisher in cls.fishers:
                fisher.start()
        else:
            for fisher in fishers_list:
                fisher.start()

    @classmethod
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

    @classmethod
    def pause_fishers(cls, fisher, delay=None):
        cls.send_message(f'stop_fishing() calling')
        if delay is None:  # infinit pausing
            pass
            # while True:
            #     fisher.pause_fisher(None)
        else:
            fisher.pause_fisher(delay)

    def send_status_to_server(self, *status):
        if super().is_connected():
            super().client_send(status)  # ШЛЁМ СООБЩЕНИЕ НА СЕРВЕР

    def get_status_from_server(self):
        if super().is_connected():
            return super().client_receive_message()  # ПОЛУЧАЕМ СООБЩЕНИЯ С СЕРВЕРА

    def fisher_response(self, id, response):
        self.send_status_to_server(id, response)
        message_from_other_machines = self.get_status_from_server()
        # fisher params
        # 0 - not fishing
        # 1 - fishing
        # 2 - busy with actions (mail,trade and etc.)
        # 8 - paused
        # 9 - error/stucked

        if 'Out of soski' in message_from_other_machines:
            if self.has_supplier:
                for sup in self.suppliers:
                    sup.supply(id, 'soski')

        if response == 'Out of soski':
            if self.has_supplier:
                for sup in self.suppliers:
                    sup.supply(id, 'soski')
            # cls.send_message(f'fisher {id} is not fishing')
        if response == 1:
            pass
            # cls.send_message(f'fisher {id} is fishing')
        if response == 2:
            pass
            # cls.send_message(f'fisher {id} busy with action (mailing, trading and etc.)')
        if response == 8:
            self.send_message(f'fisher {id} is paused')
        if response == 9:
            self.send_message(f'fisher {id} stucked (ERROR)')
            # cls.raise_error()

    def request_server_for_supplying(self, fisher_id, list):
        self.send_status_to_server(fisher_id, self.machine_id, list)

    def allow_fisher_to_trade(self, id):
        self.fishers[id].trading_is_allowed = True

    def listen_to_server(self):
        fisher_receiver_id, machine_recevier_id, machine_supplier_id, list = self.get_status_from_server() # как разделить сообщения - для рыбака или для саплаера?
        if self.has_supplier and self.machine_id == machine_supplier_id:
            if self.machine_id == machine_recevier_id:
                if self.fishers[fisher_receiver_id]:
                    self.allow_fisher_to_trade(fisher_receiver_id)
            self.suppliers[0].supply(list)
        else:
            if self.fishers[fisher_receiver_id]:
                self.allow_fisher_to_trade(fisher_receiver_id)

    # @classmethod
    def run(self):
        self.send_message(f'TEST FishingService run_loop() calling')
        # self.connect()  # МОЖНО ПОСТАВИТЬ В НУЖНОЕ МЕСТО МЕТОД ПОДКЛЮЧЕНИЯ К СЕРВЕРУ

        while not self.exit.is_set():
            if self.fishers:
                for fisher in self.fishers:
                    self.fisher_response(fisher.fisher_id, fisher.get_status())
                    if fisher.supply_request:
                        self.request_server_for_supplying(fisher.fisher_id, fisher.requested_items_to_supply)
                        fisher.supply_request = False
                        fisher.request_proceed = True

            self.listen_to_server()
            time.sleep(1)

    @classmethod
    def stop(cls):
        cls.stop_fishers()
        cls.send_message('thread stops')
        cls.exit.set()
        closing_time = 5
        timer = time.time()
        while time.time() - timer < closing_time:
            cls.send_message(f'timer before close ..... {time.time() - timer}')
            time.sleep(1)

        del cls.fishers
        del cls.fishing_windows
