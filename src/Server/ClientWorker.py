from Messaging.user import User


class ClientWorker:
    def __init__(self, current_user: User):
        self.__current_user = current_user

    def send_message(self):
        pass

    def receive_message(self):
        pass
