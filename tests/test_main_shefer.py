import sys
import time
import multiprocessing as mp
from multiprocessing import sharedctypes
from threading import Thread
import ctypes
import numpy as np
from tempfile import TemporaryFile

import win32gui
from multiprocessing import Process, Manager
from test_window_capture3 import *
from test_fisher import *

def list_window_names():
    temp = []

    def winEnumHandler(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd):
            # temp.append([hex(hwnd), win32gui.GetWindowText(hwnd)])
            temp.append([hwnd, win32gui.GetWindowText(hwnd)])

    win32gui.EnumWindows(winEnumHandler, None)

    return temp


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


if __name__ == '__main__':
    print('PROGRAM start--------------------------------------')
    l2window_name = 'Asterios'  # НАЗВАНИЕ ОКНА, ГДЕ БУДЕТ ВЕСТИСЬ ПОИСК
    # win_capture = ScreenCapture()
    win_capture = WindowCapture(l2window_name)

    # searching running L2 windows
    name_list, hash_list = get_l2windows_param()

    n = len(name_list)

    windows = []
    for i in range(n):
        windows.append(L2window(i, win_capture, name_list[i], hash_list[i]))

    win_capture.set_windows(windows)

    manager = Manager()
    test = manager.list()
    test.append(0)

    print('test', test)
    Process_wincap = Process(target=win_capture.start_capturing, args=(test,))

    Process_wincap.start()
    time.sleep(1)
    f = Fisher(test)
    Process_fisher = Process(target=f.start)
    Process_fisher.start()

    # Process_wincap = mp.Pool(initializer=win_capture.start_capturing, initargs=(arr,))
    time.sleep(10)
    Process_fisher.join()
    Process_wincap.join()

    sys.exit('PROGRAM ends ......... BYE BYE BYE BYE BYE BYE')
