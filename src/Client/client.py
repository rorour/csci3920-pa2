import socket


class Client:
    def __init__(self, ip: str, port: int):
        self.__ip = ip
        self.__port = port
        self.__received_msgs = []
        self.__server_receive = None
        self.__is_connected = False

    def connect(self):
        pass

    def send_message(self, msg: str):
        pass

    def receive_message(self):
        pass

    def print_messages(self):
        pass

    def disconnect(self):
        pass
