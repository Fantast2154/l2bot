# import pyautogui

class ScreenAnalyzer:

    @staticmethod
    def getScreen(i, x1, y1, x2, y2):
        screen = pyautogui.screenshot(str(i) + ".png",
                                      region=(x1, y1, (x2 - x1), (y2 - y1)))
        return screen

    @staticmethod
    def findOnScreen(screenshot, image_path):
        location = pyautogui.locate(image_path, screenshot)
        if location:
            return location
        return None
