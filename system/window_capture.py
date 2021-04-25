import threading
import numpy as np
import win32gui
import win32ui
import win32con
from threading import Thread, Lock

from system.l2window import L2window


class L2window_optimized:
    def __init__(self, window):
        print(f'TEST L2window {window.window_id} created')
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

class WindowCapture(threading.Thread):

    x_fishwin = []
    y_fishwin = []
    w_fishwin = []
    h_fishwin = []

    accurate = False
    day_time = True

    stopped = True
    lock = None
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
    offset_x = 0
    offset_y = 0

    windows_param = []
    windows_list = []
    game_windows = []
    new_windows = []

    def __init__(self, windows):
        # window_name=None

        self.send_message(f'TEST ScreenshotMaster created\n')
        threading.Thread.__init__(self)
        self.exit = threading.Event()

        self.fishing_window_pos_screenshots = []
        self.clock_pos_screenshots = []
        self.blue_bar_pos_screenshots = []
        self.red_bar_pos_screenshots = []
        self.screenshots = []
        self.imgs = []
        self.lock = Lock()

        for window in windows:
            self.game_windows.append(L2window_optimized(window))

        # self.game_windows = windows
        # self.windows_param = []

        # find the handle for the window we want to capture.
        # if no window name is given, capture the entire screen
        # if window_name is None:
        #     self.hwnd = win32gui.GetDesktopWindow()
        #     self.windows_param.append(self.hwnd)
        # else:
        #     _, self.windows_param = self.get_l2windows_param(window_name)
        #     for _ in self.windows_param:
        #         self.game_windows.append({})
        # self.hwnd = win32gui.FindWindow(None, window_name)
        # if not self.hwnd:
        #     raise Exception('Window not found: {}'.format(window_name))



    @classmethod
    def send_message(cls, message):
        print(message)

    def set_windows(self, windows_list):
        if windows_list:
            self.windows_list = windows_list

    def set_fishing_window(self, id, x_fishwin, y_fishwin, w_fishwin, h_fishwin):
        self.x_fishwin[id] = x_fishwin
        self.y_fishwin[id] = y_fishwin
        self.w_fishwin[id] = w_fishwin
        self.h_fishwin[id] = h_fishwin

    def __del__(self):
        self.send_message(f'TEST ScreenshotMaster destroyed')

    # @classmethod
    def capture_screen(self, accurate=False, object_position=(0, 0), object_size=(100, 100)):
        # self.lock.acquire()
        self.imgs = []
        # print('NUM', self.game_windows)
        for game_window in self.game_windows:
            hwnd_l = game_window['hwnd']
            w = game_window['w']
            h = game_window['h']
            cropped_x = game_window['cropped_x']
            cropped_y = game_window['cropped_y']
            # print('hwnd_l, w, h, cropped_x, cropped_y', hwnd_l, w, h, cropped_x, cropped_y)
            # get the window image data
            wDC = win32gui.GetWindowDC(hwnd_l)
            dcObj = win32ui.CreateDCFromHandle(wDC)
            cDC = dcObj.CreateCompatibleDC()
            dataBitMap = win32ui.CreateBitmap()

            if accurate:
                (xx, yy) = object_position
                (ww, hh) = object_size
                # dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
                dataBitMap.CreateCompatibleBitmap(dcObj, ww, hh)
                cDC.SelectObject(dataBitMap)
                cDC.BitBlt((0, 0), (ww, hh), dcObj, (cropped_x + xx, cropped_y + yy), win32con.SRCCOPY)
                # cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)

                # convert the raw data into a format opencv can read
                # dataBitMap.SaveBitmapFile(cDC, 'debug.bmp')
                signedIntsArray = dataBitMap.GetBitmapBits(True)
                img = np.fromstring(signedIntsArray, dtype='uint8')
                img.shape = (hh, ww, 4)
                # img.shape = (self.h, self.w, 4)

            else:
                dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
                cDC.SelectObject(dataBitMap)
                cDC.BitBlt((0, 0), (w, h), dcObj, (cropped_x, cropped_y), win32con.SRCCOPY)

                # convert the raw data into a format opencv can read
                # dataBitMap.SaveBitmapFile(cDC, 'debug.bmp')
                signedIntsArray = dataBitMap.GetBitmapBits(True)
                img = np.fromstring(signedIntsArray, dtype='uint8')
                img.shape = (h, w, 4)

            # free resources
            dcObj.DeleteDC()
            cDC.DeleteDC()
            win32gui.ReleaseDC(hwnd_l, wDC)
            win32gui.DeleteObject(dataBitMap.GetHandle())

            # drop the alpha channel, or cv.matchTemplate() will throw an error like:
            #   error: (-215:Assertion failed) (depth == CV_8U || depth == CV_32F) && type == _templ.type()
            #   && _img.dims() <= 2 in function 'cv::matchTemplate'
            img = img[..., :3]

            # make image C_CONTIGUOUS to avoid errors that look like:
            #   File ... in draw_rectangles
            #   TypeError: an integer is required (got type tuple)
            # see the discussion here:
            # https://github.com/opencv/opencv/issues/14866#issuecomment-580207109
            img = np.ascontiguousarray(img)
            self.imgs.append(img)
            # self.lock.release()

        return self.imgs

    def list_window_names(self):
        temp = []

        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                # temp.append([hex(hwnd), win32gui.GetWindowText(hwnd)])
                temp.append([hwnd, win32gui.GetWindowText(hwnd)])

        win32gui.EnumWindows(winEnumHandler, None)
        self.windows_param = temp

    def get_l2windows_param(self, l2window_name):
        hash_list = []
        name_list = []
        self.list_window_names()  # СПИСОК ВСЕХ ДОСТУПНЫХ ОКОН
        list_all_windows = self.get_windows_param()
        for window in list_all_windows:
            if window[1] == l2window_name:
                name_list.append(window[1])
                hash_list.append(window[0])
                # print(window)
        return name_list, hash_list

    def get_windows_param(self):
        return self.windows_param

    def get_screenshot(self, id):
        return self.screenshot

    @classmethod
    def send_message(cls, message):
        print(message)

    def start_capturing(self):
        pass

    def run(self):
        self.start_capturing()
        while not self.exit.is_set():
            if not self.accurate:
                self.screenshots = self.capture_screen()
            else:
                self.fishing_window_pos_screenshots = self.capture_screen(accurate=True,
                                                                          object_position=(
                                                                              self.x_fishwin, self.y_fishwin),
                                                                          object_size=(self.w_fishwin, self.h_fishwin))

                self.clock_pos_screenshots = self.capture_screen(accurate=True,
                                                                 object_position=(
                                                                     self.x_fishwin + 107, self.y_fishwin + 217),
                                                                 object_size=(30, 30))

                self.blue_bar_pos_screenshots = self.capture_screen(accurate=True,
                                                                    object_position=(
                                                                        self.x_fishwin + 17, self.y_fishwin + 249),
                                                                    object_size=(231, 14))
                if not self.day_time:
                    self.red_bar_pos_screenshots = self.capture_screen(accurate=True,
                                                                       object_position=(
                                                                           self.x_fishwin + 17, self.y_fishwin + 249),
                                                                       object_size=(231, 14))

    def stop(self):
        # self.send_message(f'TEST ScreenshotMaster stopped\n')
        self.exit.set()


if __name__ == '__main__':
    hwnd = win32gui.FindWindow(None, 'Asterios')
    print(hwnd)
    win = WindowCapture('Asterios')
    win.capture_screen()
