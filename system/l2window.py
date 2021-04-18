class L2window:

    left_top_x = 0
    left_top_y = 0
    width = 0
    height = 0
    win_capture = None

    def __init__(self, window_id, win_capture):
        self.send_message(f'TEST L2window {window_id} created')
        self.window_id = window_id
        x = 500
        y = 500
        width = 500
        height = 500

        self.left_top_x = x * window_id
        self.left_top_y = y
        self.width = width
        self.height = height

        self.win_capture = win_capture

    def __del__(self):
        self.send_message(f"TEST Window {self.window_id} destroyed")

    @classmethod
    def send_message(cls, message):
        print(message)