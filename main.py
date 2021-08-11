import multiprocessing
from multiprocessing import Process, Value, Manager
from _fisher.fishing_service import FishingService
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
from system.botnet import Server, Client
import keyboard
import PySimpleGUI as sg

def gui_window1(windows_f, windows_b, windows_s, windows_t):
    global L2_total_height
    global L2_min_x
    L2_total_height = 0
    L2_min_x = 10000
    l2button_width = 12
    l2button_height = 6

    global app_height
    global app_width
    app_height = 400
    app_width = 300

    manager = Manager()
    global l2window_rectangles
    global l2window_workers
    global l2attempt_counter
    l2window_rectangles = manager.list()
    l2window_workers = manager.list()
    l2attempt_counter = manager.list()
    workers = manager.list()
    for window in windows:
        if window.left_top_x < L2_min_x:
            L2_min_x = window.left_top_x
        if window.height + window.left_top_y > L2_total_height:
            L2_total_height = window.height + window.left_top_y

    workers = [0]*len(windows)
    l2window_rectangles_temp = []
    l2window_workers_temp = []
    for i in range(len(windows)):
        l2window_rectangles_temp.append(sg.Button(f'{i}', size=(l2button_width, l2button_height), button_color='red'))

    for i in range(len(windows)):
        l2window_workers_temp.append(sg.Text(f'', size=(l2button_width, 1), justification='center'))

    layout1 = [
        [sg.Text(f'number of unresolved windows: {len(windows)}', key='unresolved', font=("Helvetica", 15))],
        [sg.Text(f'', key='msg', size=(22, 1), font=("Helvetica", 15))],
        [*l2window_rectangles_temp],
        [*l2window_workers_temp],
        [sg.Text(f'', size=(15, 1), key='out')],
        [sg.Button(f'OK', size=(4, 1)), sg.Exit()]
    ]

    global sg_gui_temp
    sg_gui_temp = sg.FlexForm(title=")", layout=layout1, size=(app_height, app_width),
                         location=(L2_min_x, L2_total_height))


    window_input_msg_box = ['choose fisher windows', 'choose buffer windows', 'choose supplier windows', 'choose teleporter windows']

    windows_left = len(windows)

    sg_gui_temp.Read(timeout=0)

    index_list = []
    counter = 0
    l2window_workers = [0]*len(windows)
    l2attempt_counter = [0]*len(windows)

    for out_msg in window_input_msg_box:
        sg_gui_temp['msg'].Update(out_msg)
        while True:
            if windows_left <= 0:
                break
            event, values = sg_gui_temp.Read()
            if event == sg.WIN_CLOSED or event == 'Exit':
                sg_gui_temp.Close()
                return False
            for i in range(len(windows)):
                temp = f'{i}'
                if event == temp:
                    if out_msg == 'choose fisher windows':
                        windows_f.append(windows[i])
                        l2window_workers_temp[i].Update('fisher')
                        workers[i] = 'fisher'
                        windows_left -= 1
                        l2window_workers[i] = sg.Text(f'{workers[i]}_{counter}', size=(l2button_width, 1), justification='center')
                        l2attempt_counter[i] = sg.Text(f'', size=(l2button_width, 1), justification='center', key=f'fisher_{counter}')
                        # l2window_workers.append(sg.Text(f'{workers[i]}_{counter}', size=(l2button_width, 1), justification='center'))
                        counter += 1
                    if out_msg == 'choose buffer windows':
                        windows_b.append(windows[i])
                        l2window_workers_temp[i].Update('buffer')
                        workers[i] = 'buffer'
                        windows_left -= 1
                    if out_msg == 'choose supplier windows':
                        windows_s.append(windows[i])
                        l2window_workers_temp[i].Update('supplier')
                        workers[i] = 'supplier'
                        windows_left -= 1
                    if out_msg == 'choose teleporter windows':
                        windows_t.append(windows[i])
                        l2window_workers_temp[i].Update('teleporter')
                        workers[i] = 'teleporter'
                        windows_left -= 1

                    if workers[i] != 'fisher':
                        # l2window_workers.append(sg.Text(f'{workers[i]}', size=(l2button_width, 1), justification='center'))
                        l2window_workers[i] = sg.Text(f'{workers[i]}', size=(l2button_width, 1), justification='center')
                        l2attempt_counter[i] = sg.Text(f'', size=(l2button_width, 1), justification='center')


                    sg_gui_temp['unresolved'].Update(f'number of unresolved windows: {windows_left}')
                    index_list.append(i)
                    sg_gui_temp[temp].Update(disabled=True)
                    if windows_left <= 0:
                        break
            if event == 'OK':
                break

    layout1 = []

    # counter = 0
    for i in range(len(windows)):
        l2window_rectangles.append(sg.Button(f'WINDOW_{i}', size=(l2button_width, l2button_height), button_color='red'))

    sg_gui_temp['msg'].Update('')
    sg_gui_temp.Read(timeout=1)
    return True
        # if workers[i] == 'fisher':
        #     pass
        #     l2window_workers.append(sg.Text(f'{workers[i]}_{index_list[i]}', size=(l2button_width, 1), justification='center'))
        #     counter += 1
        # else:
        #     l2window_workers.append(sg.Text(f'{workers[i]}', size=(l2button_width, 1), justification='center'))

def gui_window2():
    # global app_height
    # global app_width
    # global l2window_rectangles
    # global l2window_workers
    # global l2attempt_counter
    # global L2_total_height
    # global L2_min_x
    sg_gui_temp.Close()
    layout2 = [
        [*l2window_rectangles],
        [*l2window_workers],
        [*l2attempt_counter],
        [sg.Exit()]
    ]
    sg_gui = sg.FlexForm(title="PIDAR RADAR", layout=layout2, size=(app_height, app_width),
                         location=(L2_min_x, L2_total_height))
    sg_gui.Read(timeout=0)
    return sg_gui

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
    list_window_names()  # СПИСОК ВСЕХ ДОСТУПНЫХ ОКОН
    # list_all_windows = get_window_param()

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
    msg = input('y - Запустить сервер на этой машине\nn - Ничего не делать\n')
    if msg == 'y' or msg == 'н':

        server = Server(123)
        server_process = Process(target=server.server_start)
        server_process.start()
        # return None
    # elif msg == 'c' or msg == 'c':
    #     connected_bots = []
    #     for bot_id in bots_id_list:
    #         client = Client(bot_id)
    #         client_process = Process(target=client.connect_to_server)
    #         client_process.start()
    #         connected_bots.append(client)
    #     return connected_bots
    else:
        pass
        # return None

def collapse(layout, key, visible):
    """
    Helper function that creates a Column that can be later made hidden, thus appearing "collapsed"
    :param layout: The layout for the section
    :param key: Key used to make this section visible / invisible
    :param visible: visible determines if section is rendered visible or invisible on initialization
    :return: A pinned column that can be placed directly into your layout
    :rtype: sg.pin
    """
    return sg.pin(sg.Column(layout, key=key, visible=visible, pad=(0, 0)))


if __name__ == '__main__':

    print('PROGRAM start--------------------------------------\n')

    l2window_name = 'Asterios'  # НАЗВАНИЕ ОКНА, ГДЕ БУДЕТ ВЕСТИСЬ ПОИСК
    # win_capture = ScreenCapture()
    win_capture = WindowCapture(l2window_name)

    queue = ActionQueue()

    # searching running L2 windows
    name_list, hash_list = get_l2windows_param()
    n = len(name_list)
    print('number of l2 windows:', n)
    print('-----')
    if n < 1:
        sys.exit('NO L2 WINDOWS DETECTED. PROGRAM ENDS.......')

    # create n windows L2
    manager = Manager()
    screen_manager = manager.list()

    screen_manager.append(0)

    windows = []

    windows_f = []
    windows_b = []
    windows_s = []
    windows_t = []

    for i in range(n):
        temp_window = L2window(i, win_capture, name_list[i], hash_list[i], screen_manager)
        temp_window.enum_handler()
        windows.append(temp_window)

    # t = threading.Thread(target=gui_run_application, args=(gui(),))
    # t.start()

    # setting created windows to screenshot maker
    win_capture.set_windows(windows)

    # start queueing of tasks
    # Process_queue = Process(target=queue.run, args=())
    # Process_queue.start()

    queue.start()
    # start capturing screenshots

    Process_wincap = Process(target=win_capture.start_capturing, args=(screen_manager,))
    Process_wincap.start()

    delay = 3
    for i in range(delay):
        print(f'The window capturing will start in ........ {delay - i} sec')
        time.sleep(1)



    # t = Telegram()

    if not gui_window1(windows_f, windows_b, windows_s, windows_t):
        Process_wincap.terminate()
        queue.stop()
        global sg_gui_temp
        sg_gui_temp.close()
        sys.exit('GUI EXIT EVENT. PROGRAM ENDS.......')

    # start fishing
    F = FishingService(windows_f, windows_b, windows_s, windows_t, queue)

    # Process_fishingservice = Process(target=F.run)
    # Process_fishingservice.start()
    t = threading.Thread(target=F.run)
    t.start()
    # F.run()
    # F.start_fishing()

    # timer = time.time()
    sg_gui = gui_window2()
    while True:
        event, values = sg_gui.Read(timeout=4)

        for fisher in F.fishers:
            temp = f'fisher_{fisher.fisher_id}'
            sg_gui[temp].update(f'{fisher.attempt_counter[0]}')

        if event == sg.WIN_CLOSED or event == 'Exit':
            break

    t.join()
    Process_wincap.terminate()

    # stop everything
    F.stop()

    del windows
    sg_gui.Close()
    sys.exit('PROGRAM ends ......... BYE BYE BYE BYE BYE BYE')
