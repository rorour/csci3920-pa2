from threading import Thread
from Client.client import Client, IncomingMessageChannel
import socket


class ClientMessage:
    def __init__(self):
        self.__keep_running = True
        self.__is_connected = False
        self.__is_logged_in = False
        self.__client = None
        self.__id = None
        self.__username = None
        self.__incoming_msg_channel = None
        self.__listen_for_incoming_msgs = False
        self.__ip = None
        self.__port = None
        self.__second_socket_port = None
        self.__display_name = None

    '''Starts main client-side thread.'''
    def run(self):
        while self.__keep_running:
            self.display_menu()

    '''Print User info and menu.'''
    def __menu_options(self):
        print("=" * 50)
        print(f'{"Message Board:":^50}')
        print(f'{"Connected to Server" if self.__is_connected else "Not Connected to Server":^50}')
        welcome = "Welcome "
        welcome += str(self.__display_name) + "!"
        print(f'{welcome if self.__is_logged_in else "Not Logged in":^50}')
        # print(f'Welcome {self.__username}' if self.__is_logged_in else 'Not Logged In')
        print("-" * 50)

        print("1. Connect to server")
        print("2. Login")
        print("3. Send Message")
        print("4. Print Received Messages")
        print("5. Disconnect")
        print("-" * 50)
        try:
            menu = int(input("Select option [1-5]: "))
            print("-" * 50)
            return menu
        except ValueError:
            pass

    '''Display menu and take user input for menu choice.'''
    def display_menu(self):
        option = self.__menu_options()
        if option == 1:
            if self.__is_connected:
                print("Already Connected")
            else:
                self.__menu_connect()
        elif option == 2:
            if not self.__is_logged_in:  # prevent attempting to login if already logged in
                if self.__is_connected:
                    self.__menu_login()
                    if self.__is_logged_in:
                        self.__create_incoming_channel()
                else:
                    print("Connect to server before attempting to login")
            else:
                print(f'Already logged in as {self.__username}')
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
                print("Already disconnected from server. Exiting program instead")
                self.__keep_running = False
        else:
            print("Invalid input")

    '''Connects to server with ip and port provided by keyboard input.'''
    def __menu_connect(self):
        self.__ip = str(input("Server IP: "))
        self.__port = int(input("Port: "))
        self.__client = Client(self.__ip, self.__port)

        print("Attempting to Connect...")
        self.__client.connect()

        if self.__client.is_connected:
            server_message = self.__client.receive_message()
            print(f"""[CLI] SRV -> {server_message}""")
            self.__is_connected = self.__client.is_connected  # changes connection status

    '''Gets user keyboard input for login or signup'''
    def __menu_login(self):
        log_type = str(input("Existing User? y/n : "))
        if log_type.lower() == 'y':
            self.__logging_in(True)
        elif log_type.lower() == 'n':
            print("Sign Up")
            self.__logging_in(False)
        else:
            print("Invalid Input: please answer y or n")

    '''Gets login info from keyboard input and sends to server'''
    def __logging_in(self, registered: bool):
        username = str(input("Enter Username: "))
        password = str(input("Enter Password: "))
        if registered:
            self.__client.send_message(f'LOG|{username}|{password}')
        else:
            display_name = str(input("Enter Display Name: "))
            self.__client.send_message(f'USR|{username}|{password}|{display_name}')

        server_message = self.__client.receive_message()
        print(f"""[CLI] SRV -> {server_message}""")
        server_msg = server_message.split('|')
        if server_msg[0] == '0':
            self.__username = username
            self.__is_logged_in = True
            self.__id = server_msg[2]
            self.__display_name = server_msg[3]

    """Sends message to target username"""
    def __menu_send_message(self):
        username_to = str(input("Input the username to send message to: "))
        message = str(input("Type message [max 500 char]: "))
        if len(message) <= 500:
            self.__client.send_message(f'MSG|{self.__username}|{username_to}|{message}')
            server_message = self.__client.receive_message()
            print(f"""[CLI] SRV -> {server_message}""")
        else:
            print("500 Character limit reached: Did not send message")

    '''Print all messages in queue.'''
    def __menu_print_messages(self):
        while self.__client.received_msgs:
            m = self.__client.received_msgs[0]
            print(m)
            self.__client.received_msgs.remove(m)

    '''
    Logout and disconnect from server.
    Prints all remaining received messages in queue.
    '''
    def __menu_disconnect(self):
        print('Disconnecting and shutting down.')
        # output all remaining messages in queue
        if self.__client.received_msgs:
            print('Remaining messages in queue:')
        self.__menu_print_messages()
        self.__client.send_message('OUT|OK')
        server_message = self.__client.receive_message()
        print(f"""[CLI] SRV -> {server_message}""")
        if server_message.split('|')[0] == '0':
            self.__listen_for_incoming_msgs = False
            if self.__incoming_msg_channel is not None:
                self.__incoming_msg_channel.incoming_msg_socket.close()
                self.__incoming_msg_channel.join()
            self.__client.disconnect()
            self.__is_connected = False
            self.__is_logged_in = False
            self.__keep_running = False
            print('Successfully shut down.')
        else:
            print('Did not close connection to server.')

    @property
    def keep_running(self):
        return self.__keep_running

    @property
    def keep_listening_for_incoming_msgs(self):
        return self.__listen_for_incoming_msgs

    @keep_listening_for_incoming_msgs.setter
    def keep_listening_for_incoming_msgs(self, new_val):
        self.__listen_for_incoming_msgs = new_val

    @property
    def client(self):
        return self.__client

    '''Create socket for second connection to server and start new thread once server connects.'''
    def __create_incoming_channel(self):
        self.__second_socket_port = 10010 + int(self.__id)
        self.__incoming_msg_channel = IncomingMessageChannel(self, self.__ip, self.__second_socket_port)
        self.__listen_for_incoming_msgs = True
        self.__incoming_msg_channel.start()


if __name__ == "__main__":
    messenger = ClientMessage()
    messenger.run()
