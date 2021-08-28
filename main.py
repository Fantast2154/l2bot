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


def start_auto_py(auto):
    auto.start()


def exitAutoHotKey(autohotpy, event):
    autohotpy.stop()


if __name__ == '__main__':
    print('PROGRAM start--------------------------------------\n')

    custom_personal_data = CPD()

    time.sleep(10)

    gui_window = None
    user_input = None
    relaunch_time = None

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

        rect_windows_list = []
        for hwnd in hash_list:
            rect = win32gui.GetWindowRect(hwnd)
            rect_windows_list.append([rect[0], hwnd])

        rect_windows_list.sort(key=lambda x: x[0])

        for i in range(n):
            temp_window = L2window(i, win_capture, name_list[i], hash_list[i], screen_manager)
            temp_window.hwnd = rect_windows_list[i][1]
            if log:
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
            # if not custom_personal_data.relog_logins and gui_window is None:
            custom_personal_data.relog_logins = []
            custom_personal_data.relog_passwords = []
            for nick, account in list(custom_personal_data.accounts.items())[:custom_personal_data.number_of_windows]:
                nickname = nick
                log = account[0]
                pas = account[1]
                custom_personal_data.relog_logins.append(log)
                custom_personal_data.relog_passwords.append(pas)

            Login(windows, custom_personal_data.relog_logins, custom_personal_data.relog_passwords, queue)
            time.sleep(2)

        # creating gui class
        if gui_window is None:
            gui_window = Gui_interface(windows)
            user_input, relaunch_time = gui_window.gui_window()
            print('relaunch_time ', relaunch_time / 3600, 'hours')
        else:
            user_input = gui_window.reinit_windows(windows)

        # creating fishing manager
        FishService = FishingService(windows, user_input, queue)

        # gui window loop
        process_fishingService = threading.Thread(target=FishService.run)
        process_fishingService.start()

        # for fisher in FishService.fishers:
        #     temp = f'attempt_counter_{gui_window.index[fisher.fisher_id]}'
        #     gui_window.sg_gui[temp].update(f'{fisher.attempt_counter[0]}')

        # if not log:
        #     print('not default order')
        #
        #     nick_name_list = [0]*custom_personal_data.number_of_windows
        #     if FishService.number_of_fishers != 0:
        #         exit_is_set = False
        #         while not exit_is_set:
        #             for fisher in FishService.fishers:
        #                 if fisher.nickname[0] is not None and fisher.nickname[0] not in nick_name_list:
        #                     nick_name_list[fisher.fishing_window.window_id] = fisher.nickname[0]
        #                 if len(nick_name_list) == FishService.number_of_fishers:
        #                     exit_is_set = True
        #                     break
        #
        #     window_fishers = user_input[0]
        #     window_buffers = user_input[1]
        #     window_suppliers = user_input[2]
        #     window_teleporters = user_input[3]
        #
        #     # if custom_personal_data.number_of_windows - len(nick_name_list) == 1: # PIZDA
        #     custom_personal_data.relog_logins = []
        #     custom_personal_data.relog_passwords = []
        #     for nick in nick_name_list:
        #         nickname = nick
        #         log = custom_personal_data.accounts[nick][0]
        #         pas = custom_personal_data.accounts[nick][1]
        #         custom_personal_data.relog_logins.append(log)
        #         custom_personal_data.relog_passwords.append(pas)

        relaunch_timer = time.time()
        pause_switch = True
        relaunch_windows = False
        counter = 0
        time_between_msg = 60
        program_exit = False
        while True:  # Event Loop

            event, values = gui_window.sg_gui.Read(timeout=2)

            if time.time() - relaunch_timer > relaunch_time:
                event = 'Relaunch windows'
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
                program_exit = True
                break

            # FIXME ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! FISHER DESTROYES HIMSELF..
            for fisher in FishService.fishers:
                temp = f'attempt_counter_{gui_window.index[fisher.fisher_id]}'
                gui_window.sg_gui[temp].update(f'{fisher.attempt_counter[0]}')  # FIXME

            if event == 'Relaunch windows':
                print('main: RELAUNCHING WINDOWS ===========================================')
                relaunch_windows = True
                break

            if time.time() - relaunch_timer > time_between_msg * counter:
                counter += 1
                print('main: Time to restart = ', (relaunch_time - (time.time() - relaunch_timer)) // 60, ' minutes')


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

        if program_exit:
            break
        # process_wincap.join()

        # gui_window.sg_gui.close()

    sys.exit('PROGRAM ends ......... BYE BYE BYE BYE BYE BYE')
