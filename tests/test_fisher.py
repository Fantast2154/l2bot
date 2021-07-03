import cv2
class Fisher:
    def __init__(self, m):
        self.manager = m


    def start(self):
        while True:
            cv2.imshow('fisher', self.manager[-1])
            cv2.waitKey(1)