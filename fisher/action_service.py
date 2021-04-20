import time
import pyautogui
import random
import win32api
import win32con
from threading import Thread, Lock


class ActionService:
    lock = Lock()

    def __init__(self, wincap):
        self.wincap = wincap

    def mouse_move_shefer_edition(self, params):
        [points, click, button, slow, double] = params

        offset_x = self.wincap.offset_x,
        offset_y = self.wincap.offset_y

        game_x = offset_x
        game_y = offset_y

        if points is None:
            return

        elif len(points) == 0:
            return

        elif len(points) > 1:
            for point in points:
                (x_temp, y_temp) = point

        else:
            [(x_temp, y_temp)] = points

        a = random.randint(-3, 3)
        b = random.randint(-3, 3)

        x = game_x + x_temp + a
        y = game_y + y_temp + b

        self.lock.acquire()
        if click:
            if button == 'LEFT' and not slow:
                time.sleep(0.01)
                pyautogui.moveTo(x, y)
                time.sleep(0.02)
                pyautogui.mouseDown()
                time.sleep(0.02)
                pyautogui.mouseUp()
                time.sleep(0.03)

                if double:
                    time.sleep(0.01)
                    pyautogui.moveTo(x, y)
                    time.sleep(0.02)
                    pyautogui.mouseDown()
                    time.sleep(0.02)
                    pyautogui.mouseUp()
                    time.sleep(0.02)
                    pyautogui.mouseDown()
                    time.sleep(0.02)
                    pyautogui.mouseUp()

            elif button == 'LEFT' and slow:
                time.sleep(0.1)
                pyautogui.moveTo(x, y)
                time.sleep(0.3)
                pyautogui.mouseDown()
                time.sleep(0.1)
                pyautogui.mouseUp()
                time.sleep(0.3)

            elif button == 'RIGHT' and not slow:
                time.sleep(0.06)
                pyautogui.moveTo(x, y)
                time.sleep(0.1)
                pyautogui.mouseDown(button='right')
                time.sleep(0.02)
                pyautogui.mouseUp(button='right')
                time.sleep(0.1)

            elif button == 'RIGHT' and slow:
                time.sleep(0.1)
                pyautogui.moveTo(x, y)
                time.sleep(0.3)
                pyautogui.mouseDown(button='right')
                time.sleep(0.1)
                pyautogui.mouseUp(button='right')
                time.sleep(0.3)
        else:
            time.sleep(0.01)
            pyautogui.moveTo(x, y)
            time.sleep(1)

        self.lock.release()

    def mouse_move(self, points, click=True, button='LEFT', slow=False, double=False):
        offset_x = self.wincap.offset_x,
        offset_y = self.wincap.offset_y

        game_x = offset_x
        game_y = offset_y

        if points is None:
            return

        elif len(points) == 0:
            return

        elif len(points) > 1:
            for point in points:
                (x_temp, y_temp) = point

        else:
            [(x_temp, y_temp)] = points

        a = random.randint(-3, 3)
        b = random.randint(-3, 3)

        x = game_x + x_temp + a
        y = game_y + y_temp + b

        self.lock.acquire()
        if click:
            if button == 'LEFT' and not slow:
                time.sleep(0.01)
                pyautogui.moveTo(x, y)
                time.sleep(0.02)
                pyautogui.mouseDown()
                time.sleep(0.02)
                pyautogui.mouseUp()
                time.sleep(0.03)

                if double:
                    time.sleep(0.01)
                    pyautogui.moveTo(x, y)
                    time.sleep(0.02)
                    pyautogui.mouseDown()
                    time.sleep(0.02)
                    pyautogui.mouseUp()
                    time.sleep(0.02)
                    pyautogui.mouseDown()
                    time.sleep(0.02)
                    pyautogui.mouseUp()

            elif button == 'LEFT' and slow:
                time.sleep(0.1)
                pyautogui.moveTo(x, y)
                time.sleep(0.3)
                pyautogui.mouseDown()
                time.sleep(0.1)
                pyautogui.mouseUp()
                time.sleep(0.3)

            elif button == 'RIGHT' and not slow:
                time.sleep(0.06)
                pyautogui.moveTo(x, y)
                time.sleep(0.1)
                pyautogui.mouseDown(button='right')
                time.sleep(0.02)
                pyautogui.mouseUp(button='right')
                time.sleep(0.1)

            elif button == 'RIGHT' and slow:
                time.sleep(0.1)
                pyautogui.moveTo(x, y)
                time.sleep(0.3)
                pyautogui.mouseDown(button='right')
                time.sleep(0.1)
                pyautogui.mouseUp(button='right')
                time.sleep(0.3)
        else:
            time.sleep(0.01)
            pyautogui.moveTo(x, y)
            time.sleep(1)

        self.lock.release()

    def skills_thread_processing(self, skill_pos, click=True, button='LEFT', slow=False, double=False):
        offset_x = self.wincap.offset_x
        offset_y = self.wincap.offset_y
        t = Thread(target=self.mouse_move, args=(skill_pos, click, button, slow, double, offset_x, offset_y))
        # t.daemon = True
        t.start()

    def mouse_alt_double_click(self, point):

        VK_CODE = {'alt': 0x12}
        args = ['alt']
        for i in args:
            win32api.keybd_event(VK_CODE[i], 0, 0, 0)
            time.sleep(0.1)

        if not point:
            return None

        self.mouse_move_double_click(point)

        for i in args:
            win32api.keybd_event(VK_CODE[i], 0, win32con.KEYEVENTF_KEYUP, 0)
            time.sleep(0.1)

    def mouse_move_double_click(self, points):
        offset_x = self.wincap.offset_x,
        offset_y = self.wincap.offset_y

        game_x = offset_x
        game_y = offset_y
        if not points:
            return

        [(x_fishing, y_fishing)] = points

        x = int(game_x + x_fishing)
        y = int(game_y + y_fishing)
        self.lock.acquire()
        time.sleep(0.01)

        pyautogui.moveTo(x, y)
        time.sleep(0.01)
        pyautogui.mouseDown()
        time.sleep(0.01)
        pyautogui.mouseUp()
        time.sleep(0.01)
        pyautogui.mouseDown()
        time.sleep(0.01)
        pyautogui.mouseUp()
        # time.sleep(0.02)

        self.lock.release()

    # def mouse_click(self, point, click=True, button='LEFT', slow=False):  # add da
    #   pass

    def keyboard_press_hold_release(self, hold_time):
        pass
