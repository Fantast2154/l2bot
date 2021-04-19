import time

from system.screen_capture import ScreenCapture
from fisher.fishing_window import FishingWindow
import cv2

if __name__ == '__main__':
    wincap = ScreenCapture()
    wincap.start()

    # s = wincap.get_screenshot()
    # cv2.imshow('Test', s)
    # cv2.imwrite('TESTTEST.jpg', s)
    # cv2.waitKey(0)
    fw = FishingWindow(100, 100, 100, 100, 1, wincap)
    wincap.stop()