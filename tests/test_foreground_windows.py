import time
from system.screen_capture import ScreenCapture
import win32gui, win32com.client


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


shell = win32com.client.Dispatch("WScript.Shell")
shell.SendKeys('%')

wincap = ScreenCapture()

name_list, hash_list = get_l2windows_param(wincap)
print(hash_list)

for hwnd in hash_list * 100:
    time.sleep(0.03)
    win32gui.SetForegroundWindow(hwnd)
