import threading
import time


class ScreenshotMaster(threading.Thread):
    screenshot = 0

    def __init__(self):
        threading.Thread.__init__(self)
        self.exit = threading.Event()
        self.screenshot = 0

    @classmethod
    def send_message(cls, message):
        print(message)

    def start_capturing(self):
        self.send_message(f'TEST ScreenshotMaster starts\n')

    def run(self):
        self.start_capturing()
        while not self.exit.is_set():
            self.capture_screen()
            time.sleep(1)

    def stop(self):
        self.send_message(f'TEST ScreenshotMaster has finished its work\n')
        self.exit.set()

    @classmethod
    def capture_screen(cls):
        cls.screenshot = 0

    def get_screenshot(self):
        return self.screenshot
