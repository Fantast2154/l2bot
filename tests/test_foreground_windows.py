import time
from system.screen_capture import ScreenCapture
from test_fisher import TestFisher
from multiprocessing import Queue


def get_l2windows_param(wincap):
    win_name = 'Asterios'  # НАЗВАНИЕ ОКНА, ГДЕ БУДЕТ ВЕСТИСЬ ПОИСК
    hash_list = []
    name_list = []
    wincap.list_window_names()  # СПИСОК ВСЕХ ДОСТУПНЫХ ОКОН
    list_all_windows = wincap.get_windows_param()
    for window in list_all_windows:
        if window[1] == win_name:
            name_list.append(window[1])
            hash_list.append(window[0])
            print(window)
    return name_list, hash_list


q = Queue()
wincap = ScreenCapture()

name_list, hash_list = get_l2windows_param(wincap)
print(hash_list)

fisher_1 = TestFisher('fisher_1', hash_list[0], q)
fisher_2 = TestFisher('fisher_2', hash_list[1], q)

fisher_1.start()
fisher_2.start()

q.get()
q.get_nowait()
