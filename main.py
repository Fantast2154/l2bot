from fisher.fishing_service import FishingService
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

    name_list, hash_list = win_capture.get_l2windows_param()

    n = len(name_list)
    print('number of l2 windows:', n)
    if n >= 3:
        m = 3  # number of fishers
    else:
        m = n  # number of fishers
    print('number of fishers: ', m)

    if m > n:
        send_message("I DON'T HAVE ENOUGH WINDOWS!")

    if m < 1 or m > 3:
        send_message('OMG,  ARE YOU KIDDING ME? I SUPPORT ONLY 1 OR 2 FISHERS! KEEP CALM!')
        sys.exit('PROGRAM ends ......... BY E BYE BYE BYE BYE BYE')

    # create n windows L2
    windows = []
    for i in range(n):
        windows.append(L2window(i, win_capture, name_list[i], hash_list[i]))

    win_capture.set_windows(windows)

    # start capturing screenshots
    queue.start()
    win_capture.start_capturing()

    delay = 3
    for i in range(delay):
        print(f'The window capturing will start in ........ {delay - i} sec')
        time.sleep(1)

    windows_f = windows[:m]  # first m windows to be fishers. LATER FIX THIS
    FishingService(m, windows_f, queue)
    queue.stop()
    queue.join()
    win_capture.stop()

    del windows

    sys.exit('PROGRAM ends ......... BYE BYE BYE BYE BYE BYE')
