from system.window_capture import WindowCapture
import cv2
import keyboard


wincap = WindowCapture('Asterios')

while not keyboard.is_pressed('q'):
    wincap.capture_screen()
    for i, img in enumerate(wincap.imgs):
        #print(len(wincap.imgs))
        cv2.imshow(f'{i}', img)
        cv2.waitKey(1)