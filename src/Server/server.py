import socket
import time
from datetime import date
from threading import Thread
from Messaging.user import User
from Messaging.message import Message


class Server(Thread):
    def __init__(self, ip: str, port: int, backlog: int):
        super().__init__()
        ### todo remove testing below
        self.__queued_messages = [Message('hi', 'me', 'you')]  # all Messages to send
        self.__connected_clients = []  # store ClientWorkers
        self.__user_list = []  # all registered Users
        self.__ip = ip
        self.__port = port
        self.__backlog = backlog
        self.__server_socket = None
        self.__keep_running_server = True
        self.__connection_count = 0

    @property
    def keep_running_server(self):
        return self.__keep_running_server

    @keep_running_server.setter
    def keep_running_server(self, new_val):
        self.__keep_running_server = new_val

    @property
    def server_socket(self):
        return self.__server_socket

    @property
    def queued_messages(self):
        return self.__queued_messages

    @property
    def connected_clients(self):
        return self.__connected_clients

    def run(self):
        print(f'''[SRV] Starting Server''')
        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server_socket.bind((self.__ip, self.__port))
        self.__server_socket.listen(self.__backlog)

        mqw = MessageQueueWorker(self)
        mqw.start()  # start new thread for sending out queued messages

        while self.__keep_running_server:
            print(f'''[SRV] Server waiting for connection''')
            try:
                client_socket, client_address = self.__server_socket.accept()
                self.__connection_count += 1
                print(f'''[SRV] Connection #{self.__connection_count} from {client_address}''')
                cw = ClientWorker(client_socket, self)
                self.__connected_clients.append(cw)
                cw.start()
            except ConnectionAbortedError:
                print('[SRV] No longer listening for new connections.')

        mqw.keep_sending = False  # stop sending out messages
        mqw.join()
        print('[SRV] No longer sending out messages.')

        print('[SRV] Shutting down client connections.')
        cw: ClientWorker
        for cw in self.__connected_clients:
            cw.terminate_connection()  # tell each cw to close client connection
            cw.join()

        print('[SRV] Server has been shut down.')


class ClientWorker(Thread):
    def __init__(self, client_socket: socket, server: Server):
        super().__init__()
        self.__current_user = None
        self.__client_socket = client_socket
        self.__server = server
        self.__keep_running_client = True

    def send_message(self):
        pass

    def receive_message(self):
        pass

    def current_user(self):
        return self.__current_user

    def terminate_connection(self):
        # todo remove self from server current client list
        self.__keep_running_client = False
        self.__client_socket.close()


class MessageQueueWorker(Thread):  # continuously attempts to send queued messages
    def __init__(self, server: Server):
        super().__init__()
        self.__keep_sending = True
        self.__server = server

    @property
    def keep_sending(self):
        return self.__keep_sending

    @keep_sending.setter
    def keep_sending(self, new_val):
        self.__keep_sending = new_val

    def run(self):
        while self.keep_sending:
            for m in self.__server.queued_messages:
                try:
                    # todo iterate through connected_clients.current_users
                    print(f'Currently working on {m}')
                except Exception:
                    # todo catch errors if shutdown while in loop
                    break
                    pass
            pass


