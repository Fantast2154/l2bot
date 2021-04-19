import os
import cv2
import time
from system.screen_analyzer import Vision
from system.screen_capture import ScreenCapture

if __name__ == '__main__':
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    rel_path = "../images/fishing.jpg"
    abs_file_path = os.path.join(script_dir, rel_path)

    test_object_to_find = Vision(abs_file_path, 0.9)
    wincap = ScreenCapture()

    os.startfile(abs_file_path)
    time.sleep(2)

    s = wincap.capture_screen()
    coordinates = test_object_to_find.find(s, debug_mode='rectangles')
    print(f'Coordinates: {coordinates}')
    cv2.waitKey(0)
