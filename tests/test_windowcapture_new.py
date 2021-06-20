import time

from system.window_capture import WindowCapture
from system.l2window import L2window
from main import get_l2windows_param
import cv2

if __name__ == '__main__':

    l2window_name = 'Asterios'
    name_list, hash_list = get_l2windows_param(l2window_name)
    n = len(hash_list)
    windows = []
    for i in range(n):
        windows.append(L2window(i, name_list[i], hash_list[i]))

    win_capture = WindowCapture(windows)
    win_capture.start_capturing()

    time.sleep(5)
    print('THREAD')
    #while True:
    s = win_capture.sreenshots_dict[hash_list[0]]
    #print('s', s)
    cv2.imshow('Test', s)
    cv2.imwrite('TESTWINCAP.jpg', s)
    #cv2.waitKey(1)
