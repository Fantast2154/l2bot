# import screen_analyzer
from fisher.screen_analyzer import ScreenAnalyzer

class FishingWindow:
    def __init__(self, left_top_x, left_top_y, right_bottom_x, right_bottom_y):
        self.left_top_x = left_top_x
        self.left_top_y = left_top_y
        self.right_bottom_x = right_bottom_x
        self.right_bottom_y = right_bottom_y
