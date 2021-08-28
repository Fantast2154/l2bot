import time
from multiprocessing import Manager, Process
import PySimpleGUI as sg
import win32gui
import threading


class Gui_interface:

    def __init__(self, windows):
        manager = Manager()
        self.index = []
        self.l2window_workers = []
        self.l2window_rectangles = []
        self.workers = [0] * len(windows)
        self.windows_f = []
        self.windows_b = []
        self.windows_s = []
        self.windows_t = []

        self.windows = windows
        self.L2_total_height = 0
        self.L2_min_x = 10000
        self.l2button_width = 12
        self.l2button_height = 6
        self.app_height = 285
        self.app_base_width = 650

        self.l2attempt_counter = manager.list()

        for window in windows:
            if window.left_top_x < self.L2_min_x:
                self.L2_min_x = window.left_top_x
            if window.height + window.left_top_y > self.L2_total_height:
                self.L2_total_height = window.height + window.left_top_y

        for i in range(len(self.windows)):
            self.l2window_rectangles.append(
                sg.Button(f'{i}', size=(self.l2button_width, self.l2button_height), button_color='red'))

        for i in range(len(self.windows)):
            self.l2window_workers.append(sg.Text(f'', size=(self.l2button_width, 1), justification='center'))

        for i in range(len(self.windows)):
            self.l2attempt_counter.append(sg.Text(f'', size=(self.l2button_width, 1),
                                                  justification='center', key=f'attempt_counter_{i}'))

        layout = [
            [sg.Text(f'', key='1_txt_field', size=(22, 1), font=("Helvetica", 13))],
            [*self.l2window_rectangles, sg.Button(f'OK', size=(4, 1)), sg.Button('Exit'),
             sg.Button('Relaunch windows', visible=False)],
            [*self.l2window_workers],
            [*self.l2attempt_counter],
            [sg.Text(f'number of unresolved windows: {len(self.windows)}', size=(200, 1), font=("Helvetica", 13),
                     key='2_txt_field')],
            [sg.Text(f' ', key='3_txt_field', size=(200, 1), font=("Helvetica", 12))],
        ]

        self.sg_gui = sg.FlexForm(title="PIDAR RADAR", layout=layout, size=(
            self.app_base_width, self.app_height),
                                  location=(self.L2_min_x, self.L2_total_height))

    def gui_window(self):

        window_input_msg_box = ['choose fisher windows', 'choose buffer windows', 'choose supplier windows',
                                'choose teleporter windows']

        windows_left = len(self.windows)

        self.sg_gui.Read(timeout=0)

        counter = 0

        for out_msg in window_input_msg_box:
            self.sg_gui['1_txt_field'].Update(out_msg)
            while True:
                if windows_left <= 0:
                    break
                event, values = self.sg_gui.Read()
                if event == sg.WIN_CLOSED or event == 'Exit':
                    self.sg_gui.Close()
                    return False
                if event == 'Relaunch windows':
                    self.sg_gui.Close()
                    return False
                for i in range(len(self.windows)):
                    temp = f'{i}'
                    if event == temp:
                        if out_msg == 'choose fisher windows':
                            self.windows_f.append(self.windows[i])
                            self.l2window_workers[i].Update(f'fisher_{counter}')
                            self.workers[i] = f'fisher'
                            self.index.append(i)
                            windows_left -= 1

                            self.l2window_workers[i] = sg.Text(f'{self.workers[i]}_{counter}',
                                                               size=(self.l2button_width, 1), justification='center')
                            self.sg_gui[f'attempt_counter_{i}'].update()

                            counter += 1
                        if out_msg == 'choose buffer windows':
                            self.windows_b.append(self.windows[i])
                            self.l2window_workers[i].Update('buffer')
                            self.workers[i] = 'buffer'
                            windows_left -= 1
                        if out_msg == 'choose supplier windows':
                            self.windows_s.append(self.windows[i])
                            self.l2window_workers[i].Update('supplier')
                            self.workers[i] = 'supplier'
                            windows_left -= 1
                        if out_msg == 'choose teleporter windows':
                            self.windows_t.append(self.windows[i])
                            self.l2window_workers[i].Update('teleporter')
                            self.workers[i] = 'teleporter'
                            windows_left -= 1

                        if self.workers[i] != 'fisher':
                            self.l2window_workers[i] = sg.Text(f'{self.workers[i]}', size=(self.l2button_width, 1),
                                                               justification='center')
                            self.l2attempt_counter[i] = sg.Text(f'', size=(self.l2button_width, 1),
                                                                justification='center')

                        self.sg_gui['2_txt_field'].Update(f'number of unresolved windows: {windows_left}')
                        self.sg_gui[temp].Update(disabled=True)

                        self.sg_gui.Read(timeout=10)
                        if windows_left <= 0:
                            break
                if event == 'OK':
                    break


        self.sg_gui['1_txt_field'].Update('L2 bot "Boy & co"')
        self.sg_gui.Read(timeout=10)

        layout2 = [[sg.Text('Periodic relaunch time (in minutes)')],
                   [sg.Input()],
                   [sg.OK()]]

        window = sg.Window('pip? pip.', layout2, size=(240, 100))

        event, values = window.read()
        output = 60*int(values[0])

        window.close()

        time.sleep(0.8)
        self.sg_gui['Relaunch windows'].Update(visible=True)
        self.sg_gui['2_txt_field'].Update(f'To stop the programm press "alt+q"', font=("Helvetica", 13), visible=True)
        self.sg_gui['3_txt_field'].Update(f'To pause/resume fishers press "alt+w"', font=("Helvetica", 13),
                                          visible=True)
        self.sg_gui.Read(timeout=10)

        user_input = []
        user_input.append(self.windows_f)
        user_input.append(self.windows_b)
        user_input.append(self.windows_s)
        user_input.append(self.windows_t)
        return user_input, output

    def update_window(self, param, *args):
        self.sg_gui[param].Update(*args)
        self.sg_gui.Read(timeout=0)

    def reinit_windows(self, windows):
        self.windows = windows
        user_input = []
        for i in range(len(self.windows_f)):
            id = self.windows_f[i].window_id
            self.windows_f[i].hwnd = windows[id].hwnd
            self.windows_f[i].wincap = windows[id].wincap
            self.windows_f[i].screenshot = windows[id].screenshot

        for i in range(len(self.windows_b)):
            id = self.windows_b[i].window_id
            self.windows_b[i].hwnd = windows[id].hwnd
            self.windows_b[i].wincap = windows[id].wincap
            self.windows_b[i].screenshot = windows[id].screenshot

        for i in range(len(self.windows_s)):
            id = self.windows_s[i].window_id
            self.windows_s[i].hwnd = windows[id].hwnd
            self.windows_s[i].wincap = windows[id].wincap
            self.windows_s[i].screenshot = windows[id].screenshot

        for i in range(len(self.windows_t)):
            id = self.windows_t[i].window_id
            self.windows_t[i].hwnd = windows[id].hwnd
            self.windows_t[i].wincap = windows[id].wincap
            self.windows_t[i].screenshot = windows[id].screenshot

        user_input.append(self.windows_f)
        user_input.append(self.windows_b)
        user_input.append(self.windows_s)
        user_input.append(self.windows_t)
        return user_input

    def set_fishers(self, fishers):
        self.fishers = fishers
