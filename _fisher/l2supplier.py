import threading
import time

from system.botnet import Client


class Supplier(Client, threading.Thread):
    def __init__(self, role):
        self.role = role
        super().__init__(role)


if __name__ == '__main__':
    s = Supplier('Рыбак 1')
    s.connect_to_server()
    time.sleep(3)
    s.client_send('СОСОК НЕТ')
