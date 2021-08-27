import threading
import time

import numpy as np
import win32gui
import win32ui
import win32con
import cv2
from threading import Thread, Lock
from multiprocessing import Manager

from system.l2window import L2window


class L2window_optimized:
    def __init__(self, window):
        self.window_id = window.window_id
        self.window_name = window.window_name
        self.hwnd = window.hwnd
        window_rect = win32gui.GetWindowRect(window.hwnd)
        border_pixels = 8
        titlebar_pixels = 30
        self.my_x = window_rect[0]
        self.my_y = window_rect[1]
        self.w = window_rect[2] - self.my_x - (border_pixels * 2)
        self.h = window_rect[3] - self.my_y - titlebar_pixels - border_pixels
        self.w_init = window_rect[2] - self.my_x
        self.h_init = window_rect[3] - self.my_y
        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels
        self.offset_x = self.my_x + self.cropped_x
        self.offset_y = self.my_y + self.cropped_y
        # self.send_message(f'created')

    def send_message(self, message):
        temp = 'L2window_optimized' + f' {self.window_id}' + ': ' + message
        print(temp)


# class WindowCapture(threading.Thread):
class WindowCapture:
    x_fishwin = []
    y_fishwin = []
    w_fishwin = []
    h_fishwin = []

    imgs = []

    day_time = True

    screenshot = []

    my_x = 0
    my_y = 0
    # properties
    w = 0
    h = 0
    w_init = 0
    h_init = 0

    hwnd = None
    cropped_x = 0
    cropped_y = 0
    offset_x = []
    offset_y = []
    exit_is_set = False
    window_hwnd = []
    window_id = []
    windows_param = []
    windows_list = []

    new_windows = []
    l2window_name = 0

    window_screenshot = []

    def __init__(self, l2win_name):
        # window_name=None
        manager = Manager()
        # self.send_message(f'TEST ScreenshotMaster created\n')
        # entire window accurate = False
        # accurate = True
        # self.exit_is_set = manager.list()
        # self.exit_is_set.append(False)
        global exit_event
        exit_event = False
        self.fishing_window_pos_screenshots = []
        self.clock_pos_screenshots = []
        self.blue_bar_pos_screenshots = []
        self.red_bar_pos_screenshots = []
        self.screenshots = []
        self.imgs = []
        self.sreenshots_dict = {}
        self.sreenshots_dict_SECOND = {}
        self.sreenshots_dict_THIRD = {}
        self.l2window_name = l2win_name
        self.dict_imgs1 = {}
        self.list_imgs1 = []
        self.dict_imgs2 = {}

        self.game_windows = manager.list()
        self.accurate = manager.dict()
        self.object_position_and_size = manager.dict()
        self.bar_limits = manager.dict()

    def set_windows(self, windows_list):
        if windows_list:
            for window in windows_list:
                temp_w = L2window_optimized(window)
                self.offset_x.append(temp_w.offset_x)
                self.offset_y.append(temp_w.offset_y)
                self.game_windows.append(temp_w)
                self.window_hwnd.append(window.hwnd)
                self.window_id.append(window.window_id)
                self.accurate[window.hwnd] = False

    def set_fishing_window(self, hwnd, x_fishwin, y_fishwin, w_fishwin, h_fishwin):

        self.object_position_and_size[hwnd] = [[(x_fishwin, y_fishwin), (w_fishwin, h_fishwin), 'fishing_window'],
                                               [(x_fishwin + 107, y_fishwin + 217), (30, 30), 'clock'],
                                               [(x_fishwin + 17, y_fishwin + 249), (231, 14), 'blue_bar'],
                                               [(x_fishwin + 17, y_fishwin + 249), (231, 14), 'red_bar']]
        self.bar_limits[hwnd] = [x_fishwin + 17, 231]

    # def __del__(self):
    #     self.send_message(f'destroyed')

    # @classmethod
    def capture_screen(self, accurate=False, object_position=(0, 0), object_size=(100, 100)):
        global screenshot
        w_screenshot = {}

        for game_window in self.game_windows:
            hwnd_l = game_window.hwnd
            temp = []
            # temp.append(hwnd_l)

            w = game_window.w
            h = game_window.h
            cropped_x = game_window.cropped_x
            cropped_y = game_window.cropped_y

            if self.accurate[game_window.hwnd]:

                for shefer in self.object_position_and_size[hwnd_l]:
                    # print('shefer hwnd_l', shefer, hwnd_l)
                    [object_position, object_size, object_name] = shefer
                    wDC = win32gui.GetWindowDC(hwnd_l)
                    dcObj = win32ui.CreateDCFromHandle(wDC)
                    cDC = dcObj.CreateCompatibleDC()
                    dataBitMap = win32ui.CreateBitmap()

                    (xx, yy) = object_position
                    (ww, hh) = object_size

                    dataBitMap.CreateCompatibleBitmap(dcObj, ww, hh)
                    cDC.SelectObject(dataBitMap)
                    cDC.BitBlt((0, 0), (ww, hh), dcObj, (cropped_x + xx, cropped_y + yy), win32con.SRCCOPY)

                    signedIntsArray = dataBitMap.GetBitmapBits(True)
                    img = np.fromstring(signedIntsArray, dtype='uint8')
                    img.shape = (hh, ww, 4)

                    # free resources
                    dcObj.DeleteDC()
                    cDC.DeleteDC()
                    win32gui.ReleaseDC(hwnd_l, wDC)
                    win32gui.DeleteObject(dataBitMap.GetHandle())

                    img = img[..., :3]
                    img = np.ascontiguousarray(img)

                    temp.append(img)

                w_screenshot[game_window.hwnd] = temp
            else:

                wDC = win32gui.GetWindowDC(hwnd_l)
                dcObj = win32ui.CreateDCFromHandle(wDC)
                cDC = dcObj.CreateCompatibleDC()
                dataBitMap = win32ui.CreateBitmap()

                dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
                cDC.SelectObject(dataBitMap)
                cDC.BitBlt((0, 0), (w, h), dcObj, (cropped_x, cropped_y), win32con.SRCCOPY)

                signedIntsArray = dataBitMap.GetBitmapBits(True)
                img = np.fromstring(signedIntsArray, dtype='uint8')
                img.shape = (h, w, 4)
                # self.imgs.append(img)

                # free resources
                dcObj.DeleteDC()
                cDC.DeleteDC()
                win32gui.ReleaseDC(hwnd_l, wDC)
                win32gui.DeleteObject(dataBitMap.GetHandle())

                img = img[..., :3]
                img = np.ascontiguousarray(img)

                # self.dict_imgs2[hwnd_l] = img
                # self.sreenshots_dict_THIRD[hwnd_l] = self.dict_imgs2.copy()
                temp.append(img)
                w_screenshot[game_window.hwnd] = temp

        screenshot.append(w_screenshot)
        screenshot.pop(0)
        # cv2.imshow('wincap', screenshot[-1][0][0])
        # cv2.waitKey(1)
        # self.lock.release()
        # return self.sreenshots_dict_THIRD

    def get_windows_param(self):
        return self.windows_param

    def send_message(self, message):
        temp = 'WindowCapture: ' + message
        print(temp)

    def start_capturing(self, screenshot_):
        global screenshot, exit_event
        screenshot = screenshot_
        exit_event = False
        self.run()

    def set_accurate_param(self, accurate, hwnd):
        self.accurate[hwnd] = accurate

    def run(self):
        while not exit_event:
            self.capture_screen()

    def stop(self):
        global exit_event
        exit_event = True
        self.send_message(f'stop event')

