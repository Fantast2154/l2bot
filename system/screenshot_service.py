class ScreenshotMaster:
    screenshot = 0

    def __init__(self):
        screenshot = 0

    def run(self):
        # while True:
            # self.capture_screen()
        pass

    @classmethod
    def capture_screen(cls):
        cls.screenshot = 0

    def get_screenshot(self):
        return self.screenshot
