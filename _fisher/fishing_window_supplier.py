from system.screen_analyzer import *
from system.l2window import L2window
import cv2
import time


class FishingSupplierWindow(L2window):

    def __init__(self, window_id, wincap, window_name, hwnd, screenshot):
        super().__init__(window_id, wincap, window_name, hwnd, screenshot)
        self.screenshot = screenshot

        self.hwnd = hwnd
        self.library = {}

        self.win_capture = None
        self.accurate_search = False
        self.screenshot_accurate = None
        self.init_image_database = [
            ['fishing', 'images/fishing.jpg', 0.87]]

        self.extended_image_database = [
            ['map_button', 'images/map.jpg', 0.9],
            ['equipment_bag', 'images/equipment_bag.jpg', 0.6],
            ['menu', 'images/menu.jpg', 0.6],
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
            ['claim_items_button', 'images/claim_items_button.jpg', 0.8]]

        self.vision_catcheditem_pos = [None] * 4
        self.send_message(f'<-L2window created')

        self.init_images()

    def update_screenshot(self):
        temp = self.screenshot[-1][self.hwnd][0]
        if len(temp) != 0:
            return temp
        else:
            return []

    def send_message(self, message):
        temp = 'FishingSupplierWindow' + f' {self.window_id}' + ': ' + message
        print(temp)

    def find(self, object):  # returns list of positions
        try:
            position = self.library[object][0].find(self.update_screenshot())
            return position
        except KeyError:
            self.send_message(f'find function ERROR object search')
            self.send_message(f'{KeyError}')
            return []

    def is_fishing_window(self):
        temp = self.find('fishing_window')
        if temp:
            return True
        else:
            return False

    def init_images(self):
        for obj in self.init_image_database:
            try:
                self.library[f'{obj[0]}'] = [Vision(obj[1], obj[2]), None]
            except:
                self.send_message('Error finding images1')

        for obj in self.extended_image_database:
            try:
                self.library[f'{obj[0]}'] = [Vision(obj[1], obj[2]), None]
            except:
                self.send_message('Error finding images2')

    def get_object(self, name, search=False):
        if self.library[name][0]:
            pass
        else:
            temp = 'ERROR referring to the unknown object: ' + name
            self.send_message(temp)
            return False

        if search:
            pos = self.library[name][0].find(self.update_screenshot())
            if pos:
                self.library[name][1] = pos
                return pos
            else:
                return []
        else:
            return self.library[name][1]

    def init_search(self):
        try:
            for key in self.init_image_database:
                temp = self.library[key[0]][0].find(self.update_screenshot())
                if not temp:
                    self.send_message(f'Error init search object: {key}')
                    return False
                else:
                    self.library[key[0]][1] = temp
            return True
        except:
            self.send_message('Error init search')
            return False