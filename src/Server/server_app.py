import time
from Server.server import Server


class MessengerSystem:
    def __init__(self):
        self.__server = None
        self.__keep_running_program = True

    def __print_menu(self):
        print(f'\n1. Load Data from File')
        print(f'2. Start the Messenger Service')
        print(f'3. Stop the Messenger Service')
        print(f'4. Save Data to File')
        print(f'5. End this program (also shuts down server)\n')

    def run_menu(self):
        self.__print_menu()
        try:
            option = int(input('Choose an option 1-5: '))
        except ValueError:
            print('Input must be a number.')
            return
        if option == 1:
            self.__load_from_file()
            pass
        elif option == 2:
            self.__start_service()
            # sleeping to prevent print statements from server mixing with menu print statements.
            time.sleep(0.5)
        elif option == 3:
            self.__stop_service()
            time.sleep(0.5)
        elif option == 4:
            self.__save_to_file()
            pass
        elif option == 5:
            self.__end_program()
        else:
            print(f'Unknown command {option}.')

    def __start_service(self):
        # create and run server in new thread
        self.__server = Server('127.0.0.1', 10000, 10)
        self.__server.start()
        pass

    def __stop_service(self):
        # end server thread
        self.__server.keep_running_server = False
        self.__server.server_socket.close()

    def __load_from_file(self):
        # todo
        pass

    def __save_to_file(self):
        # todo
        pass

    def __end_program(self):
        self.__keep_running_program = False
        self.__stop_service()
        pass

    @property
    def keep_running_program(self):
        return self.__keep_running_program


if __name__ == "__main__":
    messenger_system = MessengerSystem()
    while messenger_system.keep_running_program:
        messenger_system.run_menu()
