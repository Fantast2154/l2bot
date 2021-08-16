import time

from _fisher.fishing_service import FishingService
from system.telegram import Telegram
from system.l2window import L2window
import keyboard
from system.action_queue import ActionQueue

from system.window_capture import WindowCapture
import win32gui
import sys
from system.gui_interface import *


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


def client_server(bots_id_list):
    pass


if __name__ == '__main__':
    print('PROGRAM start--------------------------------------\n')
    l2window_name = 'Asterios'
    win_capture = WindowCapture(l2window_name)
    queue = ActionQueue()

    # searching running L2 windows
    name_list, hash_list = get_l2windows_param()
    n = len(name_list)
    print('number of l2 windows:', n)
    print('-----')
    if n < 1:
        sys.exit('NO L2 WINDOWS DETECTED. PROGRAM ENDS.......')

    # screenshot SUPER OBJECT
    manager = Manager()
    screen_manager = manager.list()
    screen_manager.append(0)

    # create n windows L2
    windows = []

    for i in range(n):
        temp_window = L2window(i, win_capture, name_list[i], hash_list[i], screen_manager)
        temp_window.enum_handler()
        windows.append(temp_window)

    # creating gui class
    gui_window = Gui_interface(windows)
    user_input = gui_window.gui_window()

    # setting created windows to screenshot maker
    win_capture.set_windows(windows)

    # start queueing of tasks
    queue.start()

    # start capturing screenshots
    Process_wincap = Process(target=win_capture.start_capturing, args=(screen_manager,))
    Process_wincap.start()

    # creating fishing manager
    F = FishingService(windows, user_input, queue)

    # gui window loop
    t = threading.Thread(target=F.run)
    t.start()

    pause_switch = True
    while True:  # Event Loop
        event, values = gui_window.sg_gui.Read(timeout=4)

        for fisher in F.fishers:
            temp = f'attempt_counter_{gui_window.index[fisher.fisher_id]}'
            gui_window.sg_gui[temp].update(f'{fisher.attempt_counter[0]}')

        if event == sg.WIN_CLOSED or event == 'Exit':
            print('main: PROGRAM ENDS...')
            break

        try:  # used try so that if user pressed other than the given key error will not be shown
            if keyboard.is_pressed('q'):  # if key 'q' is pressed
                print('main: EXIT EVENT DETECTED')
                time.sleep(2)
                break  # finishing the loop
            if keyboard.is_pressed('w'):  # if key 'q' is pressed

                if pause_switch:
                    print('main: PAUSE EVENT DETECTED')
                    F.pause_fishers()
                    pause_switch = False
                else:
                    print('main: RESUME EVENT DETECTED')
                    F.resume_fishers()
                    pause_switch = True
                time.sleep(2)
        except:
            continue
    F.stop()
    queue.stop()
    t.join()
    win_capture.stop()
    Process_wincap.join()

    gui_window.sg_gui.close()

    sys.exit('PROGRAM ends ......... BYE BYE BYE BYE BYE BYE')
