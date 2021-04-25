import win32gui

from fisher.fishing_service import FishingService
from system.telegram import Telegram
from system.l2window import L2window
from system.window_capture import WindowCapture
import telebot
import sys
import time


def message_gui(message):
    print(message)


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


def list_window_names():

    temp = []

    def winEnumHandler(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd):
            temp.append([hwnd, win32gui.GetWindowText(hwnd)])

    win32gui.EnumWindows(winEnumHandler, None)
    return temp


def get_l2windows_param(l2window_name):

    hash_list = []
    name_list = []

    list_all_windows = list_window_names()
    for window in list_all_windows:
        if window[1] == l2window_name:
            name_list.append(window[1])
            hash_list.append(window[0])
            print(window)
    return name_list, hash_list


if __name__ == '__main__':

    print('PROGRAM start--------------------------------------')
    l2window_name = 'Asterios'


    name_list, hash_list = get_l2windows_param(l2window_name)

    n = len(win_capture.game_windows)
    print('number of l2 windows:', n)

    if n == 0:
        message_gui('THERE ARE NO L2 WINDOWS. STUPID BASTARD')
        sys.exit('PROGRAM ends ......... BY E BYE BYE BYE BYE BYE')

    if n >= 2:
        m = 2
    else:
        m = n
    print('number of fishers: ', m)

    if m > n:
        message_gui("I DON'T HAVE ENOUGH WINDOWS!")
        sys.exit('PROGRAM ends ......... BY E BYE BYE BYE BYE BYE')

    if n == 0:
        message_gui('THERE ARE NO L2 WINDOWS. STUPID BASTARD')
        sys.exit('PROGRAM ends ......... BY E BYE BYE BYE BYE BYE')

    windows = []
    for i in range(n):
        windows.append(L2window(i, name_list[i], hash_list[i]))

    win_capture = WindowCapture(windows)
    win_capture.start()

    delay = 3
    for i in range(delay):
        print(f'The window capturing will start in ........ {delay - i} sec')
        time.sleep(1)

    windows_f = windows[:m]  # first m windows to be fishers. LATER FIX THIS
    if n > m:
        window_supplier = windows[m]
    else:
        window_supplier = []

    FishingService(windows_f, win_capture, window_supplier)

    win_capture.stop()
    win_capture.join()

    del windows

    sys.exit('PROGRAM ends ......... BYE BYE BYE BYE BYE BYE')
