import win32gui
import win32com.client
import re
import win32con
import psutil
import win32process
import win32process as wproc
import win32api as wapi


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
        # self._handle = None
        self.win_capture = win_capture

        self.enum_handler()

    def __del__(self):
        self.send_message(f"TEST Window {self.window_id} destroyed")

    def enum_handler(self):
        if win32gui.IsWindowVisible(self.hwnd):
            if self.window_name in win32gui.GetWindowText(self.hwnd):
                win32gui.MoveWindow(self.hwnd, self.left_top_x, self.left_top_y, self.width, self.height, True)

    def hide_always_on_top_windows(self):
        win32gui.EnumWindows(self._window_enum_callback_hide, None)

    def _window_enum_callback_hide(self, hwnd, unused):
        if hwnd != self.hwnd:  # ignore self
            # Is the window visible and marked as an always-on-top (topmost) window?
            if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowLong(hwnd,
                                                                         win32con.GWL_EXSTYLE) & win32con.WS_EX_TOPMOST:
                # Ignore windows of class 'Button' (the Start button overlay) and
                # 'Shell_TrayWnd' (the Task Bar).
                className = win32gui.GetClassName(hwnd)
                if not (className == 'Button' or className == 'Shell_TrayWnd'):
                    # Force-minimize the window.
                    # Fortunately, this seems to work even with windows that
                    # have no Minimize button.
                    # Note that if we tried to hide the window with SW_HIDE,
                    # it would disappear from the Task Bar as well.
                    win32gui.ShowWindow(hwnd, win32con.SW_FORCEMINIMIZE)

    def set_foreground(self):
        """put the window in the foreground"""
        # self.hide_always_on_top_windows()
        print('hwnd', self.hwnd)
        # temp_window = win32gui.GetForegroundWindow()
        # print(temp_window)
        # temp_active_window_hwnd = win32gui.IsWindowVisible(self.hwnd)
        # pid = win32process.GetWindowThreadProcessId(self.hwnd)
        # pid = win32process.GetWindowThreadProcessId(w.GetForegroundWindow())
        # print(pid)
        # print(psutil.Process(pid[-1]).name())

            # win32gui.SetForegroundWindow(self.hwnd)
        remote_thread, _ = wproc.GetWindowThreadProcessId(self.hwnd)
        wproc.AttachThreadInput(wapi.GetCurrentThreadId(), remote_thread, True)
        win32gui.SetFocus(self.hwnd)
        # check = win32gui.SetForegroundWindow(self.hwnd)



    @classmethod
    def send_message(cls, message):
        print(message)
