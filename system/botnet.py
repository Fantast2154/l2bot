import datetime
import threading
import socket
import pickle
import time
from multiprocessing import Process, Manager


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
        self.bots_processing_list = []
        self.bots_data_collection = []
        self.exit_is_set = False

    def server_message(self, text):
        print(datetime.datetime.now().time(), 'Сервер:', text)

    def data_accepting(self):
        while not self.exit_is_set:
            if not self.bots_list:
                self.bots_data_collection.clear()
            else:
                for bot in self.bots_list:
                    if bot not in self.bots_processing_list:
                        threading.Thread(target=self.data_rcv, args=(bot,)).start()

    def data_rcv(self, b):
        self.bots_processing_list.append(b)
        try:
            data_ = b.recv(self.BUFFERSIZE_TEMPORARY)

            if data_:
                decoded_data = pickle.loads(data_)
                print(datetime.datetime.now().time(), decoded_data)
                self.bots_data_collection.append(decoded_data)
                self.send_data(data_)
                self.bots_processing_list.remove(b)
        except:
            try:
                self.bots_processing_list.remove(b)
                b.close()
                self.bots_list.remove(b)
                self.server_message(f'Клиент удалён.')
            except:
                print('Клиент не в списке!!! Вот и всё...')

    def send_data(self, data):

        for bot_ in self.bots_list:
            try:
                bot_.send(data)
            except ConnectionResetError:
                self.server_message('Ошибка передачи данных')
                bot_.close()
                self.bots_list.remove(bot_)
                self.server_message(f'Клиент удалён.')

    def bots_accepting(self):
        self.server_message('Сервер запущен.')
        while not self.exit_is_set:
            clientsocket, address = self.server.accept()
            self.bots_list.append(clientsocket)
            self.server_message('Бот установил связь.')

    def server_start(self):
        t1 = threading.Thread(target=self.bots_accepting)
        t1.start()
        self.data_accepting()


class Client:
    def __init__(self, machine_id, dtt, dtr, ip=None):
        self.id = machine_id
        self.HOST = '84.237.53.150'
        # self.HOST = '213.127.70.95'

        self.dtt = dtt
        self.dtr = dtr

        self.PORT = 27015
        self.ADDRESS = (self.HOST, self.PORT)
        self.BUFFERSIZE_TEMPORARY = 1000
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.has_received = False
        self.tries = 0
        self.exit_is_set = False

        while not self.connected and not self.exit_is_set:
            if self.tries >= 2:
                self.connected = False
                self.client_message('Сервер не отвечает. Работаем в оффлайн режиме')
                break
            try:
                self.server.connect(self.ADDRESS)
                self.connected = True
                self.client_message('Соединение установлено')
                self.data_accepting_thread()
            except:
                self.client_message(
                    'Сервер не отвечает. Для технической поддержки, свяжитесь с Баганцем. Скорее всего, вы просто '
                    'дилетант. АЙПИ ИЗМЕНИЛ? САМ СЕРВЕР ЗАПУЩЕН??? Ну вот и всё.')
                self.tries += 1
                self.client_message(f'Попытка подключения {self.tries}')
                time.sleep(1)

        self.bots_list = []
        #manager = Manager()
        #self.bots_data_collection = manager.list()
        #self.bots_data_collection.append(0)
        self.bots_data_collection = {}

    def is_connected(self):
        return self.connected

    def client_message(self, text):
        print(datetime.datetime.now().time(), f'Бот {self.id}', text)

    def client_send(self):
        #print('client_send', data)

        data_to_encode = {self.id: self.dtt[0]}
        #data_to_encode = {self.id: data}
        # data_to_encode = data
        encoded_data_to_send = pickle.dumps(data_to_encode)
        try:
            self.server.send(encoded_data_to_send)
        except ConnectionResetError:
            self.server.close()

    def client_receive_message(self):
        #self.dtr[0] = self.bots_data_collection
        #print('BOTNET dtr', self.dtr[0])
        #print('BOTNETdata_collection ', self.bots_data_collection)
        self.has_received = True
        #return self.dtr[0]

    def data_accepting(self):
        while self.connected and not self.exit_is_set:
            try:
                if self.has_received:
                    self.bots_data_collection.clear()
                    #self.bots_data_collection[0] = 0
                    self.has_received = False

                data_ = self.server.recv(self.BUFFERSIZE_TEMPORARY)

                if data_:
                    decoded_data = pickle.loads(data_)
                    self.dtr[0] = decoded_data
                    self.bots_data_collection = decoded_data
                    # time.sleep(0.01)
                    #print('CLIENT', self.bots_data_collection)

            except ConnectionResetError:
                self.server.close()

    def data_accepting_thread(self):
        t = threading.Thread(target=self.data_accepting)
        t.start()
        #p = Process(target=self.data_accepting)
        #p.start()


if __name__ == '__main__':
    s = Server(123)
    s.server_start()

    # time.sleep(2)

    # c = Client()
    # c.connect_to_server()
