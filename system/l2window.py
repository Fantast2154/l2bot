class L2window:

    left_top_x = 0
    left_top_y = 0
    width = 0
    height = 0
    win_capture = None

    def __init__(self, i, win_capture):
        self.send_message(f'TEST L2window calling')
        x = 500
        y = 500
        width = 500
        height = 500

        self.left_top_x = x * i
        self.left_top_y = y
        self.width = width
        self.height = height

        self.win_capture = win_capture

    @classmethod
    def send_message(cls, message):
        print(message)