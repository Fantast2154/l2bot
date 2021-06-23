from system.screen_analyzer import *
from system.l2window import L2window
import cv2


class FishingWindow(L2window):
    library = {}
    screenshot = None
    win_capture = None

    def __init__(self, window_id, wincap, window_name, hwnd):
        super().__init__(window_id, wincap, window_name, hwnd)
        self.wincap = wincap
        # self.screenshot = wincap.get_screenshot(window_id)

        self.hwnd = hwnd
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

        self.vision_catcheditem_pos = [None] * 4
        self.send_message(f'<-L2window created')
        # self.init_images()
        # self.init_search()

    def __del__(self):
        self.send_message(f"destroyed")

    def update_screenshot(self):
        self.screenshot = self.wincap.get_screenshot(self.hwnd)

    def send_message(self, message):
        temp = 'FishingWindow' + f' {self.window_id}' + ': ' + message
        print(temp)

    def find(self, objects):  # returns list of positions
        try:
            screenshot = self.wincap.get_screenshot(self.hwnd)
            # position = object.find(screenshot)
            position = [(1, 1)]
            return position
        except:
            self.send_message('ERROR finding')
            return []

    def init_images(self):
        for obj in self.image_database:
            try:
                self.library[f'{obj[0]}'] = [Vision(obj[1], obj[2]), None]
            except:
                self.send_message('Error finding images')

    def init_search(self):
        self.screenshot = self.wincap.get_screenshot(self.hwnd)
        try:
            for key in self.library:
                self.library[key][1] = self.library[key][0].find(self.screenshot)
        except:
            self.send_message('Error init search')
