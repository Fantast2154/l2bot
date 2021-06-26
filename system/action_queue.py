import win32process

from system.action_service import ActionService
import time
import queue
import threading
from threading import Lock
import win32gui
import pyautogui
import win32com.client
import win32api
import win32con
import keyboard
import platform


def forceFocus(wnd):
    if platform.system() != 'Windows':
        return

    SPI_GETFOREGROUNDLOCKTIMEOUT = 0x2000
    SPI_SETFOREGROUNDLOCKTIMEOUT = 0x2001

    SW_RESTORE = 9
    SPIF_SENDCHANGE = 2

    import ctypes
    IsIconic = ctypes.windll.user32.IsIconic
    ShowWindow = ctypes.windll.user32.ShowWindow
    GetForegroundWindow = ctypes.windll.user32.GetForegroundWindow
    GetWindowThreadProcessId = ctypes.windll.user32.GetWindowThreadProcessId
    BringWindowToTop = ctypes.windll.user32.BringWindowToTop
    AttachThreadInput = ctypes.windll.user32.AttachThreadInput
    SetForegroundWindow = ctypes.windll.user32.SetForegroundWindow

    if IsIconic(wnd):
        ShowWindow(wnd, SW_RESTORE)

    if GetForegroundWindow() == wnd:
        return True

    ForegroundThreadID = GetWindowThreadProcessId(GetForegroundWindow(), None)
    ThisThreadID = GetWindowThreadProcessId(wnd, None)
    if AttachThreadInput(ThisThreadID, ForegroundThreadID, True):
        BringWindowToTop(wnd)
        SetForegroundWindow(wnd)
        AttachThreadInput(ThisThreadID, ForegroundThreadID, False)
        if GetForegroundWindow() == wnd:
            return True

    timeout = ctypes.c_int()
    zero = ctypes.c_int(0)
    win32gui.SystemParametersInfo(SPI_GETFOREGROUNDLOCKTIMEOUT, 0, ctypes.byref(timeout), 0)
    win32gui.SystemParametersInfo(SPI_SETFOREGROUNDLOCKTIMEOUT, 0, ctypes.byref(zero), SPIF_SENDCHANGE)
    BringWindowToTop(wnd)
    SetForegroundWindow(wnd)
    win32gui.SystemParametersInfo(SPI_SETFOREGROUNDLOCKTIMEOUT, 0, ctypes.byref(timeout), SPIF_SENDCHANGE);
    if GetForegroundWindow() == wnd:
        return True

    return False


class ActionQueue(threading.Thread):
    number = None

    actions = []
    action_params = []
    windows = []
    priority_list = []
    action_rate_list = []

    def __init__(self):
        self.send_message(f'Queue created\n')
        threading.Thread.__init__(self)
        # self.action_service = ActionService(wincap)
        self.lock = Lock()
        self.exit = threading.Event()
        # self.queue_list = queue.Queue()
        self.queue_list = []
        self.shell = win32com.client.Dispatch("WScript.Shell")
        self.shell.SendKeys('%')

    def activate_l2windows(self, windows):
        try:
            for window in windows:
                self.lock.acquire()
                time.sleep(0.05)
                self.shell.SendKeys('%')
                win32gui.SetForegroundWindow(window.hwnd)
                time.sleep(0.05)
                self.lock.release()
        except:
            print('TEST queue window activation error')

    def send_message(self, message):
        temp = 'ActionQueue' + ': ' + message
        print(temp)

    def new_task(self, count, action, action_param, window, priority='Normal', action_rate='High'):
        self.queue_list.append(count)
        self.actions.append(action)
        self.action_params.append(action_param)
        self.windows.append(window)
        # self.priority_list.append(priority)
        # self.action_rate_list.append(action_rate)
        # self.action_rate_list.insert(0, action_rate)

    def new_mouse_task(self):
        pass

    def new_keyboard_task(self):
        pass

    def click(self, x, y):
        # self.lock.acquire()
        win32api.SetCursorPos((x, y))

        print('CLICK')
        time.sleep(0.5)
        pyautogui.mouseDown()
        time.sleep(0.1)
        pyautogui.mouseUp()
        time.sleep(0.5)
        # pyautogui.mouseDown()
        # time.sleep(0.1)
        # pyautogui.mouseUp()
        # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        # time.sleep(0.2)
        # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        # time.sleep(0.2)
        # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        # time.sleep(0.2)
        # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        # self.lock.release()

    def task_execution(self, count, action, params, window, action_rate='High'):
        # try:
        # print('Qsize = ', len(self.queue_list))

        self.lock.acquire()
        print(win32gui.GetForegroundWindow())
        # win32gui.SetFocus(window.hwnd)
        # if win32gui.GetForegroundWindow() != window.hwnd:
        #     pyautogui.keyDown('alt')
        #     time.sleep(.01)
        #     pyautogui.press('tab')
        #     time.sleep(.01)
        #     pyautogui.keyUp('alt')
        #     print(win32gui.GetForegroundWindow())
        # print('TETSTSTSTS')
        # time.sleep(0.1)
        # print('tetstst', win32gui.IsWindowVisible(window.hwnd))
        # win32gui.SetForegroundWindow(window.hwnd)

        # win32gui.SetActiveWindow(window.hwnd)
        # win32gui.ShowWindow(window.hwnd, 9)
        # self.shell.SendKeys('%')
        # win32gui.BringWindowToTop(window.hwnd)
        # win32gui.SetForegroundWindow(window.hwnd)
        # win32gui.ShowWindow(window.hwnd, win32con.SW_SHOWMAXIMIZED)
        forceFocus(window.hwnd)

        # win32gui.SetForegroundWindow(window.hwnd)
        time.sleep(0.5)
        # print(f'queue {count} fisher {window.window_id} is calling {action} hwnd = {window.hwnd}\n')

        # params = [0]*6
        if action == 'mouse':

            if len(params) != 6:
                return

            [(x_temp, y_temp)] = params[0]
            x = x_temp + window.wincap.offset_x[window.window_id]
            y = y_temp + window.wincap.offset_y[window.window_id]
            print('window_id', window.window_id)
            print('window.wincap.offset_x', window.wincap.offset_x[window.window_id])
            print('window.wincap.offset_y', window.wincap.offset_y[window.window_id])
            self.click(x, y)
            # self.lock.release()
            # print(params)
            # self.action_service.mouse_master(params)
        if action == 'keyboard':
            if len(params) != 2:
                return
            # self.action_service.keyboard_master(params)
        # except:
        # print('TEST queue window activation error')
        self.lock.release()

    @classmethod
    def start_queueing(cls):
        pass

    def stop(self):
        self.send_message(f'TEST Queue destroyed\n')
        self.exit.set()

    def run(self):
        self.start_queueing()

        while not self.exit.is_set():
            # while not self.queue_list.empty():
            while self.queue_list:
                try:
                    # priority = self.priority_list[0]
                    if self.windows[0]:
                        window = self.windows[0]
                        action = self.actions[0]
                        action_param = self.action_params[0]
                    else:
                        continue
                    # action = self.actions[0]

                    # del self.priority_list[0]

                    del self.windows[0]
                    del self.actions[0]
                    del self.action_params[0]

                    self.task_execution(self.queue_list.pop(-1), action, action_param, window)
                finally:
                    pass
