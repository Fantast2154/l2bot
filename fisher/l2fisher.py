import threading
import random
from threading import Lock
import time
import win32gui
import cv2
import pyautogui
from system.screen_analyzer import *


class Fisher():

    stopped = None
    library = {}
    last_buff_time = time.time()

    fishing_is_active = 0

    def __init__(self, window, wincap, q):
        self.send_message(f'TEST fisher {window.window_id} created')
        self.wincap = wincap
        self.window = window
        self.fisher_id = window.window_id
        self.current_state = 0
        self.lock = Lock()
        self.q = q

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

    def __del__(self):
        self.send_message(f"TEST fisher {self.fisher_id} destroyed")

    def mouse_move(self, points, click=True, button='LEFT', slow=False, double=False):
        print(points)
        print(type(points))
        offset_x = self.wincap.offset_x
        offset_y = self.wincap.offset_y

        game_x = offset_x
        game_y = offset_y

        [(x_temp, y_temp)] = points

        a = random.randint(-3, 3)
        b = random.randint(-3, 3)

        x = game_x + x_temp + a
        y = game_y + y_temp + b

        self.lock.acquire()

        time.sleep(0.01)
        pyautogui.moveTo(x, y)
        time.sleep(0.02)
        pyautogui.mouseDown()
        time.sleep(0.02)
        pyautogui.mouseUp()
        time.sleep(0.03)

        self.lock.release()

    def skills_thread_processing(self, skill_pos, click=True, button='LEFT', slow=False, double=False):

        t = Thread(target=self.mouse_move, args=[skill_pos])
        # t.daemon = True
        t.start()

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
        self.screenshot = self.wincap.get_screenshot(self.window)
        try:
            for key in self.library:
                self.library[key][1] = self.library[key][0].find(self.screenshot)
        except:
            pass

    def get_status(self):
        return self.current_state

    def overweight_baits_soski_correction(self, m_send_counter, m_receive_counter):
        pass

    def start_fishing(self):
        # delay = 3
        # for i in range(delay):
        #     print(f'Fisher {self.fisher_id} will start in ........ {delay - i} sec')
        #     time.sleep(1)
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
        print('fishing')
        self.q.put(self.skills_thread_processing([(100, 100)]))

    def fishing_window(self):

        self.fishing_is_active = True
        return [(50, 50)]

    def pumping(self, count):
        pass

    def reeling(self, count):
        pass

    def blue_bar(self):
        pass

    def red_bar(self):
        pass

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
