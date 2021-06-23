from system.screen_analyzer import *
from system.l2window import L2window
import cv2


class RelaunchWindow(L2window):
    library = {}
    screenshot = None
    win_capture = None

    def __init__(self, window_id, wincap, window_name, hwnd):
        super().__init__(window_id, wincap, window_name, hwnd)
        self.send_message(f'TEST FishingWindow {window_id} created')
        self.wincap = wincap
        self.screenshot = wincap.get_screenshot(window_id)
        self.window_id = window_id
        self.hwnd = hwnd


    def __del__(self):
        self.send_message(f"TEST FishingWindow {self.window_id} destroyed")

    def update_screenshot(self):
        self.screenshot = self.wincap.get_screenshot(self.window_id)

    @classmethod
    def send_message(cls, message):
        print(message)

    def find(self, objects): # returns list of positions
        try:
            screenshot = self.wincap.get_screenshot(self.window_id)
            # position = object.find(screenshot)
            position = [(1, 1)]
            return position
        except:
            print('ERROR finding', objects)
            return []

    def init_images(self):
        for obj in self.image_database:
            try:
                self.library[f'{obj[0]}'] = [Vision(obj[1], obj[2]), None]
            except:
                print('Error finding images')

    def init_search(self):
        self.screenshot = self.wincap.get_screenshot(self.window_id)
        try:
            for key in self.library:
                self.library[key][1] = self.library[key][0].find(self.screenshot)
        except:
            pass