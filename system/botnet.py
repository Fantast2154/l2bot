import datetime
import threading
import socket
import pickle
import time


class Server:
    def __init__(self, machine_id):
        self.id = machine_id
        self.HOST = ''
        self.PORT = 27015
        self.ADDRESS = (self.HOST, self.PORT)
        self.BUFFERSIZE_TEMPORARY = 1000

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDRESS)
        self.server.listen(10)

        self.bots_list = []
        self.bots_data_collection = []
        self.breaked = False

    def server_message(self, text):
        print(datetime.datetime.now().time(), 'Сервер:', text)

    def data_accepting(self):
        data_storage_dict = {}
        while True:
            if not self.bots_list:
                self.bots_data_collection.clear()

            for bot in self.bots_list:
                try:
                    data = bot.recv(self.BUFFERSIZE_TEMPORARY)
                    if data:
                        decoded_data = pickle.loads(data)
                        print(datetime.datetime.now().time(), decoded_data)
                        self.bots_data_collection.append(decoded_data)
                except ConnectionResetError:
                    self.server_message(f'Ошибка получения данных от {bot}')
                    bot.close()
                    self.bots_list.remove(bot)
                    self.server_message(f'Клиент удалён.')

                for item in self.bots_data_collection:
                    for key, value in item.items():
                        if data_storage_dict.get(key) is not None:
                            data_storage_dict[key].append(value)
                        else:
                            data_storage_dict[key] = [value]

                # {уникальный ID машины-отправителя: [сообщение1, сообщение2, ...]} - вид отправляемого сообщения
                #data_to_send = self.bots_data_collection
                data_to_send = data_storage_dict.copy()
                # data_to_send = decoded_data
                encoded_data_to_send = pickle.dumps(data_to_send)
                data_storage_dict.clear()

                for bot_ in self.bots_list:
                    try:
                        bot_.send(encoded_data_to_send)
                    except ConnectionResetError:
                        self.server_message('Ошибка передачи данных')
                        bot_.close()
                        self.bots_list.remove(bot_)
                        self.server_message(f'Клиент удалён.')

    def bots_accepting(self):
        self.server_message('Сервер запущен.')
        while True:
            clientsocket, address = self.server.accept()
            self.bots_list.append(clientsocket)
            self.server_message('Бот установил связь.')
            self.breaked = False

    def server_start(self):
        t1 = threading.Thread(target=self.bots_accepting)
        t2 = threading.Thread(target=self.data_accepting)

        t1.start()
        t2.start()


class Client:
    def __init__(self, machine_id, ip=None):
        self.id = machine_id
        self.HOST = '84.237.53.150'
        self.PORT = 27015
        self.ADDRESS = (self.HOST, self.PORT)
        self.BUFFERSIZE_TEMPORARY = 1000
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.tries = 0

        while not self.connected:
            if self.tries >= 2:
                self.connected = False
                self.client_message('Сервер не отвечает. Работаем в оффлайн режиме')
                break
            try:
                self.client.connect(self.ADDRESS)
                self.connected = True
                self.client_message('Соединение установлено')
            except:
                self.client_message(
                    'Сервер не отвечает. Для технической поддержки, свяжитесь с Баганцем. Скорее всего, вы просто дилетант. АЙПИ ИЗМЕНИЛ? САМ СЕРВЕР ЗАПУЩЕН??? Ну вот и всё.')
                self.tries += 1
                self.client_message(f'Попытка подключения {self.tries}')
                time.sleep(1)

        self.bots_list = []
        self.bots_data_collection = ''

    def is_connected(self):
        return self.connected

    def client_message(self, text):
        print(datetime.datetime.now().time(), f'Бот {self.id}', text)

    def client_send(self, data):
        data_to_encode = {self.id: data}
        #data_to_encode = data
        encoded_data_to_send = pickle.dumps(data_to_encode)
        self.client.send(encoded_data_to_send)

    def client_receive_message(self):
        return self.bots_data_collection

    def data_accepting(self):
        while self.connected:
            try:
                data = self.client.recv(self.BUFFERSIZE_TEMPORARY)
                if data:
                    decoded_data = pickle.loads(data)
                    self.bots_data_collection = decoded_data
                    print(decoded_data)
            except ConnectionResetError:
                self.client.close()

    def connect_to_server(self):
        t = threading.Thread(target=self.data_accepting)
        t.start()


if __name__ == '__main__':
    s = Server()
    s.server_start()

    # time.sleep(2)

    # c = Client()
    # c.connect_to_server()
