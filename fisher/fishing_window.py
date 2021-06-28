import threading

from system.screen_analyzer import *
from system.l2window import L2window
import cv2


class FishingWindow(L2window):



    def __init__(self, window_id, wincap, window_name, hwnd):
        super().__init__(window_id, wincap, window_name, hwnd)
        self.wincap = wincap
        # self.screenshot = wincap.get_screenshot(window_id)

        self.hwnd = hwnd
        self.library = {}
        self.screenshot = None
        self.win_capture = None
        self.init_image_database = [
            ['fishing', 'images/fishing.jpg', 0.8],
            ['pumping', 'images/pumping.jpg', 0.87],
            ['reeling', 'images/reeling.jpg', 0.87]]

        self.extended_image_database = [
            ['bait', 'images/bait.jpg', 0.90],
            ['soski', 'images/soski.jpg', 0.7],
            ['blue_bar', 'images/blue_bar2.jpg', 0.8],
            ['colored', 'images/colored_2.jpg', 0.94],
            ['luminous', 'images/luminous_2.jpg', 0.94],
            ['clock', 'images/clock3.jpg', 0.8],
            ['map_button', 'images/map.jpg', 0.9],
            ['equipment_bag', 'images/equipment_bag.jpg', 0.6],
            ['menu', 'images/menu.jpg', 0.6],
            ['fishing_window', 'images/fishing_window.jpg', 0.6],
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
        # self.init_search()

    def __del__(self):
        self.send_message(f"destroyed")

    def update_screenshot(self, object=None):

        if object is None:

            [self.screenshot] = self.wincap.get_screenshot(self.hwnd)[self.hwnd]
            # temp = self.wincap.get_screenshot(self.hwnd)[self.hwnd]
        else:

            temp = self.wincap.get_screenshot(self.hwnd).get(object, None)
            if temp is None:
                return self.screenshot
            else:
                self.screenshot = temp
            # cv2.imshow('1', self.screenshot)
            # cv2.waitKey(1)
            # temp = self.wincap.get_screenshot(self.hwnd)[self.hwnd]

        return self.screenshot

    def send_message(self, message):
        temp = 'FishingWindow' + f' {self.window_id}' + ': ' + message
        print(temp)

    def find(self, object, accurate=False):  # returns list of positions
        try:
            if not accurate:
                position = self.library[object][0].find(self.update_screenshot())
            else:
                self.send_message(f'TEST object {object}')
                position = self.library[object][0].find(self.update_screenshot(object=object))
                self.send_message(f'TEST position {position}')
            return position
        except KeyError:
            self.send_message(f'ERROR object search')
            self.send_message(f'{KeyError}')
            return []

    def start_accurate(self):
        try:
            self.send_message(f'TEST {KeyError}')
            [(x_fishwin, y_fishwin, w_fishwin, h_fishwin)] = self.library['fishing_window'][0].find(
                self.update_screenshot(), coordinates_and_sizes=True)
            self.wincap.set_fishing_window(self.hwnd, x_fishwin, y_fishwin, w_fishwin, h_fishwin)
            self.wincap.set_accurate_param(True, self.hwnd)
        except KeyError:
            self.send_message(f'TEST {KeyError}')
            self.send_message('Error recording fishing_window')

    def is_fishing_window(self):

        if self.library['fishing_window'][1]:
            temp = self.find('fishing_window', accurate=True)
            return temp
        else:
            return False

    def is_blue_bar(self):
        return self.find('blue_bar', accurate=True)

    def is_red_bar(self):
        return self.find('red_bar', accurate=True)

    def is_clock(self):
        return self.find('clock', accurate=True)

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
        if self.library[name][0]:
            pass
            # if self.library[name][0]:
            #     pass
            # else:
            #     temp = 'ERROR referring to the unknown object: ' + name
            #     # self.send_message(temp)
            #     return []
        else:
            temp = 'ERROR referring to the unknown object: ' + name
            # self.send_message(temp)
            return False

        if search:
            pos = self.library[name][0].find(self.update_screenshot())
            if pos:
                self.library[name][1] = pos
            # print(f'DATABASE IF {self.window_id}: {pos}')
                return pos
            else:
                return []
        else:
            # print(f'DATABASE ELSE {self.window_id}: {self.library[name][1]}')
            return self.library[name][1]

    def init_search(self):
        try:
            for key in self.init_image_database:
                # self.send_message(f'{key}')
                temp = self.library[key[0]][0].find(self.update_screenshot())
                if not temp:
                    return False
                else:
                    self.library[key[0]][1] = temp
            return True
        except:
            self.send_message('Error init search')
            return False

    # def start(self):
    #     t = threading.Thread(target=self.run)
    #     t.start()
    #
    # def run(self):
    #     while True:
            # print(f'RUN TEST {self.window_id}', self.library['fishing'][1])
            # print(f'RUN TEST {self.window_id}:{id(self.library)}')
