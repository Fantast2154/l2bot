import datetime
import threading
import socket
import pickle
import time


class Client:
    def __init__(self, machine_id, ip=None):
        self.id = machine_id
        self.HOST = '84.237.53.150'
        # self.HOST = '213.127.70.95'

        self.PORT = 27015
        self.ADDRESS = (self.HOST, self.PORT)
        self.BUFFERSIZE_TEMPORARY = 1000
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.has_received = False
        self.tries = 0

        while not self.connected:
            if self.tries >= 2:
                self.connected = False
                self.client_message('Сервер не отвечает. Работаем в оффлайн режиме')
                break
            try:
                self.server.connect(self.ADDRESS)
                self.connected = True
                self.client_message('Соединение установлено')
                self.connect_to_server()
            except:
                self.client_message(
                    'Сервер не отвечает. Для технической поддержки, свяжитесь с Баганцем. Скорее всего, вы просто дилетант. АЙПИ ИЗМЕНИЛ? САМ СЕРВЕР ЗАПУЩЕН??? Ну вот и всё.')
                self.tries += 1
                self.client_message(f'Попытка подключения {self.tries}')
                time.sleep(1)

        self.bots_list = []
        self.bots_data_collection = {}

    def is_connected(self):
        return self.connected

    def client_message(self, text):
        print(datetime.datetime.now().time(), f'Бот {self.id}', text)

    def client_send(self, data):
        print('client_send', data)
        data_to_encode = {self.id: data}
        # data_to_encode = data
        encoded_data_to_send = pickle.dumps(data_to_encode)
        self.server.send(encoded_data_to_send)

    def client_receive_message(self):
        #if not self.has_received:
        x = self.bots_data_collection
        self.has_received = True
        return x

    def data_accepting(self):
        while self.connected:

            try:
                if self.has_received:
                    self.bots_data_collection.clear()
                    self.has_received = False

                data = self.server.recv(self.BUFFERSIZE_TEMPORARY)
                #print('data', data)
                #
                if data:
                    decoded_data = pickle.loads(data)
                    self.bots_data_collection = decoded_data
                    #time.sleep(0.01)
                    print('CLIENT', decoded_data)

            except ConnectionResetError:
                self.server.close()

    def connect_to_server(self):
        t = threading.Thread(target=self.data_accepting)
        t.start()


if __name__ == '__main__':
    s = Server(123)
    s.server_start()

    # time.sleep(2)

    # c = Client(123)
    # c.connect_to_server()
