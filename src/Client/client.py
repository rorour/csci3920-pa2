import socket
from threading import Thread


class Client:
    def __init__(self, ip: str, port: int):
        self.__ip = ip
        self.__port = port
        self.__received_msgs = []
        self.__server_receive = None
        self.__is_connected = False

    def connect(self):
        try:
            self.__server_receive = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__server_receive.connect((self.__ip, self.__port))
            self.__is_connected = True
        except ConnectionError as c:
            print(f'Could not Connect: {c}')

    def send_message(self, msg: str):
        self.__server_receive.send(msg.encode("UTF-8"))

    def receive_message(self):
        return self.__server_receive.recv(1024).decode("UTF-8")

    def print_messages(self):
        # todo: implement
        pass

    def disconnect(self):
        self.__server_receive.close()
        self.__is_connected = False

    @property
    def is_connected(self):
        return self.__is_connected


class IncomingMessageChannel(Thread):
    __port_num = 10010

    def __init__(self, client_app, ip):
        super().__init__()
        self.__client_app = client_app
        self.__incoming_msg_socket = None
        self.__ip = ip
        self.__port = IncomingMessageChannel.__port_num
        IncomingMessageChannel.__port_num += 1
        self.__backlog = 1

    # @staticmethod
    # def port_num():
    #     return IncomingMessageChannel.__port_num
    #
    # @staticmethod
    # def increment_port_num():
    #     IncomingMessageChannel.__port_num += 1

    def run(self):
        # create second socket
        self.__incoming_msg_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__incoming_msg_socket.bind((self.__ip, self.__port))
        self.__incoming_msg_socket.listen(self.__backlog)

        # send second socket port num to server
        self.__client_app.client.send_message(f'{self.__ip}|{self.__port}')

        # while keep running client
        while self.__client_app.keep_listening_for_incoming_msgs:
            pass
            # read message
        # add to client queue
        # send confirmation to server

        pass

