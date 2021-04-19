import os
import time
from test_fisher import TestFisher
# from queue import Queue
from multiprocessing import Queue

#os.startfile('C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Accessories\paint')
#time.sleep(2)
q = Queue()

test_window_1 = [800, 500, 900, 500]
test_window_2 = [1100, 400, 1000, 400]

fisher_1 = TestFisher('fisher_1', test_window_1, q)
fisher_2 = TestFisher('fisher_2', test_window_2, q)

fisher_1.start()
fisher_2.start()

# WARNING! МЫШКА БУДЕТ ДВИГАТЬСЯ В ТЕЧЕНИЕ 10 СЕКУНД. НЕ БЕСПОКОЙТЕСЬ!
q.get()
