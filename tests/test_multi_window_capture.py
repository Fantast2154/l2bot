from system.window_capture import WindowCapture
import cv2

wincap = WindowCapture('Asterios')
wincap.capture_screen()

for i, img in enumerate(wincap.imgs):
    print(len(wincap.imgs))
    cv2.imshow(f'{i}', img)

cv2.waitKey(0)