import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# import ../db.py
# from fisher.screen_analyzer import ScreenAnalyzer
import screen_analyzer

class FishingWindow:
    def __init__(self, left_top_x, left_top_y, right_bottom_x, right_bottom_y):
        self.left_top_x = left_top_x
        self.left_top_y = left_top_y
        self.right_bottom_x = right_bottom_x
        self.right_bottom_y = right_bottom_y
