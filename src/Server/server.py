import socket
from threading import Thread
from Messaging.user import User
from Messaging.message import Message


class Server(Thread):
    def __init__(self, ip: str, port: int, backlog: int):
        super().__init__()
        self.__queued_messages = []  # all Messages to send
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

    @property
    def user_list(self):
        return self.__user_list

    @property
    def connection_count(self):
        return self.__connection_count

    '''
    Runs thread to accept connections from clients and passes connections to ClientWorker.
    Starts MessageQueueWorker thread to send messages to clients.
    Shuts down server and all connections when keep_running_server is False.
    '''
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
                print(f'''\n[SRV] Connection #{self.__connection_count} from {client_address}''')
                cw = ClientWorker(client_socket, self, self.__connection_count)
                self.__connected_clients.append(cw)
                cw.start()
            except (ConnectionAbortedError, OSError):
                print('[SRV] No longer listening for new connections.')

        mqw.keep_sending = False  # stop sending out messages
        mqw.join()
        print('[SRV] No longer sending out messages.')

        print('[SRV] Shutting down client connections.')
        cw: ClientWorker
        for cw in self.__connected_clients:
            cw.terminate_connection()  # tell each cw to close client connection
            cw.join()

        print('[SRV] Finished shutting down.')


class ClientWorker(Thread):
    def __init__(self, client_socket: socket, server: Server, id):
        super().__init__()
        self.__current_user = None  # User Type
        self.__client_socket = client_socket
        self.__server = server
        self.__keep_running_client = True
        self.__outgoing_msg_socket = None
        self.__id = id

    @property
    def outgoing_msg_socket(self):
        return self.__outgoing_msg_socket

    def __send_message(self, msg):
        self.__client_socket.send(msg.encode('UTF-8'))


    def __receive_message(self, max_length: int = 1024):
        msg = self.__client_socket.recvmsg(max_length)[0].decode('UTF-8')
        return msg

    def current_user(self):
        return self.__current_user

    '''Terminate client connection and remove self from list of connected clients.'''
    def terminate_connection(self):
        self.__server.connected_clients.remove(self)
        self.__keep_running_client = False
        if self.__client_socket is not None:
            self.__client_socket.close()
        print(f'[SRV] Connection #{self.__id} closed.')

    '''Runs thread which allows connected client to log in and then processes client requests.'''
    def run(self):
        self.__send_message('Connected to Messaging System Server')
        # first message should be registration or login
        not_disconnected = self.__login_or_register()
        if not_disconnected:
            self.__second_socket_connection()
            # process client request
            while self.__keep_running_client:
                try:
                    self.__process_client_request()
                except Exception as e:
                    print(e)
        else:
            print(f'Client {self.__id} disconnected before login.')

    '''Logs in User if registered and not already logged in.'''
    def __log_in(self, msg_args):
        username = msg_args[1]
        password = msg_args[2]
        # check if user is registered
        registered = False
        correct_password = False
        u: User
        for u in self.__server.user_list:
            if u.username == username:
                registered = True
                if u.password == password:
                    correct_password = True
                    user_to_login = u
                break
        if not registered:
            self.__send_message(f'1|User {username} not registered.')
            return
        # check if user is already logged in
        already_logged_in = False
        cw: ClientWorker
        for cw in self.__server.connected_clients:
            if cw.current_user() is not None and cw.current_user().username == username:
                already_logged_in = True
                break
        if already_logged_in:
            self.__send_message(f'2|User {username} already logged in.')
            return
        # check password
        if correct_password:
            self.__send_message(f'0|Correct password|{self.__id}|{user_to_login.display_name}')  # provide connection # to create unique port number
            self.__current_user = user_to_login
        else:
            self.__send_message(f'1|Incorrect password.')

    '''Creates a new User if username is not taken.'''
    def __create_user(self, msg_args):
        username = msg_args[1]
        password = msg_args[2]
        display_name = msg_args[3]
        # check if username already exists
        registered = False
        u: User
        for u in self.__server.user_list:
            if u.username == username:
                registered = True
        if registered:
            self.__send_message(f'1|Username {username} already registered.')
            return
        else:
            new_user = User(username, password, display_name)
            self.__server.user_list.append(new_user)
            self.__log_in(['0', username, password])
        pass

    '''Takes client input and passes to method to either log in or register new User.'''
    def __login_or_register(self):
        not_disconnected = True
        msg_args = ['']
        while self.__current_user is None and not msg_args[0] == 'OUT':
            msg = self.__receive_message()
            msg_args = msg.split('|')
            if msg_args[0] == 'LOG':
                self.__log_in(msg_args)
                pass
            elif msg_args[0] == 'USR':
                self.__create_user(msg_args)
                pass
            elif msg_args[0] == 'OUT':
                self.__send_message('0|OK')
                self.terminate_connection()
                not_disconnected = False
            else:
                self.__send_message('1|Unknown command to log in user.')
        return not_disconnected

    '''Process request from client: either receive message from client or log out'''
    def __process_client_request(self):
        client_msg = self.__receive_message()
        client_msg_args = client_msg.split('|')
        if client_msg_args[0] == 'MSG':  # recv msg from client
            self.__process_incoming_msg(client_msg_args)
        elif client_msg_args[0] == 'OUT':  # logout and disconnect client
            self.__send_message('0|OK')
            self.terminate_connection()

    '''Set up second connection to client to send messages from other Users to client'''
    def __second_socket_connection(self):
        # get port num from original connection
        new_socket_info = self.__receive_message()
        new_socket_info = new_socket_info.split('|')
        ip = new_socket_info[0]
        port = int(new_socket_info[1])
        # connect to second socket
        self.__outgoing_msg_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__outgoing_msg_socket.connect((ip, port))

    '''
    Accept incoming message from client if sender & receiver are registered.
    Sends confirmation to client.
    '''
    def __process_incoming_msg(self, client_msg_args):
        sender = client_msg_args[1]
        recipient = client_msg_args[2]
        msg_content = client_msg_args[3]
        # check if user is registered
        found_recipient = [u for u in self.__server.user_list if u.username == recipient]
        if not found_recipient:
            self.__send_message(f'1|No target user {recipient}.')
            return
        found_sender = [u for u in self.__server.user_list if u.username == sender]
        if not found_sender:
            self.__send_message(f'1|No source user {sender}.')
            return
        self.__server.queued_messages.append(Message(msg_content, sender, recipient))
        self.__send_message('0|Message accepted')


class MessageQueueWorker(Thread):
    def __init__(self, server: Server):
        super().__init__()
        self.__keep_sending = True
        self.__server = server

    def __send_message(self, socket: socket, msg):
        socket.send(msg.encode('UTF-8'))

    def __receive_message(self, socket: socket, max_length: int = 1024):
        #msg = socket.recvmsg(max_length)[0].decode('UTF-8')
        msg = socket.recv(max_length).decode('UTF-8')
        return msg

    @property
    def keep_sending(self):
        return self.__keep_sending

    @keep_sending.setter
    def keep_sending(self, new_val):
        self.__keep_sending = new_val

    '''Runs MessageQueueWorker thread to continuously attempt to send queued messages to logged-in Users'''
    def run(self):
        while self.keep_sending:
            u: ClientWorker
            for u in self.__server.connected_clients:
                # filter out connected users that have not logged in
                if u.current_user() is not None and u.outgoing_msg_socket is not None:
                    try:
                        user_msgs = [m for m in self.__server.queued_messages if m.recipient == u.current_user().username]
                        for msg in user_msgs:
                            self.__send_message(u.outgoing_msg_socket, str(msg))
                            confirmation = self.__receive_message(u.outgoing_msg_socket)
                            try:
                                print(
                                    f'Attempted to send {msg} to {u.current_user().username} : Client said -> {confirmation}')
                                if confirmation.split('|')[0] == '0':
                                    self.__server.queued_messages.remove(msg)
                            except Exception as e:
                                print(f'MessageQueueWorker: {e}')
                    except OSError as ose:
                        # this will be thrown if second socket is not finished setting up. move on to different CW
                        pass
