import multiprocessing
from multiprocessing import Process, Value, Manager

import keyboard

from _fisher.fishing_service import FishingService
from system.telegram import Telegram
from system.l2window import L2window
from system.screen_capture import ScreenCapture
from system.action_queue import ActionQueue
# from tests.test_queue_shefer import ActionQueue
from system.window_capture import WindowCapture
import win32gui
import sys
import time
import threading


def send_message(message):
    temp = 'MAIN' + ': ' + message
    print(temp)

def list_window_names():
    temp = []

    def winEnumHandler(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd):
            # temp.append([hex(hwnd), win32gui.GetWindowText(hwnd)])
            temp.append([hwnd, win32gui.GetWindowText(hwnd)])

    win32gui.EnumWindows(winEnumHandler, None)

    windows_param = temp
    return windows_param


def get_l2windows_param():
    hash_list = []
    name_list = []
    list_window_names()  # СПИСОК ВСЕХ ДОСТУПНЫХ ОКОН
    # list_all_windows = get_window_param()

    for window in list_window_names():
        if window[1] == l2window_name:
            name_list.append(window[1])
            hash_list.append(window[0])
    return name_list, hash_list

def input_number(message):
    while True:
        try:
            userInput = int(input(message))
            if userInput < 0:
                print('The value must be >= 0')
                continue
        except ValueError:
            print("Not an integer! Try again.")
            continue
        else:
            return userInput

if __name__ == '__main__':

    print('PROGRAM start--------------------------------------')
    l2window_name = 'Asterios'  # НАЗВАНИЕ ОКНА, ГДЕ БУДЕТ ВЕСТИСЬ ПОИСК
    # win_capture = ScreenCapture()
    win_capture = WindowCapture(l2window_name)

    queue = ActionQueue()

    # searching running L2 windows
    name_list, hash_list = get_l2windows_param()
    n = len(name_list)
    print('number of l2 windows:', n)
    print('-----')
    max_number_of_fishers = 3
    if n >= max_number_of_fishers:
        number_of_fishers = max_number_of_fishers
    else:
        number_of_fishers = n
    number_of_buffers = 0
    number_of_suppliers = 0
    number_of_teleporters = 0
    print('number of fishers: ', number_of_fishers)
    print('number of buffers: ', number_of_buffers)
    print('number of suppliers: ', number_of_suppliers)
    print('number of teleporters: ', number_of_teleporters)
    print('-----------------------')

    # if number_of_fishers < 1 or number_of_fishers > max_number_of_fishers:
    #     send_message('OMG,  ARE YOU KIDDING ME? I SUPPORT ONLY <= 3 FISHERS! KEEP CALM!')
    #     sys.exit('PROGRAM ends ......... BY E BYE BYE BYE BYE BYE')

    # create n windows L2
    manager = Manager()
    screen_manager = manager.list()
    screen_manager.append(0)

    windows = []
    for i in range(n):
        windows.append(L2window(i, win_capture, name_list[i], hash_list[i], screen_manager))

    # setting created windows to screenshot maker
    win_capture.set_windows(windows)

    # start queueing of tasks
    # Process_queue = Process(target=queue.run, args=())
    # Process_queue.start()
    queue.start()
    # start capturing screenshots

    Process_wincap = Process(target=win_capture.start_capturing, args=(screen_manager,))
    Process_wincap.start()

    delay = 3
    for i in range(delay):
        print(f'The window capturing will start in ........ {delay - i} sec')
        time.sleep(1)

    windows_f = windows[:number_of_fishers]  # first m windows to be fishers. LATER FIX THIS

    # t = Telegram()

    # start fishing
    F = FishingService(number_of_fishers, number_of_buffers, number_of_suppliers, number_of_teleporters, windows_f, queue)

    # F.start_fishing()

    timer = time.time()

    # while time.time() - timer < 70:
    while True:
        time.sleep(10)

    Process_wincap.join()

    # stop everything
    F.stop()

    # queue.stop()
    # queue.join()
    win_capture.stop()

    del windows

    sys.exit('PROGRAM ends ......... BYE BYE BYE BYE BYE BYE')
