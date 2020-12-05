import time
import json

from Messaging.user import User
from Messaging.message import Message
from Server.server import Server


class MessengerSystem:
    def __init__(self):
        self.__server = None
        self.__keep_running_program = True

    '''Print Server App menu.'''
    def __print_menu(self):
        print(f'\n1. Load Data from File')
        print(f'2. Start the Messenger Service')
        print(f'3. Stop the Messenger Service')
        print(f'4. Save Data to File')
        print(f'5. End This Program (also shuts down Messenger Service without saving)\n')

    '''
    Display menu with options  to start/stop/load/save server.
    Takes user input from keyboard.
    '''
    def run_menu(self):
        while self.__keep_running_program:
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

    '''Create and run server in new thread'''
    def __start_service(self):
        self.__server = Server('127.0.0.1', 10000, 10)
        self.__server.start()
        pass

    '''Stop running server.'''
    def __stop_service(self):
        if self.__server is None:
            print('Server must be started first.')
            return
        # end server thread
        self.__server.keep_running_server = False
        self.__server.server_socket.close()

    '''
    Load saved Users and queued Messages.
    Must be called after server has started running.
    '''
    def __load_from_file(self):
        if self.__server is None:
            print('Server must be started first.')
            return
        try:
            with open('saved_messenger_system.json', 'r') as infile:
                server_info_json = json.load(infile)
            user_list_json = server_info_json[0]
            queued_messages_json = server_info_json[1]
        except Exception as e:
            print(f'Error loading file: {e}')
            return

        for u_dict in user_list_json:
            new_un = u_dict['_User__username']
            new_pw = u_dict['_User__password']
            new_dn = u_dict['_User__display_name']
            self.__server.user_list.append(User(new_un, new_pw, new_dn))

        for m_dict in queued_messages_json:
            m_msg = m_dict['_Message__msg']
            m_sen = m_dict['_Message__sender']
            m_rec = m_dict['_Message__recipient']
            self.__server.queued_messages.append(Message(m_msg, m_sen, m_rec))
        print('Users and Messages loaded from file successfully.')

    '''Save registered Users and queued Messages to file.'''
    def __save_to_file(self):
        if self.__server is None:
            print('Server must be started first.')
            return
        with open('saved_messenger_system.json', 'w') as outfile:
            outfile.write('[\n')
            json.dump([x.__dict__ for x in self.__server.user_list], outfile)
            outfile.write(',\n')
            json.dump([x.__dict__ for x in self.__server.queued_messages], outfile)
            outfile.write('\n]')

    '''Stop running server and shut down main thread.'''
    def __end_program(self):
        self.__keep_running_program = False
        self.__stop_service()

    @property
    def keep_running_program(self):
        return self.__keep_running_program


if __name__ == "__main__":
    messenger_system = MessengerSystem()
    messenger_system.run_menu()
