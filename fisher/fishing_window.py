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
        self.init_image_database = [
            ['fishing', 'images/fishing.jpg', 0.8],
            ['pumping', 'images/pumping.jpg', 0.87],
            ['reeling', 'images/reeling.jpg', 0.87],
            ['bait', 'images/bait.jpg', 0.90],
            ['soski', 'images/soski.jpg', 0.95],
            ['map_button', 'images/map.jpg', 0.9],
            ['equipment_bag', 'images/equipment_bag.jpg', 0.6],
            ['menu', 'images/menu.jpg', 0.6]]

        self.extended_image_database = [
            ['blue_bar', 'images/blue_bar2.jpg', 0.8],
            ['colored', 'images/colored_2.jpg', 0.94],
            ['luminous', 'images/luminous_2.jpg', 0.94],
            ['clock', 'images/clock3.jpg', 0.8],
            ['fishing_window', 'images/fishing_window.jpg', 0.7],
            ['red_bar', 'images/red_bar3.jpg', 0.8],
            ['buff', 'images/cdbuff.jpg', 0.87],
            ['soski_activated', 'images/soski_activated.jpg', 0.78],
            ['sun', 'images/sun2.jpg', 0.7],
            ['moon', 'images/moon2.jpg', 0.7],
            ['disconnect_EN', 'images/disconnect_EN.jpg', 0.4],
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
        self.init_images()
        self.init_search()

    def __del__(self):
        self.send_message(f"destroyed")

    def update_screenshot(self):
        self.screenshot = self.wincap.get_screenshot(self.hwnd)
        return self.screenshot

    def send_message(self, message):
        temp = 'FishingWindow' + f' {self.window_id}' + ': ' + message
        print(temp)

    def find(self, object):  # returns list of positions
        try:
            position = self.library[object][0].find(self.update_screenshot())
            return position
        except:
            self.send_message('ERROR object search')
            return []

    def fishing_window(self):
        if self.library['fishing_window'][1]:
            pass
        return self.find('fishing_window')

    def record_fishing_window(self):
        try:
            self.library['fishing_window'][1] = self.find('fishing_window')
            [(x_fishwin, y_fishwin, w_fishwin, h_fishwin)] = self.library['fishing_window'][0].find(self.update_screenshot(), coordinates_and_sizes = True)
            self.wincap.set_fishing_window(self.hwnd, x_fishwin, y_fishwin, w_fishwin, h_fishwin)
            self.wincap.set_accurate_param(True, self.hwnd)
        except:
            self.send_message('Error recording fishing_window')

    def blue_bar(self):
        return self.find('blue_bar')

    def red_bar(self):
        return self.find('red_bar')

    def init_images(self):
        for obj in self.init_image_database:
            try:
                # {'key', [obj, [(x,y]/None]
                self.library[f'{obj[0]}'] = [Vision(obj[1], obj[2]), None]
            except:
                self.send_message('Error finding images1')

        for obj in self.extended_image_database:
            try:
                # {'key', [obj, [(x,y]/None]
                self.library[f'{obj[0]}'] = [Vision(obj[1], obj[2]), None]
            except:
                self.send_message('Error finding images2')

    def get_object(self, name, search=False):
        if name:
            if self.library[name][0]:
                pass
            else:
                temp = 'ERROR referring to the unknown object: ' + name
                self.send_message(temp)
                return []
        else:
            temp = 'ERROR referring to the unknown object: ' + name
            self.send_message(temp)
            return []

        if search:
            object = self.library[name][0].find(self.update_screenshot())
            self.library[name][1] = object
            return object
        else:
            return self.library[name][1]

    def init_search(self):
        self.update_screenshot()
        try:
            for key in self.init_image_database:
                temp = self.library[key[0]][0].find(self.screenshot)
                if not temp:
                    return False
                else:
                    self.library[key[0]][1] = temp
            return True
        except:
            self.send_message('Error init search')
            return False
