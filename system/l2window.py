class L2window:
    def __init__(self, i):
        self.send_message(f'TEST L2window calling')
        x = 500
        y = 500
        width = 500
        height = 500

        self.left_top_x = x * i
        self.left_top_y = y
        self.width = width
        self.height = height

    @classmethod
    def send_message(cls, message):
        print(message)