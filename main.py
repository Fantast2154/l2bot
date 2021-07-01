import keyboard

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

def foo():
    global pause
    while True:
        if keyboard.is_pressed('p'):
            print('PRIVET!!!!!')
            pause = True




if __name__ == '__main__':
    t = threading.Thread(target=foo)
    t.start()
    global pause
    pause = False
    print('PROGRAM start--------------------------------------')
    l2window_name = 'Asterios'  # НАЗВАНИЕ ОКНА, ГДЕ БУДЕТ ВЕСТИСЬ ПОИСК
    # win_capture = ScreenCapture()
    win_capture = WindowCapture(l2window_name)

    queue = ActionQueue()

    # searching running L2 windows
    name_list, hash_list = win_capture.get_l2windows_param()

    n = len(name_list)
    print('number of l2 windows:', n)
    max_number_of_fishers = 3
    if n >= max_number_of_fishers:
        m = max_number_of_fishers  # number of fishers
    else:
        m = n  # number of fishers
    print('number of fishers: ', m)

    if m < 1 or m > 3:
        send_message('OMG,  ARE YOU KIDDING ME? I SUPPORT ONLY < 3 FISHERS! KEEP CALM!')
        sys.exit('PROGRAM ends ......... BY E BYE BYE BYE BYE BYE')

    # create n windows L2
    windows = []
    for i in range(n):
        windows.append(L2window(i, win_capture, name_list[i], hash_list[i]))

    # setting created windows to screenshot maker
    win_capture.set_windows(windows)

    # start queueing of tasks
    queue.start()
    # start capturing screenshots
    win_capture.start_capturing()

    delay = 3
    for i in range(delay):
        print(f'The window capturing will start in ........ {delay - i} sec')
        time.sleep(1)

    windows_f = windows[:m]  # first m windows to be fishers. LATER FIX THIS

    # t = Telegram()

    # start fishing
    F = FishingService(m, windows_f, queue)

    F.start_fishing()

    timer = time.time()

    # while time.time() - timer < 70:
    while True:
        #time.sleep(2)
        if pause:
            pause = False
            t.join()
            break


    # stop everything
    F.stop()

    queue.stop()
    # queue.join()
    win_capture.stop()

    del windows

    sys.exit('PROGRAM ends ......... BYE BYE BYE BYE BYE BYE')
