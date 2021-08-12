import datetime
import threading
import socket
import pickle
import time
import multiprocessing


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

        # ШТУЧКИ ДЛЯ ФИШИНГ СЕРВИС
        self.number_of_fishers_ = 0
        self.number_of_suppliers_ = 0
        self.number_of_teleporters_ = 0
        self.number_of_buffers_ = 0

        self.fishers_request = {}
        self.suppliers_request = {}
        self.teleporters_request = {}
        self.buffers_request = {}

        self.fishers = []
        self.suppliers = []
        self.teleporters = []
        self.buffers = []

        self.has_supplier = False

        while not self.connected:
            if self.tries >= 2:
                self.connected = False
                self.client_message('Сервер не отвечает. Работаем в оффлайн режиме')
                break
            try:
                self.client.connect(self.ADDRESS)
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
        # print('client_send', data)
        data_to_encode = {self.id: data}
        # data_to_encode = data
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
                    # print(decoded_data)
            except ConnectionResetError:
                self.client.close()

    def connect_to_server(self):
        # t1 = threading.Thread(target=self.data_accepting)
        # t2 = threading.Thread(target=self.process_server_data)
        # t1.start()
        # t2.start()

        p1 = multiprocessing.Process(target=self.data_accepting)
        p2 = multiprocessing.Process(target=self.process_server_data)
        p1.start()
        p2.start()

    def listen_to_server_0(self):
        amount = {'amount': {
            'fishers': self.number_of_fishers_,
            'suppliers': self.number_of_suppliers_,
            'teleporters': self.number_of_teleporters_,
            'buffers': self.number_of_buffers_
        }}

        status = {'status': {
            'fishers': [{fisher.fisher_id: fisher.current_state[0]} for fisher in self.fishers],
            'suppliers': [{supplier.supplier_id: supplier.current_state[0]} for supplier in self.suppliers],
            'teleporters': [{teleporter.teleporter_id: teleporter.current_state[0]} for teleporter in self.teleporters],
            'buffers': [{buffer.buffer_id: buffer.current_state[0]} for buffer in self.buffers]
        }}

        request = {'request': {
            'fishers': self.fishers_request,
            'suppliers': self.suppliers_request,
            'teleporters': self.teleporters_request,
            'buffers': self.buffers_request
        }}

        data = {}
        data.update(amount)
        data.update(status)
        data.update(request)

        self.client_send(data)

    def request_server_for_supplying(self, fisher_id, dic):
        self.fishers_request = {fisher_id: dic}

    def start_supply(self, supplies):
        # supplies = supplies[sender_id] = {fisher_id: dic_resource}
        # supplies = {sender_id: {fisher_id: {'d_baits': a, 'n_baits': b, 'soski': c}}}
        print('^^^^^^^^^^^^start_supply^^^^^^^^^^^^^^^^^^^^^^^^')
        exit_ = False
        while not exit_:
            for supp in self.suppliers:
                if supp.current_state[0] == 'available':
                    for sender_id, supps in supplies.copy().items():
                        # supps = {fisher_id: dic_resource}
                        # dic_resource = {'d_baits': a, 'n_baits': b, 'soski': c}
                        for fisher_id, dic_resource in supps.items():
                            supp.supply(sender_id, fisher_id, dic_resource)
                            exit_ = True
                        # del supplies[sender_id]
                else:
                    continue

    # def start_supply(self, supplies):
    #     # supplies = supplies[sender_id] = {fisher_id: dic_resource}
    #     # supplies = {sender_id: {fisher_id: {'d_baits': a, 'n_baits': b, 'soski': c}}}
    #     exit_ = False
    #     while not exit_:
    #         for supp in self.suppliers:
    #             if supp.current_state[0] == 'available':
    #                 for t in q:
    #                     for fisher_ID, resource in t.items():
    #                         self.fishers[fisher_ID].supply_request_proceed[0] = True
    #                         self.fishers[fisher_ID].current_state[0] = 'busy'
    #                         print('fisher_ID', fisher_ID)
    #                         self.fishers[fisher_ID].trading_is_allowed[0] = True
    #                         time.sleep(0.5)
    #                         supp.supply(fisher_ID, resource)
    #                         time.sleep(0.5)
    #                         print('!!!!!!!!!!!!!!!!!!!!!!.trading_is_allowed[0]',
    #                               self.fishers[fisher_ID].trading_is_allowed[0])
    #                         exit_ = True
    #             else:
    #                 continue
    #
    #     print('start_supply q', q)

    def process_server_data(self):
        c = 0
        while True:
            c += 1
            if c > 1000000000:
                print('BOTNET process_server_data')
            continue

        # {уникальный ID машины-отправителя: [сообщение1, сообщение2, ...]} - вид отправляемого сообщения сообщение1
        # имеет вид {fisher_id: dict} -> {fisher_id: {'d_baits': a, 'n_baits': b, 'soski': c}}, где a,
        # b и c - количество дневных наживок, ночных наживок и сосок соответственно

        self_proceed = False
        proceed = False
        any_supp_is_available = []
        who_requests_supplying = {}
        supplies = {}
        supplying = False

        while True:
            message = self.client_receive_message()
            if message:
                for sender_id, data_ in message.items():
                    temp_fishers_ids = []
                    for datum in data_:
                        for fisher_status in datum['status']['fishers']:
                            for fisher_id, status in fisher_status.items():
                                if status == 'requests supplying':
                                    # print('self.message', self.message)
                                    temp_fishers_ids.append(fisher_id)

                        if datum['request']['fishers'].items():
                            # print('ITEMS request fishers', datum['request']['fishers'].items())
                            # dic_resource = {'d_baits': a, 'n_baits': b, 'soski': c}
                            for fisher_id, dic_resource in datum['request']['fishers'].items():
                                supplies[sender_id] = {fisher_id: dic_resource}
                                proceed = True

                        for supp_status in datum['status']['suppliers']:
                            if 'available' in supp_status.values():
                                any_supp_is_available.append(True)
                    if temp_fishers_ids:
                        who_requests_supplying[sender_id] = temp_fishers_ids
                    # print('who_requests_supplying', who_requests_supplying)

                if message.get(self.id) is not None:
                    shefer = message.get(self.id)
                    self_proceed = True

            if self_proceed:
                # print('self_proceed', self_proceed)
                for data in shefer:
                    # print("data['status']['fishers']", data['status']['fishers'])
                    # print('fishers amount', data['amount']['fishers'])
                    # print('fishers status ', data['status']['fishers'])
                    # print('fishers request', data['request']['fishers'])
                    for fishers_status in data['status']['fishers']:
                        for fisher_id, status in fishers_status.items():
                            if status == 'requests supplying' and numpy.array(any_supp_is_available).any():
                                # print("status", status)
                                temp_dict = {'dbaits': 0, 'nbaits': 0, 'soski': 0}
                                for index, key in enumerate(temp_dict):
                                    temp_dict[key] = self.fishers[fisher_id].requested_items_to_supply[index]

                                resource = temp_dict.copy()
                                # print('++++++++++++++++++++++++++++++++++request_server_for_supplying fisher_id resource', fisher_id, resource)

                                self.request_server_for_supplying(fisher_id, resource)
                                self.fishers[fisher_id].supply_request_proceed[0] = True
                                self.fishers[fisher_id].current_state[0] = 'busy'
                                self.fishers[fisher_id].trading_is_allowed[0] = True

                                print('PARAMETERS ARE CHANGED')
                                self_proceed = False

            if self.has_supplier and proceed:
                # print('!!!!!!!!!!!!!!self.has_supplier and proceed!!!!!!!!!!!!!!!!!!', who_requests_supplying)
                need_to_supply = False
                proceed = False
                # print('(((((((((((((((((((( who_requests_supplying', who_requests_supplying)
                for sender_id, fishers_ids in who_requests_supplying.items():
                    for fisher_index in fishers_ids:
                        # dic_resource = {'d_baits': a, 'n_baits': b, 'soski': c}
                        if supplies[sender_id][fisher_index].values():
                            # print('000000000000000000need_to_supply!!!!')
                            need_to_supply = True

                if need_to_supply:
                    # print('start_supply', supplies)
                    self.start_supply(supplies)
                    who_requests_supplying.clear()

                who_requests_supplying = {}
                any_supp_is_available = []
                supplies = {}
