import socket


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


#   temp name
class CliServer:
    pass
