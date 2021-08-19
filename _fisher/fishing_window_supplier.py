from system.screen_analyzer import *
from system.l2window import L2window
import cv2
import time


class FishingSupplierWindow(L2window):

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
            ['trade', 'images/trade/trade_icon.jpg', 0.87]]

        self.extended_image_database = [
            ['map_button', 'images/map.jpg', 0.9],
            ['baits', 'images/trade/bait_2.jpg', 0.93],
            ['equipment_bag', 'images/equipment_bag.jpg', 0.6],
            ['soski', 'images/items/soski_2.jpg', 0.93],
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

    def update_screenshot(self):
        temp = self.screenshot[-1][self.hwnd][0]
        if len(temp) != 0:
            return temp
        else:
            return []

    def update_accurate_screenshot(self, object, coordinates, w, d):
        [(x, y)] = coordinates
        temp = self.screenshot[-1][self.hwnd][0][y:y + d, x:x + w]
        # cv2.imshow('1', temp)
        # cv2.waitKey(0)
        # position = self.library[object][0].find(self.update_screenshot())
        return temp

    def send_message(self, message):
        temp = 'FishingSupplierWindow' + f' {self.window_id}' + ': ' + message
        print(temp)

    def find(self, object, accurate=False, coordinates=None, w=None, d=None):  # returns list of positions
        try:
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

    def is_exchange_menu(self):
        temp_coordinates = self.find('exchange_menu')
        if temp_coordinates:
            return temp_coordinates
        else:
            return []

    def is_soski(self):
        temp_coordinates = self.find('exchange_menu')
        if temp_coordinates:
            [(x, y)] = temp_coordinates
            temp_coordinates2 = [(x-260//2, y-35//2)]
            coordinates = self.find('soski', coordinates=temp_coordinates2, w=260, d=500, accurate=True)
            [(out_x, out_y)] = coordinates
            return [(out_x + x - 260 // 2, out_y + y - 35 // 2)]
        else:
            return []

    def is_baits(self):
        temp_coordinates = self.find('exchange_menu')
        if temp_coordinates:
            [(x, y)] = temp_coordinates
            temp_coordinates2 = [(x-260//2, y-35//2)]
            coordinates = self.find('baits', coordinates=temp_coordinates2, w=260, d=500, accurate=True)
            #print(coordinates)
            if coordinates:
                (out_x, out_y) = coordinates[0]
                return [(out_x + x - 260 // 2, out_y + y - 35 // 2)]
        else:
            return []
    def is_input_field(self):
        temp_coordinates = self.is_confirm_button()
        if temp_coordinates:
            [(x, y)] = temp_coordinates
            coordinates = [(x, y-35)]
            return coordinates
        else:
            return []

    def is_confirm_button(self):
        temp_coordinates = self.find('confirm_button')
        #print(temp_coordinates)
        if temp_coordinates:
            return temp_coordinates
        else:
            return []

    def is_small_bag(self):
        temp_coordinates = self.find('exchange_menu')
        if temp_coordinates:
            [(x, y)] = temp_coordinates
            temp_coordinates2 = [(x-260//2, y-35//2)]
            coordinates = self.find('small_bag', coordinates=temp_coordinates2, w=260, d=500, accurate=True)
            [(out_x, out_y)] = coordinates
            return [(out_x + x - 260 // 2, out_y + y - 35 // 2)]
        else:
            return []

    def is_ok_button(self):
        temp_coordinates = self.find('exchange_menu')
        if temp_coordinates:
            [(x, y)] = temp_coordinates
            #temp_coordinates2 = [(x-260//2, y-35//2)]
            temp_coordinates2 = [(x-300//2, y-40//2)]
            #coordinates = self.find('ok_button', coordinates=temp_coordinates2, w=260, d=500, accurate=True)
            #coordinates = self.find('ok_button', coordinates=temp_coordinates2, w=300, d=550, accurate=True)
            coordinates = self.find('ok_button')
            [(out_x, out_y)] = coordinates
            #return [(out_x + x - 260 // 2, out_y + y - 35 // 2)]
            return coordinates
        else:
            return []

    def is_cancel_button(self):
        temp_coordinates = self.find('exchange_menu')
        if temp_coordinates:
            [(x, y)] = temp_coordinates
            temp_coordinates2 = [(x-260//2, y-35//2)]
            coordinates = self.find('cancel_button', coordinates=temp_coordinates2, w=260, d=500, accurate=True)
            [(out_x, out_y)] = coordinates
            return [(out_x + x - 260 // 2, out_y + y - 35 // 2)]
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
                self.send_message(f'Error finding images2 {obj}')

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
