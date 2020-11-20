import socket
from datetime import date
from threading import Thread
from Messaging.user import User


class Server:
    def __init__(self, ip: str, port: int, backlog: int):
        self.__queued_messages = []  # all Messages to send
        self.__connected_clients = []  # store ClientWorker & Username together
        self.__user_list = []  # all registered Users
        self.__ip = ip
        self.__port = port
        self.__backlog = backlog
        self.__server_socket = None
        self.__keep_running_server = True
        self.__connection_count = 0

    def load_from_file(self):
        pass

    def save_data(self):
        pass

    def __start_service(self):
        print(f'''Starting Messenger Service''')
        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server_socket.bind((self.__ip, self.__port))
        self.__server_socket.listen(self.__backlog)

        while self.__keep_running_server:
            print(f'''Listening for Connections''')
            try:
                client_socket, client_address = self.__server_socket.accept()
                self.__connection_count += 1
                print(f'''Got a connection from {client_address}''')
                cw = ClientWorker(client_socket, self)
                self.__connected_clients.append(cw)
                cw.start()
            except Exception as e:
                print(e)

    def __stop_service(self):
        print(f'''Stopping Service''')
        self.__keep_running_server = False
        cw: ClientWorker
        for cw in self.__connected_clients:
            cw.terminate_connection()  # tell each cw to close client connection
            cw.join()
        self.__server_socket.close()
        print(f'''Messenger Service Stopped.''')
        pass

    def print_menu(self):
        print(f'1. Load Data from File')
        print(f'2. Start the Messenger Service')
        print(f'3. Stop the Messenger Service')
        print(f'4. Save Data to File')

    def __run_menu(self):
        self.print_menu()
        option = int(input('Choose an option 1-4.'))
        if option == 1:
            print(f'1. Load Data from File')
            pass
        elif option == 2:
            self.__start_service()
        elif option == 3:
            self.__stop_service()
        elif option == 4:
            print(f'4. Save Data to File')
            pass
        else:
            print(f'Unknown command {option}.')

    def run(self):
        while True:
            self.__run_menu()


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

    def terminate_connection(self):
        self.__keep_running_client = False
        self.__client_socket.close()


# Server App ################################################################################
if __name__ == "__main__":
    # create & run server
    server = Server('127.0.0.1', 10000, 10)
    server.run()
    pass
