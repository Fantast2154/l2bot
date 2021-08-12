import time
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



class FishingService():
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

    def __init__(self, window_fishers, window_buffers, window_suppliers, window_teleporters, q):
        manager = Manager()
        self.p_server = None
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
        # super().__init__(self.machine_id)  # ИНИЦИАЛИЗИРУЕМ РОДИТЕЛЬСКИЙ КЛАСС Client И ПРИСОЕДИНЯЕМСЯ К СЕРВАЧКУ
        self.fishing_service_client = Client(self.machine_id)
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
        self.process_buffers = list(range(number_of_buffers))

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

        for buffer_id in range(number_of_buffers):
            win_capture = window_buffers[buffer_id].wincap
            window_name = window_buffers[buffer_id].window_name
            hwnd = window_buffers[buffer_id].hwnd
            screenshot = window_buffers[buffer_id].screenshot
            temp_buffer_window = FishingBufferWindow(buffer_id, win_capture, window_name, hwnd, screenshot)
            temp_buffer_window.window_id = window_buffers[buffer_id].window_id
            self.buffer_windows.append(temp_buffer_window)

            temp_buffer = Buffer(temp_buffer_window, buffer_id, number_of_buffers, q)
            self.buffers.append(temp_buffer)

        for supplier_id in range(number_of_suppliers):
            win_capture = window_suppliers[supplier_id].wincap
            window_name = window_suppliers[supplier_id].window_name
            hwnd = window_suppliers[supplier_id].hwnd
            screenshot = window_suppliers[supplier_id].screenshot
            temp_supplier_window = FishingSupplierWindow(supplier_id, win_capture, window_name, hwnd, screenshot)
            temp_supplier_window.window_id = window_suppliers[supplier_id].window_id
            self.supplier_windows.append(temp_supplier_window)

            temp_supplier = Supplier(temp_supplier_window, supplier_id, number_of_suppliers, q)
            self.suppliers.append(temp_supplier)

        # wincap
        self.win_capture = self.windows[0].wincap

        self.number_of_fishers = number_of_fishers
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
        self.send_message(f'start_fishing')
        if fisher_id is None:
            for fisher in self.fishers:
                temp_fisher_process = Process(target=fisher.start_fishing)
                self.process_fishers[fisher.fisher_id] = temp_fisher_process
                self.process_fishers[fisher.fisher_id].start()
                self.process_fishers[fisher.fisher_id] = None
                # temp_fisher_process.start()
        else:
            if fisher_id < len(self.process_fishers):
                temp_fisher_process = Process(target=self.fishers[fisher_id].start_fishing)
                self.process_fishers[fisher_id] = temp_fisher_process
                self.process_fishers[fisher_id].start()
                self.process_fishers[fisher_id] = None

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

    def run(self):
        flag = False
        self.send_message(f'TEST FishingService run_loop() calling')
        self.server_update_start()
        while True:
            #self.server_update()
            time.sleep(1)

    def stop(self):
        self.stop_fishers()
        self.send_message('thread stops')
        closing_time = 5
        timer = time.time()
        while time.time() - timer < closing_time:
            self.send_message(f'timer before close ..... {time.time() - timer}')
            time.sleep(1)

        del self.fishers
        del self.fishing_windows

    # def update_fishers_attempt(self, id, attempt):
    #     temp = f'fisher_{id}'
    #     print(attempt)
    #     global sg_gui
    #     sg_gui[temp].update(f'{attempt}')

    def server_update(self):
        print('Process+++++++++++++++++++Process server_update+++++++++++++++++++++Process')
        while True:
            print(111)
            self.fishing_service_client.number_of_fishers_ = self.number_of_fishers_
            self.fishing_service_client.number_of_suppliers_ = self.number_of_suppliers_
            self.fishing_service_client.number_of_teleporters_ = self.number_of_teleporters_
            self.fishing_service_client.number_of_buffers_ = self.number_of_buffers_

            self.fishing_service_client.fishers_request = self.fishers_request
            self.fishing_service_client.suppliers_request = self.suppliers_request
            self.fishing_service_client.teleporters_request = self.teleporters_request
            self.fishing_service_client.buffers_request = self.buffers_request

            self.fishing_service_client.fishers = self.fishers
            self.fishing_service_client.suppliers = self.suppliers
            self.fishing_service_client.teleporters = self.teleporters
            self.fishing_service_client.buffers = self.buffers
            self.fishing_service_client.has_supplier = self.has_supplier

    def server_update_start(self):

        # t1 = Thread(target=self.server_update, args=())
        # t1.start()
        self.p_server = Process(target=self.server_update)
        self.p_server.start()
