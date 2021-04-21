from fisher.fishing_service import FishingService
from system.telegram import Telegram
from system.l2window import L2window
from system.screen_capture import ScreenCapture
# from system.action_queue import ActionQueue
from tests.test_queue_shefer import ActionQueue
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


def get_l2windows_param(wincap, l2window_name):
    hash_list = []
    name_list = []
    wincap.list_window_names()  # СПИСОК ВСЕХ ДОСТУПНЫХ ОКОН
    list_all_windows = wincap.get_windows_param()
    for window in list_all_windows:
        if window[1] == l2window_name:
            name_list.append(window[1])
            hash_list.append(window[0])
            print(window)
    return name_list, hash_list


if __name__ == '__main__':

    print('PROGRAM start--------------------------------------')
    win_capture = ScreenCapture()
    # queue = ActionQueue(win_capture)

    l2window_name = 'Asterios'  # НАЗВАНИЕ ОКНА, ГДЕ БУДЕТ ВЕСТИСЬ ПОИСК
    name_list, hash_list = get_l2windows_param(win_capture, l2window_name)

    # n = input_number('number of l2 windows: ')
    n = len(name_list)
    print('number of l2 windows:', n)
    if n >= 2:
        m = 2  # m = input_number('')
    else:
        m = n
    print('number of fishers: ', m)

    if m > n:
        message_gui("I DON'T HAVE ENOUGH WINDOWS!")

    if m < 1 or m > 2:
        message_gui('OMG,  ARE YOU KIDDING ME? I SUPPORT ONLY 1 OR 2 FISHERS! KEEP CALM!')
        sys.exit('PROGRAM ends ......... BY E BYE BYE BYE BYE BYE')

    windows = []
    for i in range(n):
        windows.append(L2window(i, win_capture, name_list[i], hash_list[i]))

    win_capture.set_windows(windows)
    # queue.start()
    win_capture.start()

    delay = 3
    for i in range(delay):
        print(f'The window capturing will start in ........ {delay - i} sec')
        time.sleep(1)

    windows_f = windows[:m]  # first m windows to be fishers. LATER FIX THIS
    FishingService(m, windows_f)
    # queue.stop()
    # queue.join()
    win_capture.stop()
    win_capture.join()





    del windows

    sys.exit('PROGRAM ends ......... BYE BYE BYE BYE BYE BYE')
