import threading


class Farmer(threading.Thread):
    def __init__(self, fishing_window, number):
        threading.Thread.__init__(self)
        self.fishing_window = fishing_window
        self.number = number

    farmer_window = None
    number = None
