from system.screen_analyzer import *
from system.l2window import L2window
import cv2
import time


class FishingBufferWindow(L2window):

    def __init__(self, window_id, wincap, window_name, hwnd, screenshot):
        super().__init__(window_id, wincap, window_name, hwnd, screenshot)
        self.wincap = wincap
        self.screenshot = screenshot

        self.hwnd = hwnd
        self.library = {}

        self.win_capture = None
        self.accurate_search = False
        self.screenshot_accurate = None
        self.init_image_database = [
            ['buff_song', 'images/supporting/song_of_wind.jpg', 0.87]]

        self.extended_image_database = [
            ['map_button', 'images/map.jpg', 0.9],
            ['baits', 'images/trade/bait.jpg', 0.80],
            ['equipment_bag', 'images/equipment_bag.jpg', 0.6],
            ['soski', 'images/items/soski_test.jpg', 0.8],
            ['menu', 'images/menu.jpg', 0.6],
            ['disconnect_EN', 'images/disconnect_EN.jpg', 0.4],
            ['weight_icon', 'images/weight.jpg', 0.9],
            ['login', 'images/login.jpg', 0.95],
            ['mailbox', 'images/mailbox.jpg', 0.8],
            ['sendmail_button', 'images/sendmail_button.jpg', 0.8],
            ['send_button', 'images/send_button.jpg', 0.8],
            ['exchange_menu', 'images/trade/exchange_menu2.jpg', 0.8],
            ['treangle', 'images/trade/treangle.jpg', 0.8],
            ['ok_button', 'images/trade/ok_button.jpg', 0.8],
            ['cancel_button', 'images/trade/cancel_button.jpg', 0.8],
            ['small_bag', 'images/trade/small_bag.jpg', 0.8],
            ['confirm_button', 'images/trade/confirm_button.jpg', 0.7],
            ['trade_request', 'images/trade/trade_request_icon2.jpg', 0.8],
            ['catched_item0', 'images/items/catcheditem0.jpg', 0.8],
            ['catched_item1', 'images/items/catcheditem1.jpg', 0.8],
            ['catched_item2', 'images/items/catcheditem2.jpg', 0.8],
            ['catched_item3', 'images/items/catcheditem3.jpg', 0.8],
            ['claim_items_button', 'images/claim_items_button.jpg', 0.8]
        ]

        self.init_images()
        self.init_search()

    def update_screenshot(self):
        temp = self.screenshot[-1][self.hwnd][0]
        if len(temp) != 0:
            return temp
        else:
            return []

    def update_accurate_screenshot(self, object, coordinates, w, d):
        [(x, y)] = coordinates
        temp = self.screenshot[-1][self.hwnd][0][y:y + d, x:x + w]
        return temp

    def send_message(self, message):
        temp = 'FishingSupplierWindow' + f' {self.window_id}' + ': ' + message
        print(temp)

    def find(self, object, accurate=False, coordinates=None, w=None, d=None):  # returns list of positions
        try:
            position = []
            if not accurate:
                position = self.library[object][0].find(self.update_screenshot())

            if accurate:
                position = self.library[object][0].find(
                    self.update_accurate_screenshot(object=object, coordinates=coordinates, w=w, d=d))

            return position

        except KeyError:
            self.send_message(f'find function ERROR object search')
            self.send_message(f'{KeyError}')
            return []

    def is_trade_request(self):
        temp_coordinates = self.find('trade_request')
        if temp_coordinates:
            return temp_coordinates
        else:
            return []

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

    def get_object(self, object, search=False):
        if self.library[object][0]:
            pass
        else:
            temp = 'ERROR referring to the unknown object: ' + object
            self.send_message(temp)
            return False

        if search:
            pos = self.library[object][0].find(self.update_screenshot())
            if pos:
                self.library[object][1] = pos
                return pos
            else:
                return []
        else:
            return self.library[object][1]

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
