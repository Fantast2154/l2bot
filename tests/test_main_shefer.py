import sys
import time
from multiprocessing import Process
from threading import Thread

import win32gui

from test_window_capture import *


class Boyko:
    def __init__(self):
        self.i = 0

    def update(self):
        while True:
            self.i += 1

    def get(self):
        return self.i

    def start(self):
        t = Thread(target=self.update)
        t.start()


def main_reader(a, hwnd):
    while True:
        # print(a.get_screenshot(hwnd))
        pass


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

    # setting created windows to screenshot maker
    win_capture.set_windows(windows)

    # start capturing screenshots
    Process_wincap = Process(target=win_capture.start_capturing)
    Process_wincap.start()

    litle_boyko = Boyko()
    print(hash_list[0])
    t = Thread(target=main_reader, args=(win_capture, hash_list[0]))
    t.start()
    t.join()
    sys.exit('PROGRAM ends ......... BYE BYE BYE BYE BYE BYE')
