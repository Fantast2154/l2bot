import win32process
from pywinauto import win32functions

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
import pywinauto
from ctypes import windll
import ctypes

import sys
import win32gui as wgui
import win32process as wproc
import win32api as wapi

import pyperclip


# return self

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
    win32gui.SystemParametersInfo(SPI_SETFOREGROUNDLOCKTIMEOUT, 0, ctypes.byref(timeout), SPIF_SENDCHANGE)
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
        # for param in self.action_params:
        #     print('ACTION PARAM', param[0])
        self.windows.append(window)
        # self.priority_list.append(priority)
        # self.action_rate_list.append(action_rate)
        # self.action_rate_list.insert(0, action_rate)

    def new_mouse_task(self):
        pass

    def new_keyboard_task(self):
        pass

    def window_init(self, window):

        x = window.wincap.offset_x[window.window_id] + 10
        y = window.wincap.offset_y[window.window_id] - 10
        win32api.SetCursorPos((x, y))
        time.sleep(0.1)
        pyautogui.mouseDown()
        time.sleep(0.1)
        pyautogui.mouseUp()
        time.sleep(0.1)

        for i in range(20):
            win32api.SetCursorPos((x+i, y+i))
            time.sleep(0.01)

        print(f'WINDOW {window.window_id} WAS INITIALIZED')

    def click(self, x, y):
        # self.lock.acquire()
        win32api.SetCursorPos((x, y))
        #win32api.

        #pyperclip.copy('123')
        #time.sleep(1)
        #pyperclip.paste()
        #keyboard.send('F4')
        #pyautogui.drag(1, 1, duration=0.1, mouseDownUp=False)
        #win32api.SetCursorPos((x+2, y+2))
        #time.sleep(0.1)
        for i in range(3):
            win32api.SetCursorPos((x+i, y+i))
            #time.sleep(0.01)
        # time.sleep(0.01)
        # pyautogui.mouseDown()
        # time.sleep(0.02)
        # pyautogui.mouseUp()
        # time.sleep(0.01)
        time.sleep(0.01)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        time.sleep(0.01)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        time.sleep(0.01)
        # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        # time.sleep(0.2)
        # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        # self.lock.release()

    def task_execution(self, count, action, params, window, action_rate='High'):
        # try:
        # print('Qsize = ', len(self.queue_list))
        # keyboard.send('s')

        self.lock.acquire()

        #self.focus_by_BOYKO(window.hwnd)
        #self.shell.SendKeys('%')
        #win32gui.SetForegroundWindow(window.hwnd)
        #time.sleep(1)

        # ============================
        # remote_thread, _ = win32process.GetWindowThreadProcessId(handle)
        # win32process.AttachThreadInput(win32api.GetCurrentThreadId(), remote_thread, True)
        # prev_handle = win32gui.SetFocus(handle)

        # ===========================
        # app = pywinauto.application.Application()
        # t, c = u'WINDOW SWAPY RECORDS', u'CLASS SWAPY RECORDS'
        # handle = pywinauto.findwindows.find_windows(title=t, class_name=c)[0]
        # w = app.window(handle=handle)
        # w.Setfocus()

        # win32gui.SetForegroundWindow(window.hwnd)

        # print(f'queue {count} fisher {window.window_id} is calling {action} hwnd = {window.hwnd}\n')

        # params = [0]*6
        if action == 'mouse':

            if len(params) != 6:
                return

            [(x_temp, y_temp)] = params[0]
            x = x_temp + window.wincap.offset_x[window.window_id]
            y = y_temp + window.wincap.offset_y[window.window_id]
            # print('window_id', window.window_id)
            # print('window.wincap.offset_x', window.wincap.offset_x[window.window_id])
            # print('window.wincap.offset_y', window.wincap.offset_y[window.window_id])
            self.focus_by_BOYKO(window.hwnd)
            time.sleep(0.01)
            # self.SetFocus(window.hwnd)
            #win32api.PostMessage(window.hwnd, win32con.WM_CHAR, ord('x'), 0)

            #win32api.SendMessage(window.hwnd, win32con.WM_CHAR, ord('x'), 0)

            #time.sleep(0.5)

            self.click(x, y)
            #time.sleep(0.5)
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
                    if self.windows:
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

    def SetFocus(self, hwnd):
        print('TEST SetFocus')
        """Set the focus to this control
    
        Activate the window if necessary"""
        win32gui.UpdateWindow(hwnd)
        # find the current foreground window
        cur_foreground = win32gui.GetForegroundWindow()
        # print(f'TEST cur_foreground {cur_foreground}')
        # if it is already foreground then just return
        # if hwnd != cur_foreground:
        if True:

            # get the thread of the window that is in the foreground
            # cur_fore_thread = windll.kernel32.GetCurrentThreadId()
            cur_fore_thread = win32api.GetCurrentThreadId()
            print(f'TEST cur_fore_thread {cur_fore_thread}')
            # cur_fore_thread = win32process.GetWindowThreadProcessId(cur_foreground)

            # get the thread of the window that we want to be in the foreground
            control_thread = windll.user32.GetWindowThreadProcessId(cur_foreground, None)
            print(f'TEST control_thread {control_thread}')
            # control_thread = win32process.GetWindowThreadProcessId(hwnd) #TEST

            # if a different thread owns the active window
            if cur_fore_thread != control_thread:
                # Attach the two threads and set the foreground window
                win32process.AttachThreadInput(cur_fore_thread, control_thread, True)
                res = windll.user32.AttachThreadInput(control_thread, cur_fore_thread, True)
                print(f'TEST res {res}')
                ERROR_INVALID_PARAMETER = 87
                if res == 0 and ctypes.GetLastError() != ERROR_INVALID_PARAMETER:
                    print("WARN: could not attach thread input to thread {0} ({1})"
                          .format(control_thread, ctypes.GetLastError()))
                    return

                # detach the thread again
                win32process.AttachThreadInput(
                    cur_fore_thread, control_thread, False)
                # res2 = windll.user32.AttachThreadInput(control_thread, cur_fore_thread, True)
                wproc.AttachThreadInput(wapi.GetCurrentThreadId(), control_thread, True)
                self.shell.SendKeys('%')
                cur_fore_thread = windll.kernel32.GetCurrentThreadId()
                print(f'TEST cur_fore_thread {cur_fore_thread}')
                cur_fore_thread = win32process.GetWindowThreadProcessId(cur_foreground)

                # get the thread of the window that we want to be in the foreground
                control_thread = windll.user32.GetWindowThreadProcessId(cur_foreground, None)
                print(f'TEST control_thread {control_thread}')
                win32gui.SetForegroundWindow(hwnd)  # TEST
                win32gui.SetFocus(hwnd)
                focus_whd = windll.user32.SetFocus(hwnd)
                print(f'TEST set_focus_whd {focus_whd}')
                focus_whd2 = windll.user32.GetFocus()
                print(f'TEST get_focus_whd {focus_whd2}')
                # print(f'TEST res2 {res2}')
            else:  # same threads - just set the foreground window
                win32gui.SetForegroundWindow(hwnd)

        # make sure that we are idle before returning
        win32functions.WaitGuiThreadIdle(hwnd)

        # only sleep if we had to change something!
        time.sleep(.06)

    def focus_by_BOYKO(self, HEX):
        remote_thread, i = wproc.GetWindowThreadProcessId(HEX)
        wproc.AttachThreadInput(wapi.GetCurrentThreadId(), remote_thread, True)
        prev_handle = wgui.SetFocus(HEX)
        self.shell.SendKeys('%')
        win32gui.SetForegroundWindow(HEX)
