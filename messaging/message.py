class Message:
    def __init__(self, msg: str, sender_username: str, recipient_username: str):
        self.__msg = msg
        self.__sender = sender_username
        self.__recipient = recipient_username

    @property
    def msg(self):
        return self.__msg

    @property
    def sender(self):
        return self.__sender

    @property
    def recipient(self):
        return self.__recipient
