import threading

from system.screen_analyzer import *
from system.l2window import L2window
import cv2
import time


class FishingWindow(L2window):

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
            ['fishing', 'images/fishing/fishing.jpg', 0.87],
            ['pumping', 'images/fishing/pumping.jpg', 0.87],
            ['reeling', 'images/fishing/reeling.jpg', 0.87],
            ['attack', 'images/fishing/attack.jpg', 0.87],
            ['trade_supplier', 'images/trade/trade_icon.jpg', 0.83]]

        self.extended_image_database = [
            ['bait', 'images/fishing/bait.jpg', 0.90],
            ['soski', 'images/soski.jpg', 0.7],
            ['hp_window', 'images/farming/hp_window.jpg', 0.87],
            ['blue_bar', 'images/fishing/blue_bar2.jpg', 0.75],
            ['colored', 'images/fishing/colored_2.jpg', 0.94],
            ['luminous', 'images/fishing/luminous_2.jpg', 0.94],
            ['clock', 'images/fishing/clock2.jpg', 0.87],
            ['map_button', 'images/map.jpg', 0.9],
            ['equipment_bag', 'images/equipment_bag.jpg', 0.6],
            ['menu', 'images/menu.jpg', 0.6],
            ['fishing_window', 'images/fishing/fishing_window.jpg', 0.7],
            ['red_bar', 'images/fishing/red_bar3.jpg', 0.8],
            ['buff', 'images/fishing/cdbuff.jpg', 0.87],
            ['soski_activated', 'images/soski_activated.jpg', 0.78],
            ['sun', 'images/sun2.jpg', 0.7],
            ['moon', 'images/moon2.jpg', 0.7],
            ['ok_button', 'images/trade/ok_button.jpg', 0.8],
            ['disconnect_EN', 'images/disconnect_EN.jpg', 0.4],
            ['weight_icon', 'images/weight.jpg', 0.9],
            ['exchange_menu', 'images/trade/exchange_menu2.jpg', 0.8],
            ['login', 'images/login.jpg', 0.95],
            ['mailbox', 'images/mailbox.jpg', 0.8],
            ['sendmail_button', 'images/sendmail_button.jpg', 0.8],
            ['send_button', 'images/send_button.jpg', 0.8],
            ['confirm_button', 'images/confirm_button.jpg', 0.8],
            ['cancel_button', 'images/cancel_button.jpg', 0.8],
            ['claim_items_button', 'images/claim_items_button.jpg', 0.8],
            ['catched_item_0', 'images/items/catcheditem1.jpg', 0.7],
            ['catched_item_1', 'images/items/catcheditem2.jpg', 0.7],
            ['catched_item_2', 'images/items/catcheditem3.jpg', 0.7],
            ['catched_item_3', 'images/items/catcheditem4.jpg', 0.7]]

        self.vision_catcheditem_pos = [None] * 4
        # self.send_message(f'<-L2window created')

        self.init_images()

    # def __del__(self):
    #     self.send_message(f"destroyed")
    # [{hwnd1: [], hwnd2: []}]


    def update_screenshot(self):
        temp = self.screenshot[-1][self.hwnd][0]
        # while True:
        #     temp = self.screenshot[-1][0][0]
        #     cv2.imshow('BOYKO MALCHISHKA', temp)
        #     cv2.waitKey(1)
        if len(temp) != 0:
            # cv2.imshow('BOYKO MALCHISHKA', temp[0])
            # cv2.waitKey(1)
            return temp
        else:
            return []

    def update_accurate_screenshot(self, object=False):
        if object:
            temp = self.screenshot[-1][self.hwnd]
            # print('=============================================')
            # print('1+++', type(self.screenshot[-1]))
            # print(self.screenshot[-1])
            # print('2++', type(self.screenshot[-1][self.hwnd]))
            # print(self.screenshot[-1][self.hwnd])
            # print(f'3 ------------{self.hwnd} -------------------------', type(self.screenshot[-1][self.hwnd][2]))
            # print(self.screenshot[-1][self.hwnd][2])
            # print('===THEEND===')
            # while True:
            #     temp = self.screenshot[-1][0]
            #     cv2.imshow('BOYKO MALCHISHKA', temp[2])
            #     cv2.waitKey(1)
            # print(f'{self.window_id} ---', object)
            if object == 'fishing_window':
                self.screenshot_accurate = temp[0]
                # cv2.imshow('fishing_window', temp[0])
                # cv2.waitKey(1)
            elif object == 'clock':
                self.screenshot_accurate = temp[1]
                # cv2.imshow(f'??lock{self.window_id}', temp[1])
                # cv2.waitKey(1)
            elif object == 'blue_bar':
                # print('test --------------------------')
                self.screenshot_accurate = temp[2]
                # cv2.imshow(f'blue_bar{self.window_id}', temp[2])
                # cv2.moveWindow(f'blue_bar{self.window_id}', self.left_top_x, self.left_top_y + self.height + 15)
                # cv2.waitKey(1)
            elif object == 'red_bar':
                self.screenshot_accurate = temp[3]
                # cv2.imshow(f'red_bar{self.window_id}', temp[3])
                # cv2.moveWindow(f'red_bar{self.window_id}', 40, 30)
                # cv2.waitKey(1)
            else:
                return []
            #self.send_message(f'{self.screenshot_accurate}')
            return self.screenshot_accurate
        else:
            return []

    def send_message(self, message):
        temp = '\t' * 11 * self.window_id +'FishingWindow ' + f'{self.window_id}: {message}'
        print(temp)

    def find(self, object, accurate=False):  # returns list of positions
        try:
            # timer = time.time()
            if not accurate:
                position = self.library[object][0].find(self.update_screenshot())
            else:
                position = self.library[object][0].find(self.update_accurate_screenshot(object=object))
            # self.send_message((f'TIMER {time.time() - timer}'))
            return position
        except KeyError:
            self.send_message(f'find function ERROR object search')
            self.send_message(f'{KeyError}')
            return []

    def start_accurate_search(self):
        self.wincap.set_accurate_param(True, self.hwnd)
        self.accurate_search = True
        self.send_message('start_accurate command is ON')

    def stop_accurate_search(self):
        self.wincap.set_accurate_param(False, self.hwnd)
        self.accurate_search = False
        self.send_message('start_accurate command is OFF')

    def record_fishing_window(self):
        try:
            [(x_fishwin, y_fishwin, w_fishwin, h_fishwin)] = self.library['fishing_window'][0].find(
                self.update_screenshot(), coordinates_and_sizes=True)
            self.wincap.set_fishing_window(self.hwnd, x_fishwin, y_fishwin, w_fishwin, h_fishwin)
            # self.send_message('fishing window has been recorded')
        except:
            self.send_message('Error recording fishing window')

    def is_exchange_menu(self):
        temp_coordinates = self.find('exchange_menu')
        if temp_coordinates:
            return temp_coordinates
        else:
            return []

    def is_fishing_window(self):

        temp = self.find('fishing_window', accurate=True)
        if temp:
            return True
        else:
            return False

    def is_blue_bar(self):
        temp = self.find('blue_bar', accurate=True)
        if temp:
            return temp
        else:
            return False

    def is_red_bar(self):
        temp = self.find('red_bar', accurate=True)
        if temp:
            return temp
        else:
            return False

    def is_clock(self):
        temp = self.find('clock', accurate=True)
        if temp:

            return temp
        else:
            return False

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
                pass
                # self.send_message('Error finding images2')

    def get_object(self, object, search=False):
        print('GET O, EBANIY', object, search)
        if self.library[object][0]:
            print('GET O passsssssssss ')
            pass
        else:
            temp = 'ERROR referring to the unknown object: ' + object
            self.send_message(temp)
            print('Gsend_message asdasdasd13123123sss ')
            return False

        if search:
            # pos = self.library[object][0].find(self.update_screenshot())
            pos = self.find(object)
            print('__________________get_object', pos)

            if pos:
                self.library[object][1] = pos
                # print(f'DATABASE IF {self.window_id}: {pos}')
                return pos
            else:
                return []
        else:
            return self.library[object][1]

    def init_search(self):
        try:
            for key in self.init_image_database:
                # self.send_message(f'{key}')
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

    def activate_window(self):
        coords = [(self.left_top_x + 200, self.left_top_y - 10)]
        return coords