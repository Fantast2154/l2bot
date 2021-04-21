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
    last_buff_time = time.time()
    fishing_is_active = 0
    screenshot = None
    screenshot_fishing_window = None
    screenshot_fishing_blue_bar = None
    screenshot_fishing_red_bar = None
    screenshot_fishing_clock = None

    # timers
    timer_start_fishing = 0

    #pos
    clock_pos = None
    fishing_window_pos = None
    red_bar_pos = None
    blue_bar_pos = None

    #fishing_params
    day_time = True
    max_rest_time = 1

    def __init__(self, window, wincap, q):
        self.send_message(f'TEST fisher {window.window_id} created')
        self.wincap = wincap
        self.window = window
        self.fisher_id = window.window_id
        self.current_state = 0
        self.lock = Lock()
        self.q = q
        self.counter = 0

        self.image_database = [
        ['fishing', '../images/fishing.jpg', 0.8],
        ['pumping', '../images/pumping.jpg', 0.87],
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
        self.screenshot = self.wincap.get_screenshot(self.fisher_id)
        return self.screenshot

    def update_day_screen(self):
        self.screenshot_fishing_window = self.wincap.get_screenshot(self.fisher_id)
        self.screenshot_fishing_clock = self.wincap.get_screenshot(self.fisher_id)
        self.screenshot_fishing_blue_bar = self.wincap.get_screenshot(self.fisher_id)

    def update_night_screen(self):
        self.screenshot_fishing_window = self.wincap.get_screenshot(self.fisher_id)
        self.screenshot_fishing_clock = self.wincap.get_screenshot(self.fisher_id)
        self.screenshot_fishing_blue_bar = self.wincap.get_screenshot(self.fisher_id)
        self.screenshot_fishing_red_bar = self.wincap.get_screenshot(self.fisher_id)

    @classmethod
    def send_message(cls, message):
        print(message)

    def init_images(self):
        for obj in self.image_database:
            try:
                self.library[f'{obj[0]}'] = [Vision(obj[1], obj[2]), None]
                print([Vision(obj[1], obj[2]), None])
            except:
                pass
                # print('Error finding images')

    def init_search(self):
        try:
            for key in self.library:
                self.library[key][1] = self.library[key][0].find(self.update_full_screen())
        except:
            pass

    def init_params(self):
        self.day_time = True
        self.max_rest_time = 1
        self.timer_start_fishing = time.time()
        self.fishing_window_pos = []

    def get_status(self):
        return self.current_state

    def overweight_baits_soski_correction(self, m_send_counter, m_receive_counter):
        pass

    def resting(self):
        return time.time() - self.timer_start_fishing

    def start_fishing(self):
        # delay = 3
        # for i in range(delay):
        #     print(f'Fisher {self.fisher_id} will start in ........ {delay - i} sec')
        #     time.sleep(1)
        # self.init_search()
        self.send_message(f'TEST fisher {self.fisher_id} starts fishing\n')

        # before start fishing
        #click buff
        self.last_buff_time = time.time()

    def stop_fishing(self):
        # before stop fishing
        self.send_message(f'TEST fisher {self.fisher_id} has finished fishing\n')

    def buff_is_active(self):
        if time.time() - self.last_buff_time < 30:
            return False
        else:
            return True

    def fishing(self):
        # print('fishing')
        x = self.window.left_top_x + 100
        y = self.window.left_top_y + 100
        self.q.put(self.mouse_move([(x, y)]))
        print(f'fisher {self.fisher_id} is fishing')

    def fishing_window(self):
        # get screenshot
        # find window
        self.fishing_is_active = True

        return self.fishing_window_pos

    def pumping(self, count):
        pass

    def reeling(self, count):
        pass

    def clock(self):
        # get_screenshot
        # find clock
        self.clock_pos = None
        return self.clock_pos

    def blue_bar(self):
        # get_screenshot
        # find blue_bar
        self.blue_bar_pos = None
        return self.blue_bar_pos

    def red_bar(self):
        # get_screenshot
        # find red_bar
        self.red_bar_pos = None
        return self.red_bar_pos

    def turn_on_soski(self):
        pass

    def choose_nigtly_bait(self):
        pass

    def choose_daily_bait(self):
        pass

    def send_mail(self):
        pass

    def send_trade(self):
        pass

    def receive_trade(self):
        pass

    def receive_mail(self):
        pass

    def change_bait(self):
        pass
