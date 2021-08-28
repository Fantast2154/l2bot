import time

import keyboard
import pyperclip

from system.screen_analyzer import *
from system.l2window import L2window
import cv2


class Login:
    library = {}
    screenshot = None
    win_capture = None

    def __init__(self, windows, logins, passwords, q):
        self.send_message(f'login module created')

        self.windows = windows
        self.q = q
        self.library = {}

        self.logins = {}
        self.passwords = {}
        log = iter(logins)
        pas = iter(passwords)

        for window in self.windows:
            self.logins[window.hwnd] = next(log)
            self.passwords[window.hwnd] = next(pas)

        self.win_capture = None
        self.accurate_search = False
        self.screenshot_accurate = None
        self.init_image_database = [
            # ['1st', 'images/login/stages/1st.jpg', 0.77],
            # ['2nd', 'images/login/stages/2nd.jpg', 0.77],
            # ['3rd', 'images/login/stages/3rd.jpg', 0.77],
            # ['4th', 'images/login/stages/4th.jpg', 0.87],
            ['logging', 'images/login/stages/logging.jpg', 0.6],
            ['login', 'images/login/stages/login.jpg', 0.95],
            ['login_field', 'images/login/stages/login_field2.jpg', 0.99],
            ['pass_field', 'images/login/stages/pass_field2.jpg', 0.97],
            ['select', 'images/login/stages/select.jpg', 0.6],
            ['server', 'images/login/stages/server.jpg', 0.6],
            ['terms', 'images/login/stages/terms.jpg', 0.6],
            ['character', 'images/login/stages/character.jpg', 0.6]]

        self.init_images()

        self.stages()

    def __del__(self):
        self.send_message(f"login module destroyed")

    def stages(self):
        error_found = False
        stage1 = self.stage_one()
        self.stage_two_four()

    def stage_one(self):
        for window in self.windows:
            login = self.find('login', window)
            if login:
                login_field = self.find('login_field', window)
                pass_field = self.find('pass_field', window)
                self.login(window, login_field, pass_field)
            else:
                return False

    def stage_two_four(self):
        for _ in range(3):
            for window in self.windows:
                self.q.new_task('mouse',
                                [[(100, 100)], True, 'LEFT', False, False, False],
                                window)
                time.sleep(1)
                keyboard.send('enter')
                time.sleep(0.2)

    def login(self, window, login_field, pass_field):
        # print('login_field', login_field)
        self.q.new_task('mouse',
                        [login_field, True, 'LEFT', False, False, False],
                        window)
        time.sleep(0.1)
        self.q.new_task('mouse',
                        [login_field, True, 'LEFT', False, 'double', False],
                        window)
        time.sleep(1)
        pyperclip.copy(self.logins[window.hwnd])
        # print('login', self.logins[window.hwnd])
        time.sleep(0.1)
        keyboard.send('ctrl+v')
        time.sleep(1)
        # print('pass_field', pass_field)
        self.q.new_task('mouse',
                        [pass_field, True, 'LEFT', False, False, False],
                        window)
        time.sleep(0.1)
        self.q.new_task('mouse',
                        [pass_field, True, 'LEFT', False, 'double', False],
                        window)
        time.sleep(1)
        pyperclip.copy(self.passwords[window.hwnd])
        # print('password', self.passwords[window.hwnd])
        time.sleep(0.1)
        keyboard.send('ctrl+v')
        time.sleep(0.5)
        keyboard.send('enter')
        time.sleep(1)

    def update_screenshot(self, window):
        while True:
            screenshot = window.screenshot
            if not screenshot[0]:
                continue
            hwnd = window.hwnd

            # print(screenshot)
            temp = screenshot[-1][hwnd][0]
            if len(temp) != 0:
                return temp
            else:
                return []

    def send_message(cls, message):
        print(message)

    def find(self, object, window):  # returns list of positions
        # try:
        position = self.library[object][0].find(self.update_screenshot(window))
        return position
        # except KeyError:
        #     self.send_message(f'find function ERROR object search')
        #     self.send_message(f'{KeyError}')
        #     return []

    def init_images(self):
        for obj in self.init_image_database:
            try:
                self.library[f'{obj[0]}'] = [Vision(obj[1], obj[2]), None]
            except:
                print('Error finding images')


class RelaunchWindow(L2window):
    library = {}
    screenshot = None
    win_capture = None

    def __init__(self, window_id, wincap, window_name, hwnd):
        super().__init__(window_id, wincap, window_name, hwnd)
        self.send_message(f'TEST FishingWindow {window_id} created')
        self.wincap = wincap
        self.screenshot = wincap.get_screenshot(window_id)
        self.window_id = window_id
        self.hwnd = hwnd

    def __del__(self):
        self.send_message(f"RelaunchWindow destroyed")

    def update_screenshot(self):
        self.screenshot = self.wincap.get_screenshot(self.window_id)

    @classmethod
    def send_message(cls, message):
        print(message)

    def find(self, objects):  # returns list of positions
        try:
            screenshot = self.wincap.get_screenshot(self.window_id)
            # position = object.find(screenshot)
            position = [(1, 1)]
            return position
        except:
            print('ERROR finding', objects)
            return []

    def init_images(self):
        for obj in self.image_database:
            try:
                self.library[f'{obj[0]}'] = [Vision(obj[1], obj[2]), None]
            except:
                print('Error finding images')

    def init_search(self):
        self.screenshot = self.wincap.get_screenshot(self.window_id)
        try:
            for key in self.library:
                self.library[key][1] = self.library[key][0].find(self.screenshot)
        except:
            pass
