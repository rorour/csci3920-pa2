from threading import Thread
from Client.client import Client
import socket


class ClientMessage:
    def __init__(self):
        self.__keep_running = True
        self.__is_connected = False
        self.__is_logged_in = False
        self.__client = None
        self.__username = None

    def __menu_options(self):
        print("=" * 30)
        print(f'{"Message Board:":^30}')
        print("1. Connect to server")
        print("2. Login")
        print("3. Send Message")
        print("4. Print Received Messages")
        print("5. Disconnect")
        try:
            menu = int(input("Select option [1-5]: "))
            return menu
        except ValueError:
            pass

    def display_menu(self):
        option = self.__menu_options()
        if option == 1:
            if self.__is_connected:
                print("Already Connected")
            else:
                self.__menu_connect()
        elif option == 2:
            if self.__is_connected:
                self.__menu_login()
            else:
                print("Connect to server before attempting to login")
        elif option == 3:
            if self.__is_logged_in:
                self.__menu_send_message()
            else:
                print("Must be logged in first before using this feature")
        elif option == 4:
            if self.__is_logged_in:
                self.__menu_print_messages()
            else:
                print("Must be logged in first before using this feature")
        elif option == 5:
            if self.__is_connected:
                self.__menu_disconnect()
            else:
                print("Already disconnected from server")
        else:
            print("Invalid input")

    def __menu_connect(self):
        # todo: Test wrong connections
        # ip = str(input("Enter IP Address: "))
        # port = int(input("Enter Port Number: "))
        # self.__client = Client(ip, port)

        # todo: delete testing stuff
        print("IP Address: 127.0.0.1")
        print("Port Number: 10000")
        client = Client('127.0.0.1', 10000)

        self.__client.connect()
        server_message = self.__client.receive_message()
        print(f"""[CLI] SRV -> {server_message}""")
        self.__is_connected = self.__client.is_connected    # changes connection status

    def __menu_login(self):
        log_type = str(input("Existing User? y/n"))
        if log_type.lower() == 'y':
            self._logging_in(True)
        elif log_type.lower() == 'n':
            print("Sign Up: ")
            self._logging_in(False)
        else:
            print("Invalid Input: please answer y or n")

    def __logging_in(self, registered: bool):
        # todo: test logging in
        username = str(input("Enter Username: "))
        password = str(input("Enter Password: "))
        if registered:
            self.__client.send_message(f'LOG|{username}|{password}')
        else:
            display_name = str(input("Enter Display Name: "))
            self.__client.send_message(f'USR|{username}|{password}|{display_name}')

        server_message = self.__client.receive_message()
        print(f"""[CLI] SRV -> {server_message}""")
        if server_message.split('|')[0] == '0':
            self.__username = username
            self.__is_logged_in = True

    def __menu_send_message(self):
        """Sends message to target username"""
        # todo: test sending messages
        username_to = str(input("Input the username to send message to: "))
        message = str(input("Type message: "))
        self.__client.send_message(f'MSG|{self.__username}|{username_to}|{message}')
        server_message = self.__client.receive_message()
        print(f"""[CLI] SRV -> {server_message}""")

    def __menu_print_messages(self):
        # todo: implement receiving messages
        pass

    def __menu_disconnect(self):
        self.__client.send_message('OUT|OK')
        server_message = self.__client.receive_message()
        print(f"""[CLI] SRV -> {server_message}""")
        if server_message.split('|')[0] == '0':
            self.__client.disconnect()
            self.__is_connected = False
            self.__is_logged_in = False
            self.__keep_running = False
        self.__keep_running = True  # todo: delete this once server/client messaging is completed

    @property
    def keep_running(self):
        return self.__keep_running


if __name__ == "__main__":
    messenger = ClientMessage()
    while messenger.keep_running:
        messenger.display_menu()
