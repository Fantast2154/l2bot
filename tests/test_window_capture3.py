import time

import cv2
import numpy as np
import win32con
import win32gui
import win32ui
from test_l2window import L2window

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
        self.send_message(f'created')

    def send_message(self, message):
        temp = 'L2window_optimized' + f' {self.window_id}' + ': ' + message
        print(temp)


# class WindowCapture(threading.Thread):
class WindowCapture:

    def __init__(self, l2win_name):
        # window_name=None

        self.send_message(f'TEST ScreenshotMaster created\n')
        # self.exit = threading.Event()
        # entire window accurate = False
        # accurate = True
        self.windows = []
        self.window_hwnd = []
        self.window_id = []
        self.test = []
        self.window_screenshot = 0
        self.test = 0
        self.count = 0

        # self.outfile = 0

    def set_windows(self, windows_list):
        if windows_list:
            for window in windows_list:
                temp_w = L2window_optimized(window)
                self.window_hwnd.append(window.hwnd)
                self.window_id.append(window.window_id)
            self.windows = windows_list

    def __del__(self):
        self.send_message(f'destroyed')

    def capture_screen2(self):
        global shared
        # arr = np.frombuffer(shared, dtype=np.uint8).reshape((200, 200))

        [object_position, object_size, object_name] = (200, 200), (200, 200), 'fish'
        wDC = win32gui.GetWindowDC(self.window_hwnd[0])
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()

        (xx, yy) = object_position
        (ww, hh) = object_size

        dataBitMap.CreateCompatibleBitmap(dcObj, ww, hh)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (ww, hh), dcObj, (xx, yy), win32con.SRCCOPY)

        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (hh, ww, 4)

        # free resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.window_hwnd[0], wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        img = img[..., :3]
        # shared_img = np.ascontiguousarray(img)
        shared.append(img)
        shared.pop(0)
        # with open('im_arr.npy', 'wb') as f:
        #     np.save('im_arr.npy', img)



    def get_screenshot(self):
        return self.window_screenshot


    def send_message(self, message):
        temp = 'WindowCapture' + ': ' + message
        print(temp)

    def start_capturing(self, shared_arr_):
        global shared
        shared = shared_arr_
        while True:
            self.capture_screen2()

