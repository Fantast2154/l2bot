import threading
import numpy as np
import win32gui
import win32ui
import win32con
from threading import Thread, Lock

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
        self.send_message(f'created')

    def send_message(self, message):
        temp = 'L2window_optimized' + f' {self.window_id}' + ': ' + message
        print(temp)


# class WindowCapture(threading.Thread):
class WindowCapture:
    x_fishwin = []
    y_fishwin = []
    w_fishwin = []
    h_fishwin = []

    accurate = {}
    imgs = []
    dict_imgs = {}
    object_position_and_size = {}
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
    offset_x = []
    offset_y = []

    windows_param = []
    windows_list = []
    game_windows = []
    new_windows = []
    l2window_name = 0

    def __init__(self, l2win_name):
        # window_name=None

        self.send_message(f'TEST ScreenshotMaster created\n')
        self.exit = threading.Event()
        # entire window accurate = False
        # accurate = True
        self.fishing_window_pos_screenshots = []
        self.clock_pos_screenshots = []
        self.blue_bar_pos_screenshots = []
        self.red_bar_pos_screenshots = []
        self.screenshots = []
        self.imgs = []
        self.sreenshots_dict = {}
        self.lock = Lock()
        self.l2window_name = l2win_name

    def set_windows(self, windows_list):
        if windows_list:
            for window in windows_list:
                temp_w = L2window_optimized(window)
                self.offset_x.append(temp_w.offset_x)
                self.offset_y.append(temp_w.offset_y)
                self.game_windows.append(temp_w)
                #self.accurate.append(window.hwnd)

    def set_fishing_window(self, hwnd, x_fishwin, y_fishwin, w_fishwin, h_fishwin):

        self.object_position_and_size[hwnd] = [[(x_fishwin, y_fishwin), (w_fishwin, h_fishwin), 'fishing_window'],
                                               [(x_fishwin + 107, y_fishwin + 217), (30, 30), 'clock'],
                                               [(x_fishwin + 17, y_fishwin + 249), (231, 14), 'blue_bar'],
                                               [(x_fishwin + 17, y_fishwin + 249), (231, 14), 'red_bar']]

    def __del__(self):
        self.send_message(f'destroyed')

    # @classmethod
    def capture_screen(self, accurate=False, object_position=(0, 0), object_size=(100, 100)):
        # print('CAPTURING SCREEN')
        # self.lock.acquire()
        # self.imgs = []
        # print('NUM', self.game_windows)
        for game_window in self.game_windows:
            hwnd_l = game_window.hwnd

            w = game_window.w
            h = game_window.h
            cropped_x = game_window.cropped_x
            cropped_y = game_window.cropped_y
            # print('hwnd_l, w, h, cropped_x, cropped_y', hwnd_l, w, h, cropped_x, cropped_y)
            # get the window image data
            wDC = win32gui.GetWindowDC(hwnd_l)
            dcObj = win32ui.CreateDCFromHandle(wDC)
            cDC = dcObj.CreateCompatibleDC()
            dataBitMap = win32ui.CreateBitmap()
            self.imgs = []
            if self.accurate.get(hwnd_l, None):

                for [object_position, object_size, object_name] in self.object_position_and_size[hwnd_l]:
                    # print('object_position', object_position)
                    # print('object_size', object_size)
                    (xx, yy) = object_position
                    (ww, hh) = object_size
                    # dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
                    # ww = 20
                    # hh = 30
                    dataBitMap.CreateCompatibleBitmap(dcObj, ww, hh)
                    cDC.SelectObject(dataBitMap)
                    cDC.BitBlt((0, 0), (ww, hh), dcObj, (cropped_x + xx, cropped_y + yy), win32con.SRCCOPY)
                    # cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)

                    # convert the raw data into a format opencv can read
                    # dataBitMap.SaveBitmapFile(cDC, 'debug.bmp')
                    signedIntsArray = dataBitMap.GetBitmapBits(True)
                    img = np.fromstring(signedIntsArray, dtype='uint8')
                    img.shape = (hh, ww, 4)
                    self.dict_imgs[object_name] = img
                    #self.imgs.append(img)
                    # img.shape = (self.h, self.w, 4)

                    # # free resources
                    # dcObj.DeleteDC()
                    # cDC.DeleteDC()
                    # win32gui.ReleaseDC(hwnd_l, wDC)
                    # win32gui.DeleteObject(dataBitMap.GetHandle())

                    for key in self.dict_imgs.copy().keys():
                        temp_img = self.dict_imgs[key]
                        temp_img = temp_img[..., :3]
                        self.dict_imgs[key] = np.ascontiguousarray(temp_img)

                    self.sreenshots_dict[hwnd_l] = self.dict_imgs

            else:
                dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
                cDC.SelectObject(dataBitMap)
                cDC.BitBlt((0, 0), (w, h), dcObj, (cropped_x, cropped_y), win32con.SRCCOPY)

                # convert the raw data into a format opencv can read
                # dataBitMap.SaveBitmapFile(cDC, 'debug.bmp')
                signedIntsArray = dataBitMap.GetBitmapBits(True)
                img = np.fromstring(signedIntsArray, dtype='uint8')
                img.shape = (h, w, 4)
                self.imgs.append(img)



                # drop the alpha channel, or cv.matchTemplate() will throw an error like:
                #   error: (-215:Assertion failed) (depth == CV_8U || depth == CV_32F) && type == _templ.type()
                #   && _img.dims() <= 2 in function 'cv::matchTemplate'
                temp_arr = []
                for img in self.imgs:
                    img = img[..., :3]
                    # make image C_CONTIGUOUS to avoid errors that look like:
                    #   File ... in draw_rectangles
                    #   TypeError: an integer is required (got type tuple)
                    # see the discussion here:
                    # https://github.com/opencv/opencv/issues/14866#issuecomment-580207109
                    img = np.ascontiguousarray(img)
                    temp_arr.append(img)

                self.imgs = temp_arr
            # self.imgs.append(img)
            # free resources
            dcObj.DeleteDC()
            cDC.DeleteDC()
            win32gui.ReleaseDC(hwnd_l, wDC)
            win32gui.DeleteObject(dataBitMap.GetHandle())

            self.sreenshots_dict[hwnd_l] = {hwnd_l: self.imgs}
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

    def get_l2windows_param(self):
        hash_list = []
        name_list = []
        self.list_window_names()  # СПИСОК ВСЕХ ДОСТУПНЫХ ОКОН
        list_all_windows = self.get_windows_param()

        for window in list_all_windows:
            print(window)
            if window[1] == self.l2window_name:
                name_list.append(window[1])
                hash_list.append(window[0])
                # print(window)
        return name_list, hash_list

    def get_windows_param(self):
        return self.windows_param

    def get_screenshot(self, window_hwnd):
        return self.sreenshots_dict[window_hwnd]

    def send_message(self, message):
        temp = 'WindowCapture' + ': ' + message
        print(temp)

    def start_capturing(self):
        self.stopped = False
        t = Thread(target=self.thread_run)
        t.start()

    def set_accurate_param(self, accurate, hwnd):
        self.accurate[hwnd] = accurate

    def thread_run(self):

        while not self.exit.is_set():
            self.screenshots = self.capture_screen()

            '''
            for accurate in self.accurate:
            if not accurate:
                      
            else:
                pass
                
                
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
            '''

    # def run(self):
    #     self.start_capturing()
    #     while not self.exit.is_set():
    #         pass

    def stop(self):
        self.stopped = True
        # self.send_message(f'TEST ScreenshotMaster stopped\n')
        self.exit.set()

# if __name__ == '__main__':
#     # hwnd = win32gui.FindWindow(None, 'Asterios')
#     l2window_name = 'Asterios'  # НАЗВАНИЕ ОКНА, ГДЕ БУДЕТ ВЕСТИСЬ ПОИСК
#     # win_capture = ScreenCapture()
#     win_capture = WindowCapture(l2window_name)
#
#     # searching running L2 windows
#
#     name_list, hash_list = win_capture.get_l2windows_param()
#     print(hash_list[0])
#     # w = L2window(0, 'Asterios', hwnd)
#     # win = WindowCapture([w])
#
#     # win_capture.set_windows(L2window(i, win_capture, name_list[i], hash_list[i]))
#
#     # start capturing screenshots
#
#     # win_capture.start_capturing()
#     win_capture.capture_screen(accurate=True)
