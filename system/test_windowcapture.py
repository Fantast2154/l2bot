from screen_capture import ScreenshotMaster
import cv2

if __name__ == '__main__':
    wincap = ScreenshotMaster()
    s = wincap.capture_screen()
    cv2.imshow('Test', s)
    cv2.waitKey(0)