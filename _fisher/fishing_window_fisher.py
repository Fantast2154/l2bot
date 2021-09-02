import threading

from system.screen_analyzer import *
from system.l2window import L2window
import cv2
import time
from system.item_calcs import *


class FishingWindow(L2window):

    def __init__(self, fisher_id, window_id, wincap, window_name, hwnd, screenshot):
        super().__init__(window_id, wincap, window_name, hwnd, screenshot)
        self.fisher_id = fisher_id
        self.send_message('created')
        self.wincap = wincap
        self.screenshot = screenshot
        self.hwnd = hwnd
        self.library = {}

        self.win_capture = None
        self.accurate_search = False
        self.screenshot_accurate = None
        self.init_image_database = [
            ['fishing', 'images/fishing/fishing_macro.jpg', 0.77],
            ['pumping', 'images/fishing/pumping.jpg', 0.77],
            ['reeling', 'images/fishing/reeling.jpg', 0.77],
            ['attack', 'images/fishing/attack.jpg', 0.87],
            ['move_to_supplier', 'images/fishing/move_to_supplier.jpg', 0.6],
            ['a_sign', 'images/login/a_sign.jpg', 0.9],
            ['trade_supplier', 'images/trade/trade_icon.jpg', 0.7]]

        self.extended_image_database = [
            ['bait', 'images/fishing/bait.jpg', 0.90],
            ['soski', 'images/items/soski.jpg', 0.85],
            ['soski_pet', 'images/items/soski_pet2.jpg', 0.85],
            ['hp_window', 'images/farming/hp_window.jpg', 0.77],
            ['hawk_buff', 'images/fishing/hawk_buff.jpg', 0.77],
            ['fenrir_party', 'images/party/fenrir_party.jpg', 0.63],
            ['pet_menu_name_button', 'images/party/pet_menu_name_button.jpg', 0.67],
            ['mini_map', 'images/mini_map.jpg', 0.7],
            ['baits', 'images/fishing/baits_hot_sptings.jpg', 0.8],
            ['status_bar', 'images/status_bar.jpg', 0.65],
            ['blue_bar', 'images/fishing/blue_bar2.jpg', 0.75],
            ['colored', 'images/fishing/colored_2.jpg', 0.94],
            ['luminous', 'images/fishing/luminous_2.jpg', 0.94],
            ['clock', 'images/fishing/clock2.jpg', 0.87],
            ['map_button', 'images/map.jpg', 0.9],
            ['equipment_bag', 'images/equipment_bag.jpg', 0.6],
            ['menu', 'images/login/stages/menu_quests.jpg', 0.91],
            ['fishing_window', 'images/fishing/fishing_window.jpg', 0.65],
            ['red_bar', 'images/fishing/red_bar3.jpg', 0.8],
            ['buff', 'images/fishing/cdbuff.jpg', 0.87],
            ['fishing_potion_white', 'images/fishing/fishing_potion_white.jpg', 0.6],
            ['alacrity_potion_small', 'images/fishing/alacrity_potion_small.jpg', 0.7],
            ['alacrity_dex_warlock', 'images/fishing/alacrity_dex_warlock.jpg', 0.7],
            ['pet_atk1', 'images/fishing/pet_atk_1.jpg', 0.7],
            ['pet_atk2', 'images/fishing/pet_atk_2.jpg', 0.7],
            ['soski_activated', 'images/soski_activated.jpg', 0.78],
            ['sun', 'images/sun2.jpg', 0.7],
            ['moon', 'images/moon2.jpg', 0.7],
            ['ok_button', 'images/trade/ok_button.jpg', 0.8],
            ['disconnect_EN', 'images/disconnect_EN.jpg', 0.4],
            ['weight_icon', 'images/weight.jpg', 0.9],
            ['exchange_menu', 'images/trade/exchange_menu3.jpg', 0.8],
            ['login', 'images/login.jpg', 0.95],
            ['mailbox', 'images/mailbox.jpg', 0.8],
            ['sendmail_button', 'images/sendmail_button.jpg', 0.8],
            ['send_button', 'images/send_button.jpg', 0.8],
            ['confirm_button', 'images/confirm_button.jpg', 0.8],
            ['cancel_button', 'images/cancel_button.jpg', 0.8],
            ['claim_items_button', 'images/claim_items_button.jpg', 0.8]
        ]

        self.catched_fish_database = [
            ['catched_item_0', 'images/items/catcheditem0.jpg', 0.83],
            ['catched_item_1', 'images/items/catcheditem1.jpg', 0.83],
            ['catched_item_2', 'images/items/catcheditem2.jpg', 0.83],
            ['catched_item_3', 'images/items/catcheditem3.jpg', 0.83],
            ['catched_item_4', 'images/items/catcheditem4.jpg', 0.83],
            ['catched_item_5', 'images/items/catcheditem5.jpg', 0.83],
            ['catched_item_6', 'images/items/catcheditem6.jpg', 0.83],
            ['catched_item_7', 'images/items/catcheditem7.jpg', 0.83]
        ]

        self.character_database = [
            ['nat_peggl', 'images/character/nat_peggl.jpg', 0.83],
            ['starosta_derevni', 'images/character/starosta_derevni.jpg', 0.83],
            ['character_small_bag', 'images/character/bag.jpg', 0.83],
            ['podscarbiy', 'images/character/podscarbiy.jpg', 0.83]
        ]
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
                # cv2.imshow(f'сlock{self.window_id}', temp[1])
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
            # self.send_message(f'{self.screenshot_accurate}')
            return self.screenshot_accurate
        else:
            return []

    def update_screenshot_rectangle(self, coordinates, w, d):
        [(x, y)] = coordinates
        temp = self.screenshot[-1][self.hwnd][0][y:y + d, x:x + w]
        return temp

    def send_message(self, message):
        temp = '\t' * 11 * (self.fisher_id+1) + 'FishingWindow ' + f'{self.fisher_id}: {message}'
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

    def find_in_rectangle(self, object, coordinates, w, d):  # returns list of positions
        try:
            position = self.library[object][0].find(
                self.update_screenshot_rectangle(coordinates=coordinates, w=w, d=d))
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
            return True
            # self.send_message('fishing window has been recorded')
        except:
            self.send_message('Error recording fishing window')
            return False

    def is_exchange_menu(self):
        temp_coordinates = self.find('exchange_menu')
        if temp_coordinates:
            return temp_coordinates
        else:
            return []

    def is_fishing_potion_white(self):
        if self.library['fishing_potion_white'][1]:
            return self.library['fishing_potion_white'][1]
        else:
            return self.get_object('fishing_potion_white', search=True)

    def is_hawk_buff(self):
        if self.library['hawk_buff'][1]:
            return self.library['hawk_buff'][1]
        else:
            return self.get_object('hawk_buff', search=True)

    def is_pet_attack(self):
        if self.library['pet_atk1'][1]:
            return self.library['pet_atk1'][1]
        temp1 = self.get_object('pet_atk1', search=True)
        if temp1:
            return temp1
        if self.library['pet_atk2'][1]:
            return self.library['pet_atk2'][1]
        temp2 = self.get_object('pet_atk2', search=True)
        if temp2:
            return temp2
        return []

    def is_attack(self):
        if self.library['attack'][1]:
            return self.library['attack'][1]
        else:
            return self.get_object('attack', search=True)

    def window_center_pos(self):
        x = self.left_top_x + self.width//2
        y = self.left_top_y + self.height//2
        return [(x, y)]

    def is_alacrity_potion_small(self):
        if self.library['alacrity_potion_small'][1]:
            return self.library['alacrity_potion_small'][1]
        else:
            return self.get_object('alacrity_potion_small', search=True)

    def is_alacrity_dex_warlock(self):
        if self.library['alacrity_dex_warlock'][1]:
            return self.library['alacrity_dex_warlock'][1]
        else:
            return self.get_object('alacrity_dex_warlock', search=True)

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

    def recognize_number(self, coordinates):
        [(temp_x, temp_y)] = coordinates
        cords = [(temp_x-40, temp_y-36)]
        w = 40
        d = 19
        DR = DigitsRecognition()
        # img = self.update_screenshot_rectangle(coordinates=cords, w=w, d=d)
        img = self.update_screenshot()
        number, _, _ = DR.digit_finder(img)
        return number



    def is_move_to_supplier(self):
        if self.library['move_to_supplier'][1]:
            return self.library['move_to_supplier'][1]
        else:
            return self.get_object('move_to_supplier', search=True)

    def get_self_nickname(self):
        temp = self.find('character_small_bag')
        if temp:
            [(x, y)] = temp
            for character in self.character_database:
                nickname = self.find_in_rectangle(character[0], [(x-176, y-106)], 180, 50)
                if nickname:
                    return character[0]
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

        for obj in self.catched_fish_database:
            try:
                # {'key', [obj, [(x,y]/None]
                self.library[f'{obj[0]}'] = [Vision(obj[1], obj[2]), None]
            except:
                pass
                # self.send_message('Error finding images2')

        for obj in self.character_database:
            try:
                # {'key', [obj, [(x,y]/None]
                self.library[f'{obj[0]}'] = [Vision(obj[1], obj[2]), None]
            except:
                pass
                # self.send_message('Error finding images2')

    def get_object(self, object, search=False):
        if search:
            # pos = self.library[object][0].find(self.update_screenshot())
            pos = self.find(object)
            if pos:
                self.library[object][1] = pos
                # print(f'DATABASE IF {self.window_id}: {pos}')
                return pos
            else:
                return []

        if self.library[object][1]:
            return self.library[object][1]
        else:
            temp = 'ERROR referring to the unknown object: ' + object
            self.send_message(temp)
            return False

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
