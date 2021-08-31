import math
import random
import time
from multiprocessing import Manager

import pyperclip

from system.botnet import Client
import win32gui
import cv2


class TraderA:

    def __init__(self, traderA_window, traderA_id, number_of_tradersA, q):
        manager = Manager()
        self.traderA_window = traderA_window
        self.traderA_id = traderA_id
        self.number_of_tradersA = number_of_tradersA
        self.q = q
        self.send_message(f'created')

        # communication with fisher service
        self.current_state = manager.list()
        self.current_state.append('available')

        self.exit_is_set = manager.list()
        self.exit_is_set.append(False)

    def __del__(self):
        self.send_message(f"destroyed")

    def send_message(self, message):
        temp = '\t' * 10 * self.traderA_id + 'TraderA ' + f'{self.traderA_id}: {message}'
        print(temp)

    def run(self):

        while not self.exit_is_set[0]:
            self.send_message('Im ALIVE')
            time.sleep(2)