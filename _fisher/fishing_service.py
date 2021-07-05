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


# self.send_message(f'{self!r}')

class FishingService:
    fishers = []
    suppliers = []
    buffers = []
    fishing_windows = []
    process_fisher = []
    process_buffer = []
    raised_error = False

    exit = threading.Event()

    def __new__(cls, number_of_fishers, number_of_buffers, number_of_suppliers, number_of_teleporters, windows, q):
        if number_of_fishers + number_of_buffers + number_of_suppliers + number_of_teleporters != len(windows):
            print('FISHING SERVICE ERROR')
            # warning
            return None
        if number_of_fishers < 1 or number_of_fishers > 3 or number_of_fishers != len(windows):
            # warning
            return None
        return super(FishingService, cls).__new__(cls)

    def __init__(self, number_of_fishers, number_of_buffers, number_of_suppliers, number_of_teleporters, windows, q):
        # self.send_message(f'created')
        self.exit = threading.Event()

        q.activate_l2windows(windows)
        for fisher_id in range(number_of_fishers):
            #windows
            win_capture = windows[fisher_id].wincap
            window_name = windows[fisher_id].window_name
            hwnd = windows[fisher_id].hwnd
            screenshot = windows[fisher_id].screenshot
            temp_fishing_window = FishingWindow(fisher_id, win_capture, window_name, hwnd, screenshot)
            self.fishing_windows.append(temp_fishing_window)

            #fishers
            temp_fisher = Fisher(temp_fishing_window, fisher_id, number_of_fishers, q)
            temp_fisher_process = Process(target=temp_fisher.run)
            temp_fisher_process.start()
            # temp_fisher.start()
            self.process_fisher.append(temp_fisher_process)
            self.fishers.append(temp_fisher)

        # for buffer_id in range(number_of_buffers):
        #     pass
            #windows
            # win_capture = windows[buffer_id].wincap
            # window_name = windows[buffer_id].window_name
            # hwnd = windows[buffer_id].hwnd
            # screenshot = windows[buffer_id].screenshot
            # temp_buffer_window = FishingWindow(buffer_id, win_capture, window_name, hwnd, screenshot)
            # self.fishing_windows.append(temp_buffer_window)

            #fishers
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

            #fishers
            # temp_supplier = Supplier(temp_supplier_window, supplier_id, number_of_suppliers, q)
            # temp_supplier_process = Process(target=temp_supplier.run)
            # temp_supplier_process.start()
            # temp_supplier.start()
            # self.process_supplier.append(temp_supplier_process)
            # self.suppliers.append(temp_supplier)

        #wincap
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
        if delay is None: # infinit pausing
            pass
            # while True:
            #     fisher.pause_fisher(None)
        else:
            fisher.pause_fisher(delay)

    @classmethod
    def fisher_response(cls, id, response):
        # fisher params
        # 0 - not fishing
        # 1 - fishing
        # 2 - busy with actions (mail,trade and etc.)
        # 8 - paused
        # 9 - error/stucked

        if response == 0:
            pass
            # cls.send_message(f'fisher {id} is not fishing')
        if response == 1:
            pass
            # cls.send_message(f'fisher {id} is fishing')
        if response == 2:
            pass
            # cls.send_message(f'fisher {id} busy with action (mailing, trading and etc.)')
        if response == 8:
            cls.send_message(f'fisher {id} is paused')
        if response == 9:
            cls.send_message(f'fisher {id} stucked (ERROR)')
            # cls.raise_error()

    @classmethod
    def run(cls):
        # cls.send_message(f'TEST FishingService run_loop() calling')
        while not cls.exit.is_set():
            if cls.fishers:
                for fisher in cls.fishers:
                    cls.fisher_response(fisher.fisher_id, fisher.get_status())
            time.sleep(5)
            #if key is pressed:
                # cls.pause_fishers(fisher)

            # if cls.raised_error:
            #     cls.stop_fishers()
            #     break

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

