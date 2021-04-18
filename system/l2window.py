import win32gui


class L2window:

    def __init__(self, window_id, win_capture, window_name, hwnd):
        self.send_message(f'TEST L2window {window_id} created')
        self.window_id = window_id
        x = 0
        y = 0
        width = 650
        height = 650

        self.left_top_x = width * window_id
        self.left_top_y = y
        self.width = width
        self.height = height
        self.window_name = window_name
        self.hwnd = hwnd
        self._handle = None
        self.win_capture = win_capture

        self.enum_handler()

    def __del__(self):
        self.send_message(f"TEST Window {self.window_id} destroyed")

    def enum_handler(self):
        if win32gui.IsWindowVisible(self.hwnd):
            if self.window_name in win32gui.GetWindowText(self.hwnd):
                win32gui.MoveWindow(self.hwnd, self.left_top_x, self.left_top_y, self.width, self.height, True)

    def set_foreground(self):
        """put the window in the foreground"""
        win32gui.SetForegroundWindow(self._handle)

    @classmethod
    def send_message(cls, message):
        print(message)