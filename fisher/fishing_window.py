from system.screen_analyzer import *
from system.l2window import L2window
import cv2


class FishingWindow(L2window):
    library = {}
    screenshot = None
    win_capture = None

    def __init__(self, x_left_top, y_left_top, width, height, i, win_capture):
        self.send_message(f'TEST FishingWindow(L2window) calling')
        self.left_top_x = x_left_top
        self.left_top_y = y_left_top
        self.width = width
        self.height = height
        self.win_capture = win_capture
        self.screenshot = win_capture.get_screenshot()

        self.temp = [
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
            ['claim_items_button', 'images/claim_items_button.jpg', 0.8]]
        self.vision_catcheditem_pos = [None] * 4
        self.init_images()
        self.init_search()

    @classmethod
    def send_message(cls, message):
        print(message)

    def init_images(self):
        for obj in self.temp:
            self.library[f'{obj[0]}'] = [Vision(obj[1], obj[2]), None]

    def init_search(self):
        self.screenshot = self.win_capture.get_screenshot()

        for key in self.library:
            self.library[key][1] = self.library[key][0].find(self.screenshot)
