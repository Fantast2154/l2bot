import threading
import socket
import pickle
import time


class Server:
    def __init__(self):
        self.HOST = ''
        self.PORT = 27015
        self.ADDRESS = (self.HOST, self.PORT)
        self.BUFFERSIZE_TEMPORARY = 1000

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDRESS)
        self.server.listen(10)

        self.bots_list = []
        self.bots_data_collection = {}

    def server_message(self, text):
        print('Сервер:', text)

    def data_accepting(self):
        while True:
            for bot in self.bots_list:
                try:
                    data = bot.recv(self.BUFFERSIZE_TEMPORARY)
                    decoded_data = pickle.loads(data)
                    self.bots_data_collection.update(decoded_data)
                except:
                    self.server_message('Ошибка получения данных')
                    continue

            data_to_send = self.bots_data_collection
            encoded_data_to_send = pickle.dumps(data_to_send)

            for bot in self.bots_list:
                try:
                    bot.send(encoded_data_to_send)
                except:
                    self.server_message('Ошибка передачи данных')
                    continue

    def bots_accepting(self):
        self.server_message('Сервер запущен.')
        while True:
            clientsocket, address = self.server.accept()
            self.bots_list.append(clientsocket)
            self.server_message('Бот установил связь.')

    def server_start(self):
        t1 = threading.Thread(target=self.bots_accepting)
        t2 = threading.Thread(target=self.data_accepting)

        t1.start()
        t2.start()


class Client:
    def __init__(self, bot_id, ip=None):
        self.bot_id = bot_id
        self.HOST = '84.237.53.150'
        self.PORT = 27015
        self.ADDRESS = (self.HOST, self.PORT)
        self.BUFFERSIZE_TEMPORARY = 1000
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.tries = 0

        while not self.connected:
            if self.tries >= 5:
                break
            try:
                self.client.connect(self.ADDRESS)
                self.connected = True
                self.client_message('Соединение установлено')
            except:
                self.client_message('Сервер не отвечает. Для технической поддержки, свяжитесь с Баганцем. Скорее всего вы просто дилетант. АЙПИ ИЗМЕНИЛ? САМ СЕРВЕР ЗАПУЩЕН??? Ну вот и всё.')
                self.tries += 1
                time.sleep(5)

        self.bots_list = []
        self.bots_data_collection = {}

    def client_message(self, text):
        print(f'Бот {self.bot_id}', text)

    def client_send(self, data):
        data_to_encode = {self.bot_id: data}
        encoded_data_to_send = pickle.dumps(data_to_encode)
        self.client.send(encoded_data_to_send)

    def data_accepting(self):
        while self.connected:
            for bot in self.bots_list:
                try:
                    data = bot.recv(self.BUFFERSIZE_TEMPORARY)
                    decoded_data = pickle.loads(data)
                    self.bots_data_collection.update(decoded_data)
                except:
                    self.client_message('Ошибка получения данных')
                    continue

            players_count = len(self.bots_list)
            data_to_send = [self.bots_data_collection, players_count]
            encoded_data_to_send = pickle.dumps(data_to_send)

            for bot in self.bots_list:
                try:
                    bot.send(encoded_data_to_send)
                except:
                    self.client_message('Ошибка передачи данных')
                    continue

    def connect_to_server(self):
        t = threading.Thread(target=self.data_accepting)
        t.start()


if __name__ == '__main__':
    #s = Server()
    #s.server_start()

    #time.sleep(2)

    c = Client(0)
    c.connect_to_server()
    c.client_send('PRIVET')
