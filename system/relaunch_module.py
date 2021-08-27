from system.screen_analyzer import *
from system.l2window import L2window
import cv2


class Login:
    library = {}
    screenshot = None
    win_capture = None

    def __init__(self, windows, logins, passwords, q):
        self.send_message(f'login module created')
        self.logins = logins
        self.passwords = passwords

        self.windows = windows
        self.q = q
        self.library = {}

        self.win_capture = None
        self.accurate_search = False
        self.screenshot_accurate = None
        self.init_image_database = [
            ['1st', 'images/login/stages/1st.jpg', 0.77],
            ['2nd', 'images/login/stages/2nd.jpg', 0.77],
            ['3rd', 'images/login/stages/3rd.jpg', 0.77],
            ['4th', 'images/login/stages/4th.jpg', 0.87],
            ['logging', 'images/login/stages/logging.jpg', 0.6],
            ['login', 'images/login/stages/login.jpg', 0.6],
            ['login_field', 'images/login/stages/login_field2.jpg', 0.95],
            ['pass_field', 'images/login/stages/pass_field2.jpg', 0.95],
            ['select', 'images/login/stages/select.jpg', 0.6],
            ['server', 'images/login/stages/server.jpg', 0.6],
            ['terms', 'images/login/stages/terms.jpg', 0.6],
            ['character', 'images/login/stages/character.jpg', 0.6],
            ['logging', 'images/login/stages/logging.jpg', 0.7]]

        self.init_images()
        self.stages()

    def __del__(self):
        self.send_message(f"login module destroyed")

    def stages(self):
        error_found = False
        stage0 = self.stage_zero()

    def stage_zero(self):
        for window in self.windows:
            stage0 = self.find('1st', window.hwnd)
            if stage0:
                self.q.new_task('mouse',
                                [self.find('fishing', window.id), True, 'LEFT', False, False, False],
                                window)
            else:
                return False

    def update_screenshot(self, id):
        screenshot = self.windows[id].screenshot
        hwnd = self.windows[id].hwnd
        temp = screenshot[-1][hwnd][0]
        if len(temp) != 0:
            return temp
        else:
            return []

    def send_message(cls, message):
        print(message)

    def find(self, object, id):  # returns list of positions
        try:
            position = self.library[object][0].find(self.update_screenshot(id))
            return position
        except KeyError:
            self.send_message(f'find function ERROR object search')
            self.send_message(f'{KeyError}')
            return []

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
        self.send_message(f"TEST FishingWindow {self.window_id} destroyed")

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
