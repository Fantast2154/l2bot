import cv2
import numpy as np
import win32con
import win32gui
import win32ui
from multiprocessing import Manager, Process

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

    day_time = True

    lock = None

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
    # offset_x = []
    # offset_y = []

    new_windows = []
    l2window_name = 0



    def __init__(self, l2win_name):
        # window_name=None

        self.send_message(f'TEST ScreenshotMaster created\n')
        # self.exit = threading.Event()
        # entire window accurate = False
        # accurate = True
        manager = Manager()
        self.fishing_window_pos_screenshots = []
        self.clock_pos_screenshots = []
        self.blue_bar_pos_screenshots = []
        self.red_bar_pos_screenshots = []
        self.screenshots = []
        self.imgs = []
        self.imggg = None
        self.sreenshots_dict = {}
        self.sreenshots_dict_SECOND = {}
        self.sreenshots_dict_THIRD = {}
        self.l2window_name = l2win_name
        self.dict_imgs1 = {}
        self.list_imgs1 = []
        self.dict_imgs2 = {}

        self.x_fishwin = manager.list()
        self.y_fishwin = manager.list()
        self.w_fishwin = manager.list()
        self.h_fishwin = manager.list()

        self.accurate = manager.dict()

        self.object_position_and_size = {}

        self.offset_x = manager.list()
        self.offset_y = manager.list()
        self.game_windows = manager.list()
        self.window_hwnd = manager.list()
        self.window_id = manager.list()

        self.w_screenshot = manager.list()
        self.temp = manager.list()

        self.window_screenshot = manager.list()


    def set_windows(self, windows_list):
        print('windows_list', len(windows_list))
        if windows_list:
            for window in windows_list:
                temp_w = L2window_optimized(window)
                self.offset_x.append(temp_w.offset_x)
                self.offset_y.append(temp_w.offset_y)
                self.game_windows.append(temp_w)
                self.window_hwnd.append(window.hwnd)
                self.window_id.append(window.window_id)

        print(id(self.game_windows))

    def __del__(self):
        self.send_message(f'destroyed')

    def capture_screen(self, M):

        w_screenshot = M.list()
        # self.window_screenshot[:] = []
        for game_window in self.game_windows:
            hwnd_l = game_window.hwnd
            temp = M.list()

            w = game_window.w
            h = game_window.h
            cropped_x = game_window.cropped_x
            cropped_y = game_window.cropped_y

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

            dcObj.DeleteDC()
            cDC.DeleteDC()
            win32gui.ReleaseDC(hwnd_l, wDC)
            win32gui.DeleteObject(dataBitMap.GetHandle())

            img = img[..., :3]
            img = np.ascontiguousarray(img)
            # self.imggg = img
            w_screenshot.append(temp)
            w_screenshot.append(w_screenshot)
            self.window_screenshot = w_screenshot

    def get_screenshot(self):
        # self.send_message(f'self.window_hwnd {hwnd}')
        # self.send_message(f'self.window_hwnd.index(self.window_hwnd) {self.window_hwnd.index(hwnd)}')
        return self.window_screenshot
        # id = self.window_hwnd.index(hwnd)
        # self.send_message(f'len {len(self.window_screenshot)}')
        # if len(self.window_screenshot) == 0:
        #     return []
        # return self.window_screenshot[id]

    def send_message(self, message):
        temp = 'WindowCapture' + ': ' + message
        print(temp)

    def start_capturing(self):
        self.send_message('start capturing')
        master = Manager()
        while True:
            self.capture_screen(master)

