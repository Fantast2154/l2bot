import os
import time

import win32con

from _fisher.fishing_service import FishingService
from system.l2window import L2window
import keyboard
from system.action_queue import ActionQueue
from system.relaunch_module import Login
from system.window_capture import WindowCapture
import sys
from system.gui_interface import *
from tests.cpd import CPD
import datetime
import pytz


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


def calculate_time_to_server_restart(cpd):
    temp = datetime.datetime.strptime(cpd.moscow_server_restart_time, '%H:%M:%S').time()
    h = temp.hour
    m = temp.minute
    s = temp.second

    timezone = cpd.timezone
    utcmoment_naive = datetime.datetime.utcnow()
    utcmoment = utcmoment_naive.replace(tzinfo=pytz.utc)

    server_datetime = utcmoment.astimezone(pytz.timezone(timezone))
    server_datetime = server_datetime.replace(tzinfo=None)
    print('main: L2 server date', server_datetime.date())
    server_time_format = server_datetime.time().strftime("%H:%M:%S")
    print('main: L2 server time', server_time_format)
    print(f'main: L2 server planned restart time {cpd.moscow_server_restart_time} {cpd.timezone}')
    moscow_server_restart_temp = server_datetime.replace(hour=h, minute=m, second=s)
    if moscow_server_restart_temp < server_datetime:
        temper_delta = moscow_server_restart_temp + datetime.timedelta(days=1)
        temper = (temper_delta - server_datetime).total_seconds()
        print('main: time left to server restart (in hours)', round(temper / 3600, 2))
        print('main: time left to server restart (in minutes)', int(temper / 60))
        return temper

    else:
        temper = (moscow_server_restart_temp - server_datetime).total_seconds()
        print('main: time left to server restart (in hours)', round(temper / 3600, 2))
        print('main: time left to server restart (in minutes)', int(temper / 60))
        return temper


if __name__ == '__main__':
    print('PROGRAM start--------------------------------------\n')

    custom_personal_data = CPD()
    server_restart_time = calculate_time_to_server_restart(custom_personal_data)
    custom_personal_data.relaunch_windows_time *= 60
    print()
    if server_restart_time > 600:
        server_restart_time_adjusted = server_restart_time - 300  # 5 minutes in advance
    else:
        server_restart_time_adjusted = server_restart_time

    gui_window = None
    user_input = None
    global_program_timing = time.time()
    running_max_time = 7
    fisher_attempts = [0]*custom_personal_data.number_of_fishers

    server_restart_module_activated = False

    while True:
        force_restart = False
        relaunch_windows = False
        program_exit = False

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
                time.sleep(16)

            name_list, hash_list = get_l2windows_param()
            n = len(name_list)
        else:
            log = False
        # screenshot SUPER OBJECT
        manager = Manager()
        screen_manager = manager.list()
        screen_manager.append(0)


        def tue():
            # create n windows L2
            windows = []
            print('number of l2 windows:', n)

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
            # time.sleep(1)
            # process_wincap.terminate()
            # win_capture.stop()

            return windows, queue, process_queue, process_wincap


        windows, queue, process_queue, process_wincap = tue()
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

            login = Login(windows, custom_personal_data.relog_logins, custom_personal_data.relog_passwords, queue)
            windows_to_restart = login.join_the_game()
            if windows_to_restart:
                pass
                # force_restart = True
                # queue.stop()
                # process_queue.join()
                # process_wincap.terminate()
                #
                # for window in windows_to_restart:
                #     handle = window.hwnd
                #     win32gui.PostMessage(handle, win32con.WM_CLOSE, 0, 0)
                #
                #     os.startfile(custom_personal_data.launcher_path)
                #     time.sleep(13)
                #
                # name_list, hash_list = get_l2windows_param()
                # n = len(name_list)
                # time.sleep(1)
                # windows, queue, process_queue, process_wincap = tue()
            time.sleep(2)
            print('main: RELAUNCH COMPLETED ===========================================')

        # creating gui class
        if gui_window is None:
            gui_window = Gui_interface(windows)
            user_input = gui_window.gui_window()
            print('custom_personal_data.relaunch_windows_time ', custom_personal_data.relaunch_windows_time / 3600, 'hours')
        else:
            user_input = gui_window.reinit_windows(windows)
        # creating fishing manager
        FishService = FishingService(windows, user_input, queue)
        if log:
            time.sleep(6)
            for fisher in FishService.fishers:
                fisher.attempt_counter[0] = fisher_attempts[fisher.fisher_id]

        # gui window loop
        process_fishingService = threading.Thread(target=FishService.run)
        process_fishingService.start()

        relaunch_timer = time.time()
        pause_switch = True
        relaunch_windows = False
        counter = 0
        time_between_msg = 60
        program_exit = False

        while True:  # Event Loop

            event, values = gui_window.sg_gui.Read(timeout=2)

            if time.time() - relaunch_timer > custom_personal_data.relaunch_windows_time:
                event = 'Relaunch windows'

            if time.time() - global_program_timing > running_max_time * 3600:
                event = 'Exit'

            if time.time() - relaunch_timer > time_between_msg * counter:
                counter += 1
                print('main: Time to windows relaunch', (custom_personal_data.relaunch_windows_time - (time.time() - relaunch_timer)) // 60,
                      'minutes')
                print('main: Time to server restart',
                      (server_restart_time_adjusted - (time.time() - global_program_timing)) // 60, 'minutes')
                print('main: Time to ending the program',
                      (running_max_time * 3600 - (time.time() - global_program_timing)) // 60, 'minutes')

            if time.time() - global_program_timing > server_restart_time_adjusted:
                server_restart_module_activated = True

                break

            try:  # used try so that if user pressed other than the given key error will not be shown

                if keyboard.is_pressed('alt+q'):  # if key 'q' is pressed
                    print('main: EXIT EVENT DETECTED')
                    program_exit = True
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
                gui_window.sg_gui[temp].update(f'{fisher.attempt_counter[0]}')

            if event == 'Relaunch windows':
                print('main: RELAUNCHING WINDOWS ===========================================')
                relaunch_windows = True
                break

        FishService.pause_fishers()

        closing_time = 50  # awaiting fishers to stop 50 sec is recommended
        timer = time.time()
        counter = 0
        fishers_are_paused = [False]*FishService.number_of_fishers
        while time.time() - timer < closing_time:
            counter += 1
            for i in range(FishService.number_of_fishers):
                if not fishers_are_paused[i]:
                    if FishService.fishers[i].current_state[0] == 'paused':
                        fishers_are_paused[i] = True
            if all(fishers_are_paused):
                break
            time.sleep(1)

        closing_time = 10
        timer = time.time()
        counter = 0
        while time.time() - timer < closing_time:
            counter += 1
            print(f'main: Awaiting fishers to kill a monster ..... {closing_time - counter}')
            time.sleep(1)

        FishService.stop()
        queue.stop()

        process_wincap.terminate()
        time.sleep(3)
        process_wincap.close()

        # print('process_wincap.terminate()', process_wincap.is_alive())
        process_fishingService.join()
        # print('process_fishingService.join()', process_fishingService.is_alive())

        if server_restart_module_activated:
            server_restart_module_activated = False
            relaunch_windows = True
            waiting_time = 1500  # restart timer 1500 is recommended
            timer = time.time()
            counter = 0
            while time.time() - timer < waiting_time:
                print(f'the program will be relaunched in ..... {(waiting_time - counter) // 60} minutes')
                counter += 60
                time.sleep(60)

            server_restart_time = calculate_time_to_server_restart(custom_personal_data)
            server_restart_time_adjusted = server_restart_time - 300  # 5 minutes in advance

        if relaunch_windows or force_restart:
            for window in windows:
                print('restart', window.hwnd)
                handle = window.hwnd
                win32gui.PostMessage(handle, win32con.WM_CLOSE, 0, 0)

        time.sleep(3)

        # process_fishingService.join()
        # process_queue.join()

        process_fishingService = None
        process_queue = None
        process_wincap = None

        del win_capture
        del FishService

        if program_exit:
            break

        # process_wincap.join()

        # gui_window.sg_gui.close()
    gui_window.sg_gui.close()
    sys.exit('PROGRAM ends ......... BYE BYE BYE BYE BYE BYE')
