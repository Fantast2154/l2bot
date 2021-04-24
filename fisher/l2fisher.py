import threading
import random
from threading import Lock
import time
import cv2
import pyautogui
import keyboard
from system.screen_analyzer import *
import win32api
import win32con


class Fisher:
    stopped = None
    library = {}

    screenshot = None
    screenshot_fishing_window = None
    screenshot_fishing_blue_bar = None
    screenshot_fishing_red_bar = None
    screenshot_fishing_clock = None

    # timers
    timer_start_fishing = 0
    max_rest_time = 1
    timer_last_buff = time.time()

    # pos
    clock_pos = None
    fishing_window_pos = None
    red_bar_pos = None
    blue_bar_pos = None

    # fishing_params
    day_time = True
    fishing_is_active = 0
    x_border = 0
    y_border = 0
    current_bait = 0  # 0 = day, 1 = night
    mail_send_constant = 800
    mail_receive_constant = 1000
    mail_send_counter = 0
    mail_receive_counter = 0

    # Boolean parameters
    # fishing_window_first_check = False

    def __init__(self, window, wincap, q):
        self.send_message(f'TEST fisher {window.window_id} created')
        self.wincap = wincap
        self.window = window
        self.fisher_id = window.window_id
        self.q = q
        self.lock = Lock()
        self.current_state = 0

        self.counter = 0

        self.image_database = [
            ['fishing', 'images/fishing.jpg', 0.8],
            ['pumping', 'images/pumping.jpg', 0.87],
            ['reeling', 'images/reeling.jpg', 0.87],
            ['blue_bar', 'images/blue_bar2.jpg', 0.8],
            ['clock', 'images/clock3.jpg', 0.8],
            ['fishing_window', 'images/fishing_window.jpg', 0.7],
            ['red_bar', 'images/red_bar3.jpg', 0.8],
            ['cdbuff', 'images/cdbuff.jpg', 0.87],
            ['bait', 'images/bait.jpg', 0.90],
            ['colored', 'images/colored_2.jpg', 0.94],
            ['luminous', 'images/luminous_2.jpg', 0.94],
            ['soski', 'images/soski.jpg', 0.95],
            ['soski_activated', 'images/soski_activated.jpg', 0.78],
            ['map_button', 'images/map.jpg', 0.9],
            ['sun', 'images/sun2.jpg', 0.7],
            ['moon', 'images/moon2.jpg', 0.7],
            ['disconnect_EN', 'images/disconnect_EN.jpg', 0.4],
            ['menu', 'images/menu.jpg', 0.6],
            ['equipment_bag', 'images/equipment_bag.jpg', 0.6],
            ['weight_icon', 'images/weight.jpg', 0.9],
            ['login', 'images/login.jpg', 0.95],
            ['mailbox', 'images/mailbox.jpg', 0.8],
            ['sendmail_button', 'images/sendmail_button.jpg', 0.8],
            ['send_button', 'images/send_button.jpg', 0.8],
            ['confirm_button', 'images/confirm_button.jpg', 0.8],
            ['claim_items_button', 'images/claim_items_button.jpg', 0.8],
            ['catched_item_0', 'images/catcheditem1.jpg', 0.7],
            ['catched_item_1', 'images/catcheditem2.jpg', 0.7],
            ['catched_item_2', 'images/catcheditem3.jpg', 0.7],
            ['catched_item_3', 'images/catcheditem4.jpg', 0.7]]

        self.fishing_is_active = False
        self.init_images()
        self.init_params()

    def __del__(self):
        self.send_message(f"TEST fisher {self.fisher_id} destroyed")

    def init_search(self):
        # try:
        for key in self.library:
            print(key)
            self.library[key][1] = self.library[key][0].find(self.update_full_screen())
        # except:
        # pass

    def init_params(self):
        self.day_time = True
        self.max_rest_time = 1
        self.timer_start_fishing = time.time()
        self.timer_last_buff = time.time()
        self.fishing_window_pos = []
        self.x_border = 0
        self.y_border = 0
        self.current_bait = 0
        self.mail_send_constant = 800
        self.mail_receive_constant = 1000
        self.mail_send_counter = 0
        self.mail_receive_counter = 0

    @classmethod
    def send_message(cls, message):
        print(message)

    def mouse_move(self, points, click=True, button='LEFT', slow=False, double=False):
        self.window.activate_window()
        # print(points)
        # print(type(points))
        offset_x = self.wincap.offset_x
        offset_y = self.wincap.offset_y

        game_x = offset_x
        game_y = offset_y

        [(x_temp, y_temp)] = points

        a = random.randint(-3, 3)
        b = random.randint(-3, 3)

        x = game_x + x_temp + a
        y = game_y + y_temp + b

        # self.lock.acquire()

        # keyboard.send('k')
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

        # self.lock.release()

    def skills_thread_processing(self, skill_pos, click=True, button='LEFT', slow=False, double=False):
        self.window.activate_window()
        t = Thread(target=self.mouse_move, args=[skill_pos])
        # t.daemon = True
        t.start()

    def fisher_action(self):
        pass

    def update_full_screen(self):
        print(len(self.wincap.imgs))
        self.screenshot = self.wincap.capture_screen()[self.fisher_id]
        return self.screenshot

    def update_day_screen(self):

        self.wincap.accurate = True

        self.screenshot_fishing_window = self.wincap.fishing_window_pos_screenshots[self.fisher_id]
        self.screenshot_fishing_clock = self.wincap.clock_pos_screenshots[self.fisher_id]
        self.screenshot_fishing_blue_bar = self.wincap.blue_bar_pos_screenshots[self.fisher_id]

    def update_night_screen(self):

        self.wincap.accurate = True
        self.screenshot_fishing_window = self.wincap.fishing_window_pos_screenshots[self.fisher_id]
        self.screenshot_fishing_clock = self.wincap.clock_pos_screenshots[self.fisher_id]
        self.screenshot_fishing_blue_bar = self.wincap.blue_bar_pos_screenshots[self.fisher_id]
        self.screenshot_fishing_red_bar = self.wincap.red_bar_pos_screenshots[self.fisher_id]

    def fishing_window_first_check_func(self):
        # if not self.fishing_window_first_check:
        #     while not self.fishing_window_first_check:
        print('self.library', self.library)
        fishing_pos = self.library['fishing'][1]
        # skills_thread_processing(fishing_pos, slow=True)
        # self.mouse_move(fishing_pos, slow=True)
        time.sleep(1.5)
        screenshot = self.update_full_screen()
        cv2.imshow('Sc', screenshot)
        cv2.waitKey(1)
        fishing_window_coordinates_and_size = self.library['fishing_window'][0].find(screenshot,
                                                                                     coordinates_and_sizes=True)

        if fishing_window_coordinates_and_size:
            # print('fishing_window_coordinates_and_size', fishing_window_coordinates_and_size)
            [(x_fishwin, y_fishwin, w_fishwin, h_fishwin)] = fishing_window_coordinates_and_size
            # self.fishing_window_first_check = True
            # print('fishing_window_first_check', self.fishing_window_first_check)
            # self.mouse_move(fishing_pos, slow=True)
            return x_fishwin, y_fishwin, w_fishwin, h_fishwin
        else:
            if self.day_time:
                pass
                # self.mouse_move(bait_colored, slow=True)
            else:
                pass
                # self.mouse_move(bait_luminous, slow=True)
            # continue

    def init_images(self):
        print('self.image_database', self.image_database)
        for obj in self.image_database:
            # try:
            # print('obj', obj)
            # print('obj[0]', obj[0])
            # print('self.library', self.library)
            # print('self.library[obj[0]]', self.library[obj[0]])
            self.library[obj[0]] = [Vision(obj[1], obj[2]), None]
            print([Vision(obj[1], obj[2]), None])
            # except:
            # pass
            # print('Error finding images')

    def get_status(self):
        return self.current_state

    def mail_counters_correction(self):
        pass

    def resting(self):
        return time.time() - self.timer_start_fishing

    def start_fishing(self):
        # delay = 3
        # for i in range(delay):
        #     print(f'Fisher {self.fisher_id} will start in ........ {delay - i} sec')
        #     time.sleep(1)
        # self.init_search()
        self.send_message(f'TEST fisher {self.fisher_id} init\n')

        # before start fishing
        # click buff
        self.rebuff()
        self.choose_night_bait()
        self.choose_day_bait()

        x_fishwin, y_fishwin, w_fishwin, h_fishwin = self.fishing_window_first_check_func()
        self.wincap.set_fishing_window(self.fisher_id, x_fishwin, y_fishwin, w_fishwin, h_fishwin)

    def stop_fishing(self):
        # before stop fishing
        self.send_message(f'TEST fisher {self.fisher_id} has finished fishing\n')

    def is_not_fishing_too_long(self):
        if time.time() - self.timer_start_fishing > 20:
            return True
        else:
            return False

    def rebuff_time(self):
        if time.time() - self.timer_last_buff > 1140:
            return True
        else:
            return False

    def rebuff(self):
        self.send_message(f'TEST fisher {self.fisher_id} rebuff ---------------------------------\n')

    def fishing_window(self):
        # get screenshot
        # find window
        # if self.fishing_window_pos:
        #     self.timer_start_fishing = time.time()
        # self.fishing_is_active = True
        return self.fishing_window_pos

    def clock(self):
        # get_screenshot
        # find clock
        return self.clock_pos

    def blue_bar(self):
        # get_screenshot
        # find blue_bar
        # x = self.window.left_top_x + 250
        # y = self.window.left_top_y + 250
        # self.blue_bar_pos = [(x, y)]
        return self.blue_bar_pos

    def red_bar(self):
        # get_screenshot
        # find red_bar
        self.red_bar_pos = None
        return self.red_bar_pos

    def pumping(self, count):
        pass

    def fishing(self):
        self.send_message(f'TEST fisher {self.fisher_id} CLICK start fishing\n')

    def reeling(self, count):
        pass

    def daytime(self):
        return self.day_time

    def turn_on_soski(self):
        # check soski
        return True

    def choose_night_bait(self):
        self.current_bait = 1
        # click night bait

    def choose_day_bait(self):
        self.current_bait = 0
        # click day bait

    def change_bait(self):
        if self.current_bait == 0:
            self.current_bait = 1
        else:
            self.current_bait = 0

    def send_trade(self):
        return True

    def receive_trade(self):
        return True

    def send_mail(self):
        return True

    def receive_mail(self):
        return True

    def open_close_bag(self):
        return True

    def check_overweight(self):
        count = 100  # test
        return count

    def check_dbaits_count(self):
        count = 100  # test
        return count

    def check_nbaits_count(self):
        count = 100  # test
        return count

    def check_soski_count(self):
        count = 100  # test
        return count


class Trader:

    @classmethod
    def send_message(cls, message):
        print(message)

    def __init__(self, window, wincap, q):
        self.send_message(f'TEST trader {window.window_id} created')
        self.wincap = wincap
        self.window = window
        self.trader_id = window.window_id
        self.q = q
        self.lock = Lock()
