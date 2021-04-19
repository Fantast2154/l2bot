from fisher.fishing_service import FishingService
from system.telegram import Telegram
from system.l2window import L2window
from system.screen_capture import ScreenCapture
from system.action_queue import ActionQueue
import sys
import time
import win32gui
import re


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


# def enumHandler2(hwnd, lParam):
#     if win32gui.IsWindowVisible(hwnd):
#         if 'Asterios' in win32gui.GetWindowText(hwnd):
#             win32gui.MoveWindow(hwnd, 0, 0, 760, 500, True)

class WindowMgr:
    """Encapsulates some calls to the winapi for window management"""

    def __init__(self):
        """Constructor"""
        self._handle = None

    def find_window(self, class_name, window_name=None):
        """find a window by its class_name"""
        self._handle = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, hwnd, wildcard):
        """Pass to win32gui.EnumWindows() to check all the opened windows"""
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
            self._handle = hwnd

    def find_window_wildcard(self, wildcard):
        """find a window whose title matches the wildcard regex"""
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    def set_foreground(self):
        """put the window in the foreground"""
        win32gui.SetForegroundWindow(self._handle)


def get_l2windows_param(wincap):
    asterios = 'Asterios'  # НАЗВАНИЕ ОКНА, ГДЕ БУДЕТ ВЕСТИСЬ ПОИСК
    hash_list = []
    name_list = []
    wincap.list_window_names()  # СПИСОК ВСЕХ ДОСТУПНЫХ ОКОН
    list_all_windows = wincap.get_windows_param()
    for window in list_all_windows:
        if window[1] == 'Asterios':
            name_list.append(window[1])
            hash_list.append(window[0])
            print(window)
    return name_list, hash_list


if __name__ == '__main__':

    print('PROGRAM start-------------------------------------')
    queue = ActionQueue()

    win_capture = ScreenCapture()
    name_list, hash_list = get_l2windows_param(win_capture)

    # n = input_number('number of l2 windows: ')
    n = len(name_list)
    print('number of l2 windows:', n)
    m = 2  # m = input_number('')
    print('number of fishers: ', m)

    if m > n:
        message_gui("I DON'T HAVE ENOUGH WINDOWS!")

    if m < 1 or m > 2:
        message_gui('OMG,  ARE YOU KIDDING ME? I SUPPORT ONLY 1 OR 2 FISHERS! KEEP CALM!')

    windows = []
    for i in range(n):
        windows.append(L2window(i, win_capture, name_list[i], hash_list[i]))

    # w = WindowMgr()
    # w.find_window_wildcard(window_name)
    # w.set_foreground()
    # for hwnd in hash_list:
    #     enumHandler2(hwnd, None)
    #     time.sleep(3)

    queue.start()
    win_capture.start()

    delay = 3

    #time_temp = time.time()
    #while time.time() - time_temp <= delay:
    #    print('The fishing will start in ........ ', round(delay - (time.time() - time_temp), 1))
    #    time.sleep(0.5)

    for i in range(delay):
        print('The fishing will start in ........ ', delay - i)
        time.sleep(0.5)

    windows_f = windows[:m]  # first m windows to be fishers. LATER FIX THIS
    FishingService(m, windows_f, queue)

    queue.stop()
    queue.join()
    win_capture.stop()
    win_capture.join()

    del windows

    sys.exit('PROGRAM ends ......... BYE BYE BYE BYE BYE BYE')
