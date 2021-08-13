from pynput.mouse import Controller, Button
import time


def mouse_position_test(mouse, x=150 , y=150):
    mouse.position = (x, y)

def click(mouse, x=150, y=150):
    # print('params', params)
    mouse.position = (x, y)

    mouse.press(Button.left)
    time.sleep(0.07)
    mouse.release(Button.left)
    time.sleep(0.03)

if __name__ == '__main__':
    mouse = Controller()
    x = 500
    y = 500
    time.sleep(1)
    mouse_position_test(mouse, x, y)
    time.sleep(5)
    counter = 0
    while True:
        click(mouse, x, y)
        counter += 1
        if counter > 100:
            break
        time.sleep(0.1)
