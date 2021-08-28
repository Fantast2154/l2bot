import os
import time

import win32con

from _fisher.fishing_service import FishingService
from system.telegram import Telegram
from system.l2window import L2window
import keyboard
from system.action_queue import ActionQueue
from system.relaunch_module import Login
from system.window_capture import WindowCapture
import win32gui
import sys
from system.gui_interface import *
from system.cpd import CPD


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

    custom_personal_data = CPD()

    time.sleep(10)

    gui_window = None
    user_input = None

    while True:

        l2window_name = 'Asterios'
        win_capture = WindowCapture(l2window_name)

        # searching running L2 windows
        name_list, hash_list = get_l2windows_param()
        n = len(name_list)

        if n == 0:
            log = True
            print('log = ', log)
            for i in range(custom_personal_data.number_of_windows):
                os.startfile(custom_personal_data.launcher_path)
                time.sleep(11)

            name_list, hash_list = get_l2windows_param()
            n = len(name_list)
        else:
            log = False
        # screenshot SUPER OBJECT
        manager = Manager()
        screen_manager = manager.list()
        screen_manager.append(0)

        # create n windows L2
        windows = []
        print('number of l2 windows:', n)
        print('hash_list of l2 windows:', hash_list)
        print('-----')
        for i in range(n):
            temp_window = L2window(i, win_capture, name_list[i], hash_list[i], screen_manager)
            temp_window.enum_handler()
            windows.append(temp_window)

        # setting created windows to screenshot maker
        win_capture.set_windows(windows)

        # setting created windows to queue
        queue = ActionQueue(windows)

        # start queueing of tasks
        process_queue = threading.Thread(target=queue.run)
        process_queue.start()


        # start capturing screenshots
        process_wincap = Process(target=win_capture.start_capturing, args=(screen_manager,))
        process_wincap.start()

        # login module
        if log:
            l = Login(windows, custom_personal_data.logins, custom_personal_data.passwords, queue)
            time.sleep(2)

        # creating gui class
        if gui_window is None:
            gui_window = Gui_interface(windows)
            user_input = gui_window.gui_window()
        else:
            user_input = gui_window.reinit_windows(windows)

        # creating fishing manager
        FishService = FishingService(windows, user_input, queue)

        # gui window loop
        process_fishingService = threading.Thread(target=FishService.run)
        process_fishingService.start()

        pause_switch = True
        relaunch_windows = False

        # for fisher in FishService.fishers:
        #     temp = f'attempt_counter_{gui_window.index[fisher.fisher_id]}'
        #     gui_window.sg_gui[temp].update(f'{fisher.attempt_counter[0]}')

        while True:  # Event Loop

            event, values = gui_window.sg_gui.Read(timeout=3)

            try:  # used try so that if user pressed other than the given key error will not be shown

                if keyboard.is_pressed('alt+q'):  # if key 'q' is pressed
                    print('main: EXIT EVENT DETECTED')
                    time.sleep(2)
                    break  # finishing the loop
                if keyboard.is_pressed('alt+w'):  # if key 'q' is pressed

                    if pause_switch:
                        print('main: PAUSE EVENT DETECTED')
                        FishService.pause_fishers()
                        pause_switch = False
                    else:
                        print('main: RESUME EVENT DETECTED')
                        FishService.resume_fishers()
                        pause_switch = True
                    time.sleep(2)
            except:
                continue

            if event == sg.WIN_CLOSED or event == 'Exit':
                print('main: PROGRAM ENDS...')
                break

            #FIXME ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! FISHER DESTROYES HIMSELF..
            for fisher in FishService.fishers:
                temp = f'attempt_counter_{gui_window.index[fisher.fisher_id]}'
                gui_window.sg_gui[temp].update(f'{fisher.attempt_counter[0]}') #FIXME

            if event == 'Relaunch windows':
                relaunch_windows = True
                break

        FishService.stop()
        queue.stop()
        process_wincap.terminate()
        if relaunch_windows:
            for window in windows:
                handle = window.hwnd
                win32gui.PostMessage(handle, win32con.WM_CLOSE, 0, 0)

        time.sleep(3)

        # process_fishingService.join()
        # process_queue.join()

        process_fishingService = None
        process_queue = None
        process_wincap = None
        del FishService

        # process_wincap.join()

        # gui_window.sg_gui.close()

    sys.exit('PROGRAM ends ......... BYE BYE BYE BYE BYE BYE')
