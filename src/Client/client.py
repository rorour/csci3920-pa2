import socket
from threading import Thread


class Client:
    def __init__(self, ip: str, port: int):
        self.__ip = ip
        self.__port = port
        self.__received_msgs = []
        self.__server_receive = None
        self.__is_connected = False

    @property
    def received_msgs(self):
        return self.__received_msgs

    '''Connect to server socket.'''
    def connect(self):
        try:
            self.__server_receive = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__server_receive.connect((self.__ip, self.__port))
        except ConnectionError:
            print(f'Could not Connect')
        else:
            self.__is_connected = True

    '''Send message to server on first socket.'''
    def send_message(self, msg: str):
        self.__server_receive.send(msg.encode("UTF-8"))

    '''Receive confirmation/error message from server on first socket.'''
    def receive_message(self):
        return self.__server_receive.recv(1024).decode("UTF-8")

    '''Disconnect from server socket.'''
    def disconnect(self):
        self.__server_receive.close()
        self.__is_connected = False

    @property
    def is_connected(self):
        return self.__is_connected


class IncomingMessageChannel(Thread):
    def __init__(self, client_app, ip, port):
        super().__init__()
        self.__client_app = client_app
        self.__incoming_msg_socket = None
        self.__ip = ip
        self.__port = port
        self.__backlog = 1

    @property
    def incoming_msg_socket(self):
        return self.__incoming_msg_socket

    '''
    Runs thread which creates socket for second server connection.
    Continuously listens for messages from other Users sent by server and adds them to client's queue.
    '''
    def run(self):
        # create second socket
        self.__incoming_msg_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__incoming_msg_socket.bind((self.__ip, self.__port))
        self.__incoming_msg_socket.listen(self.__backlog)

        # send second socket port num to server
        self.__client_app.client.send_message(f'{self.__ip}|{self.__port}')

        self.__incoming_msg_socket, client_address = self.__incoming_msg_socket.accept()

        # while keep running client
        while self.__client_app.keep_listening_for_incoming_msgs:
            # read message
            try:
                new_msg = self.__incoming_msg_socket.recv(1024).decode("UTF-8")
                # add to client queue
                self.__client_app.client.received_msgs.append(new_msg)
                # send confirmation to server
                self.__incoming_msg_socket.send('0|OK'.encode("UTF-8"))
            except IOError:
                # break from while loop when socket closed
                break
        self.__incoming_msg_socket.close()

