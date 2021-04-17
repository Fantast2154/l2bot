from fisher.fishing_service import FishingService
from system.telegram import Telegram
from system.l2window import L2window
from system.screenshot_service import ScreenshotMaster
from system.action_queue import ActionQueue
import sys


def message_gui(message):
    print(message)


def input_number(message):
    while True:
        try:
            userInput = int(input(message))
            if userInput < 0:
                print('The value must be >= 0')
                continue
        except ValueError:
            print("Not an integer! Try again.")
            continue
        else:
            return userInput


if __name__ == '__main__':
    ScreenshotMaster()
    print('PROGRAM start-------------------------------------')
    queue = ActionQueue()
    queue.start()
    screen_analyzer = ScreenshotMaster()
    screen_analyzer.start()

    while True:

        # n = input_number('number of windows: ')
        n = 2
        print('number of windows:', n)
        m = 2  # m = input_number('')
        print('number of fishers: ', m)

        if m > n:
            message_gui("I DON'T HAVE ENOUGH WINDOWS!")
            continue

        if m < 1 or m > 2:
            message_gui('OMG,  ARE YOU KIDDING ME? I SUPPORT ONLY 1 OR 2 FISHERS! KEEP CALM!')
            continue

        windows = []
        for i in range(n):
            windows.append(L2window(i, screen_analyzer))

        windows_f = windows[:m]  # first m windows to be fishers. LATER FIX THIS
        FishingService(m, windows_f, queue)

        queue.stop()
        screen_analyzer.stop()

        sys.exit('PROGRAM ends ......... BYE BYE BYE BYE BYE BYE')
        # print()
        # answer = input('You want to restart the program (type yes) ')
        # if answer != 'yes':
        #     sys.exit('BYE BYE BYE BYE BYE BYE')
        # print('PROGRAM restart-------------------------------------')
        # print()
    # fishing_service.startFishing()
